.. _systemd-services:

systemd Services and Timers
===========================

Cargt images use systemd to start and supervise everything that runs on the
board: Weston, Wi-Fi and Bluetooth bring-up, NetworkManager, SWUpdate and
your own applications. Each of these is a **unit**, usually a ``.service``
file. This page covers the commands you need day to day. The examples are
from an i.MX 93 00363 on the 00428 carrier, running a wrynose image.

.. contents:: On this page
   :local:
   :depth: 1

Running Now vs. Starting at Boot
--------------------------------

Two separate questions apply to every service: is it **running now**
(active), and does it **start at boot** (enabled)? Different commands
change each one:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 60

   * - Command
     - Effect
   * - ``systemctl start <unit>``
     - Start it now. It does not start at the next boot unless it is
       enabled.
   * - ``systemctl stop <unit>``
     - Stop it now. If it is enabled, it starts again at the next boot.
   * - ``systemctl restart <unit>``
     - Stop and start it, for example after changing its configuration.
   * - ``systemctl reload <unit>``
     - Ask it to reread its configuration without stopping, for services
       that support it.
   * - ``systemctl enable <unit>``
     - Start it at every boot. It does not start it now.
   * - ``systemctl disable <unit>``
     - Stop starting it at boot. It does not stop it now.
   * - ``systemctl enable --now <unit>``
     - Enable it and start it now.
   * - ``systemctl disable --now <unit>``
     - Disable it and stop it now.

Check the two states with ``is-active`` and ``is-enabled``, which print one
word per unit:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl is-active weston nxp-wifi swupdate
   active
   inactive
   active
   root@imx93-cargt-00363-00428:~# systemctl is-enabled weston nxp-wifi swupdate
   enabled
   enabled
   enabled

``nxp-wifi`` is enabled but inactive, and that is correct: it only loads
the Wi-Fi driver at boot and then exits. ``weston`` and ``swupdate`` keep
running.

``systemctl status <unit>`` shows both states, the main process and the last
log lines:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl status swupdate
   ● swupdate.service - SWUpdate daemon
        Loaded: loaded (/usr/lib/systemd/system/swupdate.service; enabled; preset: enabled)
        Active: active (running) since Fri 2026-10-30 17:08:26 UTC; 20h ago
    Invocation: 88b7df9ed3754e6bad75b102363a4633
   TriggeredBy: ● swupdate.socket
          Docs: https://github.com/sbabic/swupdate
                https://sbabic.github.io/swupdate
      Main PID: 616 (swupdate)
   ...

``Loaded`` shows the unit file and whether it is enabled; ``Active`` shows
whether it runs. ``TriggeredBy`` means a socket unit can also start it on
demand.

Finding Problems
----------------

.. code-block:: bash

   systemctl is-system-running        # "running" when nothing has failed, else "degraded"
   systemctl list-units --failed      # the units that failed
   journalctl -u <unit> -b            # a unit's log since boot
   systemctl reset-failed <unit>      # clear a failed state after fixing it

On a board where everything started:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl is-system-running
   running
   root@imx93-cargt-00363-00428:~# systemctl list-units --failed
     UNIT LOAD ACTIVE SUB DESCRIPTION

   0 loaded units listed.

``systemctl list-unit-files --state=enabled`` lists what starts at boot.
:doc:`debugging-linux` covers ``journalctl`` and the kernel log in more
detail.

Turning a Service Off Completely
--------------------------------

A disabled service can still be started by another unit that needs it, or
by its socket. ``mask`` prevents it from starting at all, until ``unmask``:

.. code-block:: bash

   systemctl mask --now <unit>
   systemctl unmask <unit>

Use this, for example, to keep a service out of the way while you run the
same program by hand.

Looking at and Changing a Unit
------------------------------

``systemctl cat`` prints a unit's file, and any drop-in files that change
it:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl cat nxp-wifi
   # /usr/lib/systemd/system/nxp-wifi.service
   [Unit]
   Description=NXP WiFi service
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/env modprobe moal mod_para=nxp/wifi_mod_para.conf drvdbg=0x00000000
   ExecStartPost=/usr/bin/sleep 3

   [Install]
   WantedBy=multi-user.target

Do not edit files under ``/usr/lib/systemd``: a software update replaces
them. To change a setting, add a drop-in, which overrides only the lines it
contains:

.. code-block:: bash

   systemctl edit <unit>       # opens an editor for /etc/systemd/system/<unit>.d/override.conf
   systemctl restart <unit>

``systemctl edit`` reloads systemd for you. If you create or change unit
files any other way, run ``systemctl daemon-reload`` before restarting the
unit, or systemd keeps using the old version. To override a setting that
can appear several times, such as ``ExecStart``, clear it first with an
empty line:

.. code-block:: ini

   [Service]
   ExecStart=
   ExecStart=/usr/bin/my-wrapper

Files in ``/etc`` are on the root file system, which a full software update
replaces, so install your units and drop-ins from your own Yocto layer for
products; see :doc:`application-development`.

Timers
------

A ``.timer`` unit starts a service on a schedule, like cron.
``systemctl list-timers`` shows the timers and when each runs next:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl list-timers --all
   NEXT                            LEFT LAST                         PASSED UNIT                         ACTIVATES
   Sat 2026-10-31 17:23:22 UTC 3h 16min Fri 2026-10-30 17:23:22 UTC 20h ago systemd-tmpfiles-clean.timer systemd-tmpfiles-clean.service

   1 timers listed.

A minimal pair that runs a script every 15 minutes, starting 2 minutes
after boot. The timer starts the service with the same name:

.. code-block:: ini

   # /etc/systemd/system/my-report.service
   [Unit]
   Description=Send a status report

   [Service]
   Type=oneshot
   ExecStart=/usr/bin/my-report.sh

.. code-block:: ini

   # /etc/systemd/system/my-report.timer
   [Unit]
   Description=Send a status report every 15 minutes

   [Timer]
   OnBootSec=2min
   OnUnitActiveSec=15min

   [Install]
   WantedBy=timers.target

Enable the **timer**, not the service:

.. code-block:: bash

   systemctl daemon-reload
   systemctl enable --now my-report.timer
   systemctl list-timers my-report.timer

``OnCalendar=*-*-* 02:00:00`` runs at a fixed time of day instead. A timer
that uses wall-clock time needs a correct clock; see :ref:`rtc`.

System and User Services
------------------------

Most units are system units, run by systemd as process 1. systemd can also
run a **user manager** per logged-in user, with that user's own units,
controlled with ``systemctl --user``. Weston is the main example, and the
platforms differ:

- **i.MX:** Weston is a system service, ``weston.service``, running as
  root:

  .. code-block:: text

     root@imx93-cargt-00363-00428:~# systemctl status weston
     ● weston.service - Weston, a Wayland compositor, as a system service
          Loaded: loaded (/usr/lib/systemd/system/weston.service; enabled; preset: enabled)
          Active: active (running) since Fri 2026-10-30 17:08:27 UTC; 20h ago
     ...

  Restart it with ``systemctl restart weston``.

- **STM32MP2:** the system service ``weston-graphical-session.service``
  logs in the ``weston`` user and starts Weston as that user's own
  ``weston.service``. Restart the whole session with
  ``systemctl restart weston-graphical-session``, or control Weston in the
  ``weston`` user's manager from a root shell:

  .. code-block:: text

     root@cargt-00395-01-00365-xxxxxxxxxxxx:~# systemctl --user -M weston@ status weston
     ● weston.service - Weston, a Wayland compositor, as a user service
          Loaded: loaded (/usr/lib/systemd/user/weston.service; disabled; preset: enabled)
          Active: active (running) since Mon 2026-11-02 18:57:03 UTC; 2h 47min ago
     TriggeredBy: ● weston.socket
     ...
     root@cargt-00395-01-00365-xxxxxxxxxxxx:~# systemctl --user -M weston@ restart weston

  ``weston.service`` shows as ``disabled`` because the session starts it,
  not the ``weston`` user's boot targets. Restarting the whole session also
  restarts the ``weston`` user's other services, such as PipeWire. These
  examples are from an STM32MP257F 00395-01 on the 00365 carrier; the
  hostname ends in the board's MAC address, shown here as ``x``.

The Main Cargt Services
-----------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 35 65

   * - Unit
     - What it does
   * - ``weston.service``
     - The Wayland compositor (a user unit on STM32MP2; see above)
   * - ``nxp-wifi.service``
     - Loads the Wi-Fi driver at boot (i.MX); see :doc:`wifi`
   * - ``nxp-bluetooth.service``
     - Brings up Bluetooth after Wi-Fi; see :doc:`bluetooth`
   * - ``NetworkManager.service``
     - Ethernet, Wi-Fi and cellular; see :doc:`networking`
   * - ``swupdate.service``, ``swupdate-progress.service``
     - SWUpdate and its web interface, and the reboot after an update
       (i.MX); see :doc:`software-updates`
   * - ``grow-data-part.service``
     - Grows and mounts ``/data`` at boot (i.MX); see :doc:`storage`

On STM32MP2, ``rauc status`` shows the update state; see
:doc:`rauc-ota-updates`.

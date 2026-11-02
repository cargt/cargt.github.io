.. _power-watchdog:

Power-Off, Watchdog and Suspend
===============================

This page explains what ``poweroff`` does on Cargt SOMs, how the hardware
watchdog is used, and which suspend modes to use.

.. contents:: On this page
   :local:
   :depth: 1

Powering Off
------------

Shut down with ``poweroff`` (the same as ``systemctl poweroff``). systemd
stops the services, unmounts the file systems and then asks the firmware to
switch the board off.

**i.MX 91 and i.MX 93 (00363):** the firmware (TF-A) asks the processor's
battery-backed power module (BBNSM) to switch the system power off. On an
i.MX 91 00363 on the 00365 carrier, the board stopped responding about
6 seconds after ``systemctl poweroff`` and did not restart; whether the
power supply rails were actually switched off has not been confirmed by
measurement yet.

**STM32MP2 (00395):** OP-TEE switches the PMIC off, and the board stays off
until its power is removed and reconnected. On an STM32MP257F 00395-02 on
the 00365 carrier, running the published image of October 2026, the board
dropped off its USB connection about 3 seconds after ``systemctl poweroff``
and stayed off.

The Hardware Watchdog
---------------------

A hardware watchdog resets the board if software stops "feeding" it within
its timeout, so a board that hangs restarts by itself. The processors on
Cargt SOMs have one, which Linux provides as ``/dev/watchdog0``. Only one
program can have it open at a time,
and opening it starts the countdown, so it is normally left to systemd.

STM32MP2: systemd Uses It
~~~~~~~~~~~~~~~~~~~~~~~~~

On STM32MP2 images, systemd opens the watchdog at boot and feeds it, with a
32-second timeout. The settings come from
``/lib/systemd/system.conf.d/01-watchdog.conf``:

.. code-block:: text

   [Manager]
   RuntimeWatchdogSec=32
   ShutdownWatchdogSec=32
   RebootWatchdogSec=32

From an STM32MP257F 00395-02:

.. code-block:: text

   # dmesg | grep -i watchdog
   [    1.148628] arm_smc_wdt watchdog: Watchdog registered (timeout=32 sec, nowayout=0)
   [    3.438284] systemd[1]: Using hardware watchdog 'arm_smc_wdt', version 0, device /dev/watchdog0
   [    3.441719] systemd[1]: Watchdog running with a hardware timeout of 32s.
   # systemctl show -p RuntimeWatchdogUSec -p RebootWatchdogUSec
   RuntimeWatchdogUSec=32s
   RebootWatchdogUSec=32s
   # ls -l /proc/1/fd | grep watchdog
   l-wx------ 1 root root 64 Oct 30 21:25 10 -> /dev/watchdog0

This means:

- If the system hangs so badly that systemd itself stops running, the board
  resets within 32 seconds.
- ``ShutdownWatchdogSec`` and ``RebootWatchdogSec`` keep the watchdog
  running while the board shuts down or reboots, so a shutdown that hangs
  also ends in a reset after 32 seconds.
- ``/dev/watchdog0`` is held by systemd (process 1), so an application that
  tries to open it gets an error because the device is busy. To have the
  watchdog cover your application, use systemd's service watchdog instead;
  see `Watching a Service`_.

RAUC's automatic fallback to the previous slot also relies on the watchdog
resetting a board that fails to boot; see :doc:`rauc-ota-updates`.

i.MX: Available to Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On i.MX images, systemd does not use the watchdog while the system runs; it
only arms it during a reboot (``RebootWatchdogSec=60``, the Yocto default).
``/dev/watchdog0`` is free. On an i.MX 93 00363, it is the i.MX ``wdog3``
(``imx7ulp-wdt`` driver), and a timeout resets the board through the PMIC:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl show -p RuntimeWatchdogUSec -p RebootWatchdogUSec
   RuntimeWatchdogUSec=0
   RebootWatchdogUSec=1min
   root@imx93-cargt-00363-00428:~# basename $(readlink /sys/class/watchdog/watchdog0/device/driver)
   imx7ulp-wdt

To have systemd feed it, as on STM32MP2, add a configuration file such as
``/etc/systemd/system.conf.d/10-watchdog.conf`` and reboot:

.. code-block:: text

   [Manager]
   RuntimeWatchdogSec=30
   RebootWatchdogSec=60

For a product, install the file from your own layer, or set
``WATCHDOG_RUNTIME_SEC = "30"`` for the ``systemd`` recipe, which writes
``RuntimeWatchdogSec`` into ``/etc/systemd/system.conf``.

An application can instead open ``/dev/watchdog0`` itself, but then it
must keep writing to it. If it exits without writing the magic character
``V`` first, the board resets when the timeout expires.

Watching a Service
~~~~~~~~~~~~~~~~~~

systemd can also restart, or reboot the board, when one service stops
responding. Add ``WatchdogSec=`` to the service and have the program call
``sd_notify(0, "WATCHDOG=1")`` (from ``libsystemd``) more often than that:

.. code-block:: ini

   [Service]
   ExecStart=/usr/bin/my-app
   WatchdogSec=10
   Restart=on-watchdog

If the program misses the deadline, systemd kills it and, with
``Restart=on-watchdog``, starts it again. To reboot the board instead,
leave out ``Restart=`` and add ``FailureAction=reboot``. This works on every Cargt image,
whether or not systemd uses the hardware watchdog. A shell script can feed
it with ``systemd-notify WATCHDOG=1`` if the service has
``NotifyAccess=all``.

Suspend
-------

``/sys/power/state`` lists the sleep states the kernel offers, and
``/sys/power/mem_sleep`` which kind of sleep ``mem`` means (the one in
brackets):

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /sys/power/state /sys/power/mem_sleep
   freeze mem
   s2idle [deep]

STM32MP2 images also list ``disk``. ``freeze`` (suspend-to-idle) stops
user space and idles the CPUs; ``mem`` with ``deep`` also powers down most
of the SoC, which saves more power but needs every driver to resume
correctly.

On i.MX 93 00363 boards, use suspend-to-idle, and wake the board with the
internal RTC's alarm; see :ref:`rtc`:

.. code-block:: bash

   rtcwake -d rtc1 -m freeze -s 10

Suspend on the other SOMs has not been tested by Cargt yet.

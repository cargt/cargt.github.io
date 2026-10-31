.. _debugging-linux:

Debugging in Linux
==================

When something on a board does not work, three places usually explain why:
the kernel log (``dmesg``), the systemd journal (``journalctl``), and the
kernel's view of the hardware in sysfs. The examples on this page are from
an i.MX 93 00363 on the 00428 carrier, running a wrynose image.

.. contents:: On this page
   :local:
   :depth: 1

The Kernel Log: dmesg
---------------------

``dmesg`` prints the kernel's messages since boot: drivers starting,
hardware found or missing, and errors.

.. code-block:: bash

   dmesg                         # everything since boot
   dmesg -w                      # keep printing new messages (Ctrl+C to stop)
   dmesg -T                      # wall-clock times instead of seconds since boot
   dmesg --level=err,warn        # errors and warnings only
   dmesg | grep -i <driver>      # messages from one driver or device

Errors and warnings are a good first look after a change:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# dmesg --level=err,warn
   [    0.000000] KASLR disabled due to lack of seed
   ...
   [    1.807044] ili9881c-dsi 4ae10000.dsi.0: supply power not found, using dummy regulator
   [    3.838892] ilitek_ts 2-0041: protocol init failed: -5
   [    3.847296] ilitek_ts 2-0041: probe with driver ilitek_ts failed with error -5
   ...
   [   12.916423] at24 0-0050: supply vcc not found, using dummy regulator

Many warnings are harmless: ``supply ... not found, using dummy regulator``
means the device tree does not name a regulator for a supply that is
always on. Lines saying a **probe failed** matter: the driver gave up on that
device. The number is a negated Linux error code; here ``-5`` is ``EIO``, an
I/O error, which on an I²C device usually means it did not answer. This
board's touch controller at address 0x41 on I²C bus 2 did not respond, so
the touchscreen does not work. Other common codes are ``-2`` (``ENOENT``, a
file such as firmware not found), ``-19`` (``ENODEV``, no such device) and
``-110`` (``ETIMEDOUT``).

``-517`` (``EPROBE_DEFER``) is different: the driver is waiting for
something else, such as a regulator or clock, and the kernel retries it
later. If a device never appears, check whether it is still waiting:

.. code-block:: bash

   cat /sys/kernel/debug/devices_deferred    # empty: nothing is waiting

The kernel log lives in a fixed-size buffer in memory, so very old messages
are overwritten on a busy system, and it starts empty at every boot.

The systemd Journal: journalctl
-------------------------------

The journal collects the kernel log and the output of every systemd service.

.. code-block:: bash

   journalctl -b                       # everything since this boot
   journalctl -f                       # follow new messages
   journalctl -u NetworkManager        # one service (unit)
   journalctl -u NetworkManager -f     # follow one service
   journalctl -p err -b                # errors and worse since boot
   journalctl --since "10 min ago"     # a time range (also "2026-10-31 13:00")
   journalctl -k                       # the kernel log only, like dmesg
   journalctl -b -o short-precise      # timestamps with microseconds

``-p err`` is the quickest way to see what failed during boot:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# journalctl -b -p err --no-pager
   Oct 30 17:08:19 imx93-cargt-00363-00428 kernel: ilitek_ts 2-0041: protocol init failed: -5
   Oct 30 17:08:19 imx93-cargt-00363-00428 kernel: ilitek_ts 2-0041: probe with driver ilitek_ts failed with error -5
   Oct 30 17:08:22 imx93-cargt-00363-00428 pipewire[271]: mod.portal: Failed to connect to session bus: Input/output error
   ...

``systemctl status <unit>`` shows a service's state together with its last
few log lines, and ``systemctl --failed`` lists the services that failed.

The Journal Is Lost at Reboot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On Cargt i.MX images the journal is kept in memory, under ``/run/log/journal``,
and limited to 64 MB. ``/var/log`` is a link to ``/var/volatile/log``, which
is also in memory. So logs from before the last reboot are gone, and
``journalctl -b -1`` has nothing to show:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# journalctl -b -1
   Specifying boot ID or boot offset has no effect, no persistent journal was found.
   root@imx93-cargt-00363-00428:~# journalctl --list-boots
   IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY
     0 0e91bd6ab74e4303a9760dab20a7fe61 Fri 2026-10-30 17:08:19 UTC Sat 2026-10-31 14:00:02 UTC
   root@imx93-cargt-00363-00428:~# journalctl --disk-usage
   Archived and active journals take up 10.9M in the file system.

This keeps the eMMC from wearing out under constant logging. To catch the
messages before a crash or reboot, copy them to ``/data`` while you
reproduce the problem, for example from a second SSH session:

.. code-block:: bash

   journalctl -f -o short-precise > /data/journal-$(date +%Y%m%d-%H%M).txt

To keep the journal across reboots in your own image, remove the table that
makes ``/var/log`` volatile, in your distro configuration or
``local.conf``:

.. code-block:: text

   FILESYSTEM_PERMS_TABLES:remove = "files/fs-perms-volatile-log.txt"

and set ``Storage=persistent`` in a ``journald.conf.d`` drop-in. The journal
is then written to the root file system, so it is replaced by every
software update, and it adds eMMC writes. This has not been tested on Cargt
images.

Hardware in sysfs
-----------------

sysfs, under ``/sys``, shows the kernel's devices and drivers as files. Most
files hold one value and can be read with ``cat``; ``grep . <files>`` prints
several files with their names. :ref:`linux-basics` shows sysfs for GPIO,
analog inputs and I²C devices.

**Temperature.** Each thermal zone has a type, a temperature in thousandths
of a degree, and its trip points (see :doc:`thermal-characterization`):

.. code-block:: text

   root@imx93-cargt-00363-00428:~# for z in /sys/class/thermal/thermal_zone*; do echo "$z $(cat $z/type) $(cat $z/temp)"; done
   /sys/class/thermal/thermal_zone0 cpu-thermal 40850
   root@imx93-cargt-00363-00428:~# grep . /sys/class/thermal/thermal_zone0/trip_point_*
   /sys/class/thermal/thermal_zone0/trip_point_0_hyst:2000
   /sys/class/thermal/thermal_zone0/trip_point_0_temp:95000
   /sys/class/thermal/thermal_zone0/trip_point_0_type:passive
   /sys/class/thermal/thermal_zone0/trip_point_1_hyst:2000
   /sys/class/thermal/thermal_zone0/trip_point_1_temp:105000
   /sys/class/thermal/thermal_zone0/trip_point_1_type:critical

**Network interfaces.** Link state, speed and packet counters:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# grep . /sys/class/net/eth0/statistics/{rx_packets,tx_packets,rx_errors,rx_dropped} /sys/class/net/eth0/{operstate,speed,duplex}
   /sys/class/net/eth0/statistics/rx_packets:892296
   /sys/class/net/eth0/statistics/tx_packets:2047
   /sys/class/net/eth0/statistics/rx_errors:0
   /sys/class/net/eth0/statistics/rx_dropped:186706
   /sys/class/net/eth0/operstate:up
   /sys/class/net/eth0/speed:1000
   /sys/class/net/eth0/duplex:full

``rx_errors`` counts damaged frames, which point to cabling or the PHY.
``rx_dropped`` also counts frames the board did not want, such as traffic
for protocols it does not use, so a large number on a busy office network is
normal.

**Displays.** Each display output has a connection status:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# grep -H . /sys/class/drm/*/status
   /sys/class/drm/card0-DSI-1/status:connected

**Backlight.** The current and maximum brightness; write a number to
``brightness`` to change it:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# for b in /sys/class/backlight/*; do echo "$b $(cat $b/brightness)/$(cat $b/max_brightness) actual=$(cat $b/actual_brightness)"; done
   /sys/class/backlight/pwm_backlight 5/100 actual=5

Which Driver Has a Device?
~~~~~~~~~~~~~~~~~~~~~~~~~~

Every device directory has a ``driver`` link when a driver has bound to it.
A device without one was found but is not working. For the I²C devices:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# for d in /sys/bus/i2c/devices/*-*; do n=$(cat $d/name 2>/dev/null); dr=$(basename "$(readlink $d/driver)" 2>/dev/null); echo "$(basename $d) $n ${dr:-<no driver>}"; done
   0-0025 pca9451a nxp-pca9450
   0-0032 rx8111 rtc-rx8111
   0-0050 24c02 at24
   1-0051 ptn5110 tcpci
   2-0041 ili2520 <no driver>
   i2c-0 44340000.i2c <no driver>
   i2c-1 44350000.i2c <no driver>
   i2c-2 42530000.i2c <no driver>

The ``i2c-N`` entries are the buses themselves, which have no driver link.
The touch controller at ``2-0041`` has no driver either, which matches the
probe failure in the kernel log above.
The same works for any device, for example a network interface:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# basename $(readlink /sys/class/net/eth0/device/driver)
   imx-dwmac
   root@imx93-cargt-00363-00428:~# basename $(readlink /sys/class/net/mlan0/device/driver)
   wlan_sdio

debugfs
-------

debugfs, mounted at ``/sys/kernel/debug``, holds internal driver and kernel
state such as clocks (``clk``), GPIOs (``gpio``) and the deferred-probe
list used above. It is meant for development: its files change between
kernel versions, some are slow or unsafe to read, and writing to them can
change hardware settings directly. Read what you need while debugging, and
do not build products that depend on it.

.. code-block:: bash

   ls /sys/kernel/debug
   cat /sys/kernel/debug/gpio                # every GPIO and who uses it

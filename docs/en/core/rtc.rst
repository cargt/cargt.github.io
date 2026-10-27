.. _rtc:

Real-Time Clock
===============

Linux keeps the time in the system clock while the board runs. To keep the
time while the board is off, Cargt designs use a battery-backed real-time
clock (RTC).

The examples on this page are from i.MX 93 00363 SOMs on 00428 carriers.

RTC Devices
-----------

These boards have two RTCs:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 15 30 55

   * - Device
     - Hardware
     - Notes
   * - ``rtc0``
     - Epson RX8111 at I²C address 0x32
     - Battery-backed. Keeps the time while the board is off, if a backup
       battery is fitted. ``/dev/rtc`` links to it, and Linux reads and
       writes it by default.
   * - ``rtc1``
     - i.MX 93 internal RTC (BBNSM)
     - Runs only while the board has power, so it starts at 1970 after
       every power-up. It has a wake alarm; see `Waking from Suspend`_.

.. code-block:: text

   root@imx93-cargt-00363-00428:~# for r in /sys/class/rtc/rtc*; do echo "$(basename $r): $(cat $r/name)"; done
   rtc0: rtc-rx8111 0-0032
   rtc1: bbnsm_rtc 44440000.bbnsm:rtc

Reading and Setting the Time
----------------------------

.. code-block:: text

   root@imx93-cargt-00363-00428:~# timedatectl
                  Local time: Tue 2026-10-27 18:47:57 UTC
              Universal time: Tue 2026-10-27 18:47:57 UTC
                    RTC time: Tue 2026-10-27 18:47:57
                   Time zone: UTC (UTC, +0000)
   System clock synchronized: yes
                 NTP service: active
             RTC in local TZ: no

   root@imx93-cargt-00363-00428:~# hwclock -r
   2026-10-27 18:47:57.218413+00:00

   root@imx93-cargt-00363-00428:~# hwclock -r -f /dev/rtc1
   1970-01-01 00:07:00.424777+00:00

Keep the RTC in UTC (``RTC in local TZ: no``), and set the time zone with
``timedatectl set-timezone``.

**With network time (the default):** ``systemd-timesyncd`` sets the system
clock from NTP, and the kernel copies the system clock to ``rtc0`` about
every 11 minutes while it is synchronized (``CONFIG_RTC_SYSTOHC``). There is
nothing to configure.

**Without network access**, turn NTP off, set the system clock, and write it
to the RTC:

.. code-block:: bash

   timedatectl set-ntp false
   timedatectl set-time "2026-10-27 18:50:00"
   hwclock --systohc       # copy the system clock to rtc0
   hwclock -r

To go back to network time, turn NTP on again. ``systemd-timesyncd`` may
take a while to correct the clock; restarting it makes it synchronize
immediately:

.. code-block:: bash

   timedatectl set-ntp true
   systemctl restart systemd-timesyncd
   timedatectl              # wait for "System clock synchronized: yes"

At Boot
-------

Early in boot, the kernel sets the system clock from ``rtc0``
(``CONFIG_RTC_HCTOSYS``). On a board with a backup battery, after the power
had been off:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# dmesg | grep rtc
   [    1.324561] bbnsm_rtc 44440000.bbnsm:rtc: registered as rtc1
   [    2.801999] rtc-rx8111 0-0032: registered as rtc0
   [    2.807241] rtc-rx8111 0-0032: setting system clock to 2026-10-27T18:40:59 UTC (1793126459)

On a board without a battery, the RX8111 flags that it lost power, and the
kernel leaves the system clock alone until NTP sets it:

.. code-block:: text

   [    2.777646] rtc-rx8111 0-0032: registered as rtc0
   [    2.782502] rtc-rx8111 0-0032: hctosys: unable to read the hardware clock

If a board with a battery shows this message, check the battery.

Waking from Suspend
-------------------

The RX8111 alarm is not used on these boards (``rtc0`` has no
``wakealarm``), but the internal RTC can wake the board from suspend:

.. code-block:: bash

   rtcwake -d rtc1 -m mem -s 10    # suspend to RAM, wake after 10 seconds

.. warning::

   On current images (wrynose, October 2026), suspend is aborted on boards
   with an IW610 or IW612 module, because the Wi-Fi module's wake line
   (``wifi_oob_wakeup``) is active when the board tries to suspend.
   ``rtcwake`` then reports ``write error``, and ``dmesg`` shows
   ``Wakeup pending. Abort CPU freeze``. ``cat /sys/power/pm_wakeup_irq``
   shows which interrupt aborted the suspend.

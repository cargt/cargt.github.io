.. _real-time-linux:

Real-Time Linux (PREEMPT_RT) on i.MX 95
=======================================

Cargt provides a real-time Linux build for i.MX 95 designs. It is based on
`NXP Real-time Edge Software <https://www.nxp.com/design/design-center/software/development-software/real-time-edge-software:REALTIME-EDGE-SOFTWARE>`_
3.5 and uses a fully preemptible (``PREEMPT_RT``) Linux kernel. This page
explains what the build contains, how to build and install it, how to measure
latency on your hardware, and how to tune the system for deterministic
real-time applications.

.. note::

   This page assumes you can already build and flash a standard Cargt image.
   If not, start with the :ref:`yocto-tutorial` and :ref:`running-linux`.

What is PREEMPT_RT?
-------------------

A standard Linux kernel is tuned for throughput. A high-priority task can be
delayed for a long time by interrupt handlers, spinlocks and other
non-preemptible kernel code. ``PREEMPT_RT`` makes almost all of the kernel
preemptible:

- Most interrupt handlers run as kernel threads with a scheduling priority, so
  your real-time task can be given a higher priority than device interrupts.
- Spinlocks become sleeping locks with priority inheritance, so a low-priority
  task holding a lock cannot block a high-priority task indefinitely.
- The worst-case time from an event (such as a timer expiring) to your
  ``SCHED_FIFO`` task running becomes small and predictable. This time is
  called *scheduling latency*.

``PREEMPT_RT`` gives **bounded latency, not zero latency**. The bound you
achieve depends on the SoC, the kernel configuration, the system load and how
you configure your application. The `Measuring latency`_ and
`Tuning for determinism`_ sections show how to measure and improve it.

Typical uses are motion control and servo loops, industrial fieldbus masters
(EtherCAT, CANopen), time-sensitive networking (TSN) and precise time
synchronization (PTP).

What Cargt provides
-------------------

The real-time build is a separate Yocto distro, ``cargt-imx-rt``, in
``meta-imx-cargt``.

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Component
     - Real-time build (``cargt-imx-rt``)
   * - Linux kernel
     - NXP ``real-time-edge-linux`` 6.18.20-rt (the NXP lf-6.18.20 BSP kernel
       plus ``PREEMPT_RT``, TSN and switch support), with all Cargt board
       support and device trees
   * - Bootloader, System Manager, DDR init
     - The same Cargt U-Boot, System Manager and OEI as the standard Cargt
       build
   * - Distro
     - ``cargt-imx-rt`` is built on ``cargt-imx-xwayland`` (Wayland/Weston with
       XWayland, systemd, NetworkManager). It only adds the real-time kernel
       and the Real-time Edge package configuration.
   * - Image
     - ``cargt-image-rt`` is ``cargt-image-dev`` plus the real-time packages
       below. That includes GStreamer multimedia, camera support on machines
       with a camera, the SWUpdate client, package management, and development
       and debug tools.
   * - Real-time userspace
     - ``rt-tests`` (``cyclictest``), ``rteval``, ``stress-ng``, ``linuxptp``
       (``ptp4l``, ``phc2sys``), ``isochron``, the IgH EtherCAT master,
       open62541 (OPC UA), libmodbus and CANopen tools
   * - Cargt additions
     - ``cargt-rt-check`` (an on-target check and latency test) and
       ``cargt-rt-config`` (real-time defaults: deep CPU idle states disabled,
       EtherCAT drivers not autoloaded)

Supported hardware
~~~~~~~~~~~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 45 55

   * - ``MACHINE``
     - Hardware
   * - ``imx95-cargt-00414-00365``
     - :ref:`00414` i.MX 95 OSM-L SOM on the 00365 carrier board
   * - ``imx95-cargt-00414-00428``
     - 00414 SOM on the 00428 carrier board
   * - ``imx95-cargt-00414-osm-som``
     - 00414 SOM on a custom carrier board
   * - ``imx95-15x15-lpddr4x-frdm``
     - NXP FRDM-IMX95 development board (useful as a reference)

The build has been validated on the 00414 SOM on the 00365 carrier board and on
the NXP FRDM-IMX95.

How it relates to NXP Real-time Edge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NXP ships Real-time Edge as its own Yocto distro, ``nxp-real-time-edge``, for
NXP evaluation boards. Cargt does not use that distro for Cargt hardware:

- It replaces the U-Boot source and selects NXP evaluation-board System Manager
  configurations. Neither is correct for a Cargt SOM.
- It replaces the kernel source in a way that drops board-specific kernel
  patches and device trees.

Instead, ``cargt-imx-rt`` keeps the Cargt board support and takes only the
real-time kernel and userspace from ``meta-real-time-edge``. The two Real-time
Edge layers, ``meta-real-time-edge`` and ``meta-rtos-industrial``, are pinned
in the Cargt manifest to the release that matches the Cargt BSP
(Real-time Edge 3.5 with NXP lf-6.18.20-2.0.0).

.. warning::

   Only use ``meta-real-time-edge`` with the NXP BSP release its manifest pins.
   The Cargt manifest already pins matching versions. Do not mix layers from a
   different Real-time Edge or NXP BSP release.

Kernel configuration
~~~~~~~~~~~~~~~~~~~~

On top of NXP's real-time defconfig, the ``cargt-imx-rt`` kernel enables:

- ``CONFIG_PREEMPT_RT=y``: the fully preemptible kernel.
- ``CONFIG_CPU_FREQ_DEFAULT_GOV_PERFORMANCE=y``: all CPUs run at their maximum
  clock (1.8 GHz on the 00414). With frequency scaling (``ondemand``), the
  average wake-up latency of an idle CPU was 22 µs instead of 6 µs.
- ``CONFIG_NO_HZ_FULL=y`` and ``CONFIG_RCU_NOCB_CPU=y``: allow an isolated CPU
  to run without the scheduler tick. These options have no effect unless you
  enable them on the kernel command line (see `Isolating a CPU`_).

Build the real-time image
-------------------------

The real-time build uses the same source tree as the standard Cargt build. If
you have already followed the :ref:`yocto-tutorial`, you have everything you need.

#. Download the source code (skip this if you already have a Cargt wrynose
   tree):

   .. code-block:: bash

      mkdir -p ~/yocto
      cd ~/yocto
      repo init -u https://github.com/cargt/imx_manifest -b wrynose -m cargt-imx-6.18.20-2.0.0.xml
      repo sync

#. Create a **separate build directory** for the real-time distro:

   .. code-block:: bash

      DISTRO=cargt-imx-rt MACHINE=imx95-cargt-00414-00365 source ./imx-cargt-setup.sh -b bld-rt

   The setup script adds the Real-time Edge layers only when
   ``DISTRO=cargt-imx-rt``.

   .. note::

      Keep real-time builds in their own build directory. The Real-time Edge
      layers also patch Arm Trusted Firmware, ``imx-mkimage``, ``linuxptp``,
      ``iproute2`` and ``lldpd``, which would change your standard builds if
      the layers were added to a shared build directory. The download and
      sstate directories can be shared.

#. Build the image:

   .. code-block:: bash

      # Full root filesystem and SD/eMMC image
      bitbake cargt-image-rt
      # SWUpdate package for updating a running system
      bitbake cargt-image-rt-swu

#. The output is in ``bld-rt/tmp/deploy/images/<machine>/``:

   .. list-table::
      :header-rows: 1
      :widths: 55 45

      * - File
        - Use
      * - ``cargt-image-rt-<machine>.rootfs.wic.zst`` and ``.wic.bmap``
        - Complete SD card or eMMC image
      * - ``cargt-image-rt-swu-<machine>.rootfs.swu``
        - SWUpdate package
      * - ``imx-boot-<machine>-sd.bin-flash_a55``
        - Boot image (U-Boot, ATF, OP-TEE, System Manager)

To return to the build directory later:

.. code-block:: bash

   source setup-environment bld-rt

Install the image
-----------------

Use any of the standard Cargt methods:

- **Update a running system with SWUpdate.** This is the quickest way to move a
  board to the real-time image. It keeps the ``/data`` partition and installs
  into the inactive root partition. See :ref:`swupdate`.

  .. code-block:: bash

     # On the target, with the .swu file copied to /data
     swupdate -v -i /data/cargt-image-rt-swu-imx95-cargt-00414-00365.rootfs.swu
     reboot

- **Write a complete image to an SD card** from your Linux host:

  .. code-block:: bash

     cd bld-rt/tmp/deploy/images/imx95-cargt-00414-00365
     # Replace sdX with your SD card device. Check it with lsblk first!
     sudo bmaptool copy --bmap cargt-image-rt-imx95-cargt-00414-00365.rootfs.wic.bmap \
         cargt-image-rt-imx95-cargt-00414-00365.rootfs.wic.zst /dev/sdX

- **Flash eMMC with UUU.** See :ref:`running-linux`.

Verify the real-time kernel
---------------------------

After boot, check that the real-time kernel is running:

.. code-block:: bash

   uname -v
   # #1 SMP PREEMPT_RT ...
   cat /sys/kernel/realtime
   # 1
   cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor
   # performance

Then run the Cargt check script. It checks the kernel, failed services, kernel
locking warnings, Ethernet, the SOM EEPROM and USB Type-C. Then it runs
``cyclictest`` with the system idle and under ``stress-ng`` load:

.. code-block:: bash

   cargt-rt-check              # 15 minutes per latency run (default)
   cargt-rt-check -d 2m        # quick check
   cargt-rt-check -n           # system checks only, no latency runs

The report is written to ``/data/rt-check/<serial>-<date>/report.txt``, with
the full ``cyclictest`` histograms and logs alongside it. Example output:

.. code-block:: text

   == Kernel
     PASS  uname reports PREEMPT_RT
     PASS  /sys/kernel/realtime = 1
     info  cpufreq governors: 6 performance
     PASS  deep CPU idle states disabled (6/6)
   == System
     PASS  no failed systemd units
     PASS  no RT locking splats in dmesg
     PASS  eth0 up 1000Mb/s
     PASS  SOM EEPROM record readable (/sys/bus/i2c/devices/0-0050/eeprom)
   == Latency (cyclictest -m -S -p 98 -i 1000, 15m per run)
     idle: max 83 us  (per CPU: 67 60 83 80 60 62)  histogram overflows (>400 us): 0
     load: max 106 us  (per CPU: 72 81 106 83 91 86)  histogram overflows (>400 us): 0

Measuring latency
-----------------

``cyclictest`` is the standard tool for measuring scheduling latency. It runs a
high-priority thread that asks to wake up at a fixed interval and records how
late each wake-up actually was.

.. code-block:: bash

   # One SCHED_FIFO priority 98 thread per CPU, 1 ms interval, memory locked,
   # 10 minutes, histogram up to 400 us
   cyclictest -m -S -p 98 -i 1000 -h 400 -q -D 10m

The summary lines at the end of the output give the results per CPU:

.. code-block:: text

   # Min Latencies: 00004 00004 00004 00004 00004 00004
   # Avg Latencies: 00013 00013 00013 00013 00013 00013
   # Max Latencies: 00118 00116 00108 00114 00101 00117

Keep the following in mind:

- **The maximum is the number that matters.** A real-time system is judged by
  its worst case, not its average.
- **Measure under load.** An idle system hides most sources of latency. Run a
  representative load at the same time, or a synthetic one:

  .. code-block:: bash

     stress-ng --cpu 6 --vm 2 --vm-bytes 25% --io 2 --timer 2 -t 10m &
     cyclictest -m -S -p 98 -i 1000 -h 400 -q -D 10m

- **Measure for a long time.** Rare events set the worst case. Use minutes to
  check a configuration and many hours (overnight) to qualify a system.
- **Measure on your final hardware and enclosure.** Temperature, thermal
  throttling and your own peripherals and drivers all affect the result.

Reference results
~~~~~~~~~~~~~~~~~

These results were measured on a 00414 SOM on a 00365 carrier board and on an
NXP FRDM-IMX95, on an open bench, with ``cyclictest -m -p 98 -i 1000`` and the
``stress-ng`` load shown above. Both boards gave the same results, so they
reflect the SoC and kernel configuration rather than the carrier board. Use
them as a guide, not as a specification.

.. list-table::
   :header-rows: 1
   :widths: 52 12 12 12 12

   * - Configuration
     - Avg idle
     - Max idle
     - Avg load
     - Max load
   * - ``ondemand`` governor, all CPUs, 15 min
     - 23 µs
     - 83 µs
     - 13 µs
     - 106 µs
   * - ``performance`` governor (default), all CPUs, 10 h
     -
     -
     - 13 µs
     - 118 µs
   * - ``performance`` + CPU 5 isolated, CPU 5, 10 h
     -
     -
     - 6 µs
     - **48 µs**

There were no samples above 400 µs, no stress test failures and no thermal
throttling in any of these runs.

Tuning for determinism
----------------------

CPU frequency
~~~~~~~~~~~~~

The ``cargt-imx-rt`` kernel uses the ``performance`` governor by default, so
the CPUs do not change clock speed. Check or change it at runtime:

.. code-block:: bash

   cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor
   echo performance > /sys/devices/system/cpu/cpufreq/policy0/scaling_governor

Running at full clock increases power consumption and SoC temperature. Check
the temperature of your design under your worst-case load and ambient
conditions:

.. code-block:: bash

   grep . /sys/class/thermal/thermal_zone*/type /sys/class/thermal/thermal_zone*/temp

CPU idle states
~~~~~~~~~~~~~~~

The i.MX 95 has a deep CPU idle state (``cpu-pd-wait``, which powers the core
down) in addition to the light ``WFI`` state:

.. code-block:: bash

   grep . /sys/devices/system/cpu/cpu5/cpuidle/state*/name
   # .../state0/name:WFI
   # .../state1/name:cpu-pd-wait

A CPU that wakes up from ``cpu-pd-wait`` adds **hundreds of microseconds** of
latency. In our tests, a 1 ms periodic loop measured a 264 µs worst case with
the deep state allowed and 37–49 µs without it.

**The cargt-imx-rt image disables deep idle states by default.**
``cargt-rt-config`` installs ``/usr/lib/tmpfiles.d/cargt-rt-cpuidle.conf``,
which disables every idle state above ``WFI`` on all CPUs at boot. Check it
with:

.. code-block:: bash

   grep . /sys/devices/system/cpu/cpu*/cpuidle/state1/disable
   # .../cpu0/cpuidle/state1/disable:1  (1 = disabled)

This costs some idle power on every CPU. If your design needs the power saving
and only some workloads are real-time:

- Allow deep idle again until reboot:

  .. code-block:: bash

     for s in /sys/devices/system/cpu/cpu*/cpuidle/state[1-9]*/disable; do echo 0 > $s; done

- Allow it permanently by masking the configuration file:

  .. code-block:: bash

     ln -s /dev/null /etc/tmpfiles.d/cargt-rt-cpuidle.conf

With deep idle allowed, a real-time application must block deep idle states
itself for as long as it runs. Open ``/dev/cpu_dma_latency``, write ``0`` and
keep the file open; closing the file allows deep idle states again.
``cyclictest`` does this automatically. The example in
`Writing a real-time application`_ also does it, so it works with either
setting.

Isolating a CPU
~~~~~~~~~~~~~~~

Isolating a CPU is the most effective tuning step. Keep a CPU free of other
tasks and device interrupts and run only your real-time task on it. The i.MX
95 has six Cortex-A55 cores (CPUs 0–5). The examples below reserve CPU 5.

#. Add these arguments to the kernel command line:

   .. code-block:: text

      isolcpus=domain,managed_irq,5 irqaffinity=0-4

   - ``isolcpus=domain,managed_irq,5``: the scheduler does not place tasks on
     CPU 5 unless they are explicitly pinned there. Managed interrupts also
     avoid it where possible.
   - ``irqaffinity=0-4``: device interrupts go to CPUs 0–4 by default.

#. The Cargt U-Boot environment adds the variable ``mcore_args`` to the kernel
   command line. Set it to make the change permanent.

   From Linux:

   .. code-block:: bash

      fw_setenv mcore_args 'isolcpus=domain,managed_irq,5 irqaffinity=0-4'
      reboot

   Or from the U-Boot prompt:

   .. code-block:: text

      setenv mcore_args 'isolcpus=domain,managed_irq,5 irqaffinity=0-4'
      saveenv
      boot

   To try the arguments for a single boot only, run ``setenv`` followed by
   ``run bsp_bootcmd`` and do not run ``saveenv``.

#. After the reboot, check the result:

   .. code-block:: bash

      cat /proc/cmdline
      cat /sys/devices/system/cpu/isolated
      # 5

#. Run your real-time task on CPU 5 (see `Writing a real-time application`_),
   or test it with ``cyclictest``:

   .. code-block:: bash

      # Compare isolated CPU 5 with CPU 4 while CPUs 0-4 are loaded
      taskset -c 0-4 stress-ng --cpu 5 --vm 2 --vm-bytes 25% --io 2 --timer 2 -t 10m &
      cyclictest -m -p 98 -i 1000 -t 2 -a 4,5 -h 400 -q -D 10m

In the reference measurements, isolation reduced the worst-case latency under
load from about 120 µs to 48 µs.

.. dropdown:: Should I also use nohz_full and rcu_nocbs?

   ``nohz_full=5 rcu_nocbs=5`` remove the scheduler tick and RCU callbacks from
   an isolated CPU. The ``cargt-imx-rt`` kernel supports them, but in our
   measurements they did **not** improve the worst case for a task that sleeps
   and wakes periodically, such as ``cyclictest`` or a typical control loop.
   The worst case under load stayed at 48 µs, and idle wake-ups became
   slower. They help a task that runs continuously on the CPU without
   sleeping, such as a polling loop. Measure your own application before you
   enable them.

Interrupt and kernel thread priorities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``PREEMPT_RT``, interrupt handlers run as kernel threads named
``irq/<number>-<name>``, at ``SCHED_FIFO`` priority 50 by default. If your
real-time task depends on a device, for example a CAN or Ethernet interrupt,
raise that interrupt thread above your other tasks:

.. code-block:: bash

   # Find the interrupt threads (named irq/<number>-<device>)
   ps -eLo pid,cls,rtprio,psr,comm | grep irq/
   #   1071  FF     50   0 irq/289-can0
   # Example: run the can0 interrupt thread at priority 80
   chrt -f -p 80 $(pgrep 'irq/.*-can0$')

You can also move a device interrupt onto the isolated CPU so that your task
and its interrupt run on the same core:

.. code-block:: bash

   echo 5 > /proc/irq/<irq-number>/smp_affinity_list

Writing a real-time application
-------------------------------

A real-time application should:

- use a real-time scheduling policy (``SCHED_FIFO``) with a priority above
  ordinary tasks and the interrupt threads it does not depend on,
- lock its memory (``mlockall``) and pre-fault its stack, so that page faults
  cannot occur in the real-time loop,
- keep the CPU out of deep idle states by holding ``/dev/cpu_dma_latency`` at
  ``0``. The cargt-imx-rt image already disables them by default, but holding
  the request keeps the application correct if that default is changed (see
  `CPU idle states`_),
- wait for an absolute time (``clock_nanosleep`` with ``TIMER_ABSTIME``), so
  that wake-up times do not drift,
- avoid system calls that can block for an unbounded time inside the loop
  (file I/O, memory allocation, ``printf`` to a slow console).

The following example runs a 1 ms periodic loop and reports its worst
wake-up latency:

.. code-block:: c

   // rt-loop.c - periodic SCHED_FIFO loop with latency measurement
   // Build: gcc -O2 -o rt-loop rt-loop.c
   // Run:   taskset -c 5 ./rt-loop
   #include <fcntl.h>
   #include <sched.h>
   #include <stdint.h>
   #include <stdio.h>
   #include <string.h>
   #include <sys/mman.h>
   #include <time.h>
   #include <unistd.h>

   #define PERIOD_NS  1000000L   /* 1 ms */
   #define LOOPS      10000

   static void prefault_stack(void)
   {
       unsigned char buf[64 * 1024];
       memset(buf, 0, sizeof(buf));
   }

   int main(void)
   {
       struct sched_param sp = { .sched_priority = 80 };
       struct timespec next, now;
       long lat, max_lat = 0;
       int32_t zero = 0;

       /* Keep CPUs out of deep idle states while this file stays open */
       int pm_qos_fd = open("/dev/cpu_dma_latency", O_WRONLY);
       if (pm_qos_fd < 0 || write(pm_qos_fd, &zero, sizeof(zero)) != sizeof(zero))
           perror("/dev/cpu_dma_latency");

       if (mlockall(MCL_CURRENT | MCL_FUTURE))
           perror("mlockall");
       prefault_stack();
       if (sched_setscheduler(0, SCHED_FIFO, &sp))
           perror("sched_setscheduler (run as root)");

       clock_gettime(CLOCK_MONOTONIC, &next);
       for (int i = 0; i < LOOPS; i++) {
           next.tv_nsec += PERIOD_NS;
           if (next.tv_nsec >= 1000000000L) {
               next.tv_nsec -= 1000000000L;
               next.tv_sec++;
           }
           clock_nanosleep(CLOCK_MONOTONIC, TIMER_ABSTIME, &next, NULL);
           clock_gettime(CLOCK_MONOTONIC, &now);

           lat = (now.tv_sec - next.tv_sec) * 1000000000L
                 + (now.tv_nsec - next.tv_nsec);
           if (lat > max_lat)
               max_lat = lat;

           /* ... real-time work goes here ... */
       }
       printf("max wake-up latency: %ld us\n", max_lat / 1000);
       if (pm_qos_fd >= 0)
           close(pm_qos_fd);
       return 0;
   }

The real-time image includes ``packagegroup-core-buildessential``, so you can
build and test small programs like this directly on the target. For production
software, add a Yocto recipe (see :ref:`yocto-development`).

To start a real-time application as a service, set its scheduling and CPU in
the systemd unit:

.. code-block:: ini

   [Service]
   ExecStart=/usr/bin/my-rt-app
   CPUSchedulingPolicy=fifo
   CPUSchedulingPriority=80
   CPUAffinity=5
   LimitMEMLOCK=infinity

Precise time synchronization (PTP)
----------------------------------

The i.MX 95 Ethernet controllers (ENETC) timestamp PTP packets in hardware.
``ptp4l`` from ``linuxptp`` can synchronize the Ethernet hardware clocks
(``/dev/ptp0``) of several boards to within tens of nanoseconds.

#. Check that the port supports hardware timestamping:

   .. code-block:: bash

      ethtool -T eth1

#. On the board that provides the time (the grandmaster):

   .. code-block:: bash

      chrt -f 70 ptp4l -i eth1 -2 -m --priority1=100

#. On each board that follows it:

   .. code-block:: bash

      chrt -f 70 ptp4l -i eth0 -2 -s -m

   ``-2`` uses IEEE 802.3 (layer 2) transport, so no IP address is needed.
   ``-s`` makes the board a slave only. Once synchronized (servo state
   ``s2``), the slave reports its offset from the master every second:

   .. code-block:: text

      ptp4l[115.438]: master offset         22 s2 freq  +16584 path delay       715

#. To make the system clock (``CLOCK_REALTIME``) follow the Ethernet hardware
   clock, also run ``phc2sys``:

   .. code-block:: bash

      chrt -f 60 phc2sys -s eth0 -w -m

Between a 00414 on a 00365 carrier and an FRDM-IMX95, connected by a direct
cable, overnight under full CPU load, the median offset was 8 ns, 99 % of
samples were within 35 ns and 99.9 % within 223 ns.

.. note::

   Always run ``ptp4l`` and ``phc2sys`` with a real-time priority (``chrt -f``).
   At normal priority, a busy system can delay ``ptp4l`` by hundreds of
   milliseconds, which causes ``clockcheck: clock jumped`` messages and short
   losses of synchronization.

Configuration examples for other PTP profiles (gPTP/802.1AS, telecom profiles,
transparent clocks) are installed in ``/etc/ptp4l_cfg/``.

EtherCAT
--------

The real-time image includes the IgH EtherCAT master (``ethercat`` tool and
kernel modules) with NXP's native ENETC drivers.

The EtherCAT device drivers are **not loaded automatically**.
``cargt-rt-config`` blacklists them in
``/etc/modprobe.d/cargt-rt-ethercat.conf``. Otherwise udev would load them on
every boot and leave an unconfigured EtherCAT master and a second set of
Ethernet drivers alongside the standard ones. The EtherCAT service still loads
the modules by name once you configure it in ``/etc/ethercat.conf``.

An EtherCAT master needs an Ethernet port of its own. See the NXP
`Real-time Edge Yocto Project User Guide <https://www.nxp.com/docs/en/user-guide/RTEDGEYOCTOUG.pdf>`_
and the
`IgH EtherCAT Master documentation <https://docs.etherlab.org/ethercat/1.6/doxygen/index.html>`_
for how to configure the master and dedicate a port.

Troubleshooting
---------------

``/sys/kernel/realtime`` does not exist or is 0
   The standard kernel is running. Check that the image was built with
   ``DISTRO=cargt-imx-rt`` and that SWUpdate switched to the new root
   partition (``cat /proc/cmdline``).

``cyclictest`` maximum is much higher than the reference results
   Check the CPU governor, look for thermal throttling in
   ``/sys/devices/system/cpu/cpufreq/policy0/scaling_cur_freq`` during the
   test, and look for drivers or services that run at a high real-time
   priority (``ps -eLo pid,cls,rtprio,comm | sort -k3 -n``).

A point-to-point Ethernet link loses its IP address every 45 seconds
   NetworkManager tries DHCP on every port by default. On a port without a DHCP
   server it gives up after 45 seconds and removes the port's addresses. Give
   the port a static configuration:

   .. code-block:: bash

      nmcli con add type ethernet ifname eth1 con-name p2p-eth1 \
          ipv4.method manual ipv4.addresses 192.168.77.1/24 ipv6.method disabled

``ptp4l`` reports ``clockcheck: clock jumped`` or ``SYNCHRONIZATION_FAULT``
   ``ptp4l`` was delayed by other load. Run it with ``chrt -f 70`` (see
   `Precise time synchronization (PTP)`_).

References
----------

- `NXP Real-time Edge Software <https://www.nxp.com/design/design-center/software/development-software/real-time-edge-software:REALTIME-EDGE-SOFTWARE>`_
- `NXP Real-time Edge Yocto Project User Guide (RTEDGEYOCTOUG) <https://www.nxp.com/docs/en/user-guide/RTEDGEYOCTOUG.pdf>`_
- `Linux Foundation real-time Linux wiki <https://wiki.linuxfoundation.org/realtime/start>`_
- `cyclictest documentation <https://wiki.linuxfoundation.org/realtime/documentation/howto/tools/cyclictest/start>`_
- `Kernel parameters: isolcpus, irqaffinity, nohz_full <https://docs.kernel.org/admin-guide/kernel-parameters.html>`_
- `linuxptp project <https://linuxptp.nwtime.org/>`_

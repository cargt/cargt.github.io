.. _cortex-m:

The Cortex-M Cores
==================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX`

Most i.MX SoCs have a Cortex-M core next to the Cortex-A cores that run
Linux. This page says which core each Cargt SOM has, when Cargt advises
using it and when an external microcontroller is the better choice, and
how to start firmware on the i.MX 93's Cortex-M33 from Linux.

.. contents:: On this page
   :local:
   :depth: 1

Which Core Each SOM Has
-----------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 25 20 55

   * - SoC
     - Cortex-M core
     - In Cargt images
   * - i.MX 8M Plus (00377)
     - Cortex-M7
     - Free for your firmware. U-Boot has ``bootaux``. Cargt has no RPMsg
       device trees for it.
   * - i.MX 91 (00363-91)
     - None
     - See :doc:`catalog/soms/00363-91-imx91-osml-iw612`.
   * - i.MX 93 (00363, 00324, 00359)
     - Cortex-M33
     - Free for your firmware, unless the NPU is on (see :doc:`npu`). The
       00363 has ``-rpmsg`` device trees; see `Running Firmware on the
       i.MX 93 M33`_.
   * - i.MX 95 (00414)
     - Cortex-M33 and Cortex-M7
     - The M33 runs the System Manager, so it is not available. The M7 is
       free; see :doc:`imx95-system-manager`.

When to Use an External Microcontroller
---------------------------------------

The Cortex-M core is part of the same SoC as Linux, so it shares its
power, reset and clocks with Linux. Cargt advises an external
microcontroller instead when your product needs any of these:

- **I/O that keeps running while Linux restarts.** A reboot, a software
  update or a watchdog reset resets the whole SoC, the Cortex-M core
  included.
- **I/O within a fixed, short time after power-on.** The core runs nothing
  until U-Boot (``bootaux``) or Linux (remoteproc) loads its firmware, and
  that happens only after the boot ROM and U-Boot have started.
- **Firmware that is updated and tracked on its own.** Cargt images and
  software updates don't build or install Cortex-M firmware. You add it to
  your image yourself, for example in ``/lib/firmware``.

The Cortex-M core suits jobs that Linux starts and that may stop when Linux
restarts, such as time-critical sampling or a protocol with tight timing.

Each peripheral belongs either to Linux or to the Cortex-M firmware, never
both. Give a peripheral to the firmware by disabling it in the Linux
device tree. Linux also turns off clocks that no Linux driver uses, so the
firmware's clocks have to be listed on the Cortex-M node, as the i.MX 93
``-rpmsg`` device trees do for LPUART2.

Running Firmware on the i.MX 93 M33
-----------------------------------

The ``-rpmsg`` device trees for the 00363 turn on the M33 under Linux
remoteproc, with RPMsg for messages between Linux and the M33. They also
reserve 16 MB of DDR at ``0xa5000000`` for the M33. The default device
trees leave the M33 alone.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 60

   * - Machine
     - ``-rpmsg`` device trees
   * - ``imx93-cargt-00363-00365``
     - ``imx93-cargt-00363-00365-rpmsg.dtb``,
       ``imx93-cargt-00363-00365-glt0557201280is1-rpmsg.dtb``,
       ``imx93-cargt-00363-00365-glt1011280800is1-rpmsg.dtb``
   * - ``imx93-cargt-00363-00428``
     - ``imx93-cargt-00363-00428-rpmsg.dtb``,
       ``imx93-cargt-00363-00428-glt0557201280is1-rpmsg.dtb``

These device trees give LPUART2 to the M33, because NXP's example
firmware uses it as its debug console. On the 00363, LPUART2 is the
mikroBUS UART, so Linux has no mikroBUS UART with them. There are no
``-rpmsg`` variants for the 2.8" SPI display, which uses the same pins as
GPIOs.

Select one and reboot:

.. code-block:: bash

   fw_setenv fdtfile boot/imx93-cargt-00363-00365-rpmsg.dtb
   reboot

After the reboot, the M33 shows up as ``remoteproc0``, offline:

.. code-block:: bash

   cat /sys/class/remoteproc/remoteproc0/name     # imx-rproc
   cat /sys/class/remoteproc/remoteproc0/state    # offline

The image has NXP's example firmware for the i.MX 93 EVK in
``/lib/firmware``. The ``str_echo`` example echoes back whatever Linux
sends it. Start it:

.. code-block:: bash

   cd /sys/class/remoteproc/remoteproc0
   echo imx93-11x11-evk_m33_TCM_rpmsg_lite_str_echo_rtos.elf > firmware
   echo start > state

The firmware announces an RPMsg channel, and the ``imx_rpmsg_tty`` driver
creates ``/dev/ttyRPMSG30``. Text written to it comes back from the M33:

.. code-block:: bash

   stty -F /dev/ttyRPMSG30 raw -echo
   cat /dev/ttyRPMSG30 &
   echo hello > /dev/ttyRPMSG30

``echo stop > state`` stops the M33 and removes the tty. The
``imx93-11x11-evk_m33_TCM_rpmsg_lite_pingpong_rtos_linux_remote.elf``
example works the same way with the ``imx_rpmsg_pingpong`` module.

Your own firmware is built with NXP's MCUXpresso SDK for the i.MX 93. Link
it to run from the M33's TCM: remoteproc loads the ELF file into the TCM
itself and can't load firmware linked to the DDR region. The DDR region is
for the firmware's data at run time.

.. note::

   U-Boot's ``bootaux`` can also start firmware before Linux, and Linux
   then attaches to it (``state`` reads ``attached``). The firmware is
   then already running when Linux turns off the clocks that no Linux
   driver uses. The ``-rpmsg`` device trees keep LPUART2's clock on for
   NXP's examples. If your firmware uses other peripherals that Linux
   doesn't drive, add their clocks to the ``&cm33`` node too, or the
   firmware stops when Linux turns them off.

These steps were checked on an i.MX 93 00363 on the 00428 with the
``imx93-cargt-00363-00428-glt0557201280is1-rpmsg`` device tree.

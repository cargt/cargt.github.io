.. _imx95-system-manager:

i.MX 95 Boot Firmware and System Manager
========================================

The i.MX 95 boots differently from the i.MX 8M Plus, i.MX 91 and i.MX 93.
Before U-Boot runs on the Cortex-A55 cores, two firmware stages run on the
Cortex-M33: **OEI**, which trains the DDR, and the **System Manager**,
which stays running for as long as the board is on. The System Manager
owns the chip's power, clocks, resets and pins, and decides which of them
Linux may use. This page explains the boot chain, what the System Manager
does, and what to check when you design a carrier board or change
the configuration. The examples are from an i.MX 95 00414 on the 00365
carrier, running a wrynose image.

.. contents:: On this page
   :local:
   :depth: 1

The Boot Chain
--------------

The boot container (``imx-boot``, see :doc:`storage`) holds every stage up
to U-Boot:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 22 18 60

   * - Stage
     - Runs on
     - What it does
   * - Boot ROM and ELE firmware
     - ROM, EdgeLock Enclave
     - The ROM loads the boot container. The EdgeLock Enclave (ELE)
       firmware checks each part of it, and its signatures when secure boot
       is enabled (see :doc:`secure-boot`).
   * - OEI
     - Cortex-M33
     - Trains the DDR. OEI reads the DDR configuration from the SOM EEPROM
       and trains the matching memory part; see :doc:`production`. OEI then
       ends.
   * - System Manager
     - Cortex-M33
     - Starts and keeps running. It powers up the A55 cores and starts
       SPL on them, and then serves requests from Linux and U-Boot.
   * - SPL, ATF, OP-TEE, U-Boot
     - Cortex-A55
     - SPL loads ATF, OP-TEE and U-Boot from the second container, as on
       the other i.MX SOMs. See :doc:`u-boot`.
   * - Linux
     - Cortex-A55
     - Asks the System Manager for clocks, power, pins and more while it
       runs.

The Cortex-M7 can run your own firmware alongside Linux (see
`The Logical Machines`_). Cargt images do not include M7 firmware in the
boot container.

The System Manager, OEI and the rest of the boot container are not part of
the root file system, so a software update (see :doc:`software-updates`)
does not replace them. To change them, re-flash the board; see
:ref:`running-linux`.

What the System Manager Does
----------------------------

On the i.MX 8M Plus, i.MX 91 and i.MX 93, Linux drives the clock, power
and pin hardware directly. On the i.MX 95 it does not: it sends a request
to the System Manager over the Arm SCMI (System Control and Management
Interface) protocol, and the System Manager checks whether Linux may
use that resource before it acts. The System Manager also handles the
power management ICs (PMICs), the temperature sensors, the watchdog and the
reset reasons.

The kernel log shows the System Manager's version and configuration:

.. code-block:: text

   root@imx95-cargt-00414-00365:~# dmesg | grep -i -E 'scmi|sm '
   ...
   arm-scmi arm-scmi.0.auto: SCMI Protocol v2.1 'NXP:IMX' Firmware version 0x380
   ...
   arm-scmi arm-scmi.0.auto: SM Version	= Build 896, Commit 44f76dcb Oct 09 2026 20:36:59
   arm-scmi arm-scmi.0.auto: Board		= Cargt 00414 SOM, attr=0x00000000
   arm-scmi arm-scmi.0.auto: SM Config	= mx95cargt00414, mSel = 0
   ...
   scmi-imx-misc-ctrl scmi_dev.15: SYS Boot reason: por, origin: -1, errid: -1
   scmi-imx-misc-ctrl scmi_dev.15: LM Boot reason: sw, origin: 2, errid: 1
   ...
   arm-scmi arm-scmi.0.auto: i.MX LMM: 3 Logical Machines

- ``SM Config`` is the name of the System Manager configuration built into
  the image; ``mx95cargt00414`` is Cargt's for the 00414.
- ``SYS Boot reason`` is why the whole chip last reset, for example
  ``por`` (power on). ``LM Boot reason`` is why Linux's own logical machine
  last started, for example ``sw`` (a software reboot). Check them after an
  unexpected reset.

Linux's pin controller is the System Manager's too: the pin control
device is ``scmi_dev.8-scmi-pinctrl-imx`` under
``/sys/kernel/debug/pinctrl/``. You still describe pins in the Linux device
tree as usual.

The Logical Machines
--------------------

The System Manager splits the chip into **logical machines** (LMs). Each
one has its own processors, peripherals, pins and memory, and can be
started, stopped and reset without the others. The Cargt configuration has
three:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 15 85

   * - LM
     - What it owns
   * - SM
     - The System Manager itself on the Cortex-M33, and the hardware it needs:
       the PMIC I²C bus (LPI2C1), its debug UART (LPUART2), the I/O pin
       controller, two watchdogs (WDOG1, WDOG2) and the pins of
       those peripherals.
   * - M7
     - The Cortex-M7, with its own timers, watchdog (WDOG5) and memory. No
       pins.
   * - AP
     - The Cortex-A55 cores running Linux, and every other peripheral and pin.

Two things follow from this:

- **Linux can only use what the AP owns.** A peripheral or pin owned by
  the SM or M7 does not work from Linux, even if the Linux device tree
  enables it: the System Manager refuses the request. LPI2C1 and LPUART2
  are the SM's, so a carrier board cannot use them from Linux.
- **The SOM EEPROM is on LPI2C1**, the System Manager's bus, so U-Boot reads
  it through the System Manager. The Cargt configuration adds a control for
  this.

NXP's evaluation-board configuration gives CAN_FD1, LPUART3 and the pins
GPIO_IO14 and GPIO_IO15 to the M7. The Cargt configuration gives them to
Linux instead, because the 00365 carrier uses them as CAN_A and UART_A on
the OSM connector.

Linux can start and stop firmware on the M7 through the System Manager.
The kernel log shows ``imx-rproc imx95-cm7: Using LMM Protocol OPS``, and
the M7 appears as ``/sys/class/remoteproc/remoteproc1``, offline by
default. Running M7 firmware has not been tested on a Cargt board for this
page.

Changing the Configuration
--------------------------

The configuration is a text file in the Cargt BSP layer,
``meta-imx-cargt/recipes-bsp/imx-system-manager/imx-system-manager/mx95cargt00414.cfg``.
It is not read at run time: the build turns it into System Manager source
code. The machine configuration selects it with
``SYSTEM_MANAGER_CONFIG = "mx95cargt00414"``.

Each LM has a section, and each resource and pin is listed in the section
of the LM that owns it. For example, in the AP section:

.. code-block:: text

   CAN_FD1             OWNER
   ...
   LPUART3             OWNER
   ...
   PIN_GPIO_IO14       OWNER
   PIN_GPIO_IO15       OWNER

To move a peripheral to a different LM, for example to give one to your M7
firmware, move its line, and the lines of its pins, to that LM's section.
Make the change in your own Yocto layer rather than in
``meta-imx-cargt``: copy the file into
``recipes-bsp/imx-system-manager/imx-system-manager/`` in your layer and
add a ``imx-system-manager_%.bbappend`` with:

.. code-block:: bash

   FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

Your layer needs a higher priority than ``meta-imx-cargt`` so that its copy
is used. Then rebuild the image, which rebuilds the boot container, and
re-flash the board. This was not built for this page; see :doc:`yocto` for
creating a layer.

The System Manager source and its configuration format are documented in
NXP's `imx-sm <https://github.com/nxp-imx/imx-sm>`_ repository.

The System Manager Console and Production Builds
------------------------------------------------

The System Manager prints to its own debug UART, LPUART2 at 115200 baud,
not to the Linux console. Cargt images build it with NXP's debug monitor
in the mode that starts when a character is received on that UART
(``SYSTEM_MANAGER_MONITOR_MODE = "2"``, the NXP default). The monitor has
commands to show information and the reset reason, and also to reset and
power off the system. Output from the System Manager console was not
captured for this page.

NXP states that the debug monitor changes the System Manager's timing and
must not be used in a product. For production images, turn it off in your
layer or distribution configuration:

.. code-block:: bash

   SYSTEM_MANAGER_MONITOR_MODE = "0"

See :doc:`production` for the other steps before production.

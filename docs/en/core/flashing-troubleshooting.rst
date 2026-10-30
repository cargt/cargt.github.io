.. _flashing-troubleshooting:

Flashing Troubleshooting and Recovery
=====================================

This page helps when flashing a board does not work, and explains how to
recover a board that no longer boots. For the normal flashing steps, see
:ref:`running-linux`.

.. contents:: On this page
   :local:
   :depth: 1

Serial Download Mode
--------------------

Every Cargt SOM can be flashed over USB, even with an empty or damaged eMMC,
because the processor's boot ROM can load the boot loader over USB into RAM
(serial download mode on i.MX, USB DFU on STM32MP2). The flashing tool then
writes the eMMC from that RAM copy. Nothing on the eMMC needs to work, so a
board without a microSD slot can always be recovered this way.

The boot switches (SW1) on Cargt carriers select the boot mode. From the
SOM quick start guides, for the 00365 carrier:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 30 30

   * - Mode
     - i.MX (BOOT1, BOOT0)
     - STM32MP2 (BOOT0, BOOT1)
   * - Flash over USB
     - 0, 1 (USB / serial download)
     - 0, 0 (UART and USB)
   * - Boot from eMMC (default)
     - 1, 0
     - 1, 0
   * - Boot from microSD
     - 1, 1
     - 0, 1

Note that the i.MX and STM32MP2 guides list the two switches in opposite
order. Change the switches with the power off, and set them back to eMMC
after flashing. The quick start guides are linked from each SOM's page in
the :doc:`index`.

On a custom carrier, bring the SOM's boot-mode pins (``BOOT_SEL`` on OSM
SOMs) out to switches, jumpers or test points, so that you can always reach
serial download mode. A board whose boot loader still runs can also enter
UUU's fastboot mode from U-Boot; see :ref:`uuu-from-environment`. That
does not help when the boot loader itself is damaged.

i.MX: UUU
---------

Use a Recent UUU
~~~~~~~~~~~~~~~~

UUU only talks to processors it knows. An older version waits forever for a
board it does not recognise. The first version that knows each processor's
boot ROM:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 25 45

   * - Processor
     - Minimum UUU
     - USB ID in serial download mode
   * - i.MX 8M Plus
     - any 1.4 or later
     - ``1fc9:0146``
   * - i.MX 93
     - 1.4.243
     - ``1fc9:014e``
   * - i.MX 91
     - 1.5.177
     - ``1fc9:0159``
   * - i.MX 95
     - 1.5.141
     - ``1fc9:015d`` (``1fc9:015c`` needs 1.5.181)

Use the newest release from the
`UUU releases page <https://github.com/nxp-imx/mfgtools/releases>`__. The
first line UUU prints is its version:

.. code-block:: text

   $ uuu -lsusb
   uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.5.233-0-g79ce7d2

   Connected Known USB Devices
           Path     Chip    Pro     Vid     Pid     BcdVersion      Serial_no
           ====================================================================

With nothing listed, as here, UUU sees no board it can flash.

"Wait for Known USB Device Appear..."
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UUU prints this and waits when it cannot find a board it knows:

.. code-block:: text

   $ uuu -b emmc_all imx-boot.tagged <image>.wic.zst
   uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.5.233-0-g79ce7d2
   Wait for Known USB Device Appear...

Work through these checks in order:

1. **Is the board in serial download mode?** Check the boot switches (see
   above), and power the board off and on after changing them.

2. **Does the host see the board on USB?** On Linux, run ``lsusb`` and look
   for vendor ``1fc9`` (NXP):

   .. code-block:: bash

      lsusb | grep 1fc9

   If nothing with ``1fc9`` appears, the problem is the connection: use a
   USB cable that carries data (some charging cables do not), connect it to
   the carrier's USB download port as shown in the quick start guide, and
   try another port on the host, without a hub.

3. **Is UUU new enough?** If ``lsusb`` shows the board but ``uuu -lsusb``
   does not list it, the processor's USB ID is missing from your UUU (see
   the table above). Install a newer UUU.

4. **Linux permissions.** If ``uuu -lsusb`` lists the board only when run
   with ``sudo``, install UUU's udev rules, then unplug and reconnect the
   board:

   .. code-block:: bash

      sudo sh -c "uuu -udev > /etc/udev/rules.d/70-uuu.rules"
      sudo udevadm control --reload

   The rules list the USB IDs that this version of UUU knows, so run these
   commands again after updating UUU.

Once the board is found, ``uuu -lsusb`` lists it with the protocol it is
using: ``SDPS:`` for the boot ROM, and ``FB:`` once U-Boot's fastboot is
running (``1fc9:0152``), as in the example in :ref:`running-linux`.

The i.MX 95
~~~~~~~~~~~

On the i.MX 95, ``uuu imx-boot`` and the built-in ``-b`` scripts stop after
the boot ROM stage. Load the boot loader into RAM with the explicit script
in :ref:`running-linux` instead. A complete procedure for flashing the eMMC
of an i.MX 95 00414 over USB is not documented yet; contact Cargt if you
need to recover one.

Flashing Stops Partway
~~~~~~~~~~~~~~~~~~~~~~

If UUU stops with an error partway through, power the board off and on with
the boot switches still on serial download, and run the same command again:
UUU starts again from the boot ROM and rewrites everything. ``-v`` prints each step, and ``-l <file>`` saves a log to send to
Cargt.

When flashing several boards at once from a host with little memory, UUU
can run out of memory; flash one board at a time with ``-m``, as described
in :ref:`running-linux`.

STM32MP2: STM32CubeProgrammer
-----------------------------

STM32MP2 SOMs are flashed with ST's
`STM32CubeProgrammer <https://www.st.com/en/development-tools/stm32cubeprog.html>`__
over USB, using a flash layout (``.tsv``) file that lists the partitions and
the file for each.

1. **Install STM32CubeProgrammer** from ST. On Linux, also install its udev
   rules so it can use the USB port without ``sudo``:

   .. code-block:: bash

      sudo apt-get install libusb-1.0-0
      cd <STM32CubeProgrammer install directory>/Drivers/rules
      sudo cp *.* /etc/udev/rules.d/

   On Windows, run ``STM32 Bootloader.bat`` from the ``Drivers/DFU_Driver``
   folder of the installation to install the USB DFU driver.

2. **Download the image directory** for your machine from the
   `Cargt image repository <https://yocto.cargt.com/images>`__, for example
   ``scarthgap/stm32mp25-cargt-00395-02-00365/``. The flash layout refers to
   files in the ``arm-trusted-firmware/``, ``fip/`` and other directories
   next to it, so keep the directory structure.

3. **Put the board in USB mode:** with the power off, set the boot switches
   to UART and USB (see `Serial Download Mode`_), connect the carrier's USB
   port to the host, and power on.

4. **Check the connection:**

   .. code-block:: bash

      STM32_Programmer_CLI -l usb

   The board appears under ``DFU Interface``. With no board in USB mode, the
   tool prints ``No STM32 device in DFU mode connected``.

5. **Flash the eMMC.** From the image directory, pass the path to the flash
   layout:

   .. code-block:: bash

      cd stm32mp25-cargt-00395-02-00365
      STM32_Programmer_CLI -c port=usb1 \
          -w flashlayout_cargt-image-dev/optee/FlashLayout_emmc_stm32mp257f-cargt-00395-02-00365-optee.tsv

   Use this ``optee`` layout without a display suffix: it is the only one
   with the A/B partitions that RAUC updates need (see
   :ref:`running-linux`).

6. **Boot from eMMC:** power off, set the boot switches back to eMMC, and
   power on.

If ``STM32_Programmer_CLI -l usb`` does not list the board, check the boot
switches, the cable and the udev rules or Windows driver, as for UUU above.

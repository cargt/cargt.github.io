Getting Started
===============

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

This page takes you from a Cargt board in hand to a logged-in Linux shell,
using a pre-built image. It applies to every Cargt SOM. Where i.MX and
STM32MP2 differ, pick your platform in the tabs; the choice applies to
every tab on the page.

.. _Cargt Package Repository Images: https://yocto.cargt.com/images

.. contents::
   :local:
   :depth: 1

Step 1: What You Need
---------------------

- A Cargt SOM fitted to its carrier board, and the carrier's power supply.
- A USB cable from the carrier's USB device (download) port to your host
  computer, for flashing.
- A serial connection to the carrier's debug console (a USB-to-serial
  adapter or the carrier's console port; see your carrier's page in the
  :doc:`index`).
- A Linux or Windows host computer with the flashing tool for your
  platform:

  .. tab-set::
      :sync-group: platform

      .. tab-item:: i.MX
          :sync: imx

          `UUU <https://github.com/nxp-imx/mfgtools/releases>`__ (NXP's
          Universal Update Utility). Use a recent version; see
          :doc:`flashing-troubleshooting`.

      .. tab-item:: STM32MP2
          :sync: stm32mp2

          `STM32CubeProgrammer <https://www.st.com/en/development-tools/stm32cubeprog.html>`__
          for eMMC, or ``bmaptool`` on a Linux host for an SD card.

Step 2: Find Your MACHINE
-------------------------

Every image is built for one ``MACHINE``: a SOM on a carrier board, such as
``imx93-cargt-00363-00365``. Read the part number on your SOM and match it
to a ``MACHINE`` with :doc:`identify-som`, then find its release and image
directory in :doc:`releases`. An image for a different ``MACHINE`` may not
boot.

Step 3: Connect the Serial Console
----------------------------------

The debug console shows the boot messages, the U-Boot prompt and the Linux
login prompt. Connect a terminal program at 115200 baud, 8N1, no flow
control. From a Linux host, for example:

.. code-block:: bash

   picocom -b 115200 /dev/ttyUSB0      # exit with Ctrl+A, Ctrl+X

See :ref:`the U-Boot page <u-boot>` for more about the console.

.. warning::

   On current :doc:`00326 <catalog/carrier-boards/00326-sodimm-carrier>`
   boards, a cable on the console UART during reset can make the board hang
   on reboot. See the 00326 page.

.. _running-linux:

Step 4: Download and Flash an Image
-----------------------------------

Flashing erases everything on the target storage.

.. tab-set::
    :sync-group: platform

    .. tab-item:: i.MX
        :sync: imx

        .. note::

           CARGT recommends eMMC for performance and reliability.
           eMMC is the default. Using SD card requires changing U-Boot variables and expert knowledge.

        #. Put the board into the UUU mode as per the hardware design's user guide.

           - Option 1: For OSM-L based designs, this typically involves holding the BOOT button while powering on the board.
           - Option 2: If the board has no BOOT button, set ``bootcmd`` in the U-Boot environment; see `NXP - Enter UUU mode using U-Boot Environment Variable Method`_.

        #. Connect the board to the host computer via USB and check the connection by running:

           .. code-block:: bash

              uuu -lsusb

           The output should list the connected device.
        #. Download these files for your machine from the `Cargt Package Repository Images`_,
           for example from ``wrynose/imx93-cargt-00363-00365/``:

           - ``imx-boot.tagged`` - the bootloader
           - ``cargt-image-<type>-<machine>.rootfs.wic.zst`` - the full disk image
             (partition table and filesystems), compressed with zstd
           - ``cargt-image-<type>-<machine>.rootfs.wic.bmap`` - optional, the block
             map that makes flashing much faster; see `Faster Flashing with bmap`_

           .. note::

              scarthgap images name the bootloader file ``imx-boot-tagged``.
              Use whichever name is in the directory you downloaded from.

        #. Flash the bootloader and image. This erases everything on the target
           storage.

           To eMMC:

           .. code-block:: bash

              uuu -b emmc_all imx-boot.tagged cargt-image-dev-imx93-cargt-00363-00365.rootfs.wic.zst

           To an SD card:

           .. code-block:: bash

              uuu -b sd_all imx-boot.tagged cargt-image-dev-imx93-cargt-00363-00365.rootfs.wic.zst

        #. Power cycle the board without holding the BOOT button. If you entered
           UUU mode by changing ``bootcmd``, restore it first (see
           `NXP - Enter UUU mode using U-Boot Environment Variable Method`_).

        If ``uuu`` waits at ``Wait for Known USB Device Appear...`` or fails, see
        :doc:`flashing-troubleshooting`.

        For more ``uuu`` options, faster flashing with ``.wic.bmap`` and
        flashing several boards at once, see `More About Flashing with UUU`_.

    .. tab-item:: STM32MP2
        :sync: stm32mp2

        Each STM32MP2 image directory on the `Cargt Package Repository Images`_
        (for example ``scarthgap/stm32mp25-cargt-00395-02-00365/``) contains
        everything needed for both boot media:

        - **eMMC:** flash with
          `STM32CubeProgrammer <https://www.st.com/en/development-tools/stm32cubeprog.html>`__
          over USB, using this flash layout from the ``flashlayout_cargt-image-dev/``
          directory (here for the 00395-02):

          .. code-block:: text

             optee/FlashLayout_emmc_stm32mp257f-cargt-00395-02-00365-optee.tsv

          It is the only eMMC layout with the A and B partitions that RAUC updates
          need (see :doc:`rauc-ota-updates`). The layouts in ``opteemin/``, and the
          ``-glt*`` display variants in both directories, have a single set of
          partitions, so RAUC updates cannot work on a board flashed with them.
        - **SD card:** write the ``.wic`` image from a Linux host. ``bmaptool``
          uses the ``.wic.bmap`` file next to the image and only writes the blocks
          that contain data:

          .. code-block:: bash

             bmaptool copy cargt-image-dev-cargt-openstlinux-weston-stm32mp25-cargt-00395-02-00365.rootfs.wic.bz2 /dev/sdX

          Replace ``/dev/sdX`` with the SD card device (check with ``lsblk``).
          Everything on the card is erased.

        A step-by-step STM32CubeProgrammer guide is planned. For the 00395 A/B
        partition layout, see :doc:`rauc-ota-updates`.

Step 5: Boot and Log In
-----------------------

Power the board on (without holding the BOOT button) and watch the serial
console. The bootloader prints its banner, Linux boots, and the console
shows a login prompt named after the ``MACHINE``; the examples on this site
run as ``root``. To confirm the board is running the image you flashed, see
:doc:`identify-som`.

If the board doesn't boot, or the flashing tool doesn't see it, see
:doc:`flashing-troubleshooting`.

Step 6: Next Steps
------------------

- Get the board on a network: :doc:`networking` and :doc:`wifi`.
- Try the hardware from Linux: :doc:`linux-basics`.
- Build your own image with the Cargt BSP: :doc:`yocto`.
- Update a board in the field without reflashing: :doc:`software-updates`.
- The Cargt source code is on `GitHub <https://github.com/cargt>`__, and
  images and package feeds are on `yocto.cargt.com <https://yocto.cargt.com>`__;
  :doc:`releases` links them per ``MACHINE``.

More About Flashing with UUU
----------------------------

Example session on Windows, flashing a board that is already in fastboot
mode (``FB:``):

.. code-block:: text

   C:\NXP\images>uuu -lsusb
   uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.5.201-0-g727fc2b

   Connected Known USB Devices
           Path     Chip    Pro     Vid     Pid     BcdVersion      Serial_no
           ====================================================================
           4:2              FB:     0x1FC9 0x0152   0x0221   15FD978D21EA40AF

   C:\NXP\images>uuu -b emmc_all imx-boot-tagged cargt-image-core.rootfs.wic.zst
   uuu (Universal Update Utility) for nxp imx chips -- libuuu_1.5.201-0-g727fc2b

   Success 1    Failure 0

   4:2-15FD978D 8/ 8 [Done                                  ] FB: done

Other UUU options:

- ``-v`` prints verbose output.
- ``-l <log_file>`` writes a log of the session.
- ``uuu`` accepts the image uncompressed (``.wic``) or compressed
  (``.wic.zst``, ``.wic.gz``, ``.wic.bz2``).
- Program only the bootloader:

  .. code-block:: bash

     uuu -b emmc imx-boot.tagged
     uuu -b sd imx-boot.tagged

- Run the bootloader (SPL and U-Boot) from RAM without writing anything:

  .. code-block:: bash

     uuu imx-boot

.. note::

   **i.MX 95:** ``uuu imx-boot`` and the built-in ``-b`` scripts stop after
   the ROM stage on i.MX 95 and never load the SPL. Use an explicit
   ``uuu`` script instead. Save this as ``imx95-boot.uuu``:

   .. code-block:: text

      uuu_version 1.5.0
      SDPS: boot -f imx-boot
      SDPV: write -f imx-boot -skipspl
      SDPV: jump

   and run ``uuu imx95-boot.uuu``. The console shows DDR training output
   followed by the SPL and U-Boot banners. Verified on the 00414 SOM in
   serial download mode (October 2026).

Faster Flashing with bmap
~~~~~~~~~~~~~~~~~~~~~~~~~

The disk image is about 15 GB uncompressed, but most of it is empty space:
the second root partition, free space in the root file system, and
``/data``. Without help, ``uuu`` decompresses and scans all of it, and the
eMMC writes zeros to the empty areas. The ``.wic.bmap`` file published next
to each image lists the blocks that hold data (about 2.2 GB for
``cargt-image-dev``), and ``-bmap`` tells ``uuu`` to write only those:

.. code-block:: bash

   uuu -bmap -b emmc_all imx-boot.tagged cargt-image-dev-imx93-cargt-00363-00428.rootfs.wic.zst

Keep the ``.wic.bmap`` file in the same folder as the image. For
``<name>.wic.zst``, ``uuu`` looks for ``<name>.wic.bmap``. The built-in
``emmc_all`` and ``sd_all`` scripts only use it when you pass ``-bmap``.

Flashing ``cargt-image-dev`` to the eMMC of an i.MX 93 00363 on the 00428
carrier took 2 minutes 32 seconds with ``-bmap``, and 15 to 20 minutes
without it.

To flash several boards at once, run ``uuu`` in daemon mode with ``-d``; it
flashes every board that connects until you stop it. Each board needs
memory on the host computer: on a host with 2 GB of RAM, flashing three
boards at once ran out of memory, so flash one board at a time there with
``-m <usb path>`` (the paths are listed by ``uuu -lsusb``):

.. code-block:: bash

   uuu -d -bmap -b emmc_all imx-boot.tagged <image>.wic.zst          # all boards
   uuu -m 1:12 -bmap -b emmc_all imx-boot.tagged <image>.wic.zst     # one board

.. _uuu-from-environment:

NXP - Enter UUU mode using U-Boot Environment Variable Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - To enter UUU mode without using the BOOT button, you can set the U-Boot environment variable ``bootcmd`` to boot into UUU mode on the next reboot.
      Use either ``fw_setenv`` from Linux or ``setenv`` at the U-Boot prompt; see :ref:`u-boot-environment` for how to reach the prompt and which variables Cargt images use.

   .. code-block:: bash

      # Using fw_setenv (from Linux shell)
      fw_setenv bootcmd 'fastboot auto'
      fw_printenv bootcmd  # Verify the change
      reboot

      # Using setenv (from U-Boot console)
      setenv bootcmd 'fastboot auto'
      saveenv
      printenv bootcmd  # Verify the change
      reset

   .. warning::

      The board now enters fastboot on **every** boot until ``bootcmd`` is
      restored. Flashing with ``uuu`` does not necessarily reset the
      U-Boot environment. Before changing it, note the current value with
      ``fw_printenv bootcmd``. To restore the default afterwards, stop at
      the U-Boot prompt and run:

      .. code-block:: bash

         env default bootcmd
         saveenv
         reset

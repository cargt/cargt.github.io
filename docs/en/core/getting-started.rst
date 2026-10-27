Getting Started with Embedded Linux
===================================

Cargt Provided Software Resources
---------------------------------

Public Yocto Source Code Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Cargt GitHub Organization <https://github.com/cargt>`_ – Public repositories for Yocto layers, example applications, and board support packages.

Public Package Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Cargt Package Repository <https://yocto.cargt.com>`_ – Public repositories for pre-built packages and binaries for development with Cargt hardware designs.

Public Pre-compiled Images
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _Cargt Package Repository Images: https://yocto.cargt.com/images

- `Pre-built complete system images <https://yocto.cargt.com/images>`_ for supported Cargt hardware suitable for initial flashing or full system recovery.
- `Incremental update images <https://yocto.cargt.com/images>`_ compatible with SWUpdate for in-field updates without reflashing the entire system.

.. _running-linux:

Running Linux on a Cargt design
-------------------------------

Flashing a Pre-compiled image to eMMC / SD card using UUU on an i.MX design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   CARGT recommends eMMC for performance and reliability.
   eMMC is the default. Using SD card requires changing U-Boot variables and expert knowledge.

#. Put the board into the UUU mode as per the hardware design's user guide.

   - Option 1: For OSM-L based designs, this typically involves holding the BOOT button while powering on the board.
   - Option 2: U-boot Environment Variable Method can be used if BOOT button is not available. See U-Boot Environment Variables section for details.

#. Connect the board to the host computer via USB and check the connection by running:

   .. code-block:: bash

      uuu -lsusb

   The output should list the connected device.
#. Download two files for your machine from the `Cargt Package Repository Images`_,
   for example from ``wrynose/imx93-cargt-00363-00365/``:

   - ``imx-boot.tagged`` - the bootloader
   - ``cargt-image-<type>-<machine>.rootfs.wic.zst`` - the full disk image
     (partition table and filesystems), compressed with zstd

   .. note::

      Older releases named the bootloader file ``imx-boot-tagged``. Use
      whichever name is in the directory you downloaded from.

#. Flash the bootloader and image. This erases everything on the target
   storage.

   To eMMC:

   .. code-block:: bash

      uuu -b emmc_all imx-boot.tagged cargt-image-dev-imx93-cargt-00363-00365.rootfs.wic.zst

   To an SD card:

   .. code-block:: bash

      uuu -b sd_all imx-boot.tagged cargt-image-dev-imx93-cargt-00363-00365.rootfs.wic.zst

#. Power cycle the board without holding the BOOT button. If you entered
   UUU mode by changing ``bootcmd``, restore it first (see below).

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

Flashing a Pre-compiled image on an STM32MP2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each STM32MP2 image directory on the `Cargt Package Repository Images`_
(for example ``scarthgap/stm32mp25-cargt-00395-02-00365/``) contains
everything needed for both boot media:

- **eMMC:** flash with
  `STM32CubeProgrammer <https://www.st.com/en/development-tools/stm32cubeprog.html>`__
  over USB, using the ``FlashLayout_emmc_*.tsv`` flash layout from the
  ``flashlayout_cargt-image-dev/`` directory. Use the main layout, not one of
  the ``-glt*`` display variants.
- **SD card:** write the ``.wic`` image from a Linux host. ``bmaptool``
  uses the ``.wic.bmap`` file next to the image and only writes the blocks
  that contain data:

  .. code-block:: bash

     bmaptool copy cargt-image-dev-cargt-openstlinux-weston-stm32mp25-cargt-00395-02-00365.rootfs-<timestamp>.wic.bz2 /dev/sdX

  Replace ``/dev/sdX`` with the SD card device (check with ``lsblk``).
  Everything on the card is erased.

A step-by-step STM32CubeProgrammer guide is planned. For the 00395 A/B
partition layout, see :doc:`rauc-ota-updates`.

Understanding U-Boot Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

U-Boot variables can be accessed through either the console or ssh session.

   - Console: Interrupt the boot process by pressing any key during the U-Boot countdown.
      This will drop you to the U-Boot command prompt.
      U-Boot variables can be viewed and modified using the ``printenv``, ``setenv``, and ``saveenv`` commands in the U-Boot console.
   - SSH: Connect to the device via SSH once Linux has booted and access U-Boot variables using the ``fw_setenv`` and ``fw_printenv`` utilities.

NXP - Enter UUU mode using U-Boot Environment Variable Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - To enter UUU mode without using the BOOT button, you can set the U-Boot environment variable ``bootcmd`` to boot into UUU mode on the next reboot.
      Use either ``fw_setenv`` or ``setenv`` to set the variable.

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

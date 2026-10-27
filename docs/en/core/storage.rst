.. _storage:

Storage and Boot
================

This page describes how Cargt i.MX images lay out the eMMC or microSD card,
where U-Boot keeps its environment and how the ``/data`` partition is
managed. STM32MP2 00395 images use a different, RAUC-based layout; see
:doc:`rauc-ota-updates`.

Partition Layout (i.MX)
-----------------------

Every Cargt i.MX machine builds its disk image from the same WIC kickstart
file, ``cargt-dev.wks.in`` in ``meta-imx-cargt``:

.. code-block:: text

   part u-boot --source rawcopy --sourceparams="file=imx-boot" --ondisk mmcblk --no-table --align ${IMX_BOOT_SEEK}

   part / --source rootfs --ondisk mmcblk --fstype=ext4 --align 8192 --fixed-size 6144M
   part --ondisk mmcblk --fstype=ext4 --align 8192 --fixed-size 6144M
   part --ondisk mmcblk --fstype=ext4 --label data --align 8192 --fixed-size 2048M

   bootloader --ptable msdos

This gives an MBR partition table and the following layout:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 20 20 60

   * - Region
     - Size
     - Contents
   * - ``imx-boot``
     - no partition
     - Boot container (SPL, ATF, U-Boot and, on i.MX 95, OEI and System
       Manager), written raw at a 32 KiB offset (``IMX_BOOT_SEEK = "32"``).
   * - U-Boot environment
     - 16 KiB, no partition
     - Raw at offset 0x700000 (7 MiB). See `U-Boot Environment`_.
   * - Partition 1
     - 6 GiB
     - Root file system A. The kernel and device trees are in ``/boot``.
   * - Partition 2
     - 6 GiB
     - Root file system B. Empty until the first software update.
   * - Partition 3 (``data``)
     - 2 GiB, grown at boot
     - Persistent data, mounted on ``/data``. Not touched by software
       updates.

There is no FAT boot partition. U-Boot loads ``boot/Image`` and
``boot/<fdtfile>`` from the ext4 root partition selected by the ``mmcpart``
variable, and passes ``root=/dev/mmcblk<mmcdev>p<mmcpart>`` to the kernel.
Software updates write the inactive root partition and change ``mmcpart``;
see :ref:`swupdate`.

Checking the Layout
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   lsblk                  # partitions and mount points
   cat /proc/cmdline      # root= shows the running root partition
   fw_printenv mmcpart    # partition U-Boot boots next

``mmcblk0`` is the device U-Boot calls MMC 0; on most Cargt boards that is the
eMMC, and the microSD card is ``mmcblk1``. ``mmcblk0boot0`` and
``mmcblk0boot1`` are the eMMC hardware boot partitions. Cargt images do not
use them, and Linux keeps them read-only by default.

Using a Different Layout
~~~~~~~~~~~~~~~~~~~~~~~~

To change partition sizes or add partitions, copy ``cargt-dev.wks.in`` into
your own layer (for example ``files/wic/my-product.wks.in``), edit it, and
select it in your machine configuration or ``local.conf``:

.. code-block:: bash

   WKS_FILE = "my-product.wks.in"

Keep the two root partitions as partitions 1 and 2 and the same size, since
the SWUpdate post-install script switches between them by partition number.
Keep the ``data`` label on the last partition if you want it to grow
automatically.

The ``/data`` Partition
-----------------------

The ``grow-data-part`` service (in ``cargt-image-core``, ``cargt-image-dev``
and the other Cargt images) runs at every boot, before SWUpdate starts. It:

1. Finds the disk that holds ``root=`` (the eMMC or the microSD card,
   whichever the board booted from).
2. Finds the partition labelled ``data`` on that disk.
3. If it is the last partition and there is more than 16 MiB free after it,
   grows it to the end of the disk with ``sfdisk``, then grows the ext4 file
   system online with ``resize2fs``. No reboot is needed.
4. Mounts it on ``/data``.

On the first boot after flashing, the 2 GiB partition therefore grows to fill
the eMMC. On later boots the grow step does nothing. The service log shows what
it did:

.. code-block:: bash

   journalctl -u grow-data-part

``/data`` is not listed in ``/etc/fstab``. If a microSD card with a Cargt
image is inserted in a board that booted from eMMC, both disks have a
partition labelled ``data``, and only the one on the boot disk is mounted on
``/data``.

U-Boot Environment
------------------

U-Boot stores its environment raw on the boot device, 16 KiB at offset
0x700000. Linux reads and writes the same copy with ``fw_printenv`` and
``fw_setenv`` (from ``libubootenv``), configured by ``/etc/fw_env.config``:

.. code-block:: text

   /dev/mmcblk0		0x700000	0x4000

Variables Cargt images use:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 25 75

   * - Variable
     - Purpose
   * - ``mmcdev``
     - MMC device U-Boot loads the kernel from.
   * - ``mmcpart``
     - Root partition to boot, ``1`` or ``2``. Set by software updates.
   * - ``fdtfile``
     - Device tree loaded from ``/boot``. Change it to select the device tree
       for a display; see :doc:`displays`.
   * - ``ethaddr``, ``eth1addr``
     - MAC addresses, when set. See :ref:`mac-addresses`.
   * - ``bootcmd``
     - Command run at boot. Set it to ``fastboot auto`` to re-flash over
       USB; see :doc:`getting-started`.

Reading and changing variables from Linux:

.. code-block:: bash

   fw_printenv                 # all variables
   fw_printenv mmcpart         # one variable
   fw_setenv fdtfile <name>.dtb
   fw_setenv ethaddr           # no value: delete the variable

From the U-Boot prompt, use ``printenv``, ``setenv`` and ``saveenv``. To go
back to the built-in defaults:

.. code-block:: bash

   env default -a
   saveenv

Boards That Boot from eMMC or microSD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

U-Boot keeps its environment on the device it booted from. On machines that
can boot from either (the 00414 machines and the NXP FRDM i.MX 95 boards),
the ``fw-env-bootdev`` machine feature adds a service that writes
``/run/fw_env.config`` for the boot device at every boot, and
``/etc/fw_env.config`` links to it. ``fw_printenv`` and ``fw_setenv`` then
always use the copy U-Boot uses.

.. note::

   ``bmaptool`` only writes the blocks that contain data, so it does not
   overwrite an environment saved by a previous image. If a board boots
   with unexpected settings after you write a new image with ``bmaptool``,
   run ``env default -a`` and ``saveenv`` at the U-Boot prompt once.

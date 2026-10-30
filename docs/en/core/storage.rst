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
       UUU also writes it to the eMMC boot partition and boots from there;
       see `eMMC Boot Partitions`_.
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

There is no FAT boot partition. U-Boot loads ``boot/Image`` and the
device tree named by ``fdtfile`` (``boot/<name>.dtb``) from the ext4 root partition selected by the ``mmcpart``
variable, and passes ``root=/dev/mmcblk<mmcdev>p<mmcpart>`` to the kernel.
Software updates write the inactive root partition and change ``mmcpart``;
see :ref:`swupdate`.

Checking the Layout
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   lsblk                  # partitions and mount points
   cat /proc/cmdline      # root= shows the running root partition
   fw_printenv mmcpart    # partition U-Boot boots next

On an i.MX 93 00363 on the 00428 carrier with a 32 GB eMMC, running from
partition 1:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# lsblk
   NAME         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
   mmcblk0      179:0    0 28.8G  0 disk
   |-mmcblk0p1  179:1    0    6G  0 part /
   |-mmcblk0p2  179:2    0    6G  0 part /run/media/mmcblk0p2
   `-mmcblk0p3  179:3    0    2G  0 part /data
   mmcblk0boot0 179:32   0 31.5M  1 disk
   mmcblk0boot1 179:64   0 31.5M  1 disk

   root@imx93-cargt-00363-00428:~# sfdisk -l /dev/mmcblk0
   ...
   Device         Boot    Start      End  Sectors Size Id Type
   /dev/mmcblk0p1         16384 12599295 12582912   6G 83 Linux
   /dev/mmcblk0p2      12599296 25182207 12582912   6G 83 Linux
   /dev/mmcblk0p3      25182208 29376511  4194304   2G 83 Linux

The inactive root partition is mounted under ``/run/media`` automatically.
This board's image predates ``grow-data-part``, so ``/data`` is still 2 GiB;
see `The /data Partition`_.

``mmcblk0`` is the device U-Boot calls MMC 0; on most Cargt boards that is the
eMMC, and the microSD card is ``mmcblk1``. ``mmcblk0boot0`` and
``mmcblk0boot1`` are the eMMC hardware boot partitions. When a board is
flashed with UUU, the boot loader runs from ``mmcblk0boot0``; see
`eMMC Boot Partitions`_. Linux keeps them read-only by default.

Boot Sequence
~~~~~~~~~~~~~

On i.MX 8M Plus, i.MX 91 and i.MX 93 machines, the default ``bootcmd`` is
``run distro_bootcmd;run bsp_bootcmd``. (The i.MX 95 00414 machines use
``run bsp_bootcmd`` alone and skip the distro boot scan.) U-Boot first tries the standard distro boot methods (``extlinux.conf``, boot
scripts and EFI) on the eMMC, the microSD card and USB. Cargt images
provide none of these, so it then runs ``bsp_bootcmd``, which loads the
kernel and device tree from the root partition selected by ``mmcpart``.
Stopping autoboot and running ``boot`` on an i.MX 93 00363 on the 00428
carrier, with no microSD card or USB drive:

.. code-block:: text

   u-boot=> boot
   switch to partitions #0, OK
   mmc0(part 0) is current device
   Scanning mmc 0:1...
   ...
   Error: Cannot initialize UEFI sub-system, r = 3
   MMC Device 1 not found
   no mmc device at slot 1
   starting USB...
   ...
          scanning usb for storage devices... 0 Storage Device(s) found
   Running BSP bootcmd ...
   switch to partitions #0, OK
   mmc0(part 0) is current device
   Failed to load 'boot.scr'
   35748352 bytes read in 725 ms (47 MiB/s)
   Booting from mmc ...
   40106 bytes read in 2 ms (19.1 MiB/s)
   ## Flattened Device Tree blob at 83000000
      Booting using the fdt blob at 0x83000000
   ...
   Starting kernel ...

The UEFI, MMC device 1 and USB messages come from the distro boot scan and
are harmless. ``bsp_bootcmd`` first looks for a U-Boot script ``boot.scr``
in the root partition and runs it if present (``Failed to load 'boot.scr'``
when there is none), then loads ``boot/Image`` (about 36 MB) and the device
tree named by ``fdtfile``.

U-Boot lists the MMC devices and the partition table with:

.. code-block:: text

   u-boot=> mmc list
   FSL_SDHC: 0 (eMMC)
   FSL_SDHC: 2
   u-boot=> mmc dev 0
   u-boot=> mmc part

   Partition Map for mmc device 0  --   Partition Type: DOS

   Part    Start Sector    Num Sectors     UUID            Type
     1     16384           12582912        076c4a2a-01     83
     2     12599296        12582912        076c4a2a-02     83
     3     25182208        4194304         076c4a2a-03     83

eMMC Boot Partitions
~~~~~~~~~~~~~~~~~~~~

Besides the user area that holds the partition table, an eMMC has two
hardware boot partitions, ``mmcblk0boot0`` and ``mmcblk0boot1`` (31.5 MiB
each on the 32 GB eMMC of the i.MX 93 00363). The eMMC's ``PARTITION_CONFIG``
register tells the boot ROM which area to load the boot loader from.

UUU's ``emmc_all`` script, used in :doc:`getting-started`, writes the ``.wic``
image to the user area, writes ``imx-boot`` to boot partition 1, and then
selects boot partition 1. These are its last steps (``uuu -bshow emmc_all``):

.. code-block:: text

   FB: flash -raw2sparse all _image
   FB: flash -scanterm -scanlimited 0x800000 bootloader _flash.bin
   FB: ucmd if env exists emmc_ack; then ; else setenv emmc_ack 0; fi;
   FB: ucmd mmc partconf ${emmc_dev} ${emmc_ack} 1 0

Check the setting from Linux with ``mmc`` from ``mmc-utils``. On an i.MX 93
00363 on the 00428 carrier flashed with UUU:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# mmc extcsd read /dev/mmcblk0 | grep -A2 PARTITION_CONFIG
   Boot configuration bytes [PARTITION_CONFIG: 0x08]
    Boot Partition 1 enabled
    No access to boot partition

``mmcblk0boot0`` then holds the same boot container as the 32 KiB offset in
the user area, and the boot ROM uses the copy in ``mmcblk0boot0``. This
matters in two cases:

- **Writing a new image from Linux.** ``bmaptool`` or ``dd`` writes the
  ``.wic`` image to the user area only, so the board keeps running the old
  boot loader from boot partition 1. Use UUU to update the boot loader as
  well.
- **Erasing the eMMC to force serial download mode.** Erasing the user area
  does not remove the boot loader in boot partition 1, so the board still
  boots. Change the boot switches to serial download instead (see
  :doc:`getting-started`).

Linux keeps the boot partitions read-only
(``/sys/block/mmcblk0boot0/force_ro`` is ``1``), so they cannot be
overwritten by accident.

Updating the Boot Loader from Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To replace the boot loader in boot partition 1 without UUU, write the new
``imx-boot`` file (``tmp/deploy/images/<machine>/imx-boot`` in your build,
not ``imx-boot.tagged``) to the start of ``mmcblk0boot0``.

.. danger::

   If the new boot loader is wrong or the write is interrupted, the board
   no longer boots from eMMC. It can then only be recovered by setting the
   boot switches to serial download and flashing it with UUU (see
   :doc:`getting-started`). Use an ``imx-boot`` built for the same machine,
   and do not remove power during the write.

.. code-block:: bash

   dd if=/dev/mmcblk0boot0 of=/data/boot0-backup.img bs=1M   # keep a copy
   echo 0 > /sys/block/mmcblk0boot0/force_ro                 # allow writing
   dd if=imx-boot of=/dev/mmcblk0boot0 bs=1M conv=fsync
   echo 1 > /sys/block/mmcblk0boot0/force_ro                 # read-only again
   cmp -n $(stat -c %s imx-boot) imx-boot /dev/mmcblk0boot0 && echo OK

The new boot loader runs at the next boot. While ``force_ro`` is ``1``, a
write fails:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# dd if=/data/boot0-backup.img of=/dev/mmcblk0boot0 bs=1M count=1
   dd: error writing '/dev/mmcblk0boot0': Operation not permitted

These steps were checked on an i.MX 93 00363 on the 00428 carrier by
reading all of ``mmcblk0boot0`` and writing the same bytes back. The 32 MiB
write took under half a second, and the SHA-256 checksum of the partition
was the same before and after.

Pseudo-SLC Mode
~~~~~~~~~~~~~~~

An eMMC can configure part or all of its user area as an *enhanced* area,
which most devices implement as pseudo-SLC: each cell stores one bit
instead of two or three. That area gets much better write endurance and
data retention, at a fraction of the capacity.

.. danger::

   Configuring the enhanced area is **permanent**. The eMMC accepts its
   partition settings only once (``PARTITION_SETTING_COMPLETED``), erases its
   contents when they take effect, and the capacity cannot be restored.
   Configure it on a SOM you can afford to lose first, and contact Cargt
   before using it in production.

The current settings and the largest possible enhanced area can be read
without changing anything. On the 32 GB eMMC of an i.MX 93 00363:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# mmc extcsd read /dev/mmcblk0 | grep -E "MAX_ENH|ENH_SIZE|PARTITION_SETTING|HC_WP_GRP|HC_ERASE_GRP"
   High-capacity erase unit size [HC_ERASE_GRP_SIZE: 0x01]
   High-capacity W protect group size [HC_WP_GRP_SIZE: 0x10]
   Max Enhanced Area Size [MAX_ENH_SIZE_MULT]: 0x0004cd
   Partitioning Setting [PARTITION_SETTING_COMPLETED]: 0x00
   Enhanced User Data Area Size [ENH_SIZE_MULT]: 0x000000

``PARTITION_SETTING_COMPLETED`` and ``ENH_SIZE_MULT`` are 0: no enhanced area
is configured. The largest possible enhanced area is
``MAX_ENH_SIZE_MULT`` × ``HC_WP_GRP_SIZE`` × ``HC_ERASE_GRP_SIZE`` × 512 KiB,
here 0x4cd × 16 × 1 × 512 KiB, about 9.6 GiB. Configuring the whole device
as pseudo-SLC therefore leaves about a third of its normal capacity.

``mmc enh_area set`` in ``mmc-utils`` configures the area, and the setting
takes effect after the next power cycle. Plan the partition layout for the
smaller capacity (see `Using a Different Layout`_).

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

Images built from the ``wrynose`` branch of ``meta-imx-cargt`` from
October 23, 2026 include the ``grow-data-part`` service (in
``cargt-image-core``, ``cargt-image-dev`` and the other Cargt images). It runs
at every boot, before SWUpdate starts, and:

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

**Older images** handle ``/data`` differently, depending on the machine and
the image date:

- **Up to October 13, 2026:** only the i.MX 93 00363 on the 00428 carrier
  and the i.MX 95 00414 on the 00428 mount the data partition on ``/data``,
  from ``/etc/fstab`` (``LABEL=data``), at 2 GiB. On the other machines the
  data partition is only mounted under ``/run/media``, and ``/data`` is a
  plain directory on the root file system.
- **October 14 to 22, 2026:** ``grow-data-part`` grows the data partition,
  but does not mount it. ``/etc/fstab`` mounts it on ``/data`` on the 00428
  machines and the other 00414 machines only; on the rest, ``/data`` is
  still a directory on the root file system.

Where ``/data`` is a directory on the root file system, SWUpdate stages the
whole update archive (about 440 MB) on the root partition, which then needs
that much free space. To check which you have:

.. code-block:: bash

   systemctl status grow-data-part     # "could not be found" before October 14
   grep data /etc/fstab                # an entry: an image from before October 23
   findmnt /data                       # no output: /data is on the root file system

.. _u-boot-environment:

U-Boot Environment
------------------

U-Boot stores its environment raw on the boot device, 16 KiB at offset
0x700000. Linux reads and writes the same copy with ``fw_printenv`` and
``fw_setenv`` (from ``libubootenv``), configured by ``/etc/fw_env.config``:

.. code-block:: text

   /dev/mmcblk0		0x700000	0x4000

The device is the eMMC: ``/dev/mmcblk0`` on most machines, and
``/dev/mmcblk2`` on the i.MX 8M Plus 00377.

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
     - Device tree to load, relative to the root partition, for example
       ``boot/<name>.dtb``. Change it to select the device tree for a
       display; see :doc:`displays`. Write a new value in the same form as
       the current one (``fw_printenv fdtfile``), and check that the file
       exists in ``/boot`` first: U-Boot cannot boot Linux without it.
   * - ``ethaddr``, ``eth1addr``
     - MAC addresses, when set. See :ref:`mac-addresses`.
   * - ``bootcmd``
     - Command run at boot. Set it to ``fastboot auto`` to re-flash over
       USB; see :ref:`uuu-from-environment`.

Reading and changing variables from Linux:

.. code-block:: bash

   fw_printenv                 # all variables
   fw_printenv mmcpart         # one variable
   fw_setenv fdtfile boot/<name>.dtb
   fw_setenv ethaddr           # no value: delete the variable

From the U-Boot prompt, use ``printenv``, ``setenv`` and ``saveenv``. Press a
key during the two-second ``Hit any key to stop autoboot`` countdown to get
the ``u-boot=>`` prompt. Some of the values ``printenv`` shows on the i.MX 93
00363 on the 00428 carrier:

.. code-block:: text

   bootcmd=run distro_bootcmd;run bsp_bootcmd
   mmcdev=0
   mmcpart=1
   fdtfile=boot/imx93-cargt-00363-00428-glt0557201280is1.dtb

The whole environment uses about 7 KB of the 16 KB available
(``Environment size: 7135/16380 bytes`` at the end of ``printenv``). To go
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

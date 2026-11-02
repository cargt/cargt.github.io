.. _u-boot:

The U-Boot Command Line
=======================

U-Boot is the boot loader on every Cargt board: it starts the processor's
memory, then loads the Linux kernel and device tree and starts Linux. Its
command line is useful for trying a different device tree or root
partition for one boot, checking the eMMC, and recovering a board whose
Linux does not start. This page covers how to reach it and the commands
that help most. The examples are from an i.MX 8M Plus 00377 on the 00365
carrier, running a wrynose image.

.. contents:: On this page
   :local:
   :depth: 1

Getting to the Prompt
---------------------

The U-Boot command line is on the debug serial console, the same UART
that shows the Linux boot messages and login prompt. Connect a terminal
program to it with these settings:

- 115200 baud, 8 data bits, no parity, 1 stop bit (115200 8N1)
- No hardware or software flow control

From a Linux PC, for example:

.. code-block:: bash

   picocom -b 115200 /dev/ttyUSB0      # exit with Ctrl+A, Ctrl+X

Power on or reboot the board. U-Boot prints the board and memory it found,
then counts down; press any key before it reaches 0:

.. code-block:: text

   U-Boot 2024.04+gde16f4f1722+p0 (Sep 02 2024 - 10:44:35 +0000)

   CPU:   i.MX8MP[8] rev1.1 1600 MHz (running at 1200 MHz)
   CPU:   Industrial temperature grade (-40C to 105C) at 39C
   Model: Cargt i.MX8MP 00377 OSM-L SOM on 00365 carrier board
   DRAM:  4 GiB
   ...
   MMC:   FSL_SDHC: 0, FSL_SDHC: 1, FSL_SDHC: 2
   Loading Environment from MMC... OK
   ...
   Net:   eth0: ethernet@30be0000, eth1: ethernet@30bf0000 [PRIME]
   Fastboot: Normal
   Normal Boot
   Hit any key to stop autoboot:  0
   u-boot=>

The countdown is 2 seconds on i.MX boards and 1 second on STM32MP2 boards.
The prompt is ``u-boot=>`` on i.MX and ``STM32MP>`` on STM32MP2.

To get more time, lengthen the countdown from Linux before you reboot. The
change is saved, so it applies to every boot until you set it back:

.. code-block:: bash

   fw_setenv bootdelay 5     # 5 seconds
   fw_setenv bootdelay       # back to the built-in default

Type ``boot`` at the prompt to continue booting Linux as normal, or
``reset`` to restart the board.

Finding Your Way Around
-----------------------

.. code-block:: text

   help                  list every command
   help <command>        usage of one command
   version               U-Boot version and build
   bdinfo                memory layout and board information

``help`` lists each command with a one-line description:

.. code-block:: text

   u-boot=> help
   ?         - alias for 'help'
   base      - print or set address offset
   bdinfo    - print Board Info structure
   ...
   boot      - boot default, i.e., run 'bootcmd'
   ...
   cargt_eeprom- Cargt EEPROM inspect/repair utility
   ...

Commands can be shortened to any unambiguous prefix, for example
``printenv`` to ``print``. Press the up arrow for the previous command.
Numbers are hexadecimal: ``md 0x80000000 10`` reads sixteen words.

``version`` shows the U-Boot build. Software updates replace only the root
file system (see :doc:`software-updates`), not U-Boot, so U-Boot stays the
version the board was flashed with.

The Environment
---------------

U-Boot's settings are text variables in its **environment**, which is
saved on the eMMC. :ref:`u-boot-environment` describes where it is stored,
the variables Cargt images use, and how to read and change it from Linux
with ``fw_printenv`` and ``fw_setenv``. At the prompt:

.. code-block:: text

   printenv                    all variables
   printenv fdtfile            one variable
   setenv bootdelay 5          set a variable (in memory only)
   setenv bootdelay            delete a variable
   editenv fdtfile             edit a variable in place
   saveenv                     write the environment to the eMMC
   env default -a              go back to the built-in defaults (in memory)
   run <variable>              run the commands stored in a variable

``setenv`` changes the copy in memory only. Until you run ``saveenv`` the
change lasts for the current boot, and is gone at the next reset. That
makes ``setenv`` followed by ``boot`` the safe way to try something, for
example a different device tree:

.. code-block:: text

   setenv fdtfile boot/imx8mp-cargt-00377-00365-glt1011280800is1.dtb
   boot

If the new setting works, make it permanent with ``fw_setenv`` from Linux,
or with ``setenv`` and ``saveenv`` at the prompt.

Undoing a Bad Change
~~~~~~~~~~~~~~~~~~~~

If you saved a setting that stops Linux from starting, for example an
``fdtfile`` that does not exist, stop at the prompt and restore the
defaults:

.. code-block:: text

   env default -a
   saveenv
   boot

This also clears any settings you made on purpose, such as MAC addresses
written with ``fw_setenv`` (see :ref:`mac-addresses`) or a display device
tree. Note them first with ``printenv`` if you need them. To reset a single
variable instead:

.. code-block:: text

   env default fdtfile
   saveenv

How i.MX Boards Boot
--------------------

These are the variables that control booting on the 00377:

.. code-block:: text

   u-boot=> printenv bootcmd mmcdev mmcpart mmcautodetect fdtfile boot_targets console
   bootcmd=run distro_bootcmd;run bsp_bootcmd
   mmcdev=2
   mmcpart=2
   mmcautodetect=yes
   fdtfile=boot/imx8mp-cargt-00377-00365-hdmi.dtb
   boot_targets=usb0 mmc1 mmc2
   console=ttymxc3,115200

``bootcmd`` runs two steps:

#. ``distro_bootcmd`` is U-Boot's standard scan. It looks on the devices in
   ``boot_targets`` for an ``extlinux/extlinux.conf``, a ``boot.scr``
   script or an EFI application, and boots the first one it finds. Cargt
   images contain none of these, so on a normal board the scan finds
   nothing and moves on. The devices and their order differ between SOMs;
   on the i.MX 93 00363 they are ``mmc0 mmc1 usb0``.
#. ``bsp_bootcmd`` loads the kernel ``boot/Image`` and the device tree
   named by ``fdtfile`` from the ext4 root partition ``mmcpart`` on MMC
   device ``mmcdev``, and starts Linux with
   ``root=/dev/mmcblk<mmcdev>p<mmcpart>``.

Because the scan runs first, a microSD card or USB stick that carries a
``boot.scr`` or an ``extlinux.conf`` takes over the boot. Remove it if a
board boots something unexpected.

During the scan U-Boot prints messages such as these; they are normal:

.. code-block:: text

   MMC: no card present
   Unable to open OP-TEE session (err=-5)
   mm_communicate failed!
   Error: Cannot initialize UEFI sub-system, r = 3
   Running BSP bootcmd ...
   ...
   Failed to load 'boot.scr'
   37603840 bytes read in 118 ms (303.9 MiB/s)
   Booting from mmc ...

``mmcautodetect=yes`` makes U-Boot set ``mmcdev`` to the device it booted
from at every boot: ``2`` on the 00377, whose eMMC is MMC device 2, and
``0`` on most other SOMs. Setting ``mmcdev`` yourself has no effect unless
you also set ``mmcautodetect`` to ``no``.

To boot the other root partition once, for example to check the previous
software version after an update (see :doc:`software-updates`):

.. code-block:: text

   setenv mmcpart 1
   boot

The kernel command line is built by ``mmcargs``. To add kernel arguments
for one boot:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 70

   * - SOM
     - How to add kernel arguments
   * - i.MX 95 00414
     - ``setenv mcore_args '<arguments>'``
   * - i.MX 8M Plus 00377
     - ``setenv cargt_bootargs '<arguments>'`` (not set by default)
   * - i.MX 91 and i.MX 93
     - No variable for this; edit ``mmcargs`` with ``editenv mmcargs`` and
       add the arguments at the end.

Then run ``boot``. In Linux, ``cat /proc/cmdline`` shows the command line
the kernel received.

How STM32MP2 Boards Boot
------------------------

On STM32MP2 boards, U-Boot boots the ``extlinux.conf`` file on the boot
file system (``bootfs``) partition. That file names the kernel and the
kernel command line, and uses ``FDTDIR``, so U-Boot loads the device tree
named by ``fdtfile`` from it. ``fdtfile`` holds the file name alone, for
example:

.. code-block:: text

   fdtfile=stm32mp257f-cargt-00395-02-00365.dtb

so the same one-boot test works:

.. code-block:: text

   setenv fdtfile stm32mp257f-cargt-00395-02-00365-glt1011280800is1.dtb
   boot

Each of the two software slots has its own ``bootfs`` partition.
``bootcmd`` boots slot A and ``altbootcmd`` boots slot B; RAUC changes
which one is which during an update, and U-Boot's boot counter
(``bootcount``, ``bootlimit=3``) falls back to the other slot after three
failed boots. :doc:`rauc-ota-updates` describes this in detail. Do not
change these variables by hand unless you are following that page.

This section comes from the U-Boot configuration in the STM32MP2 layers.
It has not yet been checked at the prompt of a Cargt STM32MP2 board.

Looking at Storage
------------------

.. code-block:: text

   mmc list                     the MMC devices: eMMC and microSD
   mmc dev ${mmcdev}            select the device U-Boot boots from
   mmc info                     size and type of the selected device
   mmc part                     its partition table
   ls mmc ${mmcdev}:${mmcpart} /boot      list a directory
   load mmc ${mmcdev}:${mmcpart} ${loadaddr} /boot/Image    read a file into memory

On the 00377:

.. code-block:: text

   u-boot=> mmc list
   FSL_SDHC: 0
   FSL_SDHC: 1
   FSL_SDHC: 2 (eMMC)
   u-boot=> mmc dev ${mmcdev}
   switch to partitions #0, OK
   mmc2(part 0) is current device
   u-boot=> mmc part

   Partition Map for MMC device 2  --   Partition Type: DOS

   Part	Start Sector	Num Sectors	UUID		Type
     1	16384     	12582912  	076c4a2a-01	83
     2	12599296  	12582912  	076c4a2a-02	83
     3	25182208  	35889152  	076c4a2a-03	83
   u-boot=> ls mmc ${mmcdev}:${mmcpart} /boot
   <DIR>       4096 .
   <DIR>       4096 ..
   <SYM>         39 Image
           37603840 Image-6.18.20-2.0.0-g4a0a00cc7ffa-dirty
   ...
              60925 imx8mp-cargt-00377-00365-glt0557201280is1.dtb
              61026 imx8mp-cargt-00377-00365-glt1011280800is1.dtb
              59631 imx8mp-cargt-00377-00365-hdmi.dtb
              59064 imx8mp-cargt-00377-00365.dtb

Partitions 1 and 2 are the two root file systems and 3 is the data
partition (see :doc:`storage`). ``ls`` and ``load`` work on ext4 and FAT
file systems. ``ls`` is the quickest way to check that a device tree you
are about to set in ``fdtfile`` exists.

Looking at Hardware
-------------------

These commands only read. Use them to check that a device answers before
Linux is involved:

.. code-block:: text

   i2c bus                      list the I²C buses
   i2c dev 0                    select bus 0
   i2c probe                    list the addresses that answer on it
   i2c md 0x50 0 0x10           read 16 bytes from address 0x50
   gpio status                  the GPIOs U-Boot's drivers use
   md ${loadaddr} 0x10          read memory

For example:

.. code-block:: text

   u-boot=> i2c dev 0
   Setting bus to 0
   u-boot=> i2c probe
   Valid chip addresses: 25 32 50

U-Boot only knows the devices its own device tree describes, so ``gpio
status`` and ``i2c bus`` list fewer devices than Linux does.

On i.MX boards, ``cargt_eeprom read`` prints the production information
in the SOM's EEPROM, including its part number:

.. code-block:: text

   u-boot=> cargt_eeprom read
   Cargt EEPROM Production Information:
   	Part number: 012-00377-BE
   	Production date: 20260903
   	Serial number: 0x000xxxxx
   	EEPROM struct version: 0x2
   	DRAM rank: 1
   	DRAM size: 4096 MB
   	DRAM speed: 4000 MT/s

U-Boot also has commands that write: ``mw``, ``i2c mw``, ``mmc write``,
``gpio set``, ``cargt_eeprom setrank`` and others. They change hardware
directly and can leave a board that does not boot. Do not use the
``fuse`` command at all: fuses are one-time programmable, and a wrong
value cannot be undone and can stop the processor from booting. Fuses are
only programmed as part of :doc:`secure-boot`.

Network and USB
---------------

U-Boot can use Ethernet for testing and for loading files from a TFTP
server:

.. code-block:: text

   dhcp                         get an address
   ping <address>               check the connection
   tftp ${loadaddr} <file>      load a file from the TFTP server in serverip

``dhcp`` tries the port marked ``[PRIME]`` in the boot messages first,
and moves on to the next port if that one has no link. After it gets an
address it also tries to load a file over TFTP, and reports an error when
no server is set. That error does not matter if you only wanted the
address. Here ``eth1`` had no cable, and the address came over ``eth0``:

.. code-block:: text

   u-boot=> dhcp
   ethernet@30bf0000 Waiting for PHY auto negotiation to complete......................................... TIMEOUT !
   phy_startup() failed: -110FAILED: -110BOOTP broadcast 1
   BOOTP broadcast 2
   BOOTP broadcast 3
   DHCP client bound to address <address> (1012 ms)
   *** ERROR: `serverip' not set
   Cannot autoload with TFTPGET

``ums`` makes the eMMC appear on your PC as a USB drive, over the board's
USB device port, so you can read or replace files without booting Linux:

.. code-block:: text

   ums 0 mmc ${mmcdev}          share the eMMC; Ctrl+C to stop

Unmount the drive on the PC before you press Ctrl+C. ``ums`` was not run
for this page. Writing to a root
partition this way changes that slot outside the control of the software
update system.

To re-flash a board from U-Boot over USB, see :ref:`uuu-from-environment`
for i.MX. On STM32MP2, STM32CubeProgrammer talks to U-Boot over USB in
the same way; see :doc:`getting-started`.

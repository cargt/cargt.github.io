.. _production:

Production Data
===============

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX`

SOM EEPROM
----------

Each Cargt i.MX SOM has a small I²C EEPROM at address 0x50 that Cargt
programs during production. It holds the part number, serial number, build
date and the DRAM configuration. The boot loader uses the DRAM fields to
select the DDR timing for the memory fitted to that SOM, so one boot image
works for every memory option of a SOM.

Record Format
~~~~~~~~~~~~~

The record starts at offset 0 and is 48 bytes long. Multi-byte fields are
big-endian. Cargt production programs version 2 records, with the reserved
bytes set to 0.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 10 10 25 55

   * - Offset
     - Size
     - Field
     - Contents
   * - 0
     - 4
     - Magic
     - ``0x43524754`` (``CRGT``)
   * - 4
     - 2
     - Size
     - Size of the record in bytes
   * - 6
     - 1
     - Version
     - Record version (1, 2 or 3)
   * - 7
     - 13
     - Part number
     - Cargt part number, ``xxx-xxxxx-xx``, null terminated
   * - 20
     - 4
     - Serial number
     - Cargt serial number
   * - 24
     - 9
     - Date
     - Build date, ``YYYYMMDD``, null terminated
   * - 33
     - 2
     - DRAM size
     - DRAM size in MB
   * - 35
     - 2
     - DRAM speed
     - DRAM speed in MT/s
   * - 37
     - 1
     - DRAM ranks
     - Number of DRAM ranks (version 2 and later)
   * - 38
     - 1
     - DDR configuration ID
     - DDR configuration used by the i.MX 95 (version 3 and later)
   * - 39
     - 5
     - Reserved
     -
   * - 44
     - 4
     - CRC32
     - CRC32 of bytes 0 to 43

Reading the EEPROM in U-Boot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On i.MX 8M Plus, i.MX 91 and i.MX 93 SOMs, SPL prints the record on the
console at every boot, followed by the DDR timing it selected from it. From
an i.MX 93 00363 (2 GB, two ranks) on the 00428 carrier:

.. code-block:: text

   U-Boot SPL 2026.04-lf_v2026.04+g6eeef838dac+p0 (Jun 02 2026 - 15:03:39 +0000)
   ...
   Reading Cargt EEPROM over I2C...
   Cargt EEPROM read complete.
   ...
   Cargt EEPROM Production Information:
           Part number: 012-00363-FE
           Production date: 20260929
           Serial number: <decimal> (0x<hex>)
           EEPROM struct version: 0x2
           DRAM rank: 2
           DRAM size: 2048 MB
           DRAM speed: 3733 MT/s
           CRC32: 0x<crc> (OK)
           Selected board timing: 2048MB @ 3733 MT/s (rank 2)
   DDR: 3733MTS

To print it again, stop autoboot and run ``cargt_eeprom read`` at the U-Boot
prompt:

.. code-block:: text

   u-boot=> cargt_eeprom read
   Cargt EEPROM Production Information:
           Part number: 012-00363-FE
           Production date: 20260929
           Serial number: <decimal> (0x<hex>)
           EEPROM struct version: 0x2
           DRAM rank: 2
           DRAM size: 2048 MB
           DRAM speed: 3733 MT/s
           CRC32: 0x<crc> (OK)

Version 3 records (i.MX 95) add a ``DDR config ID`` line. Older U-Boot
builds print the serial number in hexadecimal only and leave out the CRC
line.

Reading the EEPROM in Linux
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The SOM device tree declares the EEPROM, so Linux binds the ``at24``
driver to it and the record can be read as a file. It is on I²C bus 0 on
the i.MX 8M Plus 00377, the i.MX 91 and i.MX 93 00363, and the i.MX 95
00414:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# ls /sys/bus/i2c/drivers/at24/
   0-0050  bind  module  uevent  unbind
   root@imx93-cargt-00363-00428:~# hexdump -C -n 48 /sys/bus/i2c/devices/0-0050/eeprom
   00000000  43 52 47 54 00 30 02 30  31 32 2d 30 30 33 36 33  |CRGT.0.012-00363|
   00000010  2d 46 45 00 xx xx xx xx  32 30 32 36 30 39 32 39  |-FE.....20260929|
   00000020  00 08 00 0e 95 02 00 00  00 00 00 00 xx xx xx xx  |................|
   00000030

The file is 256 bytes, the size of the 24C02, and only root can read it.
Some display carriers have a second EEPROM, on the display, at address
0x54; it is not the SOM EEPROM.

These shell commands print the fields:

.. code-block:: bash

   E=/sys/bus/i2c/devices/0-0050/eeprom
   num() { od -An -tu1 -j$1 -N$2 $E | awk '{ for (i = 1; i <= NF; i++) v = v * 256 + $i } END { print v }'; }
   str() { dd if=$E bs=1 skip=$1 count=$2 2>/dev/null | tr -d '\0'; }
   echo "Magic:          $(str 0 4)"
   echo "Version:        $(num 6 1)"
   echo "Part number:    $(str 7 13)"
   echo "Serial number:  $(num 20 4)"
   echo "Date:           $(str 24 9)"
   echo "DRAM:           $(num 33 2) MB, $(num 35 2) MT/s, $(num 37 1) rank(s)"
   [ "$(num 6 1)" -ge 3 ] && echo "DDR config ID:  $(num 38 1)"

On the same i.MX 93 board, and on an i.MX 95 00414 with a version 3
record:

.. code-block:: text

   Magic:          CRGT
   Version:        2
   Part number:    012-00363-FE
   Serial number:  <decimal>
   Date:           20260929
   DRAM:           2048 MB, 3733 MT/s, 2 rank(s)

.. code-block:: text

   Magic:          CRGT
   Version:        3
   Part number:    012-00414-X1
   Serial number:  <decimal>
   Date:           20261009
   DRAM:           2048 MB, 6400 MT/s, 1 rank(s)
   DDR config ID:  1

The serial number is the SOM's Cargt serial number. To check the CRC, on an
image with Python:

.. code-block:: bash

   python3 -c "import binascii; d = open('$E', 'rb').read(48); print('CRC OK' if binascii.crc32(d[:44]) == int.from_bytes(d[44:], 'big') else 'CRC BAD')"

``free`` reports less than the DRAM size, because the kernel and reserved
memory regions (for example for the Cortex-M core and the GPU) are not
counted. On the boards above, ``free -m`` showed a total of 1939 MB for
2048 MB on the i.MX 93, 3615 MB for 4096 MB on the i.MX 8M Plus, and
1703 MB for 2048 MB on the i.MX 95.

.. warning::

   The file is writable by root. Do not write to it; see the warning
   below about the DRAM fields.

How the DRAM Fields Are Used
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **i.MX 8M Plus, i.MX 91 and i.MX 93:** SPL reads the DRAM size, speed and
  rank count, and selects the matching DDR timing built into the image.
- **i.MX 95:** DDR training runs before SPL, in the OEI firmware on the
  Cortex-M33. OEI reads the DDR configuration ID, or matches older records
  by size and rank count. If the EEPROM is blank or invalid, OEI tries each
  configuration in turn, two-rank configurations first.

.. warning::

   Do not change the DRAM fields. A DRAM size larger than the memory
   actually fitted lets Linux use memory that does not exist, which causes
   random crashes under load rather than a clean boot failure. If you think
   a SOM's EEPROM is wrong, contact Cargt.

If the EEPROM is blank or its CRC is wrong, SPL assumes one rank. A version
1 record, or a version 2 record with a rank of 0, is treated as two ranks.

``cargt_eeprom setrank <1|2>`` rewrites the DRAM rank field and the CRC, and
updates a version 1 record to version 2. It is a repair tool for SOMs
programmed with the wrong rank count; use it only when Cargt asks you to.

.. _limit-ram:

Limiting RAM for Testing
------------------------

To check that your application runs on a SOM with less memory than the
one on your desk, boot with the ``mem=`` kernel argument. Linux then uses
only that much RAM. The memory is still fitted and SPL still sets it up
for its full size, as the EEPROM says; only Linux leaves the rest unused.

On i.MX boards, U-Boot adds ``cargt_bootargs`` to the end of the kernel
command line. It is not set by default. Stop U-Boot at its prompt (see
:doc:`u-boot`), set it, and boot:

.. code-block:: text

   u-boot=> printenv mmcargs cargt_bootargs
   mmcargs=setenv bootargs ${jh_clk} console=${console} root=/dev/mmcblk${mmcdev}p${mmcpart} rootwait rw ${cargt_bootargs}
   ## Error: "cargt_bootargs" not defined
   u-boot=> setenv cargt_bootargs mem=1024M
   u-boot=> boot

Without ``saveenv`` this lasts for one boot; the next reset boots with all
the memory again. From an i.MX 8M Plus 00377 with 4 GB on the 00365
carrier:

.. code-block:: text

   [    0.000000] OF: reserved mem: failed to allocate memory for node 'linux,cma': size 960 MiB
   [    0.000000] Kernel command line: console=ttymxc3,115200 root=/dev/mmcblk2p2 rootwait rw mem=1024M
   [    0.007902] Memory: 949980K/1048576K available (23104K kernel code, 2162K rwdata, 9160K rodata, 2112K init, 687K bss, 61388K reserved, 32768K cma-reserved)

.. code-block:: text

   root@imx8mp-cargt-00377-00365:~# free -m
                  total        used        free      shared  buff/cache   available
   Mem:             966         349         501          12         200         616
   root@imx8mp-cargt-00377-00365:~# grep CmaTotal /proc/meminfo
   CmaTotal:          32768 kB

Normally the same board shows a total of 3615 MB and a ``CmaTotal`` of
983040 kB.

.. note::

   The contiguous memory area (CMA) that the GPU, video codecs, display
   and camera allocate from is sized in the device tree for the full
   memory, 960 MiB on the 00377. With ``mem=1024M`` it does not fit, and
   the kernel falls back to a 32 MiB CMA, as the first line above shows.
   Weston still started, but graphics, video and camera use can fail with
   a 32 MiB CMA, so the test is pessimistic for those. Add ``cma=<size>`` to ``cargt_bootargs`` to choose the size
   yourself; this was not tested for this page.

To keep the limit across resets, ``saveenv`` after setting
``cargt_bootargs``, or set it from Linux with
``fw_setenv cargt_bootargs mem=1024M``. ``fw_setenv cargt_bootargs`` with
no value removes it. STM32MP2 boards boot with extlinux and do not use
``cargt_bootargs``.

.. _mac-addresses:

Ethernet MAC Addresses
----------------------

U-Boot chooses each Ethernet port's MAC address in this order:

1. The ``ethaddr`` (first port) or ``eth1addr`` (second port) variable in the
   U-Boot environment, if set.
2. The MAC address programmed in the SoC's eFuses (one-time programmable
   memory).
3. If neither is set, a random address. Without an address in the eFuses
   or the environment, a board gets a new MAC address, and so a new DHCP
   lease, at every boot.

U-Boot passes the address to Linux in the device tree, so Linux uses the same
address.

Setting Addresses in the U-Boot Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For production, use addresses from your own IEEE-assigned range. On boards
without programmed eFuses, you can instead derive stable, locally
administered addresses from the SoC unique ID. Run this once per board from
Linux, then reboot:

.. code-block:: bash

   uid=$(cat /sys/devices/soc0/serial_number)
   h=$(printf %s "$uid" | sha256sum | cut -c1-8)
   base="02:${h:0:2}:${h:2:2}:${h:4:2}:${h:6:2}"
   fw_setenv ethaddr  "${base}:00"   # first port, eth0
   fw_setenv eth1addr "${base}:01"   # second port, eth1
   fw_printenv ethaddr eth1addr

The ``02`` first byte marks the address as locally administered, so it
cannot clash with a vendor-assigned address. Cargt verified this method on
the i.MX 95 00414.

To go back to the eFuse addresses, delete the variables:

.. code-block:: bash

   fw_setenv ethaddr
   fw_setenv eth1addr

Programming MAC eFuses is permanent and the fuse locations differ for each
i.MX processor. See the processor's reference manual (Fusemap chapter) and
`contact Cargt <https://www.cargt.com/cargt-about/contact-us>`__ for production programming.

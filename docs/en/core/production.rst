.. _production:

Production Data
===============

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
`contact Cargt <https://www.cargt.com/>`__ for production programming.

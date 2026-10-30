.. _identify-som:

Identifying Your SOM and Choosing the MACHINE
=============================================

Every Cargt image and Yocto build is for one ``MACHINE``: a SOM on a
carrier board, such as ``imx93-cargt-00363-00365``. Flash, update and build
with the ``MACHINE`` that matches your hardware. This page shows how to
identify the SOM and the image on a board, and how to pick the ``MACHINE``.

.. contents:: On this page
   :local:
   :depth: 1

Finding the SOM Part Number
---------------------------

The SOM's board number is printed on its silkscreen, for example
``105-00395-01`` along the edge of an STM32MP2 00395-01; the photos on each
SOM's page in the :doc:`index` show where. During production, Cargt
programs the SOM's full part number into its EEPROM, together with the
serial number and the memory configuration (see :ref:`production`). The
part number identifies the build variant, such as the processor, memory and
temperature grade, which the silkscreen does not show.

On i.MX 8M Plus, i.MX 91 and i.MX 93 SOMs, the boot loader prints the EEPROM
record on the serial console at every boot:

.. code-block:: text

   Cargt EEPROM Production Information:
           Part number: 012-00363-FE
           Production date: 20260929
           Serial number: <decimal> (0x<hex>)
           EEPROM struct version: 0x2
           DRAM rank: 2
           DRAM size: 2048 MB
           DRAM speed: 3733 MT/s

To print it again, stop autoboot and run ``cargt_eeprom read`` at the U-Boot
prompt.

From Linux, the EEPROM is a 24C02 at I²C address 0x50 on bus 0, and the
``at24`` driver makes its contents readable in sysfs. The part number is
the 13 bytes from offset 7. From an i.MX 93 00363 on the 00428 carrier:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /sys/bus/i2c/devices/0-0050/name
   24c02
   root@imx93-cargt-00363-00428:~# head -c 20 /sys/bus/i2c/devices/0-0050/eeprom | tail -c 13
   012-00363-FE

The whole 48-byte record, with the serial number (offsets 20 to 23) and the
CRC (offsets 44 to 47) replaced by ``xx``:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# hexdump -C -n 48 /sys/bus/i2c/devices/0-0050/eeprom
   00000000  43 52 47 54 00 30 02 30  31 32 2d 30 30 33 36 33  |CRGT.0.012-00363|
   00000010  2d 46 45 00 xx xx xx xx  32 30 32 36 30 39 32 39  |-FE.....20260929|
   00000020  00 08 00 0e 95 02 00 00  00 00 00 00 xx xx xx xx  |................|

The fields are described in :ref:`production`: version 2 (``02``), 2048 MB
(``08 00``), 3733 MT/s (``0e 95``) and two ranks (``02``). Do not write to
the EEPROM: the boot loader selects the DDR timing from it.

Decoding an 00363 Part Number
-----------------------------

The i.MX 91 and i.MX 93 00363 SOM's part number has the form
``012-00363-XY``. The last two characters are hexadecimal digits that encode
the build variant, four bits each, most significant bit first:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 15 15 70

   * - Digit
     - Bits
     - Meaning
   * - X
     - T
     - Temperature grade: 0 = commercial (0 to 95 °C), 1 = industrial
       (−40 to 105 °C)
   * - X
     - W
     - Wireless: 0 = none, 1 = NXP IW612 (Wi-Fi and Bluetooth)
   * - X
     - PP (two bits)
     - Processor: 00 = i.MX 9131 (i.MX 91, single Cortex-A55, full feature
       set), 01 = i.MX 9301 (i.MX 93, single Cortex-A55, reduced feature
       set), 10 = i.MX 9332 (i.MX 93, dual Cortex-A55, no NPU), 11 = i.MX
       9352 (i.MX 93, dual Cortex-A55, full feature set)
   * - Y
     - RR (two bits)
     - RAM: 00 = 256 MB, 01 = 512 MB, 10 = 1 GB, 11 = 2 GB
   * - Y
     - FF (two bits)
     - eMMC: 00 = 8 GB, 01 = 16 GB, 10 = 32 GB, 11 = 64 GB

For example, ``012-00363-FE``:

- ``F`` is ``1111``: industrial grade, IW612, i.MX 9352.
- ``E`` is ``1110``: 2 GB RAM (``11``) and 32 GB eMMC (``10``).

The processor bits decide between the i.MX 91 and i.MX 93 machines. The
NPU examples in :doc:`npu` need an i.MX 9352 (``PP`` = ``11``).

Other SOMs
----------

For the other SOMs, read the variant from the silkscreen (see the photos on
the SOM's page in the :doc:`index`). In particular,
the STM32MP2 00395 comes in two variants, 00395-01 and 00395-02, that need
different machines and images; the silkscreen shows which one you have.

Choosing the MACHINE
--------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 25 45

   * - SOM
     - Carrier
     - ``MACHINE``
   * - 00363 with an i.MX 91 (``PP`` = ``00``)
     - 00365
     - ``imx91-cargt-00363-00365``
   * - 00363 with an i.MX 93 (``PP`` = ``01``, ``10`` or ``11``)
     - 00365
     - ``imx93-cargt-00363-00365``
   * - 00363 with an i.MX 93
     - 00428
     - ``imx93-cargt-00363-00428``
   * - 00377 (i.MX 8M Plus)
     - 00365
     - ``imx8mp-cargt-00377-00365``
   * - 00414 (i.MX 95)
     - 00365
     - ``imx95-cargt-00414-00365``
   * - 00414 (i.MX 95)
     - 00428
     - ``imx95-cargt-00414-00428``
   * - 00324 (i.MX 93)
     - 00326
     - ``imx93-cargt-00324-00326``
   * - 00359 (i.MX 93)
     - 00406
     - ``imx93-cargt-00359-00406``
   * - 00395-01 (STM32MP2)
     - 00365
     - ``stm32mp25-cargt-00395-01-00365``
   * - 00395-02 (STM32MP2)
     - 00365
     - ``stm32mp25-cargt-00395-02-00365``
   * - 00395
     - 00365 revision 3 (older)
     - ``stm32mp25-cargt-00395-00365v3``

For your own carrier board, start from the SOM-only machine, such as
``imx93-cargt-00363-osm-som``, ``imx91-cargt-00363-osm-som`` or
``imx95-cargt-00414-osm-som``, and add your carrier's device tree in your
own layer. :doc:`yocto` lists all the machines, and each SOM's page in the
:doc:`index` links to its published images.

Checking the Image on a Board
-----------------------------

On i.MX images, ``/etc/hwrevision`` names the ``MACHINE`` the image was
built for. SWUpdate uses the same file to check updates:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /etc/hwrevision
   imx93-cargt-00363-00428 1.0

The image's device tree also names the hardware it describes:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /proc/device-tree/model
   Cargt i.MX93 00428 carrier board with 5.5-in MIPI DSI Display(GLT0557201280IS1-CTP)

On STM32MP2 images, ``/etc/rauc/system.conf`` holds the machine's RAUC
``compatible`` string, such as ``cargt-stm32mp25-00395-02-00365``.

What a Mismatch Looks Like
--------------------------

Software updates check the machine before they install anything:

- **SWUpdate (i.MX)** compares the board name in the update's
  ``sw-description`` with the first word of ``/etc/hwrevision`` and refuses
  an update built for another machine. See :doc:`software-updates`.
- **RAUC (STM32MP2)** compares the bundle's ``compatible`` string, such as
  ``cargt-stm32mp25-00395-02-00365``, with the one in
  ``/etc/rauc/system.conf``, and refuses a bundle for another machine,
  including one for the other 00395 variant. See :doc:`rauc-ota-updates`.

If a board was flashed with the image for another carrier or SOM variant,
flash the image for the right ``MACHINE``; see :ref:`running-linux` and
:doc:`flashing-troubleshooting`.

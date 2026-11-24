.. _cb-00326:

00326 — SODIMM Carrier Board
==============================

.. thumbnail:: /_static/images/photos/carrier-boards/00326-1.jpg
   :group: cb-00326
   :width: 45%
   :title: 00326 SODIMM Carrier Board - top

.. thumbnail:: /_static/images/photos/carrier-boards/00326-2.jpg
   :group: cb-00326
   :width: 45%
   :title: 00326 SODIMM Carrier Board - angled

Supported SOMs
---------------

- :doc:`/core/catalog/soms/00324-imx93-sodimm` — i.MX 93 SODIMM

Software
---------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 60

   * - SOM
     - Yocto machine
   * - 00324 (i.MX 93)
     - ``imx93-cargt-00324-00326`` (wrynose, scarthgap)

Release links are on the :doc:`00324 SOM page </core/catalog/soms/00324-imx93-sodimm>`.

Displays
---------

The image includes device trees for the
:doc:`10.1" and 7" LVDS and 2.8" SPI displays </core/displays>`. Select one with
the ``fdtfile`` U-Boot variable, for example
``fw_setenv fdtfile boot/imx93-cargt-00324-00326-glt1011280800is1.dtb``:

- ``imx93-cargt-00324-00326.dtb`` (no display, default)
- ``imx93-cargt-00324-00326-glt1011280800is1.dtb``
- ``imx93-cargt-00324-00326-glt028240320is1.dtb``
- ``imx93-cargt-00324-00326-glt0701024600is2.dtb`` (7" 1024x600 LVDS)

The image also has ``imx93-cargt-00324-00326-00375.dtb`` for the 00375
Wi-Fi HaLow (MM6108) M.2 module.

Known Issues
-------------

.. _cb-00326-console-boot-strap:

Console Cable and the Boot Mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning::

   On current 00326 boards, a USB-serial adapter on the console header
   (J5) during power-up or reset can change the boot mode. The board then
   doesn't boot from eMMC.

The console TX pin, UART1_TXD, is also the i.MX 93 BOOT_MODE0 strap. In
normal eMMC boot, nothing on the board holds it low. Only the SoC pad's
weak internal pull-down does. J5 connects the pin straight to the cable.

Most USB-serial adapters (FTDI, CP210x, CH34x) have a pull-up on their RX
input. That pull-up wins over the pad's pull-down, so BOOT_MODE0 reads 1
at reset:

- With a microSD card in the slot, the board boots from the card instead
  of the eMMC.
- With no card, the boot ROM falls back to the USB serial downloader, and
  the board appears to hang.

There are two ways around this:

- **Add a pull-down in the cable.** Fit a 4.7 kΩ resistor from the
  adapter's RX wire to GND. This holds BOOT_MODE0 low against the
  adapter's pull-up. SW1 (force serial download) still works, because the
  board's 1 kΩ drive beats the 4.7 kΩ pull-down. An adapter with a strong
  pull-up, such as 10 kΩ, can still leave the pin close to the logic
  threshold, so check the board boots from eMMC with your adapter
  attached.
- **Connect the cable after the board has started**, or reboot from an
  SSH session with the cable removed.

The pull-down doesn't stop the adapter from back-powering the SoC through
its TX line while the board is off. If the board misbehaves at power-up
with the adapter attached, connect the adapter after the board is
powered.

A console cable with the 4.7 kΩ pull-down has been tested on the bench:
the 00324 on the 00326 boots from eMMC with the cable attached.

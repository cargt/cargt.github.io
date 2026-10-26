.. _cb-00326:

00326 — SODIMM Carrier Board
==============================

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
:doc:`10.1" LVDS and 2.8" SPI displays </core/displays>`. Select one with
the ``fdtfile`` U-Boot variable:

- ``imx93-cargt-00324-00326.dtb`` (no display, default)
- ``imx93-cargt-00324-00326-glt1011280800is1.dtb``
- ``imx93-cargt-00324-00326-glt028240320is1.dtb``

Known Issues
-------------

.. warning::

   On current 00326 boards, a cable connected to the console UART during
   reset can hold a boot pin in the wrong state, and the board hangs on
   reboot. Disconnect the console cable before rebooting, or reboot from
   an SSH session with the cable removed.

.. _cb-00406:

00406 — LGA Carrier Board
============================

Supported SOMs
---------------

- :doc:`/core/catalog/soms/00359-lga-murata2el` — i.MX 93 LGA

Software
---------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 60

   * - SOM
     - Yocto machine
   * - 00359 (i.MX 93)
     - ``imx93-cargt-00359-00406`` (wrynose, scarthgap)

Release links are on the :doc:`00359 SOM page </core/catalog/soms/00359-lga-murata2el>`.

The 00406 has no display or audio hardware. The Weston compositor is
installed but disabled on this machine.

USB Type-C
-----------

Both USB Type-C ports use NXP PTN5110 port controllers. U-Boot reports both
at boot:

.. code-block:: text

   TCPC: Vendor ID [0x1fc9], Product ID [0x5110]
   TCPC: Vendor ID [0x1fc9], Product ID [0x5110]

.. _00359:

00359 — LGA with Murata 2EL
=============================

.. list-table::
   :widths: 20 80

   * - Vendor
     - NXP
   * - Processor
     - i.MX 93
   * - Form Factor
     - LGA
   * - Wireless Module
     - Murata 2EL

.. Product photo not yet available - reserved for the photos phase.
   Once the image lands in _static/images/photos/00359-lga-murata2el.png,
   uncomment:
..
.. .. figure:: /_static/images/photos/00359-lga-murata2el.png
..    :align: center
..    :width: 400px
..    :alt: 00359 LGA with Murata 2EL module photo

Resources
---------

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files

Software Releases
------------------

See `yocto.cargt.com <https://yocto.cargt.com>`__ for available images and releases.

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: Yocto

        scarthgap (kernel 6.6.36)

    .. grid-item-card:: Yocto

        wrynose (kernel 6.18.20)

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Release
     - Packages
     - Pre-built Images
     - Status
   * - scarthgap (kernel 6.6.36)
     - `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx93_cargt_00359_00406/>`__
     - `Images <https://yocto.cargt.com/images/scarthgap/imx93-cargt-00359-00406/>`__
     - Available
   * - wrynose (kernel 6.18.20)
     - `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx93_cargt_00359_00406/>`__
     - `Images <https://yocto.cargt.com/images/wrynose/imx93-cargt-00359-00406/>`__
     - Available

Source Code
------------

- `imx_manifest <https://github.com/cargt/imx_manifest>`__ - Yocto repo manifest
- `meta-imx-cargt <https://github.com/cargt/meta-imx-cargt>`__ - Cargt BSP layer


Compatible Carrier Boards
--------------------------

- :doc:`/core/catalog/carrier-boards/00406-lga-carrier`

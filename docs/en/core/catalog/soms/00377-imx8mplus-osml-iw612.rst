.. _00377:

00377 — i.MX 8M Plus OSM-L with IW612
=======================================

.. list-table::
   :widths: 20 80

   * - Vendor
     - NXP
   * - Processor
     - i.MX 8M Plus
   * - Form Factor
     - OSM-L
   * - Wireless Module
     - NXP IW612 Dual-Band Wi-Fi 6 BLE

.. thumbnail:: /_static/images/photos/soms/00377-1.png
   :group: 00377
   :width: 30%
   :title: 00377 i.MX 8M Plus OSM-L with IW612 - angled

.. thumbnail:: /_static/images/photos/soms/00377-2.png
   :group: 00377
   :width: 30%
   :title: 00377 i.MX 8M Plus OSM-L with IW612 - top

.. thumbnail:: /_static/images/photos/soms/00377-3.png
   :group: 00377
   :width: 30%
   :title: 00377 i.MX 8M Plus OSM-L with IW612 - bottom

Resources
---------

- `Quick Start Guide <https://downloads.cargt.com/datasheets/qsgs/imx8%20Quick%20Start%20PDF%20v1.pdf>`__
- `Datasheet <https://downloads.cargt.com/datasheets/IMX8MMRM.pdf>`__

Software Releases
------------------

See `yocto.cargt.com <https://yocto.cargt.com>`__ for available images and releases.
**wrynose** is recommended for new designs; **scarthgap** remains available for existing designs already qualified on it.

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: Yocto

        scarthgap (kernel 6.6.36)

        :bdg-secondary:`Existing designs`

    .. grid-item-card:: Yocto

        wrynose (kernel 6.18.20)

        :bdg-success:`New designs`

.. list-table::
   :header-rows: 1
   :widths: 25 25 25 25

   * - Release
     - Packages
     - Pre-built Images
     - Status
   * - scarthgap (kernel 6.6.36) :bdg-secondary:`Existing designs`
     - `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx8mp_cargt_00377_00365/>`__
     - `Images <https://yocto.cargt.com/images/scarthgap/imx8mp-cargt-00377-00365/>`__
     - Available
   * - wrynose (kernel 6.18.20) :bdg-success:`New designs`
     - `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx8mp_cargt_00377_00365/>`__
     - `Images <https://yocto.cargt.com/images/wrynose/imx8mp-cargt-00377-00365/>`__
     - Available

Source Code
------------

- `imx_manifest <https://github.com/cargt/imx_manifest>`__ - Yocto repo manifest
- `meta-imx-cargt <https://github.com/cargt/meta-imx-cargt>`__ - Cargt BSP layer


Compatible Carrier Boards
--------------------------

- :doc:`/core/catalog/carrier-boards/00365-osml-carrier`

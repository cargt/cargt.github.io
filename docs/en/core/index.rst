Product Catalog
=================

SOMs
=====

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: By Processor
        :link: catalog/by-processor
        :link-type: doc

        Browse SOMs grouped by processor (i.MX 8M Plus, i.MX 91, i.MX 93, i.MX 95,
        STM32MP2).

    .. grid-item-card:: By Form Factor
        :link: catalog/by-form-factor
        :link-type: doc

        Browse SOMs grouped by form factor (OSM-L, SODIMM, LGA).

.. toctree::
    :maxdepth: 1

    catalog/by-processor
    catalog/by-form-factor
    catalog/soms/index

Carrier Boards
===============

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: 00326 – SODIMM Carrier Board
        :link: /core/catalog/carrier-boards/00326-sodimm-carrier
        :link-type: doc

        Supports 1 SOM

    .. grid-item-card:: 00406 – LGA Carrier Board
        :link: /core/catalog/carrier-boards/00406-lga-carrier
        :link-type: doc

        Supports 1 SOM

    .. grid-item-card:: 00365 – OSM-L Carrier Board
        :link: /core/catalog/carrier-boards/00365-osml-carrier
        :link-type: doc

        Supports 5 SOMs

    .. grid-item-card:: 00428 – OSM-L Carrier Board
        :link: /core/catalog/carrier-boards/00428-osml-carrier
        :link-type: doc

        Supports 2 SOMs

.. toctree::
    :maxdepth: 1

    catalog/carrier-boards/index

Displays
========

Cargt sells LVDS, MIPI-DSI and SPI touchscreen displays for its carrier boards. See
:doc:`displays` for photos, wiring and device tree selection.

Other Supported Boards
======================

The Cargt i.MX BSP also builds for the NXP FRDM i.MX 95
development board (machine ``imx95-15x15-lpddr4x-frdm``), which is useful for
evaluating software before Cargt hardware is available:
`wrynose images <https://yocto.cargt.com/images/wrynose/imx95-15x15-lpddr4x-frdm/>`__,
`real-time images <https://yocto.cargt.com/images/wrynose-rt/imx95-15x15-lpddr4x-frdm/>`__.

Thermal Characterization
========================

Will your product need a heatsink? :doc:`thermal-characterization` gives the
warmest air each Cargt SOM can run in for a range of loads, CPU frequency caps
and cooling options, in open air and in a sealed enclosure. Results are
available for the 00414 i.MX 95, the 00377 i.MX 8M Plus and the 00363
i.MX 93.

.. toctree::
    :hidden:

    thermal-characterization

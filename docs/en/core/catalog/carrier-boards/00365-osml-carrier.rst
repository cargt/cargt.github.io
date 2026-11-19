.. _cb-00365:

00365 — OSM-L Carrier Board
==============================

.. thumbnail:: /_static/images/photos/carrier-boards/00365-1.png
   :group: cb-00365
   :width: 45%
   :title: 00365 OSM-L Carrier Board (with i.MX 91 OSM-L SOM mounted)

.. thumbnail:: /_static/images/photos/carrier-boards/00365-top.jpg
   :group: cb-00365
   :width: 45%
   :title: 00365 OSM-L Carrier Board - top, no SOM

.. thumbnail:: /_static/images/photos/carrier-boards/00365-bottom.jpg
   :group: cb-00365
   :width: 45%
   :title: 00365 OSM-L Carrier Board - bottom

Supported SOMs
---------------

- :doc:`/core/catalog/soms/00363-91-imx91-osml-iw612` — i.MX 91 OSM-L
- :doc:`/core/catalog/soms/00363-93-imx93-osml-iw612` — i.MX 93 OSM-L
- :doc:`/core/catalog/soms/00377-imx8mplus-osml-iw612` — i.MX 8M Plus OSM-L
- :doc:`/core/catalog/soms/00395-stm32mp257f-osml-iw610` — STM32MP257F OSM-L
- :doc:`/core/catalog/soms/00414-imx95-osml` — i.MX 95 OSM-L

Block Diagrams
---------------

.. figure:: /_static/images/diagrams/Block-diagram-i.MX93-OSM-L-00365-Rev-B-20260210.png
   :align: center
   :alt: i.MX 93 00363-93 OSM-L SOM on 00365 Carrier Board Block Diagram

   i.MX 93 00363-93 OSM-L SOM on 00365 Carrier Board Block Diagram

.. figure:: /_static/images/diagrams/Block-diagram-STM32MP2-00395-OSM-L-00365-Rev-D-20260213.png
   :align: center
   :alt: STM32MP257 00395 OSM-L SOM on 00365 Carrier Board Block Diagram

   STM32MP257 00395 OSM-L SOM on 00365 Carrier Board Block Diagram

.. _cb-00365-hardware:

Hardware Reference
------------------

These tables come from the Cargt device trees for each SOM on the 00365
(``meta-imx-cargt`` wrynose and ``meta-cargt-stm32mp-addons`` scarthgap).
They are a guide for writing your own device tree or for checking a board,
not a replacement for the schematic.

I²C Devices
~~~~~~~~~~~

The carrier's devices all sit on one I²C bus. Which controller that is
depends on the SOM:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 60

   * - SOM
     - Carrier I²C controller
   * - i.MX 91 and i.MX 93 00363
     - ``lpi2c2``
   * - i.MX 95 00414
     - ``lpi2c2`` (OSM I2C_A)
   * - i.MX 8M Plus 00377
     - ``i2c2``
   * - STM32MP2 00395-02
     - ``i2c3``
   * - STM32MP2 00395-01
     - ``i2c1`` (shared with the SOM's devices)

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 15 30 55

   * - Address
     - Device
     - Notes
   * - 0x20
     - NXP PCA9555 GPIO expander
     - Resets and enables for the carrier; see `GPIO Expander Lines`_
   * - 0x51
     - NXP PTN5110 USB-C controller
     - USB-C(A) port
   * - 0x52
     - NXP PTN5110 USB-C controller
     - USB-C(C) port
   * - 0x1a
     - Sony IMX335 camera
     - STM32MP2 only, when a B-CAMS-IMX module is in CSI_A; see
       :ref:`stm32mp2-imx335`
   * - 0x36
     - OmniVision OS08A20 camera
     - Only with the OS08A20 device trees; see :doc:`/core/cameras`

The SOMs have their own devices on another bus: a 24C02 EEPROM at 0x50
(see :doc:`/core/identify-som`), an Epson RX8111 RTC at 0x32, and, on the
i.MX SOMs, the PMIC at 0x25. On the i.MX 95 00414, that bus belongs to the
System Manager, so Linux reaches the EEPROM only through it; see
:doc:`/core/rtc`.

On the i.MX 91 and i.MX 93, the device trees don't fix the Linux bus
numbers, so ``/dev/i2c-N`` can change between kernels. Find the bus by its
devices instead:

.. code-block:: bash

   i2cdetect -l
   ls /sys/bus/i2c/devices/*/name | xargs grep -H .

GPIO Expander Lines
~~~~~~~~~~~~~~~~~~~

The PCA9555 at 0x20 has these lines, named as in the 00365 schematic. The
i.MX 95 and STM32MP2 device trees use these names, so ``gpioinfo`` shows
them. The i.MX 91, i.MX 93 and i.MX 8M Plus device trees name the lines
``pca9555_20-0`` to ``pca9555_20-15``.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 10 25 65

   * - Line
     - Name
     - Drives
   * - 0
     - ETH_A_RST
     - Reset of the first Ethernet PHY
   * - 1
     - ETH_B_RST
     - Reset of the second Ethernet PHY
   * - 2
     - ETH_C_RST
     - Reset of the third PHY, which isn't used. The STM32MP2 device tree
       holds it in reset so that it stays quiet on the shared MDIO bus.
   * - 3
     - DSI_VDD_EN
     - Supply of the MIPI DSI panel
   * - 4
     - DSICT_nRST
     - Reset of the DSI panel's touch controller
   * - 5
     - LVDS_EN
     - Supply of the LVDS panel
   * - 6
     - LVDSCT_nRST
     - Reset of the LVDS panel's touch controller
   * - 7
     - CAM_PWR
     - Camera power or reset, for the CSI_A camera
   * - 8
     - UBUS_RST
     - mikroBUS reset; also the reset of the 2.8" SPI display
   * - 9
     - PCIE_PWR_EN
     - 3.3 V supply of the M.2 slot
   * - 10
     - USB_C_SEL
     - USB-C SuperSpeed mux select, on SOMs with USB 3
   * - 11 to 14
     - (unused)
     -
   * - 15
     - LVDS_I2C_SEL
     - Used by the 10.1" LVDS panel device trees (named only in the
       i.MX 95 device tree)

Ethernet
~~~~~~~~

The 00365 has two Realtek RTL8211F gigabit PHYs, connected over RGMII
(``phy-mode = "rgmii-id"``). Each PHY is on its own MDIO bus at address 0.
Their resets are expander lines 0 and 1, except on the i.MX 8M Plus, where
they are SoC GPIOs. On the i.MX 95, ETH_B's MDIO bus is bit-banged on GPIO
pins, because the i.MX 95 has one MDIO controller.

Other Interfaces
~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 25 25 25 25

   * - SOM
     - Console UART
     - CAN
     - PCIe (M.2)
   * - i.MX 91 and i.MX 93
     - ``lpuart1``
     - ``flexcan1``, ``flexcan2``
     - No
   * - i.MX 95
     - ``lpuart1``
     - ``flexcan1``, ``flexcan3``
     - Not enabled
   * - i.MX 8M Plus
     - ``uart4``
     - ``flexcan1``, ``flexcan2``
     - Yes (Gen 1)
   * - STM32MP2
     - ``usart2``
     - ``m_can1``, ``m_can2``
     - Yes

The console runs at 115200 baud. The microSD slot runs at 3.3 V only, at up
to 104 MHz.

Resources
---------

- `Quick Start Guide (i.MX 8M Plus) <https://downloads.cargt.com/datasheets/qsgs/imx8%20Quick%20Start%20PDF%20v1.pdf>`__
- `Quick Start Guide (i.MX 91 / i.MX 93) <https://downloads.cargt.com/datasheets/qsgs/imx93%20Quick%20Start%20PDF.pdf>`__
- `Quick Start Guide (STM32MP2) <https://downloads.cargt.com/datasheets/qsgs/STM32%20Quick%20Start%20PDF%20v1.pdf>`__

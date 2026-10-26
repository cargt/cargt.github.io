Supported Touchscreen Displays
==============================

10” LVDS 1280×800 – GLT1011280800is1
------------------------------------

.. thumbnail:: /_static/images/photos/displays/10-lvds-1.png
   :group: display-10-lvds
   :width: 22%
   :title: 10" LVDS 1280x800 - GLT1011280800is1

.. thumbnail:: /_static/images/photos/displays/10-lvds-2.png
   :group: display-10-lvds
   :width: 22%
   :title: 10" LVDS 1280x800 - GLT1011280800is1

.. thumbnail:: /_static/images/photos/displays/10-lvds-3.png
   :group: display-10-lvds
   :width: 22%
   :title: 10" LVDS 1280x800 - GLT1011280800is1

.. thumbnail:: /_static/images/photos/displays/10-lvds-detail.png
   :group: display-10-lvds
   :width: 22%
   :title: 10" LVDS 1280x800 - GLT1011280800is1 detail

5.5” MIPI-DSI 720×1280 – GLT0557201280is1
-----------------------------------------

.. thumbnail:: /_static/images/photos/displays/5.5-mipi-1.png
   :group: display-5.5-mipi
   :width: 22%
   :title: 5.5" MIPI-DSI 720x1280 - GLT0557201280is1

.. thumbnail:: /_static/images/photos/displays/5.5-mipi-2.png
   :group: display-5.5-mipi
   :width: 22%
   :title: 5.5" MIPI-DSI 720x1280 - GLT0557201280is1

.. thumbnail:: /_static/images/photos/displays/5.5-mipi-3.png
   :group: display-5.5-mipi
   :width: 22%
   :title: 5.5" MIPI-DSI 720x1280 - GLT0557201280is1

.. thumbnail:: /_static/images/photos/displays/5.5-mipi-4.png
   :group: display-5.5-mipi
   :width: 22%
   :title: 5.5" MIPI-DSI 720x1280 - GLT0557201280is1

2.8” SPI 240×320 – GLT028240320is1
----------------------------------

.. thumbnail:: /_static/images/photos/displays/2.8-spi-1.png
   :group: display-2.8-spi
   :width: 30%
   :title: 2.8" SPI 240x320 - GLT028240320is1

.. thumbnail:: /_static/images/photos/displays/2.8-spi-2.png
   :group: display-2.8-spi
   :width: 30%
   :title: 2.8" SPI 240x320 - GLT028240320is1

.. thumbnail:: /_static/images/photos/displays/2.8-spi-3.png
   :group: display-2.8-spi
   :width: 30%
   :title: 2.8" SPI 240x320 - GLT028240320is1

.. _Cargt Package Repository Images: https://yocto.cargt.com/images

Connecting Displays on a Cargt design
-------------------------------------

Electrical Connections
~~~~~~~~~~~~~~~~~~~~~~

- Identify the display interface supported by your LCD display (e.g., LVDS, MIPI-DSI, SPI).

+------------------------+-----------+---------------+
| Display Part Number    | Interface | Size (inches) |
+========================+===========+===============+
| GLT1011280800is1       | LVDS      | 10            |
+------------------------+-----------+---------------+
| GLT0557201280is1       | MIPI-DSI  | 5.5           |
+------------------------+-----------+---------------+
| GLT028240320is1        | SPI       | 2.8           |
+------------------------+-----------+---------------+

- Identify the corresponding connector on the carrier board or SOM for the display interface.
- Ensure the display is powered off before making any connections.

- LVDS & MIPI - There are 2 types of flex cables used for these display interfaces

   - Type A: Top-Top
   - Type B: Top-Bottom

   The flex cable type needed depends on the specific display model and board revision.
   Always refer to the documentation for your specific display model and board revision to determine the correct flex cable type if unsure.

   .. Warning::

      Pin 1 on display connector MUST connect to Pin 1 on the board.
      Only rely on the silkscreen PIN markings and documentation to identify Pin 1 on both the display and board.
      Do NOT rely on the "J" silkscreen marking position as it may not be consistent across different display models or board revisions.

   - Identify the CORRECT flex cable needed to connect the display to the board.

   Orient the board and display connectors, identifying and aligning Pin 1 on both.
   Then select the flex cable type (A or B) that matches the orientation of the connectors and allows Pin 1 on the display to connect to Pin 1 on the board.
   You may have to fold the flex cable in a specific way to achieve the correct orientation.

   .. Warning::

      Do NOT kink the flex cable as it may damage the internal wiring and cause the display to not function properly.

- SPI - The SPI display uses a Cargt MikroBus adapter board and standard MikroBus cable, so the pinout is consistent across different display models and board revisions. The adapter board is shown in the 2.8" photos above.

Software Configuration
~~~~~~~~~~~~~~~~~~~~~~

If you bought an evaluation kit with a display, the display should be pre-configured and work out of the box with the pre-compiled images from the `Cargt Package Repository Images`_.

If you are using your own display, you may need to modify the device tree to configure the display correctly.
Build a custom image with your device tree changes as described in the :ref:`yocto-tutorial`. A guide to customizing the device tree is planned.

If you are using a display that is sold by Cargt, then the necessary device tree configuration should already be included in the pre-compiled images from the `Cargt Package Repository Images`_.

How to check for available device tree overlays for display support:

   - As part of build:

   .. code-block:: bash

      ls <build_dir>/tmp/deploy/images/<machine>/*.dtb

   - On target device:

   .. code-block:: bash

      ls -l /boot/*.dtb
      # Example output - NXP:
      /boot/imx93-cargt-00363-00365-glt0557201280is1.dtb
      /boot/imx93-cargt-00363-00365-glt1011280800is1.dtb
      /boot/imx93-cargt-00363-00365.dtb
      # Example output - STM32MP2:
      /boot/stm32mp257f-cargt-00395-02-00365-glt0557201280is1.dtb
      /boot/stm32mp257f-cargt-00395-02-00365-glt1011280800is1.dtb
      /boot/stm32mp257f-cargt-00395-02-00365.dtb

Set the correct Device Tree Blob (DTB) for the display by modifying the U-Boot environment variable ``fdtfile`` to point to the appropriate DTB file that matches your display model.

   .. code-block:: bash

      # Using fw_setenv (from Linux shell)
      fw_setenv fdtfile /boot/<dtb_file_name>
      fw_printenv fdtfile  # Verify the change
      reboot

      # Using setenv (from U-Boot console)
      setenv fdtfile /boot/<dtb_file_name>
      saveenv
      printenv fdtfile  # Verify the change
      reset

   - Examples:

   .. code-block:: bash

      # For GLT0557201280is1 5.5" MIPI-DSI display:
      fw_setenv fdtfile /boot/imx93-cargt-00363-00365-glt0557201280is1.dtb

      # For GLT1011280800is1 10.1" LVDS display:
      fw_setenv fdtfile /boot/imx93-cargt-00363-00365-glt1011280800is1.dtb

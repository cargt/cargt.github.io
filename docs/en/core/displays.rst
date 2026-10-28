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

Taking Screenshots with Weston
------------------------------

Cargt images with a display run the Weston compositor, which includes
``weston-screenshooter``. It saves the whole screen as a PNG file named
``wayland-screenshot-<date>_<time>.png``. Weston only lets clients it trusts
take screenshots, so how you take one depends on where you start it.

With a Keyboard on the Board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With a USB keyboard connected to the board, press :kbd:`Super+S` (the
Windows key and :kbd:`S`). Weston starts ``weston-screenshooter`` itself and
allows it. The file is saved in Weston's working directory, ``/home/weston``
on Cargt images, or in the directory set by ``XDG_PICTURES_DIR`` in Weston's
environment (for example in ``/etc/default/weston``).

Over SSH or the Serial Console
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``weston-screenshooter`` started from a shell is only allowed when Weston
runs with ``--debug``.

.. warning::

   Without ``--debug``, ``weston-screenshooter`` prints
   ``Output capture error: unauthorized`` but still exits with status 0
   and writes a PNG file of the right size that is completely black. Check
   for the error message rather than the file.

To enable it, add a systemd drop-in that starts Weston with ``--debug``, and
restart Weston:

.. code-block:: bash

   mkdir -p /etc/systemd/system/weston.service.d
   cat > /etc/systemd/system/weston.service.d/screenshots.conf << 'END'
   [Service]
   ExecStart=
   ExecStart=/usr/bin/weston --debug --log=${XDG_RUNTIME_DIR}/weston.log --modules=systemd-notify.so
   END
   systemctl daemon-reload
   systemctl restart weston

Then take a screenshot. ``WAYLAND_DISPLAY`` tells it where Weston's socket
is, and ``XDG_PICTURES_DIR`` where to save the file (the current directory
if it is not set):

.. code-block:: bash

   WAYLAND_DISPLAY=/run/wayland-0 XDG_PICTURES_DIR=/tmp weston-screenshooter

Copy the file to your computer with ``scp``:

.. code-block:: bash

   scp root@<board-ip>:/tmp/wayland-screenshot-*.png .

.. warning::

   ``--debug`` also enables Weston's debug protocol, which lets any Wayland
   client on the board capture the screen and read Weston's debug output.
   Use it only during development, and remove the drop-in afterwards:

   .. code-block:: bash

      rm /etc/systemd/system/weston.service.d/screenshots.conf
      systemctl daemon-reload
      systemctl restart weston

Rotated Displays
~~~~~~~~~~~~~~~~

Screenshots show the framebuffer as it is sent to the panel, without the
display's rotation. The 5.5" MIPI-DSI display is a 720×1280 portrait panel
mounted in landscape: its device tree sets the panel orientation, Weston
draws the desktop rotated to match, and screenshots come out 720×1280 with
the desktop on its side. ``modetest -c`` shows the orientation as the
connector's ``panel orientation`` property:

.. code-block:: text

   root@imx93-cargt-00363-00365:~# modetest -c
   ...
   	38 panel orientation:
   		flags: immutable enum
   		enums: Normal=0 Upside Down=1 Left Side Up=2 Right Side Up=3
   		value: 3

For ``Right Side Up``, rotate the file 90° counter-clockwise on your
computer, for example with ImageMagick (for ``Left Side Up``, use ``90``):

.. code-block:: bash

   convert wayland-screenshot-<date>_<time>.png -rotate -90 screenshot.png

A screenshot taken with :kbd:`Super+S` on an i.MX 93 00363 on the 00365
carrier with the 5.5" display, after rotating it:

.. image:: /_static/images/screenshots/img-weston-screenshot.png
   :width: 60%
   :alt: Weston desktop with the Cargt wallpaper, 1280 by 720 pixels

Other Options
~~~~~~~~~~~~~

``weston-screenshooter --help`` lists further options, for example
``--format`` to save raw YUV data instead of a PNG.

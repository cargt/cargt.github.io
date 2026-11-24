Supported Touchscreen Displays
==============================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

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

The 2.8" display connects to the carrier's mikroBUS socket through the Cargt
00379 mikroBUS adapter. It works with the i.MX 91 and i.MX 93 00363 on the
00365 and 00428 carriers, and with the STM32MP2 00395-01 and 00395-02 on the
00365 carrier. The i.MX 8M Plus 00377 doesn't support it.

- The display runs landscape, at 320x240. Touch (FT6236) and the PWM
  backlight are in the display's device tree, with the touch axes matched to
  the landscape panel.
- The 00379 wires the touch controller's reset to the mikroBUS RX pin, which
  the carriers pass to the SoC as an input only. The adapter's pull-up holds
  the touch controller out of reset, so software can't reset it.
- The backlight runs at 200 Hz, because the adapter's backlight driver only
  dims at a low PWM frequency.
- Weston can't use the GPU on this SPI panel. When the image detects it, it
  starts Weston with the pixman renderer (and RGB565 on i.MX) and a smaller
  Cargt logo, using a copy of ``weston.ini`` in ``/run/cargt-weston``. Other
  displays keep the stock ``weston.ini``.

Select the display's device tree as described in `Software Configuration`_.

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

The pre-compiled images from the `Cargt Package Repository Images`_ include a device tree for each display Cargt sells, but most machines boot the device tree without a display by default. Only the i.MX 93 00363 on the 00428 carrier boots with the 5.5" MIPI-DSI display (``glt0557201280is1``) selected. On every other machine, including evaluation kits with a display, select the display's device tree with ``fdtfile`` as shown below.

If you are using your own display, you may need to modify the device tree to configure the display correctly.
Build a custom image with your device tree changes as described in the :ref:`yocto-tutorial`. A guide to customizing the device tree is planned.

How to check which display device trees are available:

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
See :ref:`u-boot-environment` for how ``fdtfile`` is written and how to change it from the U-Boot prompt.

Write the new value in the same form as the current one. On i.MX the value
is a path relative to the root partition, starting with ``boot/``. On
STM32MP2 it is the file name alone, for example
``stm32mp257f-cargt-00395-02-00365.dtb``.

   .. code-block:: bash

      fw_printenv fdtfile  # the current value, to copy its form
      fw_setenv fdtfile boot/<dtb_file_name>          # i.MX
      fw_setenv fdtfile <dtb_file_name>               # STM32MP2
      reboot

   - Examples:

   .. code-block:: bash

      # For GLT0557201280is1 5.5" MIPI-DSI display:
      fw_setenv fdtfile boot/imx93-cargt-00363-00365-glt0557201280is1.dtb

      # For GLT1011280800is1 10.1" LVDS display:
      fw_setenv fdtfile boot/imx93-cargt-00363-00365-glt1011280800is1.dtb

      # The same display on an STM32MP2 00395-02:
      fw_setenv fdtfile stm32mp257f-cargt-00395-02-00365-glt1011280800is1.dtb

      # For GLT028240320is1 2.8" SPI display on an i.MX 93 00363 / 00428:
      fw_setenv fdtfile boot/imx93-cargt-00363-00428-glt028240320is1.dtb

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

.. _display-text-console:

Text Console on the Display
---------------------------

On i.MX, the kernel has a text console on the display (the framebuffer
console, ``fbcon``). Weston covers it while it runs. Weston runs on virtual
terminal 7 (``tty7``) and switches to it when it starts, and a login prompt
runs on ``tty1``.

To see the console, stop Weston. The display then shows ``tty7``, and text
written to ``/dev/tty0`` (the terminal on screen) appears on it:

.. code-block:: bash

   systemctl stop weston
   echo "Hello from tty0" > /dev/tty0

To get the login prompt on the display, switch to ``tty1``:

.. code-block:: bash

   chvt 1

The console follows the panel orientation from the device tree, so it
reads the right way up on the 5.5" display. Start Weston again with
``systemctl start weston``, and start your own Wayland application again
after it. ``weston.socket`` can also start Weston again when an application
connects; stop it with ``systemctl stop weston.socket`` to keep Weston
off. This was checked on an i.MX 93 00363 on the 00365 with the 5.5"
display.

On STM32MP2, ST's kernel configuration turns off the framebuffer console
and the DRM driver's framebuffer emulation. There is no text console on the
display, and text written to ``/dev/tty0`` doesn't appear anywhere.
``/sys/class/vtconsole`` lists only the ``dummy device``. To add one, turn
both options on with a kernel configuration fragment for ``linux-stm32mp``
(see :doc:`yocto-development`):

.. code-block:: text

   CONFIG_DRM_FBDEV_EMULATION=y
   CONFIG_FRAMEBUFFER_CONSOLE=y

Cargt has not tested this fragment on STM32MP2.

.. _display-usb-gud:

USB Displays (GUD)
------------------

A USB display can be added with the Generic USB Display (GUD) protocol. The
display is a small board with an LCD that runs GUD gadget firmware, for
example a Raspberry Pi Zero, an RP2040 or an STM32 development board (see
the `GUD project <https://github.com/notro/gud/wiki>`__). Linux's ``gud``
driver shows it as an extra DRM card, such as ``card1``, with a ``USB-1``
connector. Touch on the display works through the normal HID driver.

On wrynose, ``cargt-image-dev`` installs the ``gud`` module on i.MX and
STM32MP2. The kernel builds it for every machine, so other images can add
``kernel-module-gud`` to ``IMAGE_INSTALL``. The module loads on its own when
a display is plugged in. scarthgap images don't have it.

Check that the display was found:

.. code-block:: bash

   lsmod | grep gud
   cat /sys/class/drm/card*-USB-*/status     # connected
   cat /sys/class/drm/card*-USB-*/modes      # for example 800x480

``gud`` binds only to the USB IDs in its own table (``16d0:10a9`` and
``1d50:614d`` in kernel 6.18). A display with another ID enumerates and its
touch works, but no DRM card appears. Add its ID by hand until the next
reboot, for example:

.. code-block:: bash

   echo "1209 4fb3 ff" > /sys/bus/usb/drivers/gud/new_id

Tested displays:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 35 40 25

   * - Host
     - Display
     - Result
   * - i.MX 93 00363 on the 00365
     - 800x480, USB high speed; 720x1280, USB high speed; 240x240
       (STM32H573I-DK), USB full speed
     - Works. The 720x1280 display needed ``new_id``.
   * - i.MX 91 00363 on the 00365
     - 240x240, USB full speed, on the carrier's USB-C port
     - Works
   * - STM32MP2 00395-01 on the 00365
     - 1024x600, USB high speed; 800x480 (STM32H747I-DISCO), on a USB 2.0
       hub
     - Works

The frame rate depends mostly on the display board, not the host. Content
that compresses well, such as a user interface, ran at 50 to 130 frames per
second on an 800x480 display. Content that doesn't compress, such as video
or noise, is limited by USB to about 25 to 28 MB/s, which is about 30
frames per second at 800x480. A full-speed display (12 Mbit/s) manages
under 10 such frames per second at 240x240. Use RGB565 buffers where you
can: XRGB8888 uses more CPU and lowers the frame rate.

Weston on a USB Display
~~~~~~~~~~~~~~~~~~~~~~~

- **STM32MP2:** on a board with no panel, Weston uses the USB display as its
  output on its own, with the GL renderer.
- **i.MX 93:** Weston starts on ``card0`` with the G2D renderer, which can't
  drive a USB display, so the USB display stays blank. A switch is coming
  (not yet merged) that runs Weston on the USB display with the pixman
  renderer and RGB565 output:

  .. code-block:: bash

     fw_setenv cargt_weston_display gud
     reboot

  The setting is in the U-Boot environment, so it survives software
  updates. A panel on the 2.8" SPI connector takes precedence over it.
- **i.MX 91:** the images have no Weston. Draw on the USB display's DRM
  card directly.

Remote Desktop (RDP)
--------------------

Weston can share the screen over the Remote Desktop Protocol (RDP), so you
can see and use a board's display from a computer, for example with Windows
Remote Desktop Connection or FreeRDP. The board keeps showing the desktop on
its own panel at the same time.

Cargt i.MX images include Weston's RDP backend and FreeRDP. It was tested
on an i.MX 93 00363 on the 00365 carrier with the rotated 5.5" MIPI-DSI
display and on an i.MX 95 00414 on the 00365 with the 10.1" LVDS display,
running ``cargt-image-dev`` (wrynose).

.. warning::

   Weston's RDP server does not check the user name or password: anyone who
   can reach port 3389 on the board can see the screen and type into it.
   Use RDP only on a network you control, or block port 3389 and connect
   through an SSH tunnel (see `Connecting through SSH`_).

The TLS Key
~~~~~~~~~~~

The RDP connection is encrypted with TLS. On its first boot, each board
creates its own self-signed certificate and key in ``/data/freerdp/keys``
(the ``cargt-rdp-keys`` service). They are on the data partition, so they
stay the same across A/B updates and also work with a read-only root
filesystem. Clients show a certificate warning the first time they connect,
because the certificate is self-signed. To create a new key, delete
``/data/freerdp/keys/server.key`` and reboot.

The ``[screen-share]`` section of ``/etc/xdg/weston/weston.ini`` points the
RDP server at that key:

.. code-block:: ini

   [core]
   modules=screen-share.so

   [screen-share]
   command=/usr/bin/weston --backend=rdp-backend.so --shell=fullscreen-shell.so --no-resizeable --rdp-tls-cert=/data/freerdp/keys/server.crt --rdp-tls-key=/data/freerdp/keys/server.key

Starting Screen Sharing
~~~~~~~~~~~~~~~~~~~~~~~

Screen sharing is off when Weston starts. Press :kbd:`Ctrl+Alt+S` on a
keyboard connected to the board to start it until Weston restarts. To start
it every time Weston starts, add ``start-on-startup=true`` to the
``[screen-share]`` section and restart Weston:

.. code-block:: ini

   [screen-share]
   command=/usr/bin/weston --backend=rdp-backend.so ...
   start-on-startup=true

.. code-block:: bash

   systemctl restart weston

To build an image that starts it automatically, set this in your
``local.conf`` or distro configuration:

.. code-block:: text

   CARGT_WESTON_RDP_AUTOSTART = "1"

Weston then starts a second Weston instance with the RDP backend, which
listens on TCP port 3389.

Connecting
~~~~~~~~~~

Connect to the board's IP address with any RDP client. Enter any user name
and password if the client asks, and accept the certificate warning. From
Linux, with FreeRDP:

.. code-block:: bash

   xfreerdp /v:<board-ip>

Windows Remote Desktop Connection connected to an i.MX 93 00363 on the 00365
carrier with the 5.5" display. The terminals show the image's release and
the two Weston processes: the one driving the panel, and the RDP instance
started by screen sharing:

.. image:: /_static/images/screenshots/img-weston-rdp.png
   :width: 90%
   :alt: Remote Desktop view of the Weston desktop with two terminals, showing os-release and the two weston processes

The remote view mirrors the board's own panel: both show the same desktop,
and keyboard and mouse input from the client goes to it.

Connecting through SSH
~~~~~~~~~~~~~~~~~~~~~~

To keep port 3389 off the network, forward it through SSH and connect to
the local end of the tunnel:

.. code-block:: bash

   ssh -N -L 13389:localhost:3389 root@<board-ip>
   xfreerdp /v:localhost:13389

.. _display-vnc:

Remote View over VNC
--------------------

Weston can also mirror the panel to a VNC viewer, with mouse and keyboard
input, while it keeps driving the panel. Unlike RDP, the VNC server checks
a login: the user Weston runs as, with that user's password, over TLS. Use
it to see and use a board's display from a computer, for example a board in
a test rack.

VNC is in wrynose development images only, and only when the build asks
for it. It opens port 5900 on every network interface. Set this in your
``local.conf`` and build ``cargt-image-dev``:

.. code-block:: text

   CARGT_WESTON_VNC = "1"

The login:

- **i.MX:** ``root``. **STM32MP2:** ``weston``, because Weston runs as that
  user there.
- The user needs a password. Development images have an empty one, which
  VNC refuses, so set it with ``passwd`` (or ``passwd weston``).
- After 5 failed logins in 15 minutes, VNC refuses that user for 10
  minutes. The lockout applies to VNC only, not to the console or SSH, and
  clears on reboot.
- ``CARGT_WESTON_VNC_EMPTY_PASSWORD = "1"`` lets the empty password log in.
  Use it only on a closed network: any password then works, and the lockout
  never triggers.

Each board makes its own self-signed TLS key pair on first boot, in
``/data/weston-vnc`` on i.MX and ``/usr/local/weston-vnc`` on STM32MP2.
Both survive software updates. The certificate's SHA-256 fingerprint is
logged at every boot, so you can compare it with what the viewer shows:

.. code-block:: bash

   journalctl -b | grep cargt-weston-vnc
   # cargt-weston-vnc: mirroring DSI-1 on port 5900, certificate sha256 Fingerprint=...

The viewer must support VeNCrypt with X509Plain, the only security type
offered. TigerVNC's ``vncviewer`` does; noVNC doesn't. Connect to the
board's IP address and accept the certificate:

.. code-block:: bash

   vncviewer <board-ip>

The VNC output is off until a viewer connects, so an idle board uses
almost no CPU. While a viewer is connected, Weston sends at most 12 frames
per second. On an STM32MP2, an animated screen with a viewer connected
used most of one CPU core for encoding.

Other settings, in the same directory as the key pair:

- Turn VNC off: create a file named ``disabled`` and restart Weston (on
  STM32MP2, reboot).
- Mirror a display other than the first connected one: write its connector
  name, such as ``HDMI-A-1``, to a file named ``output``.

With VNC loaded, ``weston-screenshooter`` needs ``--output=<name>``, for
example ``--output=DSI-1``. Without it, it waits for the VNC output, which
is off while no viewer is connected.

This was tested on an i.MX 93 00363 on the 00428 with the 5.5" display
(G2D renderer) and an STM32MP2 00395-01 on the 00365 with the 5.5" display
(GL renderer). The i.MX 91 and i.MX 95 haven't been tested.

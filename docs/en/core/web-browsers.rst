.. _web-browsers:

Web Browsers: WPE WebKit and Chrome
===================================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

A product that shows its user interface as a web page needs a browser
engine on the board. This page compares the two that run on Cargt SOMs,
`WPE WebKit <https://wpewebkit.org/>`__ and Chromium (Chrome), measured by
Cargt in November 2026: how much flash and RAM each adds, how fast each
renders on each SoC, and how to build them.

.. contents:: On this page
   :local:
   :depth: 1

Summary
-------

- **Flash:** WPE WebKit adds 163 to 174 MB to the image, and a trimmed
  build 130.5 MB. Chrome adds 382 to 385 MB. WPE WebKit saves 210 to
  250 MB per image.
- **Build time:** WPE WebKit compiled in 40 to 63 minutes on Cargt's build
  host; Chromium took 3.6 to 4.5 hours.
- **RAM:** with 1 GB of RAM (emulated, see `Caveats`_), both browsers ran
  every test page without running out of memory and at unchanged frame
  rates.
- **i.MX 95 and i.MX 8M Plus:** both browsers reach 60 frames per second
  on animation the GPU can composite. Chrome is much faster on pages that
  repaint every frame, and on WebGL on the 8M Plus. WPE WebKit uses less
  CPU on composited animation.
- **STM32MP2:** WPE WebKit only; Chromium is not supported on it.
  Composited animation runs at the panel's refresh rate, and WebGL at 26
  frames per second.
- **i.MX 93 (no 3D GPU):** either browser handles static pages. Animation
  that only moves or fades elements runs at 52 frames per second with WPE
  WebKit and 19 with Chrome, with both CPU cores busy. Pages that repaint
  every frame, and WebGL, are not usable.

Which Browser for Which SoC
---------------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 25 75

   * - SoC
     - Recommendation
   * - STM32MP2
     - WPE WebKit, the only engine that runs. It fits in 1 GB of RAM.
       Use the trimmed build (130.5 MB) where the root file system slot is
       tight: on the test board, a 3 GB slot with the development image
       had 190 MB free. Run ``cog`` under Weston.
   * - i.MX 93
     - WPE WebKit or Chrome, for mostly static pages: dashboards with text
       and number updates. 1 GB is enough. Prefer WPE WebKit when flash
       matters and the page animates only with ``transform`` and
       ``opacity``; prefer Chrome when the page repaints often. Anything
       more animated, or WebGL, needs an SoC with a GPU.
   * - i.MX 8M Plus and i.MX 95
     - Either. WPE WebKit for products where flash, RAM or build time
       matter; Chrome for heavy web applications with a lot of repainting
       or WebGL.

The **cheapest platform that runs a browser adequately** is the STM32MP2
with 1 GB and WPE WebKit. The cheapest SoC on which Chrome performs well
is the i.MX 8M Plus.

How It Was Measured
-------------------

Four synthetic test pages ran on each board, under Weston unless noted:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 20 80

   * - Page
     - Content
   * - ``static``
     - Cards and a table, no animation.
   * - ``css``
     - The worst case: 60 boxes with shadows animate their ``left``
       position over an animated gradient, so the browser lays out and
       repaints every frame.
   * - ``csst``
     - The same boxes, animating ``transform`` and ``opacity`` only, which
       the GPU can composite without repainting.
   * - ``webgl``
     - A full-screen WebGL fragment shader.

- **fps:** a ``requestAnimationFrame`` counter in each page, over 30 s.
- **CPU:** the whole system, as a percentage of all cores.
- **Browser PSS:** the proportional memory of all the browser's processes.
- **System used:** total memory minus the lowest available memory during
  the 30 s.
- **Startup:** from launch until the page first reports, with a warm cache
  unless noted.

Results
-------

i.MX 95
~~~~~~~

i.MX 95 00414 on the 00365 carrier: six Cortex-A55 cores, Mali-G310 GPU,
10.1" LVDS display (1280x800), WPE WebKit 2.52.6, Chromium 142.

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - Page
     - WPE fps
     - Chrome fps
     - WPE CPU
     - Chrome CPU
     - WPE PSS
     - Chrome PSS
   * - static
     - –
     - –
     - 3%
     - 0.8%
     - 315–324 MB
     - 329–335 MB
   * - css
     - 13.1
     - **59.8**
     - 36%
     - 36%
     - 328 MB
     - 364 MB
   * - csst
     - 59.5
     - 59.9
     - **20%**
     - 30%
     - 317 MB
     - 358 MB
   * - webgl
     - 59.9
     - 59.9
     - 14%
     - 16%
     - 340 MB
     - 341 MB

- Startup: WPE WebKit 0.57 s; Chrome 0.9 s warm, 2.6 s cold.
- WPE WebKit ran as ``MiniBrowser`` on the WPEPlatform API under Weston;
  ``cog`` on DRM, without Weston, gave the same results. ``cog`` under
  Weston does not run on this GPU (see `Launchers`_).
- WebGL reached 60 fps with the GPU's ``performance`` frequency governor.
  The default governor held the GPU at 800 MHz, which gave about 52 fps.
- Whole-system memory was not measured on this board.

i.MX 8M Plus
~~~~~~~~~~~~

i.MX 8M Plus 00377 on the 00365 carrier: four Cortex-A53 cores, GC7000UL
GPU, 10.1" LVDS display (1280x800), WPE WebKit 2.52.6, Chromium 142.

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - Page
     - WPE fps
     - Chrome fps
     - WPE CPU
     - Chrome CPU
     - System used, WPE / Chrome
     - WPE PSS
     - Chrome PSS
   * - static
     - –
     - –
     - 0.7%
     - 1.0%
     - 666 / 645 MB
     - 253 MB
     - 293 MB
   * - css
     - 7.7
     - **28.7**
     - 42%
     - 33%
     - 654 / 831 MB
     - 260 MB
     - 459 MB
   * - csst
     - 61.4
     - 61.3
     - **30%**
     - 52%
     - 659 / 643 MB
     - 261 MB
     - 321 MB
   * - webgl
     - 32.3
     - **57.3**
     - 8%
     - 21%
     - 768 / 645 MB
     - 356 MB
     - 307 MB

- Startup: WPE WebKit 0.61 s warm, 1.91 s cold; Chrome 1.0 s warm, 2.67 s
  cold.
- WPE WebKit ran as ``cog`` under Weston.
- WPE WebKit's WebGL kept the GPU fully busy for 32 fps, against 57 fps
  for Chrome. Its WebGL path on this GPU is less efficient.
- The development image without a browser used about 560 MB.

i.MX 93
~~~~~~~

i.MX 93 00363 on the 00428 carrier: two Cortex-A55 cores, no 3D GPU
(Mesa's software renderer), MIPI-DSI output (720x1280) with no panel
attached, WPE WebKit 2.52.6, Chromium 142.

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - Page
     - WPE fps
     - Chrome fps
     - WPE CPU
     - Chrome CPU
     - System used, WPE / Chrome
     - WPE PSS
     - Chrome PSS
   * - static
     - –
     - –
     - 1%
     - 3%
     - 702 / 492 MB
     - 481 MB
     - 337–348 MB
   * - css
     - 0.4 (24 s to the first frame)
     - **8.3**
     - 93%
     - 87%
     - 710 / 539 MB
     - 479 MB
     - 397 MB
   * - csst
     - **52.4**
     - 19.1
     - 85%
     - 78%
     - 698 / 569 MB
     - 483 MB
     - 431 MB
   * - webgl
     - 2.7
     - not available
     - 99%
     - –
     - 781 / 479 MB
     - 558 MB
     - 341 MB

- Startup: WPE WebKit 1.2 s warm, 2.8 s cold; Chrome 1.3 s warm, 3.2 s
  cold.
- WPE WebKit ran as ``cog`` under Weston.
- Chrome's GPU blocklist disables WebGL on Mesa's software renderer, and
  Chrome then composites in software too. ``--ignore-gpu-blocklist``
  forces WebGL on, at 5.0 fps with 98% CPU.
- The DSI output kept running and pacing frames without a panel, so the
  frame rates, CPU and memory are representative; the picture itself was
  not checked.
- The development image with Weston and no browser used about 390 MB.

**With 1 GB of RAM** (emulated, about 546 MB available before the browser
started):

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - Page
     - WPE fps
     - Chrome fps
     - WPE lowest available
     - Chrome lowest available
   * - static
     - –
     - –
     - 400 MB
     - 418 MB
   * - csst
     - 51.0
     - 19.5
     - 329 MB
     - 342 MB
   * - css
     - 0.4
     - 8.3
     - 307 MB
     - 371 MB
   * - webgl
     - 2.7
     - –
     - 247 MB
     - –

Nothing ran out of memory and the frame rates did not change. Startup was
1.5 s for WPE WebKit and 2.6 s for Chrome. On the i.MX 93 the limit is the
CPU, not the memory.

STM32MP2
~~~~~~~~

STM32MP257F 00395-01 on the 00365 carrier: two Cortex-A35 cores, GC8000UL
GPU, 5.5" MIPI-DSI display (720x1280) refreshing at 44 Hz, WPE WebKit
2.54.2, default and trimmed builds (see `Building WPE WebKit`_).

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - Page
     - Default fps
     - Trimmed fps
     - CPU
     - System used (trimmed)
     - PSS (trimmed)
   * - static
     - –
     - –
     - 3–4%
     - 400 MB
     - 165–168 MB
   * - css
     - 7.6
     - 7.8
     - 68–69%
     - 416 MB
     - 167 MB
   * - csst
     - 43 (the panel's rate)
     - 43
     - 56–57%
     - 407 MB
     - 173 MB
   * - webgl
     - 26.3 (limited by the GPU)
     - 26.2
     - 22–25%
     - 458 MB
     - 181 MB

- Startup: default 0.84 s warm, 2.85 s cold; trimmed 0.70 s warm, 2.57 s
  cold.
- WPE WebKit ran as ``cog`` under Weston.
- The development image without a browser used about 320 MB.

**With 1 GB of RAM** (emulated, trimmed build, about 426 MB available
before the browser started):

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - Page
     - fps
     - Lowest available
     - PSS
   * - static
     - –
     - 382 MB
     - 135 MB
   * - csst
     - 43.0
     - 380 MB
     - 138 MB
   * - css
     - 7.8
     - 371 MB
     - 139 MB
   * - webgl
     - 25.5
     - 339 MB
     - 155 MB

Nothing ran out of memory, the frame rates did not change, and startup was
1.07 s.

Image Size
----------

Installed size added to ``cargt-image-dev``:

.. list-table::
   :class: wrap-cells
   :header-rows: 1

   * - SoC
     - WPE WebKit
     - Trimmed WPE WebKit
     - Chrome 142
   * - i.MX 95
     - 174 MB (with ``MiniBrowser``)
     - –
     - 385 MB
   * - i.MX 8M Plus
     - 170 MB
     - –
     - 384 MB
   * - i.MX 93
     - 170 MB
     - –
     - 382 MB
   * - STM32MP2
     - 163 MB
     - **130.5 MB**
     - not supported

- **WPE WebKit:** the engine library is 119 to 121 MB. The rest is speech
  synthesis (``flite``, 27 MB), fonts (6 to 11 MB), JPEG XL (3.5 MB), the
  web inspector (1.4 MB) and ``cog`` (0.5 MB). The trimmed build saves
  space mostly by leaving out speech synthesis, JPEG XL and the inspector;
  the ``reduce-size`` compile option saved only 2 MB.
- **Chrome:** ``chromium-ozone-wayland`` is 365 to 367 MB, plus GTK 3
  (13.7 MB), which Chrome did not need to run.
- On the i.MX 95, the compressed root file system tarball grew from 449 MB
  to 510 MB with WPE WebKit.

Building WPE WebKit
-------------------

WPE WebKit comes from Igalia's `meta-webkit
<https://github.com/Igalia/meta-webkit>`__ layer. Add it to
``bblayers.conf``, then add to ``local.conf``:

.. code-block:: bash

   PREFERRED_PROVIDER_virtual/wpebackend = "wpebackend-fdo"
   IMAGE_INSTALL:append:pn-cargt-image-dev = " wpewebkit cog"

**i.MX (wrynose):** use meta-webkit's ``wrynose`` branch (WPE WebKit
2.52.6; ``wrynose-latest`` has 2.54.2). Two more lines:

.. code-block:: bash

   # NXP's mali-imx recipe doesn't register libgles2 as provided, so
   # wpewebkit's dependency on it fails to resolve. Harmless on the other GPUs.
   RDEPENDS:wpewebkit:remove:pn-wpewebkit = "libgles2"
   # i.MX 95 under Weston: add the WPEPlatform API and MiniBrowser
   PACKAGECONFIG:append:pn-wpewebkit = " wpe-platform minibrowser"

The ``libgles2`` line works around a bug in NXP's ``mali-imx.inc``: it
builds its ``RPROVIDES`` keys in an anonymous Python function, where they
are never expanded, so nothing can depend on ``libgles2``. ``bitbake -e``
hides the problem because it expands the keys when it prints them.

**STM32MP2 (scarthgap):** use meta-webkit's ``scarthgap-latest`` branch
(WPE WebKit 2.54.2); the plain ``scarthgap`` branch stops at 2.46.7. No
``libgles2`` workaround is needed. For the trimmed build:

.. code-block:: bash

   PACKAGECONFIG:remove:pn-wpewebkit = "accessibility avif gamepad jpegxl libbacktrace mediastream remote-inspector speech-synthesis spellcheck sysprof"
   PACKAGECONFIG:append:pn-wpewebkit = " reduce-size"
   # meta-webkit 2.54: video needs GStreamer's mpegts library, which the
   # recipe only adds with mediastream. Without this, do_configure fails.
   DEPENDS:append:pn-wpewebkit = " gstreamer1.0-plugins-bad"

The trimmed build keeps the JIT, video, Media Source, Web Audio, WOFF2
fonts, WebDriver and the GPU process.

Chrome
------

Chrome is ``chromium-ozone-wayland`` from the `meta-browser
<https://github.com/OSSystems/meta-browser>`__ layer; the results above
are Chromium 142.0.7444.175, from the wrynose branch. ST does not support
Chromium on the STM32MP2.

To render with the GPU, start Chromium 142 with:

.. code-block:: bash

   chromium --ozone-platform=wayland --use-gl=angle --use-angle=gles <url>

Chromium 142 rejects ``--use-gl=egl`` and falls back to software
rendering. ``--kiosk`` gives a full-screen window without browser controls.
With these flags Chrome rendered with the GPU on the i.MX 95 and 8M Plus;
on the i.MX 95 its WebGL renderer reported ``ANGLE (ARM, Mali-G310, OpenGL ES
3.2)``.

Launchers
---------

WPE WebKit has no window of its own; a launcher creates one. ``cog`` is the
usual one, and it can draw through Weston (``cog -P wl``, full screen with
``COG_PLATFORM_WL_VIEW_FULLSCREEN=1``) or directly on the display without
Weston (``cog -P drm``). Not every combination works on every GPU:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 22 39 39

   * - SoC
     - ``cog`` under Weston
     - ``cog`` on DRM, without Weston
   * - i.MX 95
     - Fails: the Mali driver lacks the EGL function
       ``eglCreateWaylandBufferFromImageWL``. Use ``MiniBrowser`` instead.
     - Works
   * - i.MX 8M Plus
     - Works
     - Fails: pages load, but frames never reach the display
   * - i.MX 93
     - Works
     - Static pages only; animated pages abort
   * - STM32MP2
     - Works
     - Fails: ``no crtc for encoder found!``

On the i.MX 95 under Weston, build the WPEPlatform API and ``MiniBrowser``
(the ``PACKAGECONFIG`` line above, +3 MB) and run
``/usr/libexec/wpe-webkit-2.0/MiniBrowser -f <url>``. A product would use a
small launcher of its own on the same API.

``cog`` writes the page's console messages to standard output with
``--enable-write-console-messages-to-stdout=true``, which helps when
debugging a page on the board. On DRM, ``cog`` crashes when it is stopped
with ``SIGTERM``; a product launcher should exit cleanly.

Caveats
-------

- **Synthetic pages.** A real page may perform anywhere between ``csst``
  and ``css``. Test with your own content.
- **Development image.** All memory figures are on ``cargt-image-dev``,
  which uses 320 to 560 MB before a browser starts. A product image leaves
  more room.
- **1 GB was emulated.** A process locked enough memory on a 2 GB board to
  leave what a 1 GB SOM would have, assuming the same kernel, CMA and GPU
  reservations. It was not measured on 1 GB hardware.
- **Different WPE WebKit versions.** 2.52.6 on i.MX, 2.54.2 on STM32MP2.
- **Displays differ.** The i.MX 95 and 8M Plus drove 1280x800 LVDS panels;
  the i.MX 93 and STM32MP2 a 720x1280 DSI output, with no panel on the
  i.MX 93 and a 44 Hz panel on the STM32MP2.
- **BSP state.** The i.MX results were built from ``meta-imx-cargt`` as of
  October 27, 2026.
- The browsers ran from a separate root file system on each board's
  existing image, using the build's GPU libraries (the board's own on the
  STM32MP2).

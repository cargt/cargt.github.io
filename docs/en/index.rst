Cargt Developer Documentation
=============================

.. rst-class:: cargt-tagline

Modern Electronics. Confidence at Every Step.

.. rst-class:: cargt-contact-link

`Contact Us <https://www.cargt.com/cargt-about/contact-us>`__

New to a Cargt board? Read :doc:`core/getting-started` to flash and boot a
pre-built image, then :doc:`core/identify-som` to find your Yocto ``MACHINE``,
then :doc:`core/yocto` to build your own image. Every release and image is
listed in :doc:`core/releases`, and :doc:`core/image-finder` has each image's files,
commands and package sizes.

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Get Started
        :link: core/getting-started
        :link-type: doc

        Flash a pre-built image to an i.MX or STM32MP2 board and log in.

    .. grid-item-card:: Image Finder
        :link: image-finder/index.html
        :link-type: url

        Pick a board and get its nightly image and the commands to flash
        it, with every package, its dependencies and installed size.

    .. grid-item-card:: Product Catalog
        :link: core/index
        :link-type: doc

        SOMs, carrier boards and thermal data, with the software releases
        for each.

    .. grid-item-card:: Develop with Yocto
        :link: core/yocto
        :link-type: doc

        Set up a build machine, build the Cargt BSP, and customize it.

    .. grid-item-card:: Using the Hardware from Linux
        :link: core/linux-basics
        :link-type: doc

        GPIO, I²C, PWM, serial, networking, Wi-Fi, Bluetooth, displays and
        cameras.

    .. grid-item-card:: Updates and Production
        :link: core/software-updates
        :link-type: doc

        SWUpdate and RAUC field updates and production data.

    .. grid-item-card:: Troubleshooting
        :link: core/troubleshooting
        :link-type: doc

        Find your symptom: flashing, booting, networking, updates or builds.

.. toctree::
  :maxdepth: 1
  :caption: Get Started

  core/getting-started
  core/identify-som
  core/releases
  core/image-finder
  core/flashing-troubleshooting

.. toctree::
  :maxdepth: 1
  :caption: Hardware

  core/index

.. toctree::
  :maxdepth: 1
  :caption: Performance

  core/benchmarks
  core/web-browsers
  core/thermal-characterization

.. toctree::
  :maxdepth: 1
  :caption: Boot, Storage and Firmware

  core/storage
  core/u-boot
  core/network-boot
  core/imx95-system-manager

.. toctree::
  :maxdepth: 1
  :caption: Using the Hardware from Linux

  core/linux-basics
  core/networking
  core/wifi
  core/bluetooth
  core/rtc
  core/power-watchdog
  core/displays
  core/cameras
  core/npu
  core/systemd-services
  core/package-management

.. toctree::
  :maxdepth: 1
  :caption: Develop

  core/yocto
  core/yocto-development
  core/application-development
  core/debugging-linux
  core/debugging-applications
  core/real-time-linux

.. toctree::
  :maxdepth: 1
  :caption: Security

  core/secure-boot
  core/key-storage
  core/selinux

.. toctree::
  :maxdepth: 1
  :caption: Deploy and Production

  core/software-updates
  core/rauc-ota-updates
  core/production

.. toctree::
  :maxdepth: 1
  :caption: Help and Reference

  core/troubleshooting
  references/index
  core/planned-topics

Cargt Developer Documentation
=============================

.. rst-class:: cargt-tagline

Modern Electronics. Confidence at Every Step.

.. rst-class:: cargt-contact-link

`Contact Us <https://www.cargt.com/cargt-about/contact-us>`__

New to a Cargt board? Read :doc:`core/getting-started` to flash and boot a
pre-built image, then :doc:`core/identify-som` to find your Yocto ``MACHINE``,
then :doc:`core/yocto` to build your own image.

.. grid:: 1 2 2 3
    :gutter: 3

    .. grid-item-card:: Get Started
        :link: core/getting-started
        :link-type: doc

        Flash a pre-built image to an i.MX or STM32MP2 board and log in.

    .. grid-item-card:: Product Catalog
        :link: core/index
        :link-type: doc

        SOMs, carrier boards, displays and thermal data, with the software
        releases for each.

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

        SWUpdate and RAUC field updates, secure boot and production data.

    .. grid-item-card:: Recovery and Troubleshooting
        :link: core/flashing-troubleshooting
        :link-type: doc

        Recover a board that won't flash or boot.

.. toctree::
  :maxdepth: 1
  :caption: Get Started

  core/getting-started
  core/identify-som
  core/flashing-troubleshooting

.. toctree::
  :maxdepth: 1
  :caption: Hardware

  core/index
  core/displays
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

.. toctree::
  :maxdepth: 1
  :caption: Deploy and Production

  core/software-updates
  core/rauc-ota-updates
  core/production

.. toctree::
  :maxdepth: 1
  :caption: Reference

  references/index
  core/planned-topics

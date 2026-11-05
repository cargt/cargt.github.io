.. _troubleshooting:

Troubleshooting
===============

Find your symptom below and follow the link to the section that covers it.
If none fits, `contact Cargt <https://www.cargt.com/cargt-about/contact-us>`__
with the ``MACHINE``, the release and the serial console output.

.. contents::
   :local:
   :depth: 1

Flashing and Recovery
---------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 45 55

   * - Symptom
     - Where to look
   * - ``uuu`` waits at ``Wait for Known USB Device Appear...``
     - :ref:`uuu-wait-for-device`
   * - ``uuu`` stops after the ROM stage on an i.MX 95
     - :ref:`uuu-imx95`
   * - Flashing stops partway or fails
     - :ref:`uuu-stops-partway`
   * - STM32CubeProgrammer doesn't see the board or fails
     - :ref:`stm32cubeprog-troubleshooting`
   * - The board doesn't boot after flashing, or a bad image needs recovering
     - :doc:`flashing-troubleshooting` (serial download mode works even with
       a blank or broken eMMC)
   * - The board boots into fastboot every time
     - ``bootcmd`` was left set to ``fastboot auto``; see
       :ref:`uuu-from-environment`
   * - The image doesn't match the board (wrong display, missing devices)
     - :ref:`machine-mismatch`

Booting and U-Boot
------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 45 55

   * - Symptom
     - Where to look
   * - A U-Boot environment change stopped the board booting
     - :ref:`u-boot-undo`
   * - An 00326 board hangs on reboot with the console cable connected
     - :doc:`catalog/carrier-boards/00326-sodimm-carrier`

Networking and Wireless
-----------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 45 55

   * - Symptom
     - Where to look
   * - Ethernet shows ``unavailable`` or has no address
     - :ref:`networking-troubleshooting`
   * - A point-to-point Ethernet link loses its address after 45 seconds
     - :ref:`rt-troubleshooting`
   * - Lost the SSH connection after changing the IP address
     - :ref:`networking-static-ip`
   * - Wi-Fi drops or doesn't stay connected
     - :ref:`wifi-link-up`
   * - Wi-Fi channels missing or transmit power limited
     - :ref:`wifi-regulatory`
   * - ``hci0`` does not appear
     - :ref:`bluetooth-no-hci0`

Software Updates
----------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 45 55

   * - Symptom
     - Where to look
   * - RAUC (STM32MP2): slot doesn't switch, ``Device or resource busy``,
       SSH host key changed after an update
     - :ref:`rauc-troubleshooting`
   * - The board fell back to the previous bank after an update
     - :ref:`rauc-rollback-safety`
   * - SWUpdate (i.MX): how an update is applied and checked
     - :ref:`swupdate`

Linux, Services and Logs
------------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 45 55

   * - Symptom
     - Where to look
   * - A service doesn't start or keeps restarting
     - :ref:`systemd-finding-problems`
   * - The journal is empty after a reboot
     - :ref:`journal-lost`
   * - Finding errors and warnings in the kernel log
     - :doc:`debugging-linux`
   * - ``/sys/kernel/realtime`` missing, or high ``cyclictest`` latency
     - :ref:`rt-troubleshooting`

Building with Yocto
-------------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 45 55

   * - Symptom
     - Where to look
   * - The build locks up, runs out of memory, or exits with a failure
     - :ref:`yocto-build-fails`

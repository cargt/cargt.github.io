.. _planned-topics:

Planned Topics
==============

These guides are being written. `Contact Cargt <https://www.cargt.com/cargt-about/contact-us>`__
if you need one of them sooner.

- **STM32MP2 flashing:** a step-by-step STM32CubeProgrammer guide (the
  00395 partition layout is in :doc:`rauc-ota-updates`)
- **Remote access:** reverse SSH with Teleport, provisioning, connecting to
  a remote device
- **Connectivity:** Bluetooth audio, NFC
- **Production configuration:** programming MAC address eFuses (i.MX and
  STM32MP2), reading the SOM EEPROM from Linux, limiting RAM size for
  testing
- **Debug and development:** debugging with Lauterbach
- **Secure boot:** a complete worked example of signing a Cargt image with
  the NXP Code Signing Tool, and kernel (OS container) signing
- **Yocto development:** adding a machine; customizing the bootloader and
  SWUpdate (the machines and distros are listed in :doc:`yocto`; layers,
  recipes, ``devtool modify``/``finish`` and kernel modules are in
  :doc:`application-development`; bitbake tasks, kernel configuration,
  device trees, custom images and ``devtool upgrade`` are in
  :doc:`yocto-development`; systemd services are in :doc:`systemd-services`)

.. _planned-topics:

Planned Topics
==============

These guides are being written. `Contact Cargt <https://www.cargt.com/>`__
if you need one of them sooner.

- **Flashing and boot:** step-by-step STM32CubeProgrammer flashing, flash
  layouts and partition tables, WIC files and custom layouts, partition
  auto-grow on first boot
- **SWUpdate internals:** how SWUpdate works, update scripts and images,
  U-Boot environment hooks and partition switching
- **Remote access:** reverse SSH with Teleport, provisioning, connecting to
  a remote device, SSH tunnels for RDP
- **Connectivity:** Bluetooth, NFC, cellular
- **IP networking:** IP forwarding, DHCP (dnsmasq, Kea), DNS (dnsmasq),
  firewalls (nftables), remote packet capture
- **Production configuration:** setting MAC addresses in one-time
  programmable memory (i.MX and STM32MP2), Cargt production EEPROM format and
  tools (from U-Boot and Linux), limiting RAM size for testing, eMMC boot
  partitions and pseudo-SLC mode
- **Debug and development:** debugging with Lauterbach, Java on i.MX,
  network boot with NFS and TFTP
- **Secure boot (AHAB) on i.MX 93:** keys and certificates, signing with the
  NXP Code Signing Tool, fusing keys, U-Boot and Linux configuration
- **Yocto development:** layers, recipes, machines and distros; adding a
  machine; bitbake tasks (``listtasks``, ``clean``, ``cleansstate``,
  ``menuconfig``); devtool (``modify``, ``add``, ``upgrade``,
  ``deploy-target``, ``finish``, ``ide-sdk``); customizing packages,
  bootloader, kernel, device tree and SWUpdate; custom images; systemd
  services; VS Code Remote-SSH

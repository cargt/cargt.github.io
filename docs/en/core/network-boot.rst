.. _network-boot:

Booting over the Network (TFTP and NFS)
=======================================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX`

During development it is often quicker to boot a board from your PC than to
flash it after every change. U-Boot loads the kernel and device tree from a
TFTP server, and Linux mounts its root file system from an NFS server. A
new build is then on the board as soon as you unpack it on the PC and
reboot, and the board's eMMC is not written.

The examples are from an i.MX 8M Plus 00377 on the 00365 carrier, booting
``cargt-image-dev`` (wrynose) from an Ubuntu 22.04 PC. Network booting is
done with the U-Boot variables of the i.MX boards; it has not been tested
on STM32MP2 boards.

.. contents:: On this page
   :local:
   :depth: 1

Setting Up the PC
-----------------

Install a TFTP server and an NFS server:

.. code-block:: bash

   sudo apt install tftpd-hpa nfs-kernel-server

``tftpd-hpa`` serves ``/srv/tftp`` by default, set in
``/etc/default/tftpd-hpa``:

.. code-block:: bash

   TFTP_USERNAME="tftp"
   TFTP_DIRECTORY="/srv/tftp"
   TFTP_ADDRESS=":69"
   TFTP_OPTIONS="--secure"

Export a directory for root file systems over NFS by adding a line to
``/etc/exports``, then reload the exports:

.. code-block:: text

   /srv/nfs4/rootfs  192.168.1.0/24(rw,sync,no_root_squash,no_subtree_check)

.. code-block:: bash

   sudo mkdir -p /srv/nfs4/rootfs
   sudo exportfs -ra
   showmount -e localhost

Replace ``192.168.1.0/24`` with your board network. ``no_root_squash`` is
needed: the board's root user must own its files. Each board, or each
image, can use its own subdirectory of the export.

The PC and the board must be on the same network, with a DHCP server
giving the board an address; a firewall on the PC must allow TFTP (UDP
port 69) and NFS.

Preparing the Files
-------------------

The root file system is the image's ``rootfs.tar.zst`` from the build's
``tmp/deploy/images/<machine>`` directory. Unpack it as root, so that the
files keep their owners and permissions:

.. code-block:: bash

   sudo mkdir /srv/nfs4/rootfs/cargt-00377-netboot
   sudo tar --zstd -xpf cargt-image-dev-imx8mp-cargt-00377-00365.rootfs.tar.zst \
       --numeric-owner -C /srv/nfs4/rootfs/cargt-00377-netboot

The kernel and device tree must match the kernel modules in that root file
system. Cargt i.MX images carry them in ``/boot``, so copy them from there
to the TFTP directory:

.. code-block:: bash

   mkdir -p /srv/tftp/cargt-00377
   R=/srv/nfs4/rootfs/cargt-00377-netboot
   cp $(readlink -f $R/boot/Image) /srv/tftp/cargt-00377/Image
   cp $R/boot/imx8mp-cargt-00377-00365-hdmi.dtb /srv/tftp/cargt-00377/

Choose the device tree for your carrier and display; the names are the
same as in ``fdtfile`` on a board booting from eMMC.

Two Changes for an NFS Root
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cargt images are made to boot from eMMC. Two of their defaults need
changing when the root file system comes from NFS:

- **Automounting.** A udev rule mounts every block device it finds under
  ``/run/media``, read-write. On an NFS boot that includes the eMMC's
  partitions. To keep the eMMC untouched, tell the rule to ignore them:

  .. code-block:: bash

     echo /dev/mmcblk | sudo tee /srv/nfs4/rootfs/cargt-00377-netboot/etc/udev/mount.ignorelist.d/emmc

- **Network management.** The kernel brings up Ethernet with DHCP before it
  mounts the root file system (``ip=dhcp``). NetworkManager and
  systemd-networkd would take over the interface later, and the board loses
  its root file system if the connection is reset. Mask both on the kernel
  command line, as in the U-Boot commands below.

Booting the Board
-----------------

Stop U-Boot at its prompt (see :doc:`u-boot`). The i.MX environment
already has the commands for network booting: ``netboot`` loads
``${image}`` and ``${fdtfile}`` from the TFTP server in ``serverip``, and
``netargs`` sets the kernel command line for an NFS root in ``nfsroot``.
Set the variables, and the masks in ``netargs``:

.. code-block:: text

   setenv autoload no
   dhcp
   setenv serverip <pc-ip>
   setenv nfsroot /srv/nfs4/rootfs/cargt-00377-netboot
   setenv image cargt-00377/Image
   setenv fdtfile cargt-00377/imx8mp-cargt-00377-00365-hdmi.dtb
   setenv ip_dyn no
   setenv netargs 'setenv bootargs ${jh_clk} ${mcore_clk} console=${console} root=/dev/nfs ip=dhcp nfsroot=${serverip}:${nfsroot},v3,tcp systemd.mask=NetworkManager.service systemd.mask=systemd-networkd.service'
   run netboot

``dhcp`` with ``autoload`` set to ``no`` gets the board an address without
trying to load a file. ``ip_dyn no`` makes ``netboot`` load the files with
``tftp`` from ``serverip``. Without ``saveenv`` these settings last for
this boot only.

U-Boot loads both files and starts the kernel:

.. code-block:: text

   u-boot=> dhcp
   ethernet@30bf0000 Waiting for PHY auto negotiation to complete......................................... TIMEOUT !
   phy_startup() failed: -110FAILED: -110BOOTP broadcast 1
   BOOTP broadcast 2
   BOOTP broadcast 3
   DHCP client bound to address <board-ip> (1025 ms)
   ...
   u-boot=> run netboot
   Booting from net ...
   Using ethernet@30be0000 device
   TFTP from server <pc-ip>; our IP address is <board-ip>
   Filename 'cargt-00377/Image'.
   Load address: 0x40400000
   Loading: *##################################################
   ...
   	 9.1 MiB/s
   done
   Bytes transferred = 37603840 (23dca00 hex)
   Using ethernet@30be0000 device
   TFTP from server <pc-ip>; our IP address is <board-ip>
   Filename 'cargt-00377/imx8mp-cargt-00377-00365-hdmi.dtb'.
   Load address: 0x43000000
   Loading: *####
   	 3.5 MiB/s
   done
   Bytes transferred = 58618 (e4fa hex)
   ...
   Starting kernel ...

The 00377 has two Ethernet ports; the timeout is the second port, which
had no cable, and U-Boot used the first. The kernel gets its own DHCP
address and mounts the root file system:

.. code-block:: text

   [    0.000000] Kernel command line: console=ttymxc3,115200 root=/dev/nfs ip=dhcp nfsroot=<pc-ip>:/srv/nfs4/rootfs/cargt-00377-netboot,v3,tcp systemd.mask=NetworkManager.service systemd.mask=systemd-networkd.service
   ...
   [    9.067941] IP-Config: Got DHCP answer from <dhcp-server>, my address is <board-ip>
   [    9.075356] IP-Config: Complete:
   ...
   [    9.383538] VFS: Mounted root (nfs filesystem) readonly on device 0:23.
   [    9.400171] Run /sbin/init as init process

systemd remounts it read-write, and the board starts as usual. On the
board:

.. code-block:: text

   root@imx8mp-cargt-00377-00365:~# findmnt -n -o SOURCE,FSTYPE /
   <pc-ip>:/srv/nfs4/rootfs/cargt-00377-netboot nfs
   root@imx8mp-cargt-00377-00365:~# systemctl is-system-running
   running
   root@imx8mp-cargt-00377-00365:~# systemd-analyze
   Startup finished in 9.546s (kernel) + 13.662s (userspace) = 23.208s
   graphical.target reached after 13.647s in userspace.

No eMMC partition is mounted. Changes you make on the board are written to
the NFS directory on the PC, and files you change there are seen by the
board at once.

To boot from eMMC again, reboot the board. Its saved environment was not
changed, so it boots as before.

Booting over the Network by Default
-----------------------------------

To net-boot at every reset, set the variables above and ``saveenv``, then
make ``bootcmd`` run ``netboot``:

.. code-block:: text

   setenv bootcmd 'dhcp; run netboot'
   saveenv

This was not tested for this page. ``env default -a`` followed by
``saveenv`` returns to the normal boot; see :doc:`u-boot`.

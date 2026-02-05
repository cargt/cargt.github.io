SOMs
==========

.. dropdown:: **Jump to Product**

    - `00363 i.MX91 OSM-L with IW612 <#i-mx91-osm-l-with-iw612>`__
    - `00324 i.MX93 SODIMM <#i-mx93-sodimm>`__
    - `00359 LGA with Murata 2EL <#lga-with-murata-2el>`__
    - `00363 i.MX93 OSM-L with IW612 <#i-mx93-osm-l-with-iw612>`__
    - `00408 i.MX95 OSM-L with IW612 <#i-mx95-osm-l-with-iw612>`__
    - `00377 i.MX8M Plus OSM-L with IW612 <#i-mx8m-plus-osm-l-with-iw612>`__
    - `00378 STM32MP257F OSM-L with CC3351 <#stm32mp257f-osm-l-with-cc3351>`__
    - `00395 STM32MP257F OSM-L with IW610 <#stm32mp257f-osm-l-with-iw610>`__
    - `00364 AM6254 OSM-L SOM with IW612 <#am6254-osm-l-som-with-iw612>`__
    - `00326 (SODIMM Carrier Board) <#sodimm-carrier-board>`__
    - `00406 (LGA Carrier Board) <#lga-carrier-board>`__
    - `00365 (OSM-L Carrier Board) <#osm-l-carrier-board>`__

NXP
---

.. _00363a:

00363 i.MX91 OSM-L with IW612
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00324:

00324 i.MX93 SODIMM
~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00359:

00359 LGA with Murata 2EL
~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00363b:

00363 i.MX93 OSM-L with IW612
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00408:

00408 i.MX95 OSM-L with IW612
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Coming Soon

.. _00377:

00377 i.MX8M Plus OSM-L with IW612
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images


STMicroelectronics
------------------

.. _00378:

00378 STM32MP257F OSM-L with CC3351
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00395:

00395 STM32MP257F OSM-L with IW610
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

Texas Instruments
-----------------

.. _00364:

00364 AM6254 OSM-L SOM with IW612
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software *Releases*
- Pre-built Images

Carrier Boards
====================

.. _00326:

00326 (SODIMM Carrier Board)
----------------------------

- Supported SOMs
  - i.MX93 00324 SODIMM SOM
- User Guide
- Hardware Design Guide
- Hardware Design Files

.. _00406:

00406 (LGA Carrier Board)
-------------------------

- Supported SOMs
  - i.MX93 00359 LGA SOM
- User Guide
- Hardware Design Guide
- Hardware Design Files

.. _00365:

00365 (OSM-L Carrier Board)
---------------------------

- Supported SOMs
  - i.MX93 00363 OSM-L SOM
  - i.MX8M Plus 00377 OSM-L SOM
  - STM32MP2 00378 OSM-L SOM
  - STM32MP2 00395 OSM-L SOM
  - AM6254 00364 OSM-L SOM
- User Guide
- Hardware Design Guide
- Hardware Design Files

Supported Touchscreen Displays
==============================

10” LVDS 1280×800 – GLT1011280800is1
------------------------------------

7” LVDS 1024×600 – GLT0701024600is2
-----------------------------------

5.5” MIPI-DSI 720×1280 – GLT0557201280is1
-----------------------------------------

2.8” SPI 240×320 – GLT028240320is1
----------------------------------

Getting Started with Embedded Linux
===================================

Cargt Provided Software Resources
---------------------------------

Public Yocto Source Code Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Cargt GitHub Organization <https://github.com/cargt>`_ – Public repositories for Yocto layers, example applications, and board support packages.

Public Package Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `Cargt Package Repository <https://yocto.cargt.com>`_ – Public repositories for pre-built packages and binaries for development with Cargt hardware designs.

Public Pre-compiled Images
~~~~~~~~~~~~~~~~~~~~~~~~~~

- .. _Cargt Package Repository Images:
- `Pre-built complete system images <https://yocto.cargt.com/images>`_ for supported Cargt hardware suitable for initial flashing or full system recovery.
- `Incremental update images <https://yocto.cargt.com/images>`_ compatible with SWUpdate for in-field updates without reflashing the entire system.

Running Linux on a Cargt design
-------------------------------

Flashing a Pre-compiled image to eMMC / SD card using UUU on an i.MX design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

   CARGT recommends eMMC for performance and reliability.
   eMMC is the default. Using SD card requires changing U-Boot variables and expert knowledge.

#. Put the board into the UUU mode as per the hardware design's user guide.

   - Option 1: For OSM-L based designs, this typically involves holding the BOOT button while powering on the board.
   - Option 2: U-boot Environment Variable Method can be used if BOOT button is not available. See U-Boot Environment Variables section for details.

#. Connect the board to the host computer via USB and check the connection by running:

   .. code-block:: bash

      uuu -lsusb

   The output should list the connected device.
#. Download the appropriate pre-compiled image from the `Cargt Package Repository Images`_.

   - This will usually be a ``.wic`` file, possibly compressed (e.g., ``.wic.zst``).
   - ``.wic`` is a disk image format that includes partitioning and filesystems.
#. Use the UUU tool to flash both the bootloader and image to eMMC / SD card.

   .. note::

      This will erase all existing data on the eMMC / SD card.

   .. code-block:: bash

      Select the appropriate command based on your target storage:
      uuu -b emmc_all imx-boot-tagged <image_file>.wic.zst
      uuu -b sd_all imx-boot-tagged <image_file>.wic.zst

#. Reboot the board.

UUU Example

.. figure:: /images/screenshots/img-nxp-uuu-commands.png

   UUU commands example output

Extra options for UUU:

- To flash only specific partitions, use the corresponding UUU command (e.g., ``-b emmc_boot``, ``-b emmc_rootfs``).
- For verbose output, add the ``-v`` flag to the UUU command.
- To log the flashing process, use the ``-l <log_file>`` option.
- To run the bootloader (SPL and U-Boot) from RAM:

   .. code-block:: bash

      uuu imx-boot

- To program just the bootloader to eMMC or SD Card

   .. code-block:: bash

      Select the appropriate command based on your target storage:
      uuu -b emmc imx-boot
      uuu -b sd imx-boot

- UUU allows multiple compression formats for the ``.wic`` image files, so you can use:

   .. code-block:: bash

      Select the appropriate command based on your target storage:
      uuu -b emmc_all imx-boot <image_file>.wic[.zst, .gzip, etc.]
      uuu -b sd_all imx-boot <image_file>.wic[.zst, .gzip, etc.]

Flashing a Pre-compiled image to eMMC using STM32Cube on an STM32MP2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Booting from eMMC
~~~~~~~~~~~~~~~~~

Flashing a Pre-compiled image to the SD card using STM32Cube on an STM32MP2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Booting from the SD card
~~~~~~~~~~~~~~~~~~~~~~~~

Understanding Flash Layouts and Partitions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Flash Layout Overview
- Partition Table Examples
- Filesystem Types
- WIC Overview
- Creating Custom Flash Layouts with WIC
- Autogrow Partitions

Understanding U-Boot Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

U-Boot variables can be accessed through either the console or ssh session.

   - Console: Interrupt the boot process by pressing any key during the U-Boot countdown.
      This will drop you to the U-Boot command prompt.
      U-Boot variables can be viewed and modified using the ``printenv``, ``setenv``, and ``saveenv`` commands in the U-Boot console.
   - SSH: Connect to the device via SSH once Linux has booted and access U-Boot variablesusing the ``fw_setenv`` and ``fw_printenv`` utilities.

SWUpdate
========

Incremental update images compatible with SWUpdate can be found in the `Cargt Package Repository Images`_ or can be built in your Yocto build environment.
The output file has a ``.swu`` extension.

For reference, the bitbake recipe file used to create SWUpdate images may have a ``-swu.bb`` ending or be called ``swupdate-image.bb``.

Example Usage: ``bitbake <machine-name>-swu`` or ``bitbake swupdate-image``

SWUpdate Methods
----------------

Web Server - Drag and Drop
~~~~~~~~~~~~~~~~~~~~~~~~~~
On a connected host computer, open a web browser and navigate to the SWUpdate web server running on the target device.

.. code-block:: bash

   http://<target_ip>:8080/

Follow the on-screen instructions to upload and install the update file.

Web Server - Command Line
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   swupdate -i <update_file>.swu -e web

USB Flash Drive
~~~~~~~~~~~~~~~
TFTP Server
~~~~~~~~~~~

SWUpdate Concepts
-----------------
- How SWUpdate Works
- Update Script Example
- Update Image Example
- U-Boot Environment Hooks and Partition Management

Package Management on a Cargt design
====================================

Cargt Package Repository
------------------------

Updating and Installing Packages using the Cargt Package Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      apt-get update
      apt-get install <package_name>

Updating using a downloaded to target ``.deb`` package file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      dpkg -i /<path_to_downloaded_package>/<package_file>.deb

Listing Installed Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      apt list --installed

Using your Own Package Repository
---------------------------------

Generating a Package Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   In your Yocto build environment, run:

   .. code-block:: bash

      bitbake package-index

   Then navigate to ``<build_dir>/tmp/deploy/deb/<machine>/`` to find the generated ``.deb`` repository files.

Simple Package Repository Hosting using Python HTTP Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   On your development host, navigate to the package repository directory (as above) and start a simple HTTP server:

   .. code-block:: bash

      cd <path_to_package_repo>
      python3 -m http.server <chosen_port_number>
      python3 -m http.server 8081

   .. note::

      Ensure that the chosen port number is open in your firewall settings.
      Choose a port number > 1024 and that is not already in use by another service such as SWUpdate (default port 8080).
      Open example:5678

Configuring the Target to use your Package Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   On the target device, add your repository to the APT sources list:

   .. code-block:: bash

      echo "deb [trusted=yes] http://<your_server_ip>:<port_number>/ ./" > /etc/apt/sources.list.d/my-custom-repo.list
      apt-get update
      apt-get install <package_name>

Advanced
~~~~~~~~

   You can list all of the packages in your repository by navigating to ``http://<your_server_ip>:<port_number>/`` in a web browser.

   Bitbake produces multiple directories such as ``armv8a``, ``all``, ``<machine-name>`` etc.
   If you add each directory as a separate line in the sources list, APT will be able to find more packages.
   Then the package server can be run from the ``<build_dir>/tmp/deploy/deb/`` directory.

   To do it at build time, add the following lines to your ``local.conf`` file on the development machine:

   .. code-block:: bash

      PACKAGE_FEED_URIS += " http://<your_server_ip>:<port_number>/ "
      PACKAGE_FEED_ARCHS = "all armv8a"
      Depending on your package repo, you may also need to specify:
      PACKAGE_FEED_BASE_PATHS = "deb"

   Further information: https://docs.yoctoproject.org/ref-manual/variables.html#term-PACKAGE_FEED_ARCHS


Remote Access
=============

- Reverse SSH using Teleport
- Provisioning
- Connecting to a Remote Device
- Using SSH Tunnel for RDP

Yocto Development
=================

Development Guides
------------------

- Layers, Recipes, Machines, Distros
- Adding a New Machine
- Changes in Meta Layer, U-Boot, Linux, SWUpdate
- Using VSCode on the Host with Remote-SSH Extension

Using bitbake
-------------

- Building Packages & Images
- Intermediate Commands: ``listtasks``, ``clean``, ``cleansstate``, ``menuconfig``, ``do_configure``, ``do_deploy``

Using devtool
-------------

- Modify Existing Recipe (``modify``)
- Add New Recipe (``add``)
  - CMake Example
  - Python Example
  - NodeJS Example
- Upgrade Recipe (``upgrade``)
- Build on Host (``build``)
- Test on Target (``deploy-target``, ``undeploy-target``)
- Update Meta Layers (``finish``)
- Other devtool Commands (``reset``, ``status``, ``menuconfig``, ``find-recipe``, ``edit-recipe``, ``ide-sdk``)

Image Customization
-------------------

- Adding/Removing Packages
- Customizing Bootloader
- Customizing Kernel
  - Adding Kernel Modules
  - Applying Kernel Patches
  - Configuring Kernel Options
- Customizing SWUpdate
- Customizing Device Tree
- Creating Custom Images
- Adding systemd Services

SBOM Generation
---------------

Connectivity
============

- Bluetooth
- NFC
- Cellular

IP Networking Examples
======================

- IP Forwarding
- DHCP Server (dnsmasq, Kea)
- DNS Server Examples (dnsmasq)
- Firewall Examples (nftables)
- Remote Packet Capture

Advanced Configuration
======================

One-Time Programmable Memory with i.MX Application Processors
-------------------------------------------------------------

- Setting MAC Addresses

One-Time Programmable Memory for STM32 MPU Application Processors
-----------------------------------------------------------------

- Setting MAC Addresses

Production EEPROM Programming
-----------------------------

- Cargt's Production EEPROM Methodology
  - Cargt's Production EEPROM Data Structure
- Supported SOMs
- Supported Methods
  - I2C via U-Boot
  - I2C via Linux
- Using Cargt's Production EEPROM Tools
- Limiting RAM size for testing

eMMC
----

- Boot Partition Management
- Pseudo-SLC for eMMC

Advanced Development
====================

Debugging with Lauterbach
-------------------------

Java Enablement on i.MX
-----------------------

Network Booting using NFS and TFTP in U-Boot
--------------------------------------------

Secure Boot (AHAB) with i.MX93
==============================

- Overview of Secure Boot
- Generating Keys and Certificates
- Signing Images with the Code Signing Tool (CST)
- Programming Keys using One-Time Programmable Memory
- Configuring U-Boot and Linux for Secure Boot


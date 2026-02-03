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

- `Pre-built complete system images <https://yocto.cargt.com/images>`_ for supported Cargt hardware suitable for initial flashing or full system recovery.
- `Incremental update images <https://yocto.cargt.com/images>`_ compatible with SWUpdate for in-field updates without reflashing the entire system.

Running Linux on a Cargt design
-------------------------------

Flashing a Pre-compiled image to eMMC using UUU on an i.MX design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Flashing a Pre-compiled image to eMMC using STM32Cube on an STM32MP2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Booting from eMMC
~~~~~~~~~~~~~~~~~

Flashing a Pre-compiled image to the SD card using UUU on an i.MX design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Incremental update images compatible with SWUpdate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- How SWUpdate Works
- Update Script Example
- Update Image Example
- U-Boot Environment Hooks and Partition Management
- Updates via:
  - Web Server
  - USB Flash Drive

Package Management on a Cargt design
====================================

- Updating and Installing Packages using the Cargt Package Repository
- Using your Own Package Repository
- Generating a Package Repository
- Simple Package Repository Hosting using Python HTTP Server
- Configuring the Target to use your Package Repository

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


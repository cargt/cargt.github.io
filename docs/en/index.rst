Cargt Developer Documentation
=============================

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
-----------------------------

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00324:

00324 i.MX93 SODIMM
-------------------

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00359:

00359 LGA with Murata 2EL
-------------------------

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00363b:

00363 i.MX93 OSM-L with IW612
------------------------------

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00408:

00408 i.MX95 OSM-L with IW612
------------------------------

- Coming Soon

.. _00377:

00377 i.MX8M Plus OSM-L with IW612
----------------------------------

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
------------------------------------

- Datasheet
- Reference Manual
- Hardware Design Guide
- Hardware Design Files
- Software Releases
- Pre-built Images

.. _00395:

00395 STM32MP257F OSM-L with IW610
----------------------------------

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
---------------------------------

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

References
==========

Yocto Development for NXP i.MX Application Processors
-----------------------------------------------------

- `NXP Yocto Project User's Guide (UG10164) <https://www.nxp.com/docs/en/fact-sheet/IMX91FAMFS.pdf>`_ – Official guide for building Linux images for NXP i.MX processors using Yocto.
- `NXP GitHub – meta-imx <https://github.com/nxp-imx/meta-imx>`_ – BSP layers and machine configurations for i.MX platforms.
- `NXP i.MX Porting Guide (UG10165) <https://www.nxp.jp/docs/en/user-guide/UG10165.pdf>`_ – Guide for customizing U-Boot for NXP i.MX processors.

NXP Product Documentation
-------------------------

Fact Sheets
~~~~~~~~~~~

- `i.MX 8M Plus Applications Processor Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/IMX8MPIECFS.pdf>`_ – Overview of features and architecture.
- `i.MX 91 Applications Processor Family Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/IMX91FAMFS.pdf>`_ – Overview of features and architecture.
- `i.MX 93 Applications Processor Family Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/iMX93FAMFS.pdf>`_ – Key features and block diagram.
- `i.MX 95 Applications Processor Family Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/IMX95FS.pdf>`_ – Overview of cores, NPU, and safety features.

Datasheets and Reference Manuals for i.MX 8M Plus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. dropdown:: 
    :open:

    - `i.MX 8M Plus Applications Processor Family Overview <https://www.nxp.com/docs/en/fact-sheet/IMX8MPLUSFAMFS.pdf>`_ – Key features and block diagram.
    - `i.MX 8M Plus Applications Processor Datasheet (Commercial) <https://www.nxp.com/docs/en/preview/PREVIEW_IMX8MPEC.pdf>`_ – Electrical characteristics and package details.
    - `i.MX 8M Plus Applications Processor Datasheet (Industrial) <https://www.nxp.com/docs/en/preview/PREVIEW_IMX8MPIEC.pdf>`_ – Electrical characteristics and package details.
    - `i.MX 8M Plus Applications Processor Reference Manual <https://www.nxp.com/docs/en/preview/PREVIEW_IMX8MPRM.pdf>`_ – Functional description and register maps.


Datasheets and Reference Manuals for i.MX 91, i.MX 93, and i.MX 95
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. dropdown:: 
    :open:
    
    - `i.MX 91 Applications Processors Data Sheet (Commercial) <https://www.nxp.com/docs/en/data-sheet/IMX91CEC.pdf>`_ – Electrical specifications and functional details.
    - `i.MX 91 Applications Processors Data Sheet (Industrial) <https://www.nxp.com/docs/en/data-sheet/IMX91IEC.pdf>`_ – Industrial-grade specifications.
    - `i.MX 93 Applications Processors Data Sheet (Commercial) <https://www.nxp.com/docs/en/data-sheet/IMX93CEC.pdf>`_ – Electrical specifications and functional details.
    - `i.MX 93 Applications Processors Data Sheet (Automotive) <https://www.nxp.com/docs/en/data-sheet/IMX93AEC.pdf>`_ – Automotive-grade specifications.
    - `i.MX 93 Applications Processors Data Sheet (Industrial) <https://www.nxp.com/docs/en/data-sheet/IMX93IEC.pdf>`_ – Industrial-grade specifications.
    - `i.MX 91 Applications Processor Reference Manual <https://www.nxp.com/docs/en/reference-manual/RM12173.pdf>`_ – Functional description and register maps.
    - `i.MX 93 Applications Processor Reference Manual <https://www.nxp.com/docs/en/reference-manual/RM12175.pdf>`_ – Functional description and register maps.
    - `i.MX 95 Product Page <https://www.nxp.com/products/i.MX95>`_ – Detailed product information and resources.

SWUpdate
--------

- `SWUpdate Documentation <https://sbabic.github.io/swupdate/>`_ – Detailed instructions for implementing secure software updates on embedded devices.
- `SWUpdate GitHub <https://github.com/sbabic/swupdate>`_ – Source code and examples for SWUpdate.

Yocto Project
-------------

- `Yocto Project Reference Manual <https://docs.yoctoproject.org/ref-manual/>`_ – Comprehensive reference for Yocto build system, metadata, and configuration.

BitBake
-------

- `BitBake User Manual <https://docs.yoctoproject.org/bitbake/>`_ – Guide to BitBake tasks, recipes, and advanced build options.

dnsmasq
-------

- `dnsmasq Man Page <https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html>`_ – Official documentation for DNS/DHCP server configuration and options.

Teleport SSH
------------

- `Teleport Server Access Guide <https://goteleport.com/docs/ssh-access/guides/server-access/>`_ – Instructions for secure remote access and reverse SSH tunneling.

nftables
--------

- `nftables Wiki <https://wiki.nftables.org/>`_ – Tutorials and examples for Linux firewall configuration using nftables.
- `netfilter.org nftables Project <https://www.netfilter.org/projects/nftables/index.html>`_ – Official project page with technical details and updates.

NXP Documentation for Secure Boot (AHAB) on i.MX Processors
-----------------------------------------------------------

- `NXP i.MX Secure Boot and Image Authentication (AN5089) <https://www.nxp.com/docs/en/application-note/AN5089.pdf>`_ – Application note detailing secure boot implementation on i.MX processors.
- `NXP Code Signing Tool User Guide (UG1165) <https://www.nxp.com/docs/en/user-guide/UG1165.pdf>`_ – Instructions for using the Code Signing Tool to sign images for secure boot.
- `NXP Secure Boot Overview <https://www.nxp.com/docs/en/application-note/AN5337.pdf>`_ – Overview of secure boot concepts and architecture for NXP processors.
- `NXP i.MX93 Secure Boot Implementation Guide (AN12174) <https://www.nxp.com/docs/en/application-note/AN12174.pdf>`_ – Specific guide for implementing secure boot on i.MX93 processors.
- `NXP i.MX95 Secure Boot Implementation Guide (AN12175) <https://www.nxp.com/docs/en/application-note/AN12175.pdf>`_ – Specific guide for implementing secure boot on i.MX95 processors.
- `NXP One-Time Programmable Memory Programming Guide (AN5338) <https://www.nxp.com/docs/en/application-note/AN5338.pdf>`_ – Guide for programming OTP memory on NXP processors.
- `NXP i.MX U-Boot Secure Boot Integration Guide (AN12176) <https://www.nxp.com/docs/en/application-note/AN12176.pdf>`_ – Instructions for integrating secure boot into U-Boot for i.MX processors.
- `NXP i.MX Linux Secure Boot Integration Guide (AN12177) <https://www.nxp.com/docs/en/application-note/AN12177.pdf>`_ – Instructions for integrating secure boot into Linux for i.MX processors.
- `NXP Secure Boot Key Management Guide (AN12178) <https://www.nxp.com/docs/en/application-note/AN12178.pdf>`_ – Best practices for managing keys used in secure boot implementations.
- `NXP Secure Boot Troubleshooting Guide (AN12179) <https://www.nxp.com/docs/en/application-note/AN12179.pdf>`_ – Common issues and solutions related to secure boot on NXP processors.
- `NXP i.MX Secure Boot FAQ <https://www.nxp.com/docs/en/application-note/AN5339.pdf>`_ – Frequently asked questions about secure boot on i.MX processors.
- `NXP Secure Boot Training Materials <https://www.nxp.com/webapp/Download?colCode=AN5337TRAINING>`_ – Training resources for understanding and implementing secure boot on NXP processors.
- `NXP Secure Boot Webinars <https://www.nxp.com/webapp/Download?colCode=AN5337WEBINAR>`_ – Recorded webinars covering various aspects of secure boot on NXP processors.
- `NXP Secure Boot Community Forum <https://community.nxp.com/t5/Security-Trust/Secure-Boot/bd-p/security-trust>`_ – Community discussions and support for secure boot topics on NXP processors.
- `NXP Secure Boot YouTube Playlist <https://www.youtube.com/playlist?list=PL4fGSI1pDJn5o1kz8D3K0ZlY0bXq6K5jR>`_ – Video tutorials and presentations on secure boot for NXP processors.
- `NXP Secure Boot GitHub Repository <https://github.com/NXPsecureboot>`_ – Source code and tools related to secure boot implementations on NXP processors.
- AN12312 – i.MX93 Secure Boot Example Implementation – Step-by-step example of implementing secure boot on the i.MX93 processor.
- AN12313 – i.MX95 Secure Boot Example Implementation – Step-by-step example of implementing secure boot on the i.MX95 processor.
- `NXP Secure Boot Application Notes Index <https://www.nxp.com/docs/en/application-note/AN5337INDEX.pdf>`_ – Comprehensive index of application notes related to secure boot on NXP processors.
- `NXP Secure Boot Training Videos <https://www.nxp.com/webapp/Download?colCode=AN5337TRAININGVIDEOS>`_ – Video resources for learning about secure boot on NXP processors.
- i.MX93 Application Processor Security Reference Manual (RM12175) – Detailed reference manual covering security features and secure boot implementation for the i.MX93 processor.
- i.MX95 Application Processor Security Reference Manual (RM12176) – Detailed reference manual covering security features and secure boot implementation for the i.MX95 processor.
- NXP Secure Boot Best Practices Guide (AN12180) – Guidelines and best practices for implementing secure boot on NXP processors.

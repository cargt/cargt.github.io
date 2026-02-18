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

- Block Diagram - i.MX93 00363 OSM-L SOM on 00365 Carrier Board

.. figure:: /images/diagrams/Block-diagram-i.MX93-OSM-L-00365-Rev-B-20260210.png
   :align: center
   :alt: i.MX93 00363 OSM-L SOM on 00365 Carrier Board Block Diagram

   i.MX93 00363 OSM-L SOM on 00365 Carrier Board Block Diagram

- Block Diagram - STM32MP257 00395 OSM-L SOM on 00365 Carrier Board

.. figure:: /images/diagrams/Block-diagram-STM32MP2-00395-OSM-L-00365-Rev-D-20260213.png
   :align: center
   :alt: STM32MP257 00395 OSM-L SOM on 00365 Carrier Board Block Diagram

   STM32MP257 00395 OSM-L SOM on 00365 Carrier Board Block Diagram

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
   :alt: UUU commands example output

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

NXP - Enter UUU mode using U-Boot Environment Variable Method
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - To enter UUU mode without using the BOOT button, you can set the U-Boot environment variable ``bootcmd`` to boot into UUU mode on the next reboot.
      Use either ``fw_setenv`` or ``setenv`` to set the variable.

   .. code-block:: bash

      # Using fw_setenv (from Linux shell)
      fw_setenv bootcmd 'fastboot auto'
      fw_printenv bootcmd  # Verify the change
      reboot

      # Using setenv (from U-Boot console)
      setenv bootcmd 'fastboot auto'
      saveenv
      printenv bootcmd  # Verify the change
      reset


SWUpdate
========

Incremental update images compatible with SWUpdate can be found in the `Cargt Package Repository Images`_ or can be built in your Yocto build environment.
The output file has a ``.swu`` extension.

For reference, the bitbake recipe file used to create SWUpdate images may have a ``-swu.bb`` ending or be called ``swupdate-image.bb``.

Example Usage: ``bitbake <machine-name>-swu`` or ``bitbake swupdate-image``

For a target to be SWUpdate compatible, the flash image must be partitioned correctly. Typically it requires 2 identical partions for the compiled code in addition to any other customer data partitions.
This is sometimes referred to as a ping-pong or A/B partition scheme. This allows the system to boot from one partition while the other is being updated, providing a fallback in case of update failure.
The SWUpdate client will manage the switching between these partitions during the update process.

Checking the run partition
--------------------------

   .. code-block:: bash

      lsblk

Before update example output:

.. figure:: /images/screenshots/img-swu-lsblk-before-update.png
   :alt: lsblk output before SWUpdate

   Kernel and root file system are on mmcblk0p1

After update example output:

.. figure:: /images/screenshots/img-swu-lsblk-after-update.png
   :alt: lsblk output after SWUpdate

   Kernel and root file system are on mmcblk0p2


SWUpdate Methods
----------------

Web Server - Command Line Startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Only needed if the SWUpdate web server is not already running on the target device.

Start the SWUpdate web server to enable browser-based uploads at ``http://<target_ip>:8080/``:

   .. code-block:: bash

      swupdate -e web

Optionally specify a different port:

   .. code-block:: bash

      swupdate -e web -p 8081

Web Server - Drag and Drop
~~~~~~~~~~~~~~~~~~~~~~~~~~
On a connected host computer, open a web browser and navigate to the SWUpdate web server running on the target device.

   .. code-block:: bash

      http://<target_ip>:8080/

Follow the on-screen instructions to upload and install the update file.

.. image:: /images/screenshots/img-swu-web-pic1.png
   :alt: SWUpdate web interface drag and drop - picture 1

.. image:: /images/screenshots/img-swu-web-pic2.png
   :alt: SWUpdate web interface drag and drop - picture 2

.. image:: /images/screenshots/img-swu-web-pic3.png
   :alt: SWUpdate web interface drag and drop - picture 3

.. image:: /images/screenshots/img-swu-web-pic4.png
   :alt: SWUpdate web interface drag and drop - picture 4

.. image:: /images/screenshots/img-swu-web-pic5.png
   :alt: SWUpdate web interface drag and drop - picture 5


USB Drive or Local File Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Direct installation from a local file on the target device can be done using the SWUpdate command line interface.
This is useful if the update file has already been transferred to the target device using another method.

.. code-block:: bash

   swupdate -i <update_file>.swu

Add verbose output for detailed progress:

.. code-block:: bash

   swupdate -i <update_file>.swu -v

TFTP Server
~~~~~~~~~~~

Download and install an update file directly from a TFTP server running on your host computer.

**Setup:**

- **Host computer** (TFTP server): Start a TFTP server and place the ``.swu`` file in the TFTP directory
- **Target device** (TFTP client): Run the SWUpdate command to download and install from the host

**Command on target device:**

.. code-block:: bash

   swupdate -d "-t tftp://<host_ip>/<update_file>.swu"

Example with specific host IP and file:

.. code-block:: bash

   swupdate -d "-t tftp://192.168.1.100/my-system-update.swu"

The ``-d`` flag specifies the download option, and ``-t`` indicates a TFTP source.

.. note::

   Ensure the TFTP server on your host is accessible from the target device and the update file is in the TFTP server's root directory or specify the full path.

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

Listing Installed Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      apt list --installed

Using a Downloaded Package File
-------------------------------

Updating using a downloaded ``.deb`` package file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      dpkg -i /<path_to_downloaded_package>/<package_file>.deb

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

      echo "deb [trusted=yes] http://<your_server_ip>:<port_number>/ ./" >> /etc/apt/sources.list.d/my-custom-repo.list
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


Updating using a downloaded to target ``.deb`` package file
-----------------------------------------------------------

   .. code-block:: bash

      dpkg -i /<path_to_downloaded_package>/<package_file>.deb

Remote Access
=============

- Reverse SSH using Teleport
- Provisioning
- Connecting to a Remote Device
- Using SSH Tunnel for RDP

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

#. Enable SPDX generation in your ``local.conf`` file:

   .. code-block:: bash

      echo 'INHERIT += "create-spdx"' >> conf/local.conf

#. Build the image:

   .. code-block:: bash

      bitbake <image_name>

#. Find the generated SBOM in the deploy directory:

   ``<build_dir>/tmp/deploy/spdx/<machine>/recipe-<image>.spdx.json``

Yocto Tutorial
=================

Setup build machine
-------------------

The build machine needs to have:
- ``repo`` tool installed
- Required packages for Yocto development (e.g., git, tar, python3, etc.)

Download and Install the repo utility from Google
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- To use this manifest repo, the ``repo`` utility must be installed first:

.. code-block:: bash

   mkdir -p ~/bin
   curl https://storage.googleapis.com/git-repo-downloads/repo > ~/bin/repo
   chmod a+x ~/bin/repo
   PATH=${PATH}:~/bin

Install required packages for Yocto development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- On Ubuntu, you can install the required packages with:

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y gawk wget git diffstat unzip texinfo gcc build-essential chrpath socat cpio python3 python3-pip python3-pexpect xz-utils debianutils iputils-ping python3-git python3-jinja2 libegl1-mesa libsdl1.2-dev python3-subunit mesa-common-dev zstd liblz4-tool file locales


On other Linux distributions, the package names may differ.
Please refer to the Yocto Project documentation for the specific packages required for your distribution.

Set the locale in Ubuntu:

.. code-block:: bash

   sudo locale-gen en_US.UTF-8

Setup the Yocto environment
---------------------------

Initialize the repo and download the source code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Initialize the repo with the appropriate manifest for your target hardware:

`Cargt GitHub account <https://github.com/cargt>`_ has public repositories for Yocto layers, example applications, and board support packages.

Generic repo commands:

.. code-block:: bash

   repo init -u <manifest_url> -b <branch_name>
   repo sync

Cargt example for NXP i.MX:

.. code-block:: bash

   mkdir -p ~/yocto
   cd ~/yocto
   repo init -u https://github.com/cargt/imx_manifest -b scarthgap -m cargt-imx-6.6.36-2.1.0.xml
   repo sync

This will download the necessary Yocto layers and source code for building images for Cargt's i.MX91, i.MX93, and i.MX8M Plus hardware designs.

Initialize build environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- To see available scripts:

.. code-block:: bash

   ls
   # Output:
   # imx-cargt-setup.sh  imx-setup-release.sh  README  README-IMXBSP  setup-environment  sources

- To see available distributions and machines:

.. code-block:: bash

   ls -1 sources/meta-imx-cargt/conf/distro
   # Output:
   # cargt-imx-wayland.conf
   # cargt-imx-xwayland-ap.conf
   # cargt-imx-xwayland.conf
   # cargt-imx-xwayland-connman.conf

   ls -1 sources/meta-imx-cargt/conf/machine/
   # Output:
   # imx8mp-cargt-00377-00365.conf
   # imx93-cargt-00324-00326.conf
   # imx93-cargt-00359-00406.conf
   # imx93-cargt-00363-00365.conf
   # imx93-cargt-00363-osm-som.conf


- Setting up the build environment - for the first time:

.. code-block:: bash

   # Generic:
   DISTRO=<selected-distro> MACHINE=<selected-machine> source ./imx-cargt-setup.sh -b <build_dir>
   # Example:
   DISTRO=cargt-imx-xwayland MACHINE=imx93-cargt-00363-00365 source ./imx-cargt-setup.sh -b bld-xwayland

This will set up the environment variables for the build and navigate to the build directory.

- Subsequent builds can be enabled with:

.. code-block:: bash

   # Generic:
   source setup-environment <build_dir>
   # Example:
   source setup-environment bld-xwayland

This will use the previous distro and machine environment variables for the build and navigate to the build directory.

Bitbake the image
-----------------

Build images
~~~~~~~~~~~~

.. note::

   This assumes you have already set up the build environment as described above and are in the build directory.

- To find available images to build:

.. code-block:: bash

   bitbake-layers show-recipes | grep image
   # Output:
   # Highlighting just the cargt ones:
   # cargt-image-chrome:
   # cargt-image-chrome-swu:
   # cargt-image-core:
   # cargt-image-core-swu:
   # cargt-image-demo:
   # cargt-image-demo-swu:
   # cargt-image-dev:
   # cargt-image-dev-swu:

- To build an image:

.. code-block:: bash

   bitbake <image_name>
   # Example:
   bitbake cargt-image-demo
   bitbake cargt-image-demo-swu

This will build the specified image and its dependencies, resulting in a complete system image that can be flashed to the target hardware.
The output images will be located in the ``<build_dir>/tmp/deploy/images/<machine>/`` directory.

Build Packages
~~~~~~~~~~~~~~

- To build a specific package:

.. code-block:: bash

   bitbake <package_name>
   # Example:
   bitbake linux-imx

This will build the specified package and its dependencies, resulting in a ``.deb`` file that can be installed on the target device.
The output package will be located in the ``<build_dir>/tmp/deploy/deb/<machine>/`` directory.

Deploy to Target
----------------

- See the `Running Linux on a Cargt design`_ section for instructions on how to flash pre-compiled images to the target hardware using UUU or STM32Cube.
- See the `SWUpdate`_ section for instructions on how to use SWUpdate to install incremental update images on the target hardware.
- See the `Package Management on a Cargt design`_ section for instructions on how to use APT or dpkg to install packages on the target hardware.

Advanced Yocto Usage
--------------------

Build fails
~~~~~~~~~~~

- Try restarting the build
- Lockup or exit failure

   - This could be due to a build machine resource issue (e.g., out of memory) or a transient issue with the build process.

   - Try reducing the number of parallel build threads by setting ``BB_NUMBER_THREADS`` and ``PARALLEL_MAKE`` in your ``local.conf`` file to a lower value.

      Use the number of CPU cores (or less) on your build machine as a general guideline.
      The build is also a function of available RAM, so if you have 12 cores but only a small amount of RAM, you may want to limit to 10 threads to avoid out of memory issues.

      Trial and error may be needed to find the optimal number of threads for your specific build machine and configuration.
      Monitor the RAM usage during the build to see if it approaches or exceeds the available memory.

      For 12 cores, you could set ``<build_dir>/conf/local.conf`` with:

      .. code-block:: bash

         BB_NUMBER_THREADS = "10"
         PARALLEL_MAKE = "-j 10"

         echo 'BB_NUMBER_THREADS = "10"' >> conf/local.conf
         echo 'PARALLEL_MAKE = "-j 10"' >> conf/local.conf
.. _software-updates:

Software Updates
================

Cargt i.MX designs use SWUpdate. Cargt STM32MP2 00395 designs use RAUC A/B updates.

.. _Cargt Package Repository Images: https://yocto.cargt.com/images

.. _swupdate:

SWUpdate
--------

Incremental update images compatible with SWUpdate can be found in the `Cargt Package Repository Images`_ or can be built in your Yocto build environment.
The output file has a ``.swu`` extension.

For reference, the bitbake recipe file used to create SWUpdate images may have a ``-swu.bb`` ending or be called ``swupdate-image.bb``.

Example Usage: ``bitbake <machine-name>-swu`` or ``bitbake swupdate-image``

For a target to be SWUpdate compatible, the flash image must be partitioned correctly. Typically it requires 2 identical partions for the compiled code in addition to any other customer data partitions.
This is sometimes referred to as a ping-pong or A/B partition scheme. This allows the system to boot from one partition while the other is being updated, providing a fallback in case of update failure.
The SWUpdate client will manage the switching between these partitions during the update process.

Checking the run partition
~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      lsblk

Before update example output:

.. figure:: /_static/images/screenshots/img-swu-lsblk-before-update.png
   :alt: lsblk output before SWUpdate

   Kernel and root file system are on mmcblk0p1

After update example output:

.. figure:: /_static/images/screenshots/img-swu-lsblk-after-update.png
   :alt: lsblk output after SWUpdate

   Kernel and root file system are on mmcblk0p2

SWUpdate Methods
~~~~~~~~~~~~~~~~

Web Server - Command Line Startup
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only needed if the SWUpdate web server is not already running on the target device.

Start the SWUpdate web server to enable browser-based uploads at ``http://<target_ip>:8080/``:

   .. code-block:: bash

      swupdate -e web

Optionally specify a different port:

   .. code-block:: bash

      swupdate -e web -p 8081

Web Server - Drag and Drop
^^^^^^^^^^^^^^^^^^^^^^^^^^
On a connected host computer, open a web browser and navigate to the SWUpdate web server running on the target device.

   .. code-block:: bash

      http://<target_ip>:8080/

Follow the on-screen instructions to upload and install the update file.

.. image:: /_static/images/screenshots/img-swu-web-pic1.png
   :alt: SWUpdate web interface drag and drop - picture 1

.. image:: /_static/images/screenshots/img-swu-web-pic2.png
   :alt: SWUpdate web interface drag and drop - picture 2

.. image:: /_static/images/screenshots/img-swu-web-pic3.png
   :alt: SWUpdate web interface drag and drop - picture 3

.. image:: /_static/images/screenshots/img-swu-web-pic4.png
   :alt: SWUpdate web interface drag and drop - picture 4

.. image:: /_static/images/screenshots/img-swu-web-pic5.png
   :alt: SWUpdate web interface drag and drop - picture 5

USB Drive or Local File Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Direct installation from a local file on the target device can be done using the SWUpdate command line interface.
This is useful if the update file has already been transferred to the target device using another method.

.. code-block:: bash

   swupdate -i <update_file>.swu

Add verbose output for detailed progress:

.. code-block:: bash

   swupdate -i <update_file>.swu -v

TFTP Server
^^^^^^^^^^^

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

RAUC A/B Updates (STM32MP2)
---------------------------

STM32MP2 00395 designs use RAUC with a dual-bank (A/B) partition layout
instead of SWUpdate. Updates install to the inactive bank, and a bank that
fails to boot falls back to the previous one automatically. See
:doc:`rauc-ota-updates`.

.. toctree::
    :hidden:

    rauc-ota-updates

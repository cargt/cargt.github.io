.. _package-management:

Package Management on a Cargt design
====================================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX`

Cargt images use ``apt`` and ``dpkg`` with Debian (``.deb``) packages built
by Yocto. This page shows how to install packages from the Cargt package
repository, from your own Yocto build, and from a local directory.

The examples on this page are from an i.MX 91 00363 on the 00365 carrier,
running ``cargt-image-dev`` (wrynose).

Package Feeds
-------------

A Yocto build puts its packages in ``<build_dir>/tmp/deploy/deb``, in one
directory per package architecture:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 35 65

   * - Directory
     - Contents
   * - ``all``
     - Architecture-independent packages, such as scripts and data
   * - ``armv8a``, ``cortexa55``, ...
     - Packages built for the processor's CPU tuning: ``cortexa55`` on the
       i.MX 91 (images from October 29, 2026), ``armv8a`` on the i.MX 93
   * - ``cortexa55-mx91``, ``armv8a-mx93``, ...
     - Packages built for one i.MX processor family
   * - ``imx91_cargt_00363_00365``, ...
     - Packages built for one machine, such as the kernel, its modules and
       the device trees

Each directory is a separate ``apt`` source (a feed). Cargt images list the
feeds on ``yocto.cargt.com`` for their machine in ``/etc/apt/sources.list``.
For the i.MX 91 00363 on the 00365, images from October 29, 2026 list:

.. code-block:: text

   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/all ./
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/cortexa55 ./
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/cortexa55-mx91 ./
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/imx91_cargt_00363_00365 ./

Earlier i.MX 91 images list ``armv8a`` and ``armv8a-mx91`` in place of the
two ``cortexa55`` feeds. Those feeds are no longer updated, so do not mix
them with the new ones; ``cat /etc/apt/sources.list`` shows which your board
uses.

The feeds are not signed, so each line has ``[trusted=yes]``.

Installing Packages
-------------------

Refresh the package lists, then search for and install packages:

.. code-block:: bash

   apt-get update
   apt-cache search <name>
   apt-get install <package>

Other useful commands:

.. code-block:: bash

   apt list --installed                 # installed packages
   apt-cache policy <package>           # installed and available versions, and their feeds
   dpkg -L <package>                    # files a package installed
   dpkg -i <file>.deb                   # install a downloaded package file

``apt-get update`` prints ``Ign`` lines for ``InRelease`` and
``Release.gpg``, because the feeds are not signed. They are harmless.

.. warning::

   Install packages from the same build as the image on the board. Kernel
   module packages only work with the kernel they were built for (see
   :ref:`application-development`), and other packages can depend on
   libraries at the versions of their own build. On an image you built
   yourself, the Cargt feeds hold packages from a different build, and
   ``apt list --upgradable`` lists some of them at the same version
   numbers. Do not run ``apt-get upgrade`` against them; point the board
   at your own build's feeds instead (see below).

.. _package-management-kernel-modules:

Kernel Modules
--------------

Each kernel module is a package in the machine's feed. The package name
and its ``Depends`` include the kernel's release string (the output of
``uname -r``), and ``Provides`` gives a name without it. In the wrynose
feed for ``imx93-cargt-00363-00428`` on November 10, 2026:

.. code-block:: text

   Package: kernel-module-can-dev-6.18.20-2.0.0-g7296eff56fe2-dirty
   Version: 6.18.20+git0+b096ce610e-r0.5
   Provides: kernel-module-can-dev
   Depends: kernel-6.18.20-2.0.0-g7296eff56fe2-dirty

The package puts the module in ``/usr/lib/modules/<release>/``. The kernel
looks for modules only in the directory named after its own release, and
refuses a module built for a different kernel.

``cargt-image-dev`` already has every module package from its build. To add
a driver to a board running an image with fewer modules, such as your own
product image, install the package for the running kernel by its full name,
then load the module:

.. code-block:: bash

   apt-get update
   apt-get install kernel-module-can-dev-$(uname -r)
   modprobe can-dev

If ``apt-get`` reports ``Unable to locate package``, the feed holds modules
for a different kernel than the one on the board. This is common on
wrynose, where release strings end in ``-dirty`` and change from one
nightly build to the next: in November 2026, i.MX 93 00363 boards on the
00428 carrier, flashed from three earlier wrynose nightlies, ran three
different kernels, and none of them matched the feed. You can then:

- update the board to the current image and check again (see
  :doc:`software-updates`); files in an image directory can come from
  different nightlies, so the image and the feed may still differ (see
  :doc:`releases`)
- build the module with your own image, in your own build (see
  :doc:`yocto-development`)

If the driver is not in the feed under any release, it is not enabled in
the kernel configuration; see :doc:`yocto-development` to enable it.

.. warning::

   Do not install a module by its name without the release, such as
   ``apt-get install kernel-module-can-dev``, on a board whose kernel does
   not match the feed. ``apt`` then also installs the feed's kernel: the
   module depends on ``kernel-<release>``, which recommends
   ``kernel-image-<release>``, and ``apt`` installs recommended packages
   by default. That package's install script points ``/boot/Image`` at the
   new kernel, which U-Boot loads at the next boot, without the new
   kernel's other modules. If this has happened, point ``/boot/Image``
   back at the running kernel before you reboot:

   .. code-block:: bash

      ln -sf Image-$(uname -r) /boot/Image

Hosting Packages from Your Own Build
------------------------------------

Any Yocto build directory can serve its packages to boards on your network.

1. Generate the package indexes (the ``Packages`` files) after building:

   .. code-block:: bash

      bitbake package-index

   Run it again after each build, so the indexes list the new packages.

2. Serve ``tmp/deploy/deb`` with Python's built-in web server. Choose any
   free port above 1024; SWUpdate's web interface uses 8080:

   .. code-block:: bash

      cd <build_dir>/tmp/deploy/deb
      python3 -m http.server 5678

   The server runs until you press Ctrl+C. Opening
   ``http://<host-ip>:5678/`` in a browser lists the feeds and their
   packages.

3. On the board, add one line per feed in a file under
   ``/etc/apt/sources.list.d/``, using your machine's directory names:

   .. code-block:: text

      # /etc/apt/sources.list.d/my-feed.list
      deb [trusted=yes] http://<host-ip>:5678/all ./
      deb [trusted=yes] http://<host-ip>:5678/cortexa55 ./
      deb [trusted=yes] http://<host-ip>:5678/cortexa55-mx91 ./
      deb [trusted=yes] http://<host-ip>:5678/imx91_cargt_00363_00365 ./

4. Update and install. ``apt-cache policy`` shows which feed a package comes
   from. Here ``hello-cmake``, the example program from
   :ref:`application-development`, exists only in the build on the host.
   That build was made before the October 29 tuning change, so its feeds are
   named ``armv8a`` and ``armv8a-mx91``:

   .. code-block:: text

      root@imx91-cargt-00363-00365:~# apt-get update
      Ign:1 http://<host-ip>:5678/all ./ InRelease
      ...
      Get:13 http://<host-ip>:5678/all ./ Packages [51.8 kB]
      Get:14 http://<host-ip>:5678/armv8a ./ Packages [1726 kB]
      Get:15 http://<host-ip>:5678/armv8a-mx91 ./ Packages [39.6 kB]
      Get:16 http://<host-ip>:5678/imx91_cargt_00363_00365 ./ Packages [202 kB]
      ...
      Reading package lists...
      root@imx91-cargt-00363-00365:~# apt-cache policy hello-cmake
      hello-cmake:
        Installed: (none)
        Candidate: 1.0-r0
        Version table:
           1.0-r0 500
              500 http://<host-ip>:5678/armv8a ./ Packages
      root@imx91-cargt-00363-00365:~# apt-get install -y hello-cmake
      ...
      Get:1 http://<host-ip>:5678/armv8a ./ hello-cmake 1.0-r0 [2752 B]
      Fetched 2752 B in 0s (38.6 kB/s)
      Selecting previously unselected package hello-cmake.
      ...
      Setting up hello-cmake (1.0-r0) ...
      root@imx91-cargt-00363-00365:~# hello-cmake
      Hello from a CMake project, built with devtool

Setting the Feeds in Your Image
-------------------------------

The feed lines in ``/etc/apt/sources.list`` come from these variables, which
Cargt sets for every i.MX machine in
``meta-imx-cargt/conf/distro/include/cargt-imx-base.inc``. To make your own
images use your own server, set them in your distro configuration or
``local.conf``. For the i.MX 91 00363 on the 00365 they expand to:

.. code-block:: text

   PACKAGE_FEED_URIS = "https://yocto.cargt.com/linux-imx/wrynose"
   PACKAGE_FEED_BASE_PATHS = ""
   PACKAGE_FEED_ARCHS = "all cortexa55 cortexa55-mx91 imx91_cargt_00363_00365"

The i.MX 93 00363 and i.MX 95 00414 machines also add their SOM's own
directory, such as ``imx93_cargt_00363_osm_som``.

Each combination of a URI, a base path and an architecture becomes one
``deb`` line. See ``PACKAGE_FEED_ARCHS`` in the `Yocto Project reference
manual <https://docs.yoctoproject.org/ref-manual/variables.html#term-PACKAGE_FEED_ARCHS>`__.

Using a Local Directory
-----------------------

``apt`` can also install from a directory on the board, such as a USB drive,
without a network. Put the ``.deb`` files in a directory, and create the
index on a Linux host with ``dpkg-scanpackages`` (in Debian and Ubuntu's
``dpkg-dev`` package):

.. code-block:: text

   $ ls
   hello-cmake_1.0-r0_arm64.deb
   $ dpkg-scanpackages -m . > Packages
   dpkg-scanpackages: info: Wrote 1 entries to output Packages file.

Copy the directory to the board (here to ``/data/apt``) and add it as a
source with ``file:``:

.. code-block:: text

   root@imx91-cargt-00363-00365:~# echo "deb [trusted=yes] file:/data/apt ./" > /etc/apt/sources.list.d/local.list
   root@imx91-cargt-00363-00365:~# apt-get update
   ...
   root@imx91-cargt-00363-00365:~# apt-cache policy hello-cmake
   hello-cmake:
     Installed: (none)
     Candidate: 1.0-r0
     Version table:
        1.0-r0 500
           500 file:/data/apt ./ Packages
   root@imx91-cargt-00363-00365:~# apt-get install -y hello-cmake

For a local source, ``apt-get update`` also reports ``Err`` lines for
``Translation-en`` files, followed by ``Ign``; they are harmless.
``apt-ftparchive packages . > Packages`` creates the same index.

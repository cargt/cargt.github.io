.. _package-management:

Package Management on a Cargt design
====================================

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
   * - ``armv8a``
     - Packages for any 64-bit Arm processor
   * - ``armv8a-mx91``, ``armv8a-mx93``, ...
     - Packages built for one i.MX processor family
   * - ``imx91_cargt_00363_00365``, ...
     - Packages built for one machine, such as the kernel, its modules and
       the device trees

Each directory is a separate ``apt`` source (a feed). Cargt images list the
feeds on ``yocto.cargt.com`` for their machine in ``/etc/apt/sources.list``:

.. code-block:: text

   root@imx91-cargt-00363-00365:~# cat /etc/apt/sources.list
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/all ./
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/armv8a ./
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/armv8a-mx91 ./
   deb [trusted=yes] https://yocto.cargt.com/linux-imx/wrynose/imx91_cargt_00363_00365 ./

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
      deb [trusted=yes] http://<host-ip>:5678/armv8a ./
      deb [trusted=yes] http://<host-ip>:5678/armv8a-mx91 ./
      deb [trusted=yes] http://<host-ip>:5678/imx91_cargt_00363_00365 ./

4. Update and install. ``apt-cache policy`` shows which feed a package comes
   from. Here ``hello-cmake``, the example program from
   :ref:`application-development`, exists only in the build on the host:

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

The feed lines in ``/etc/apt/sources.list`` come from these variables in
the machine configuration. To make your own images use your own server, set
them in your machine configuration, distro configuration or ``local.conf``.
The Cargt values for the i.MX 91 00363 on the 00365:

.. code-block:: text

   PACKAGE_FEED_URIS = "https://yocto.cargt.com/linux-imx/wrynose"
   PACKAGE_FEED_BASE_PATHS = ""
   PACKAGE_FEED_ARCHS = "all  armv8a  armv8a-mx91  imx91_cargt_00363_00365"

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

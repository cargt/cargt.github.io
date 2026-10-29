.. _application-development:

Developing Applications and Kernel Modules
==========================================

This page shows how to build your own programs and kernel modules for a
Cargt board: directly on the board, which is quick for experiments, and as
recipes in your own Yocto layer, which is how they belong in a product
image. It starts from a build set up as described in :doc:`yocto`.

The examples are from ``cargt-image-dev`` (wrynose) on an i.MX 93 00363 on
the 00428 carrier, and a ``cargt-imx-xwayland`` build for
``imx93-cargt-00363-00428``.

.. contents:: On this page
   :local:
   :depth: 1

Building on the Board
---------------------

``cargt-image-dev`` includes GCC, ``make``, CMake and the kernel source, so
small programs and kernel modules can be built on the board itself. Use
this to try something out; for a product, write a recipe (see below) so the
result is built the same way every time.

A CMake Program
~~~~~~~~~~~~~~~

A minimal CMake project, in ``~/hello-cmake``:

.. code-block:: cmake

   # CMakeLists.txt
   cmake_minimum_required(VERSION 3.16)
   project(hello-cmake VERSION 1.0 LANGUAGES CXX)

   add_executable(hello-cmake src/main.cpp)
   install(TARGETS hello-cmake RUNTIME DESTINATION bin)

.. code-block:: cpp

   // src/main.cpp
   #include <iostream>

   int main()
   {
       std::cout << "Hello from a CMake project" << std::endl;
       return 0;
   }

.. code-block:: text

   root@imx93-cargt-00363-00428:~/hello-cmake# cmake -S . -B build
   ...
   -- Build files have been written to: /root/hello-cmake/build
   root@imx93-cargt-00363-00428:~/hello-cmake# cmake --build build
   [ 50%] Building CXX object CMakeFiles/hello-cmake.dir/src/main.cpp.o
   [100%] Linking CXX executable hello-cmake
   [100%] Built target hello-cmake
   root@imx93-cargt-00363-00428:~/hello-cmake# ./build/hello-cmake
   Hello from a CMake project

A Kernel Module
~~~~~~~~~~~~~~~

The kernel source is in ``/usr/src/kernel`` (also reachable as
``/lib/modules/$(uname -r)/build``). Its build tools have to be compiled
once before the first module; this took 45 seconds on the i.MX 93:

.. code-block:: bash

   cd /usr/src/kernel
   make scripts prepare -j2

A minimal module, ``hello.c``:

.. code-block:: c

   #include <linux/module.h>
   #include <linux/init.h>

   static int __init hello_init(void)
   {
   	pr_info("hello: loaded\n");
   	return 0;
   }

   static void __exit hello_exit(void)
   {
   	pr_info("hello: unloaded\n");
   }

   module_init(hello_init);
   module_exit(hello_exit);
   MODULE_LICENSE("GPL");
   MODULE_DESCRIPTION("Example out-of-tree module");

and its ``Makefile``. The same Makefile works on the board and in a Yocto
recipe, which sets ``KERNEL_SRC`` and calls ``modules_install``:

.. code-block:: make

   obj-m := hello.o

   KERNEL_SRC ?= /lib/modules/$(shell uname -r)/build

   all:
   	$(MAKE) -C $(KERNEL_SRC) M=$(CURDIR) modules

   modules_install:
   	$(MAKE) -C $(KERNEL_SRC) M=$(CURDIR) modules_install

   clean:
   	$(MAKE) -C $(KERNEL_SRC) M=$(CURDIR) clean

Build it, load it and unload it:

.. code-block:: text

   root@imx93-cargt-00363-00428:~/hello# make
   make -C /lib/modules/6.18.20-2.0.0-g3dc3167d032d-dirty/build M=/root/hello modules
   ...
   warning: the compiler differs from the one used to build the kernel
     The kernel was built by: aarch64-poky-linux-gcc (GCC) 15.2.0
     You are using:           gcc (GCC) 15.2.0
     CC [M]  hello.o
     MODPOST Module.symvers
     CC [M]  hello.mod.o
     CC [M]  .module-common.o
     LD [M]  hello.ko
   ...
   root@imx93-cargt-00363-00428:~/hello# insmod hello.ko
   root@imx93-cargt-00363-00428:~/hello# rmmod hello
   root@imx93-cargt-00363-00428:~/hello# dmesg | tail -2
   [ 6524.084225] hello: loaded
   [ 6524.121863] hello: unloaded

The compiler warning is expected on the board: the kernel was built with
the Yocto cross-compiler, which is the same GCC version under another name.

Creating Your Own Layer
-----------------------

Keep your recipes in your own layer rather than in ``meta-imx-cargt``, so
that Cargt BSP updates do not conflict with your changes. From the build
directory:

.. code-block:: text

   $ bitbake-layers create-layer ../sources/meta-mylayer
   Add your new layer with 'bitbake-layers add-layer ../sources/meta-mylayer'
   $ bitbake-layers add-layer ../sources/meta-mylayer
   $ bitbake-layers show-layers | grep mylayer
   meta-mylayer          /scratch/yocto-cargt-wrynose/sources/meta-mylayer                       6

The new layer has a ``conf/layer.conf`` with ``LAYERSERIES_COMPAT`` set to
``wrynose`` and an example recipe you can delete.

A Recipe for a CMake Project
----------------------------

Put the project's files next to the recipe, in
``recipes-example/hello-cmake/files/``, and write the recipe
``recipes-example/hello-cmake/hello-cmake_1.0.bb``:

.. code-block:: text

   meta-mylayer/recipes-example/hello-cmake/
   ├── files
   │   ├── CMakeLists.txt
   │   └── src
   │       └── main.cpp
   └── hello-cmake_1.0.bb

.. code-block:: text

   SUMMARY = "Example CMake application"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

   SRC_URI = " \
       file://CMakeLists.txt \
       file://src/main.cpp \
   "
   S = "${UNPACKDIR}"

   inherit cmake

``inherit cmake`` runs CMake with the cross-compiler and installs the result
into the package. For a project in a Git repository, use a ``git://`` URL in
``SRC_URI`` with ``SRCREV`` instead of local files.

Build it:

.. code-block:: text

   $ bitbake hello-cmake
   ...
   NOTE: Tasks Summary: Attempted 1416 tasks of which 1302 didn't need to be rerun and all succeeded.
   $ ls tmp/deploy/deb/armv8a/ | grep hello-cmake
   hello-cmake-dbg_1.0-r0_arm64.deb
   hello-cmake-dev_1.0-r0_arm64.deb
   hello-cmake-src_1.0-r0_arm64.deb
   hello-cmake_1.0-r0_arm64.deb

The first build in a new build directory took a little over two minutes,
because the build dependencies came from the shared state cache. To try the
package on a board, copy it over and install it:

.. code-block:: text

   $ scp tmp/deploy/deb/armv8a/hello-cmake_1.0-r0_arm64.deb root@<board-ip>:/tmp/
   root@imx93-cargt-00363-00428:~# dpkg -i /tmp/hello-cmake_1.0-r0_arm64.deb
   Selecting previously unselected package hello-cmake.
   ...
   Setting up hello-cmake (1.0-r0) ...
   root@imx93-cargt-00363-00428:~# hello-cmake
   Hello from a CMake project

To include it in your image, see `Adding Your Packages to an Image`_.

Changing a Recipe's Source with devtool
---------------------------------------

``devtool modify`` unpacks a recipe's source into a Git repository in the
build's ``workspace`` directory, so you can edit it, build it and try it on
a board, and then turn your changes into patches in your layer. The same
steps work for any recipe, for example to patch a package from
``meta-imx-cargt`` or OpenEmbedded.

.. code-block:: text

   $ devtool modify hello-cmake
   ...
   INFO: Source tree extracted to /scratch/yocto-cargt-wrynose/build-docs/workspace/sources/hello-cmake
   INFO: Recipe hello-cmake now set up to build from /scratch/yocto-cargt-wrynose/build-docs/workspace/sources/hello-cmake

Edit the source in ``workspace/sources/hello-cmake``, then commit the
change. The commit message becomes the patch header, so include an
``Upstream-Status`` line (see below):

.. code-block:: bash

   cd workspace/sources/hello-cmake
   sed -i "s/Hello from a CMake project/Hello from a CMake project, built with devtool/" src/main.cpp
   git commit -a -m "Say how the program was built" -m "Upstream-Status: Inappropriate [example]"
   cd -

Build it and copy it straight to a board over SSH, without making a
package:

.. code-block:: text

   $ devtool build hello-cmake
   ...
   NOTE: Tasks Summary: Attempted 899 tasks of which 887 didn't need to be rerun and all succeeded.
   $ devtool deploy-target -s hello-cmake root@<board-ip>
   ./
   ./usr/
   ./usr/bin/
   ./usr/bin/hello-cmake
   INFO: Successfully deployed /scratch/yocto-cargt-wrynose/build-docs/tmp/work/armv8a-poky-linux/hello-cmake/1.0/image
   root@imx93-cargt-00363-00428:~# hello-cmake
   Hello from a CMake project, built with devtool

``devtool undeploy-target hello-cmake root@<board-ip>`` removes the files
again and puts back any files the deployment replaced. When the change is
ready, write it back to your layer:

.. code-block:: text

   $ devtool finish hello-cmake ../sources/meta-mylayer
   INFO: Adding new patch 0001-Say-how-the-program-was-built.patch
   INFO: Updating recipe hello-cmake_1.0.bb
   INFO: Cleaning sysroot for recipe hello-cmake...
   INFO: Preserving source tree in /scratch/yocto-cargt-wrynose/build-docs/workspace/attic/sources/hello-cmake.20261028152937

``devtool finish`` saves the commit as a patch next to the recipe, adds it
to ``SRC_URI`` and removes the recipe from the workspace:

.. code-block:: text

   SRC_URI = "file://CMakeLists.txt \
              file://src/main.cpp \
              file://0001-Say-how-the-program-was-built.patch \
              "

.. code-block:: text

   From 10a47f004aff448fc2fb51f6a7f4e2734d8ff4d7 Mon Sep 17 00:00:00 2001
   From: Example <example@example.com>
   Date: Wed, 28 Oct 2026 15:28:13 -0500
   Subject: [PATCH] Say how the program was built

   Upstream-Status: Inappropriate [example]
   ---
    src/main.cpp | 2 +-
    1 file changed, 1 insertion(+), 1 deletion(-)

For a recipe from another layer, give ``devtool finish`` your layer in the
same way. It then leaves the other layer alone and adds a ``.bbappend`` and
the patch to yours. For example, after changing a line in ``evtest`` (from
``meta-oe``) with ``devtool modify evtest`` and committing it:

.. code-block:: text

   $ devtool finish evtest ../sources/meta-mylayer
   INFO: Cleaning sysroot for recipe evtest...
   INFO: Preserving source tree in /scratch/yocto-cargt-wrynose/build-docs/workspace/attic/sources/evtest.20261028160355
   $ find ../sources/meta-mylayer -path "*evtest*" -type f
   ../sources/meta-mylayer/recipes-test/evtest/evtest/0001-Mark-the-version-line-as-patched.patch
   ../sources/meta-mylayer/recipes-test/evtest/evtest_%.bbappend
   $ cat ../sources/meta-mylayer/recipes-test/evtest/evtest_%.bbappend
   FILESEXTRAPATHS:prepend := "${THISDIR}/${PN}:"

   SRC_URI += "file://0001-Mark-the-version-line-as-patched.patch"

After ``bitbake evtest`` and installing the new package, the board runs the
patched program:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# evtest /dev/input/event0
   (patched) Input driver version is 1.0.1
   ...

.. warning::

   Patches without an ``Upstream-Status`` line fail the build on wrynose:

   .. code-block:: text

      ERROR: hello-cmake-1.0-r0 do_patch: QA Issue: Missing Upstream-Status in patch
      .../hello-cmake/files/0001-Say-how-the-program-was-built.patch
      Please add according to https://docs.yoctoproject.org/contributor-guide/recipe-style-guide.html#patch-upstream-status . [patch-status]

   ``devtool modify`` fails with the same error while the patch is in the
   recipe, so the tag cannot be added afterwards with ``devtool``. Put it in
   the commit message before ``devtool finish``, or add it to the patch file
   by hand. Use ``Inappropriate [reason]`` for changes that only make sense
   in your product, ``Pending`` if you plan to send the change upstream; see
   the Yocto Project recipe style guide for the other values.

A Recipe for a Kernel Module
----------------------------

A kernel module recipe uses ``inherit module`` with the same ``hello.c``
and ``Makefile`` as above, in ``recipes-kernel/hello-module/files/``:

.. code-block:: text

   SUMMARY = "Example out-of-tree kernel module"
   LICENSE = "GPL-2.0-only"
   LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/GPL-2.0-only;md5=801f80980d171dd6425610833a22dbe6"

   SRC_URI = " \
       file://Makefile \
       file://hello.c \
   "
   S = "${UNPACKDIR}"

   inherit module

   RPROVIDES:${PN} += "kernel-module-hello"

``bitbake hello-module`` builds the module against the kernel of the same
build. It took about ten minutes in a new build directory. The module
itself is packaged as
``kernel-module-hello-<kernel version>``:

.. code-block:: text

   $ ls tmp/deploy/deb/imx93_cargt_00363_00428/ | grep hello
   hello-module-dbg_1.0-r0_arm64.deb
   hello-module-dev_1.0-r0_arm64.deb
   hello-module-src_1.0-r0_arm64.deb
   hello-module_1.0-r0_arm64.deb
   kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty_1.0-r0_arm64.deb

A module package only works with the exact kernel it was built for, and the
package depends on it. On a board running a kernel from a different build,
``dpkg`` refuses it:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# uname -r
   6.18.20-2.0.0-g3dc3167d032d-dirty
   root@imx93-cargt-00363-00428:~# dpkg -i /tmp/kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty_1.0-r0_arm64.deb
   ...
     Package kernel-6.18.20-2.0.0-gff0565225cd7-dirty is not installed.

   dpkg: error processing package kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty (--install):
    dependency problems - leaving unconfigured

``dpkg`` leaves the package unpacked but not configured, and removing it
fails too: after deleting the module, the package's removal script runs
``depmod`` for the missing kernel's module directory. Create that directory
with a file in it, so that ``dpkg`` does not delete it, purge the package,
then delete the directory:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# K=6.18.20-2.0.0-gff0565225cd7-dirty
   root@imx93-cargt-00363-00428:~# mkdir -p /lib/modules/$K
   root@imx93-cargt-00363-00428:~# touch /lib/modules/$K/keep
   root@imx93-cargt-00363-00428:~# dpkg -P kernel-module-hello-$K
   (Reading database ... 47703 files and directories currently installed.)
   Removing kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty (1.0-r0) ...
   depmod: WARNING: could not open modules.order at /lib/modules/6.18.20-2.0.0-gff0565225cd7-dirty: No such file or directory
   ...
   Purging configuration files for kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty (1.0-r0) ...
   ...
   dpkg: warning: while removing kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty, directory '/usr/lib/modules/6.18.20-2.0.0-gff0565225cd7-dirty' not empty so not removed
   root@imx93-cargt-00363-00428:~# rm -r /lib/modules/$K

So install kernel modules as part of an image built from the same build
directory, as below, rather than as separate packages.

Adding Your Packages to an Image
--------------------------------

Add the packages to ``IMAGE_INSTALL``, and list modules that should load at
boot in ``KERNEL_MODULE_AUTOLOAD``. For a quick test, put this in
``conf/local.conf``; for a product, put it in your own image recipe or a
``.bbappend`` in your layer:

.. code-block:: text

   IMAGE_INSTALL:append = " hello-cmake hello-module"
   KERNEL_MODULE_AUTOLOAD += "hello"

Then build the image as usual. With the kernel, the rest of the image and
the two recipes already in the shared state cache, ``bitbake
cargt-image-dev`` took about 18 minutes. The image manifest lists the
packages:

.. code-block:: text

   $ grep hello tmp/deploy/images/imx93-cargt-00363-00428/cargt-image-dev-imx93-cargt-00363-00428.rootfs.manifest
   hello-cmake armv8a 1.0-r0
   hello-module imx93-cargt-00363-00428 1.0-r0
   kernel-module-hello-6.18.20-2.0.0-gff0565225cd7-dirty imx93-cargt-00363-00428 1.0-r0

The root file system contains the program, the module built for the
image's own kernel, and ``/usr/lib/modules-load.d/hello.conf`` (containing
``hello``), which ``systemd-modules-load`` reads at boot:

.. code-block:: text

   ./usr/bin/hello-cmake
   ./usr/lib/modules/6.18.20-2.0.0-gff0565225cd7-dirty/updates/hello.ko
   ./usr/lib/modules-load.d/hello.conf

Install the image with UUU or a software update (see :doc:`getting-started`
and :doc:`software-updates`).

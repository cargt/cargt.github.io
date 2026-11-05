.. _yocto-development-tasks:

Everyday Yocto Development
==========================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX`

This page collects the Yocto tasks that come up once you have your own
layer: running single bitbake tasks, finding out where a variable is set,
changing the kernel configuration and device tree, building your own
product image, and upgrading a recipe. It continues from
:doc:`application-development`, which creates the layer ``meta-mylayer``
and the ``hello-cmake`` recipe used here.

The examples are from a ``cargt-imx-xwayland`` build for
``imx93-cargt-00363-00428`` (wrynose). Commands run in the build
directory, after ``source setup-environment <build_dir>`` (see
:doc:`yocto`).

.. contents:: On this page
   :local:
   :depth: 1

Running Single Tasks
--------------------

A recipe is built by a chain of tasks: fetch, unpack, patch, configure,
compile, install, package and so on. ``bitbake -c <task> <recipe>`` runs
one of them, together with the tasks it depends on. ``listtasks`` shows
them all:

.. code-block:: text

   $ bitbake -c listtasks hello-cmake
   ...
   do_build                              Default task for a recipe - depends on all other normal tasks required to 'build' a recipe
   do_clean                              Removes all output files for a target
   do_cleanall                           Removes all output files, shared state cache, and downloaded source files for a target
   do_cleansstate                        Removes all output files and shared state cache for a target
   do_compile                            Compiles the source in the compilation directory
   do_configure                          Configures the source by enabling and disabling any build-time and configuration options for the software being built
   do_devshell                           Starts a shell with the environment set up for development/debugging
   do_fetch                              Fetches the source code
   do_install                            Copies files from the compilation directory to a holding area
   ...
   do_patch                              Locates patch files and applies them to the source code
   ...
   do_unpack                             Unpacks the source code into a working directory

``bitbake -c compile -f <recipe>`` forces a task to run again even if
bitbake thinks it is up to date. ``bitbake -c devshell <recipe>`` opens a
shell in the recipe's source directory with the cross-compiler set up,
which is useful to try a command by hand.

clean, cleansstate and cleanall
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Bitbake keeps the result of every task in the **shared state cache**
(sstate), and restores it instead of running the task again when nothing
has changed. The three clean tasks remove different amounts:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 25 75

   * - Task
     - Removes
   * - ``clean``
     - The recipe's work directory and its output in the build directory.
       The next build restores it from sstate.
   * - ``cleansstate``
     - The same, and the recipe's sstate. The next build runs every task
       again.
   * - ``cleanall``
     - The same, and the downloaded source. The next build fetches it
       again.

After ``clean``, the next build restores everything from sstate and
nothing is compiled:

.. code-block:: text

   $ bitbake -c clean hello-cmake
   $ bitbake hello-cmake
   ...
   Sstate summary: Wanted 125 Local 125 Mirrors 0 Missed 0 Current 295 (100% match, 100% complete)
   ...
   NOTE: recipe hello-cmake-1.0-r0: task do_populate_sysroot_setscene: Succeeded

After ``cleansstate``, its tasks are missing from the cache, and it is
compiled again:

.. code-block:: text

   $ bitbake -c cleansstate hello-cmake
   $ bitbake hello-cmake
   ...
   Sstate summary: Wanted 125 Local 114 Mirrors 0 Missed 11 Current 295 (91% match, 97% complete)
   ...
   NOTE: recipe hello-cmake-1.0-r0: task do_compile: Started
   NOTE: recipe hello-cmake-1.0-r0: task do_compile: Succeeded

Use ``clean`` when a build directory is in a bad state, and
``cleansstate`` when you suspect the cached result itself. If several
build directories share one sstate directory, ``cleansstate`` removes the
recipe's cache for all of them.

Finding Out Where Things Come From
----------------------------------

``bitbake-getvar`` shows a variable's value for a recipe and every place
that sets or changes it:

.. code-block:: text

   $ bitbake-getvar -r hello-cmake WORKDIR
   #
   # $WORKDIR [2 operations]
   #   set .../openembedded-core/meta/conf/bitbake.conf:416
   #     "${BASE_WORKDIR}/${MULTIMACH_TARGET_SYS}/${PN}/${PV}"
   ...
   WORKDIR=".../tmp/work/armv8a-poky-linux/hello-cmake/1.0"

``--value`` prints just the value, for scripts. ``bitbake -e <recipe>``
prints the whole environment of a recipe; the source, build and install
directories are often what you need:

.. code-block:: text

   $ bitbake -e hello-cmake | grep -E '^(WORKDIR|S|B|D)='
   B=".../tmp/work/armv8a-poky-linux/hello-cmake/1.0/build"
   D=".../tmp/work/armv8a-poky-linux/hello-cmake/1.0/image"
   S=".../tmp/work/armv8a-poky-linux/hello-cmake/1.0/sources"
   WORKDIR=".../tmp/work/armv8a-poky-linux/hello-cmake/1.0"

``bitbake-layers`` answers questions about layers. ``show-appends`` lists
the ``.bbappend`` files that change a recipe, which shows whether yours is
picked up:

.. code-block:: text

   $ bitbake-layers show-appends linux-imx
   ...
   linux-imx_6.18.bb:
     .../meta-mylayer/recipes-kernel/linux-pwm/linux-imx_%.bbappend
     .../meta-mylayer/recipes-kernel/linux/linux-imx_%.bbappend
     ...

``bitbake-layers show-recipes <recipe>`` lists every layer that provides a
recipe and its version, and ``show-layers`` lists the layers with their
priorities.

Changing the Kernel Configuration
---------------------------------

``menuconfig`` opens the kernel's configuration menu in a terminal:

.. code-block:: bash

   bitbake -c menuconfig linux-imx

This example enables the driver for CH340 and CH341 USB serial adapters.
Press ``/``, search for ``USB_SERIAL_CH341``, press ``1`` to go to it, and
``m`` to build it as a module:

.. code-block:: text

   → Search (USB_SERIAL_CH341) → USB Serial Converter support
   ...
     <M>   USB Winchiphead CH341 Single Port Serial Driver

Exit and save. The change is only in the build directory and is lost at
the next ``clean``. ``diffconfig`` turns it into a configuration
**fragment**:

.. code-block:: text

   $ bitbake -c diffconfig linux-imx
   ...
   Config fragment has been dumped into:
    .../tmp/work/imx93_cargt_00363_00428-poky-linux/linux-imx/6.18.20+git/fragment.cfg
   $ cat .../linux-imx/6.18.20+git/fragment.cfg
   CONFIG_RUSTC_VERSION=107500
   CONFIG_RUSTC_LLVM_VERSION=170006
   CONFIG_USB_SERIAL_CH341=m

Keep only the options you changed: the ``CONFIG_RUSTC_*`` lines come from
the Rust compiler on the build PC, not from your change. Save the fragment
in your layer, for example as
``recipes-kernel/linux/files/usb-serial-ch341.cfg``:

.. code-block:: text

   CONFIG_USB_SERIAL_CH341=m

and add it to the kernel recipe in
``recipes-kernel/linux/linux-imx_%.bbappend``:

.. code-block:: bash

   FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

   SRC_URI += "file://usb-serial-ch341.cfg"

Run ``bitbake linux-imx``. The kernel's configuration is built again with
the fragment, and the driver is packaged as
``kernel-module-ch341``; add that package to your image, or install it
with ``apt`` from your package repository (see :doc:`package-management`).
:doc:`linux-basics` has another fragment, for the PCA9685 PWM driver.

.. note::

   A kernel module only loads into the kernel it was built for. After a
   kernel configuration change, update the whole image, not just the
   module.

Changing the Device Tree
------------------------

A device tree for your own carrier or display goes in your layer as a
``.dts`` file that includes the Cargt one and changes what differs. A
``linux-imx_%.bbappend`` copies it into the kernel source and adds it to
``KERNEL_DEVICETREE``. :doc:`npu` walks through a complete example, which
adds the i.MX 93 NPU to the ``imx93-cargt-00363-00428`` device trees.

After ``bitbake linux-imx``, the new ``.dtb`` is in
``tmp/deploy/images/<machine>``. To check that it contains your change,
decompile it with ``dtc`` (``sudo apt install device-tree-compiler`` on
Ubuntu):

.. code-block:: text

   $ dtc -q -I dtb -O dts tmp/deploy/images/imx93-cargt-00363-00428/imx93-cargt-00363-00428-glt0557201280is1-npu.dtb | grep -A5 ethosu
   ...
   	ethosu {
   		compatible = "arm,ethosu";
   		fsl,cm33-proc = <0x54>;
   		memory-region = <0x55>;
   		power-domains = <0x56>;
   	};

Building Your Own Image
-----------------------

The Cargt images are a good starting point for a product image. Keep the
new image recipe in your layer, for example
``recipes-images/images/my-product-image.bb``. This one starts from
``cargt-image-core``, adds your programs, and removes the development
features, such as the empty root password and the compilers and debuggers:

.. code-block:: bash

   SUMMARY = "Example product image: cargt-image-core with our programs and without the development features"

   require recipes-cargt/images/cargt-image-core.bb

   # The Cargt image sets its own name; use this recipe's name for the output files
   export IMAGE_BASENAME = "${PN}"

   IMAGE_INSTALL:append = " hello-cmake evtest"

   IMAGE_FEATURES:remove = " \
       allow-empty-password \
       allow-root-login \
       empty-root-password \
       serial-autologin-root \
       tools-sdk \
       tools-debug \
       tools-profile \
   "

.. important::

   The Cargt image recipes set ``IMAGE_BASENAME``. Without the line
   that sets it to ``${PN}``, your image's files are named
   ``cargt-image-core-...`` and overwrite the real ``cargt-image-core``
   in the deploy directory.

Build it with ``bitbake my-product-image``. The files are in
``tmp/deploy/images/<machine>`` as ``my-product-image-<machine>.rootfs.*``,
and the ``.manifest`` lists every package in the image:

.. code-block:: text

   $ M=tmp/deploy/images/imx93-cargt-00363-00428/my-product-image-imx93-cargt-00363-00428.rootfs.manifest
   $ grep -E '^(hello-cmake|evtest|gdb|gcc) ' $M
   evtest armv8a 1.36-r0
   hello-cmake armv8a 1.0-r0
   $ wc -l < $M
   1450

It has 1450 packages, against 2091 in ``cargt-image-dev``, and its root
file system archive is half the size. With the empty root password and
root login removed, nobody can log in until you add a way: for example an
SSH key for root, or your own user, from your layer. Flash it like any
other image; see :doc:`getting-started`.

Upgrading a Recipe
------------------

``devtool latest-version`` compares a recipe with the newest upstream
release, and ``devtool check-upgrade-status <recipe> ...`` does it for
several at once:

.. code-block:: text

   $ devtool latest-version socat
   ...
   INFO: Current version: 1.8.1.1
   INFO: Latest version: 1.8.1.3

``devtool upgrade`` fetches the new version into the workspace, re-applies
the recipe's patches, and writes a recipe for it:

.. code-block:: text

   $ devtool upgrade socat -V 1.8.1.3
   ...
   INFO: Fetching http://www.dest-unreach.org/socat/download/socat-1.8.1.3.tar.bz2...
   INFO: Upgraded source extracted to .../workspace/sources/socat
   INFO: New recipe is .../workspace/recipes/socat/socat_1.8.1.3.bb
   $ devtool build socat

When it builds and works, ``devtool finish`` moves the new recipe and its
patches into your layer. The original recipe stays in its own layer, and
bitbake now uses the newer version from yours:

.. code-block:: text

   $ devtool finish socat ../sources/meta-mylayer
   INFO: Updating patch 0001-fix-compile-procan.c-failed.patch
   INFO: Moving recipe file to .../meta-mylayer/recipes-connectivity/socat
   INFO: Preserving source tree in .../workspace/attic/sources/socat.20261103151309
   $ bitbake-layers show-recipes socat
   ...
   socat:
     meta-mylayer         1.8.1.3
     meta                 1.8.1.1

.. note::

   ``devtool finish`` refuses with ``Source tree is not clean`` if the
   build changed files in the source tree. Recipes that use autotools
   regenerate ``configure`` and similar files there. Discard those changes
   before finishing:

   .. code-block:: bash

      cd workspace/sources/socat
      git status --short          # shows the regenerated files
      git restore configure install-sh
      git clean -fd

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

Choosing How to Change the Kernel
---------------------------------

Start with the lightest route that does the job; each route further down
the table takes more work. A kernel you build yourself has its own release
string, so modules from the Cargt package feeds do not load into it.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 40 30

   * - You need
     - Lightest route
     - See
   * - A driver that the Cargt kernel builds as a module, but your image
       leaves out
     - Install ``kernel-module-<name>`` from the feed, or add it to
       ``IMAGE_INSTALL``
     - :ref:`package-management-kernel-modules`
   * - Your own driver
     - An out-of-tree module recipe (``inherit module``), built against the
       kernel of your build. ``devtool add`` creates one from a source
       directory with a kernel module ``Makefile``.
     - :doc:`application-development`, "A Recipe for a Kernel Module"
   * - Different wiring or peripherals on your carrier
     - A device tree change
     - `Changing the Device Tree`_
   * - A driver that is not enabled, a built-in option, or a kernel patch
     - A configuration fragment or patch, and a full kernel rebuild
     - `Changing the Kernel Configuration`_

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

.. _yocto-kernel-outside-bitbake:

Building the Kernel and U-Boot Outside BitBake
----------------------------------------------

While you work on a driver or a device tree, building the kernel with
``make`` is quicker than a full ``bitbake linux-imx`` each time. Use
BitBake for anything you ship: it applies the Cargt patches and
configuration fragments the same way every time, and it builds the
packages and update files.

The examples are for an i.MX 93 00363 on the 00365
(``imx93-cargt-00363-00365``, wrynose). The STM32MP2 steps are the same
with ``linux-stm32mp`` and ``u-boot-stm32mp``.

The Kernel
~~~~~~~~~~

1. **Get the Cargt kernel source.** ``devtool modify`` unpacks it into
   ``workspace/sources/linux-imx`` in your build directory, as a Git
   repository with each Cargt patch as a commit:

   .. code-block:: bash

      devtool modify linux-imx

   While the recipe is in the devtool workspace, ``bitbake linux-imx`` and
   image builds use this source too, so your changes go into the next
   image. ``devtool finish`` turns your commits into patches in your layer
   when you are done (see `Upgrading a Recipe`_).

2. **Use the cross-compiler from your Yocto build.** It is the one
   BitBake builds the kernel with. From the build directory:

   .. code-block:: bash

      export PATH=$PWD/tmp/work/imx93_cargt_00363_00365-poky-linux/linux-imx/6.18.20+git/recipe-sysroot-native/usr/bin/aarch64-poky-linux:$PATH

   On a PC without the Yocto build, an SDK built with ``bitbake
   cargt-image-dev -c populate_sdk`` has the same compiler.

3. **Start from the Cargt configuration.** The ``.config`` from your last
   ``bitbake linux-imx`` already has the Cargt fragments in it. Build into
   a separate output directory, so the source tree stays clean:

   .. code-block:: bash

      mkdir -p ~/kernel-out
      cp tmp/work/imx93_cargt_00363_00365-poky-linux/linux-imx/6.18.20+git/build/.config ~/kernel-out/
      cd workspace/sources/linux-imx
      make O=~/kernel-out ARCH=arm64 CROSS_COMPILE=aarch64-poky-linux- olddefconfig
      make O=~/kernel-out ARCH=arm64 CROSS_COMPILE=aarch64-poky-linux- -j$(nproc) Image dtbs modules

   The first build, with all the modules, took about 11 minutes on a
   16-core PC. After a change, ``make`` builds only what changed. Leave
   out ``modules`` when you only change built-in code or a device tree.

   The kernel is ``~/kernel-out/arch/arm64/boot/Image``, and the Cargt
   device trees are in ``~/kernel-out/arch/arm64/boot/dts/freescale``.

4. **Try it on a board.** The kernel and the device trees are files in
   ``/boot`` on the root file system, so a test kernel can be copied
   over the published one. Keep a copy of the original first:

   .. code-block:: bash

      ssh root@<board-ip> cp /boot/Image /boot/Image.orig
      scp ~/kernel-out/arch/arm64/boot/Image root@<board-ip>:/boot/
      scp ~/kernel-out/arch/arm64/boot/dts/freescale/imx93-cargt-00363-00365.dtb root@<board-ip>:/boot/

   Your kernel has its own release string (``uname -r``), so it does not
   load the modules in the image. If you need modules, install them into
   a directory with ``make O=~/kernel-out ARCH=arm64
   INSTALL_MOD_PATH=~/kernel-mods modules_install`` and copy
   ``~/kernel-mods/lib/modules/<release>`` to ``/lib/modules`` on the
   board.

   If the new kernel doesn't boot, stop at the U-Boot prompt (see
   :doc:`u-boot`) and boot the original once, without saving anything:

   .. code-block:: text

      setenv image boot/Image.orig
      boot

   The next software update replaces all of these files.

U-Boot
~~~~~~

There is no separate Cargt U-Boot repository. The i.MX U-Boot is NXP's
``u-boot-imx``, plus the Cargt patches, board defconfigs and device trees
in meta-imx-cargt, under ``recipes-bsp/u-boot/``:

- ``u-boot-imx/*.patch``: board code, DDR timing and the Cargt EEPROM
  support.
- ``u-boot-imx/files/configs/``: one defconfig per machine, named after
  it, for example ``imx91-cargt-00363-00365_defconfig``.
- ``u-boot-imx/files/dts/``: the board device trees.

Use this source, not an NXP or third-party U-Boot tree. The DDR settings
for Cargt SOMs are in the Cargt patches, so U-Boot without them doesn't
train the DDR and the board doesn't boot.

``devtool modify u-boot-imx`` gives you the source with the patches as
commits. The recipe copies the defconfigs and device trees into the tree
when it configures it, so run ``bitbake u-boot-imx`` once before you look
for them there.

To check that your changes compile, you can run ``make`` in that tree with
the cross-compiler from the kernel steps above:

.. code-block:: bash

   cd workspace/sources/u-boot-imx
   make O=~/uboot-out CROSS_COMPILE=aarch64-poky-linux- imx91-cargt-00363-00365_defconfig
   make O=~/uboot-out CROSS_COMPILE=aarch64-poky-linux- -j$(nproc)

This builds U-Boot's host tools as well, so the PC needs the usual U-Boot
build packages, including ``uuid-dev``, ``libgnutls28-dev``,
``libssl-dev``, ``bison`` and ``flex`` on Ubuntu. The ``u-boot.bin`` it
makes doesn't boot on its own, as the next paragraph explains.

On i.MX, U-Boot alone does not boot. ``imx-mkimage`` packs it into
``imx-boot`` with the SPL, the DDR training firmware and Arm Trusted
Firmware, plus the EdgeLock Enclave firmware on the i.MX 9 SoCs and the
OEI and System Manager on the i.MX 95 (see :doc:`secure-boot`). Let BitBake do the packing, and use ``devtool`` for
the source:

.. code-block:: bash

   devtool modify u-boot-imx
   # edit workspace/sources/u-boot-imx
   bitbake imx-boot

The new boot image is ``tmp/deploy/images/<machine>/imx-boot.tagged``.
Run it from RAM over USB without writing anything, with ``uuu
imx-boot``, or write only the boot loader with ``uuu -b emmc
imx-boot.tagged``; see "Other UUU options" in :doc:`getting-started`.
On the i.MX 95, use the ``uuu`` script there instead.

On STM32MP2, U-Boot is packed into the FIP with TF-A and OP-TEE; see
"How STM32MP2 Boards Boot" in :doc:`u-boot`. Use ``devtool modify u-boot-stm32mp`` and
rebuild the FIP with BitBake in the same way.

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

Sizing a Production Image
~~~~~~~~~~~~~~~~~~~~~~~~~

``cargt-image-dev`` is built for development, not for size. Measured on
November 8, 2026, the published i.MX ``cargt-image-dev`` images install
1.4 to 1.5 GB on scarthgap and 1.6 to 2.5 GB on wrynose, and the wrynose-rt
``cargt-image-rt`` images 2.2 to 2.8 GB.

A few packages account for much of that. In ``cargt-image-dev`` for
``imx93-cargt-00363-00428`` on scarthgap, on the same date:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 15 45

   * - Package
     - Installed
     - What it is
   * - ``teleport``
     - 358 MB
     - Teleport remote access, a single package
   * - ``packagegroup-core-sdk``
     - 169 MB
     - Compilers and build tools for building on the board
   * - ``packagegroup-imx-security``
     - 99 MB
     - NXP's i.MX security packages
   * - ``kernel-devsrc``
     - 91 MB
     - Kernel source for building modules on the board
   * - GStreamer
     - 80 MB
     - GStreamer and its plugins (``packagegroup-fsl-gstreamer1.0-full``)

``cargt-image-core``, which the example above starts from, has no
``teleport``, ``kernel-devsrc`` or GStreamer packagegroup, and the
example's ``IMAGE_FEATURES:remove`` drops ``tools-sdk``, which installs
``packagegroup-core-sdk``. It still has ``packagegroup-imx-security``;
leave it out if your product does not use it. Check your image's
``.manifest`` for the rest.

.. _yocto-own-bsp:

Using the Cargt Layer in Your Own Yocto Setup
---------------------------------------------

The simplest way to build a product is to keep the Cargt setup: add your
layer next to ``meta-imx-cargt`` and build with a Cargt ``DISTRO`` and
``MACHINE`` (see :doc:`yocto`). If you move the Cargt machines into your own
setup instead, for example with your own ``DISTRO`` or starting from NXP's
images, keep the pieces below. The board still boots without most of them,
but parts of these docs stop applying, and some faults only show up later.

These are from ``meta-imx-cargt`` (wrynose). For STM32MP2, the same
pieces are in ``meta-st-cargt`` and ``meta-cargt-stm32mp-addons``.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 70

   * - Keep
     - Why
   * - The Cargt ``u-boot-imx``, with its patches
     - The boot loader reads the SOM's EEPROM to pick the DDR timing for
       the SOM variant, and sets up the board's USB-C ports. NXP's
       U-Boot doesn't know the Cargt boards. See :doc:`identify-som`.
   * - The Cargt kernel device trees and kernel configuration fragments
       (``cargt_common_kernel_config_mods.cfg`` and the per-board
       ``cargt_<board>_kernel_config_mods.cfg``)
     - The device trees describe the carrier. The fragments turn on the
       drivers the boards need, such as the display panels and the RTCs.
   * - ``networkmanager`` in ``DISTRO_FEATURES`` and
       ``NETWORK_MANAGER = "networkmanager"``
     - The Cargt distros set both. The Cargt images only install
       NetworkManager and ``nmcli`` when the feature is on. Without it,
       :doc:`networking` and :doc:`wifi` don't apply: static addresses,
       Wi-Fi and access point mode are all set up through NetworkManager.
   * - ``cargt-network-config``
     - The ``systemd-networkd`` files that bring up CAN and leave the
       Ethernet ports to NetworkManager. See :doc:`networking`.
   * - ``nxp-wifi-systemd`` and ``nxp-bluetooth-systemd``
     - They load the Wi-Fi driver first and the Bluetooth driver only once
       Wi-Fi is up. If Bluetooth starts first, it loads its own firmware
       and every board reports the same placeholder address,
       ``88:88:88:88:88:88``. See :ref:`bluetooth-address`.
   * - ``u-boot-fw-utils`` and the machine's ``fw_env.config``
     - ``fw_printenv`` and ``fw_setenv``, used throughout these docs and by
       software updates, need the per-machine environment location. See
       :ref:`u-boot-environment`.
   * - ``swupdate``, ``swupdate-progress``, ``swupdate-www`` and
       ``grow-data-part``
     - The per-machine ``swupdate.cfg`` and the ``/data`` partition that
       updates are staged on. See :doc:`software-updates` and
       :doc:`storage`.
   * - ``board-version``
     - Writes ``/etc/hwrevision`` (the machine name and hardware revision)
       and ``/etc/sw-versions``. SWUpdate checks ``/etc/hwrevision``
       against the ``hardware-compatibility`` list in the update's
       ``sw-description`` and refuses an update that doesn't match.
   * - The package feed settings in ``cargt-imx-base.inc``
     - Each SoC gets its own package architecture, so machines with
       different ``DISTRO_FEATURES`` (the i.MX 91 and i.MX 93, for example)
       don't overwrite each other's packages in a shared feed. See
       :doc:`package-management`.

To see everything else a Cargt image installs, compare your image's
``.manifest`` with ``cargt-image-core``'s; see `Building Your Own Image`_.

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

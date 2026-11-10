.. _releases:

Releases and Downloads
======================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

Cargt publishes Yocto BSP releases for each SOM and carrier board
combination (one ``MACHINE`` each; see :doc:`identify-som`). This page lists
every release and every ``MACHINE`` with links to its pre-built images and
package feeds on `yocto.cargt.com <https://yocto.cargt.com>`__.

.. contents::
   :local:
   :depth: 1

Current Releases
----------------

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 14 16 14 30 26

   * - Release
     - Platforms
     - Kernel
     - Manifest (``repo init``)
     - Status
   * - wrynose
     - i.MX 8M Plus, i.MX 91, i.MX 93, i.MX 95
     - 6.18.20
     - `imx_manifest <https://github.com/cargt/imx_manifest/tree/wrynose>`__
       ``-b wrynose -m cargt-imx-6.18.20-2.0.0.xml``
     - :bdg-success:`New designs`
   * - wrynose-rt
     - i.MX 95
     - 6.18.20 with ``PREEMPT_RT``
     - Same as wrynose; see :doc:`real-time-linux`
     - :bdg-success:`New designs`
   * - scarthgap
     - i.MX 8M Plus, i.MX 91, i.MX 93
     - 6.6.36
     - `imx_manifest <https://github.com/cargt/imx_manifest/tree/scarthgap>`__
       ``-b scarthgap -m cargt-imx-6.6.36-2.1.0.xml``
     - :bdg-secondary:`Existing designs`
   * - scarthgap
     - STM32MP2
     - 6.6.78
     - `stm32mp_manifest <https://github.com/cargt/stm32mp_manifest/tree/scarthgap>`__
       ``-b scarthgap -m cargt-stm32mp2.xml``
     - Current STM32MP2 release

For i.MX designs, **wrynose** is recommended for new designs. **scarthgap**
remains available for i.MX designs already qualified on it. The i.MX 95 is
supported on wrynose only. scarthgap is the current release for the
STM32MP2.

Releases by MACHINE
-------------------

i.MX
~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 22 30 16 16 16

   * - SOM / Carrier
     - ``MACHINE``
     - wrynose
     - wrynose-rt
     - scarthgap
   * - :doc:`00377 i.MX 8M Plus <catalog/soms/00377-imx8mplus-osml-iw612>` /
       :doc:`00365 <catalog/carrier-boards/00365-osml-carrier>`
     - ``imx8mp-cargt-00377-00365``
     - `Images <https://yocto.cargt.com/images/wrynose/imx8mp-cargt-00377-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx8mp_cargt_00377_00365/>`__
     - —
     - `Images <https://yocto.cargt.com/images/scarthgap/imx8mp-cargt-00377-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx8mp_cargt_00377_00365/>`__
   * - :doc:`00363 i.MX 91 <catalog/soms/00363-91-imx91-osml-iw612>` /
       :doc:`00365 <catalog/carrier-boards/00365-osml-carrier>`
     - ``imx91-cargt-00363-00365``
     - `Images <https://yocto.cargt.com/images/wrynose/imx91-cargt-00363-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx91_cargt_00363_00365/>`__
     - —
     - `Images <https://yocto.cargt.com/images/scarthgap/imx91-cargt-00363-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx91_cargt_00363_00365/>`__
   * - :doc:`00363 i.MX 93 <catalog/soms/00363-93-imx93-osml-iw612>` /
       :doc:`00365 <catalog/carrier-boards/00365-osml-carrier>`
     - ``imx93-cargt-00363-00365``
     - `Images <https://yocto.cargt.com/images/wrynose/imx93-cargt-00363-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx93_cargt_00363_00365/>`__
     - —
     - `Images <https://yocto.cargt.com/images/scarthgap/imx93-cargt-00363-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx93_cargt_00363_00365/>`__
   * - :doc:`00363 i.MX 93 <catalog/soms/00363-93-imx93-osml-iw612>` /
       :doc:`00428 <catalog/carrier-boards/00428-osml-carrier>`
     - ``imx93-cargt-00363-00428``
     - `Images <https://yocto.cargt.com/images/wrynose/imx93-cargt-00363-00428/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx93_cargt_00363_00428/>`__
     - —
     - `Images <https://yocto.cargt.com/images/scarthgap/imx93-cargt-00363-00428/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx93_cargt_00363_00428/>`__
   * - :doc:`00324 i.MX 93 SODIMM <catalog/soms/00324-imx93-sodimm>` /
       :doc:`00326 <catalog/carrier-boards/00326-sodimm-carrier>`
     - ``imx93-cargt-00324-00326``
     - `Images <https://yocto.cargt.com/images/wrynose/imx93-cargt-00324-00326/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx93_cargt_00324_00326/>`__
     - —
     - `Images <https://yocto.cargt.com/images/scarthgap/imx93-cargt-00324-00326/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx93_cargt_00324_00326/>`__
   * - :doc:`00359 i.MX 93 LGA <catalog/soms/00359-lga-murata2el>` /
       :doc:`00406 <catalog/carrier-boards/00406-lga-carrier>`
     - ``imx93-cargt-00359-00406``
     - `Images <https://yocto.cargt.com/images/wrynose/imx93-cargt-00359-00406/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx93_cargt_00359_00406/>`__
     - —
     - `Images <https://yocto.cargt.com/images/scarthgap/imx93-cargt-00359-00406/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/scarthgap/imx93_cargt_00359_00406/>`__
   * - :doc:`00414 i.MX 95 <catalog/soms/00414-imx95-osml>` /
       :doc:`00365 <catalog/carrier-boards/00365-osml-carrier>`
     - ``imx95-cargt-00414-00365``
     - `Images <https://yocto.cargt.com/images/wrynose/imx95-cargt-00414-00365/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx95_cargt_00414_00365/>`__
     - `Images <https://yocto.cargt.com/images/wrynose-rt/imx95-cargt-00414-00365/>`__
     - —
   * - :doc:`00414 i.MX 95 <catalog/soms/00414-imx95-osml>` /
       :doc:`00428 <catalog/carrier-boards/00428-osml-carrier>`
     - ``imx95-cargt-00414-00428``
     - `Images <https://yocto.cargt.com/images/wrynose/imx95-cargt-00414-00428/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx95_cargt_00414_00428/>`__
     - `Images <https://yocto.cargt.com/images/wrynose-rt/imx95-cargt-00414-00428/>`__
     - —
   * - NXP FRDM i.MX 95 (see :doc:`index`)
     - ``imx95-15x15-lpddr4x-frdm``
     - `Images <https://yocto.cargt.com/images/wrynose/imx95-15x15-lpddr4x-frdm/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx95_15x15_lpddr4x_frdm/>`__
     - `Images <https://yocto.cargt.com/images/wrynose-rt/imx95-15x15-lpddr4x-frdm/>`__
     - —
   * - NXP FRDM i.MX 95 Pro (see :doc:`yocto`)
     - ``imx95-19x19-lpddr5-frdm-pro``
     - `Images <https://yocto.cargt.com/images/wrynose/imx95-19x19-lpddr5-frdm-pro/>`__ ·
       `Packages <https://yocto.cargt.com/linux-imx/wrynose/imx95_19x19_lpddr5_frdm_pro/>`__
     - —
     - —

STM32MP2
~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 36 34

   * - SOM / Carrier
     - ``MACHINE``
     - scarthgap
   * - :doc:`00395-02 STM32MP257F <catalog/soms/00395-stm32mp257f-osml-iw610>` /
       :doc:`00365 <catalog/carrier-boards/00365-osml-carrier>`
     - ``stm32mp25-cargt-00395-02-00365``
     - `Images <https://yocto.cargt.com/images/scarthgap/stm32mp25-cargt-00395-02-00365/>`__ ·
       `Packages <https://yocto.cargt.com/openstlinux/scarthgap/stm32mp25_cargt_00395_02_00365/>`__
   * - :doc:`00395-01 STM32MP257F <catalog/soms/00395-stm32mp257f-osml-iw610>` /
       :doc:`00365 <catalog/carrier-boards/00365-osml-carrier>`
     - ``stm32mp25-cargt-00395-01-00365``
     - `Images <https://yocto.cargt.com/images/scarthgap/stm32mp25-cargt-00395-01-00365/>`__ ·
       `Packages <https://yocto.cargt.com/openstlinux/scarthgap/stm32mp25_cargt_00395_01_00365/>`__
   * - :doc:`00395 STM32MP257F <catalog/soms/00395-stm32mp257f-osml-iw610>` /
       00365 revision 3
     - ``stm32mp25-cargt-00395-00365v3``
     - `Images <https://yocto.cargt.com/images/scarthgap/stm32mp25-cargt-00395-00365v3/>`__ ·
       `Packages <https://yocto.cargt.com/openstlinux/scarthgap/stm32mp25_cargt_00395_00365v3/>`__

What Is in an Image Directory
-----------------------------

Each directory under `yocto.cargt.com/images <https://yocto.cargt.com/images>`__
holds the files for one ``MACHINE``:

- **i.MX:** the bootloader (``imx-boot.tagged``; ``imx-boot-tagged`` on
  scarthgap), the full disk image
  (``.wic.zst``) and its block map (``.wic.bmap``) for flashing with ``uuu``,
  and the SWUpdate file for field updates. See :doc:`getting-started` and
  :doc:`software-updates`.
- **STM32MP2:** the STM32CubeProgrammer flash layouts and binaries for
  eMMC, the ``.wic`` image for an SD card, and the RAUC bundle for field
  updates. See :doc:`getting-started` and :doc:`rauc-ota-updates`.

Both also hold these files, which describe the build:

- ``BUILD-INFO.txt``: the build's project, cycle and date, the
  ``repo init`` command for its manifest, the commit of each Cargt layer
  (``meta-imx-cargt`` on i.MX; ``meta-st-cargt`` and
  ``meta-cargt-stm32mp-addons`` on STM32MP2), and fingerprints of the other
  layer revisions (``source-fp``) and of the build configuration
  (``config-fp``). Only the Cargt layers are pinned to a commit. The
  manifest is given as a branch, so ``repo init`` with it fetches the
  other layers as they are today, not as they were for this build.
- ``<image>-<machine>.rootfs.manifest``: every package in the root file
  system, one per line, with its architecture and version.
- The SPDX software bill of materials for the root file system:
  ``<image>-<machine>.rootfs.spdx.json`` on wrynose and wrynose-rt,
  ``<image>-<machine>.rootfs.spdx.tar.zst`` on scarthgap (i.MX and
  STM32MP2).

.. warning::

   ``CRT.key``, ``CRT.crt`` and ``CRT.esl`` in most i.MX directories are the
   key pair and certificate that NXP's U-Boot source ships for UEFI capsule
   updates. They are sample keys, and the private key is public: use them
   for development only, and never to sign anything you ship.

Builds Are Nightly
~~~~~~~~~~~~~~~~~~

The image directories and the package feeds are updated by nightly builds,
and they keep only the latest build: each nightly replaces the files it
rebuilt, and nothing older is kept. A file is replaced only when a nightly
publishes it again, so the files in one directory can come from different
nightlies. The dates in the directory listing show when each file was
last replaced, and ``BUILD-INFO.txt`` describes the latest nightly.

Save every file you ship or test with, together with that directory's
``BUILD-INFO.txt``, ``.manifest`` and SBOM, because the same file names
will hold a different build tomorrow.

The package feeds hold the same release's packages for installing software
on a running board; see :doc:`package-management`. A board flashed from an
older nightly can differ from the feed, and kernel modules in particular
need a matching kernel; see :ref:`package-management-kernel-modules`.

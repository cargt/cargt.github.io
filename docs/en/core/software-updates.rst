.. _software-updates:

Software Updates
================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

Cargt i.MX designs use SWUpdate. Cargt STM32MP2 00395 designs use RAUC A/B updates.

.. _Cargt Package Repository Images: https://yocto.cargt.com/images

.. _swupdate:

SWUpdate
--------

How It Works
~~~~~~~~~~~~

Cargt i.MX images use the A/B root partition layout described in
:doc:`storage`: two identical root partitions and a ``data`` partition. The
board runs from one root partition while an update is written to the other.

A ``.swu`` file is a CPIO archive with four parts:

- ``sw-description``, which names the machine the update is for, lists
  its contents and gives the SHA-256 checksum of each file
- the root file system as ``<image>-<machine>.rootfs.tar.zst``
- ``update.sh``, a post-install script
- ``update-machine.sh``, a step for one machine that ``update.sh`` runs; on
  most machines it does nothing

SWUpdate checks that the ``.swu`` matches the board's machine name and
hardware revision, then writes the root file system archive to
``/data/swupdate/update.tar.zst``. ``update.sh`` then:

1. Reads the running root partition from ``root=`` in ``/proc/cmdline``.
2. Formats the other root partition (``1`` becomes ``2``, ``2`` becomes
   ``1``) as ext4.
3. Extracts the archive into it.
4. Runs ``update-machine.sh``.
5. Sets ``mmcpart`` to the new partition and starts a trial boot of it
   (see :ref:`swupdate-rollback`), in one write to the U-Boot environment.

On the i.MX 93 00363 on the 00428 carrier, ``update-machine.sh`` moves
``fdtfile`` from the device tree without a display to the 5.5" display's
device tree, if the board was still using the former.

The new root file system runs after the next reboot. The script logs each
step to ``/data/swupdate/log.txt``. If any step fails, the update is
reported as failed and the U-Boot environment is not changed.

.. _swupdate-rollback:

Trial Boot and Automatic Rollback
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A new root file system runs on trial until it has booted properly. If it
doesn't get there, the board goes back to the previous root partition by
itself, without a console.

- **U-Boot counts the trial boots.** ``update.sh`` sets
  ``upgrade_available=1``, ``bootcount=0`` and ``bootlimit=3``, and points
  ``bootcmd`` at a short script, ``cargt_ab_bootcmd``. On each boot with
  ``upgrade_available=1`` the script adds 1 to ``bootcount``. Once
  ``bootcount`` passes ``bootlimit``, it switches ``mmcpart`` back to the
  previous partition (``cargt_ab_good``) and boots that. If the new
  partition has no kernel or device tree, it switches back at once. The
  variable names are the ones U-Boot's own boot counter uses.
- **Linux marks a good boot.** ``cargt-ab-commit.service`` runs after
  ``multi-user.target``. If ``swupdate.service`` is active, it sets
  ``upgrade_available=0`` and ``bootcount=0``. From then on, the new
  partition is the one the board keeps.
- **A trial boot that doesn't finish is restarted.**
  ``cargt-ab-deadline.timer`` reboots a trial boot that isn't marked good
  10 minutes after boot, so a hung boot counts as a failed one. A kernel
  panic reboots after 10 s, and the watchdog (``RuntimeWatchdogSec=30s``)
  resets a board whose kernel or systemd stops. Each of these counts as a
  failed trial boot.

With ``bootlimit=3``, a new root file system that never boots properly
falls back on the fourth boot. Outside a trial, U-Boot never writes its
environment.

The script lives in the U-Boot environment, so it works with the U-Boot
already on a board: SWUpdate updates only the root file system. A root
file system without ``cargt-ab-boot`` (an image built before it was added)
is switched to outright, as before, because nothing in it would mark the
trial boot good.

To check the state, run ``cargt-ab-boot status``. It prints the partition
that booted, ``mmcpart``, ``upgrade_available``, ``bootcount`` against
``bootlimit``, the fallback partition (``cargt_ab_good``) and the last
result:

.. code-block:: bash

   /usr/libexec/cargt-ab-boot status

The last result, ``cargt_ab_status``, records the last result: ``trial-<partition>``,
``committed-<partition>`` or ``rolled-back-from-<partition>``.

To add your own checks before a trial boot is marked good, put executables
in ``/etc/cargt-ab-boot/commit.d/``. A check that exits non-zero leaves the
trial uncommitted. Units that must be active are listed in
``CARGT_AB_REQUIRED_UNITS`` in ``/etc/default/cargt-ab-boot``. To change
the 10-minute deadline, add a drop-in for ``cargt-ab-deadline.timer`` with
a new ``OnBootSec=``.

.. note::

   ``update.sh`` refuses to install while the running partition is still
   on trial (``upgrade_available=1``). Otherwise it would overwrite the
   partition the board falls back to. Wait until the boot is marked good.

Two limits remain:

- **The environment has one copy.** A power cut while it is being written
  (at the end of an update, once per trial boot, and when the boot is
  marked good) can corrupt it. U-Boot then starts from its built-in
  defaults, which boot partition 1 with no trial. Outside an update the
  environment is not written.
- **U-Boot doesn't start the watchdog.** A hang after U-Boot and before
  systemd starts (a kernel that stops without a panic) waits for a power
  cycle. The power cycle still counts as a failed trial boot.

Three more limits apply to the published i.MX updates and to the ``-swu``
recipes they come from:

- **Updates are not signed.** The ``.swu`` files have no
  ``sw-description.sig``, and ``public-key-file`` is commented out in the
  ``swupdate.cfg`` that Cargt images install. The checksums in
  ``sw-description`` catch a damaged file, but a board installs any
  ``.swu`` made for its machine, whoever built it. For a product, sign your
  updates and make SWUpdate check them; see `Update images from verified
  source <https://sbabic.github.io/swupdate/signed_images.html>`__ in the
  SWUpdate documentation.
- **The bootloader is not updated.** A ``.swu`` writes only the root file
  system, which holds the kernel and device trees in ``/boot``.
  ``imx-boot`` (U-Boot and the firmware it is packed with) stays as it was
  flashed; to change it, flash the board again (see :doc:`getting-started`).
- **The hardware revision is 1.0 on every board.** ``sw-description`` lists
  ``hardware-compatibility`` ``"1.0"``, and ``/etc/hwrevision`` is
  ``<machine> 1.0`` on every machine. The check keeps an update off the
  wrong machine, but it does not tell board revisions of one machine apart.
  To do that, set your own revision in both from your layer.

Getting an Update File
~~~~~~~~~~~~~~~~~~~~~~

Pre-built ``.swu`` files are in the `Cargt Package Repository Images`_, next to
the disk images. Each Cargt image has a matching ``-swu`` recipe:

.. code-block:: bash

   bitbake cargt-image-dev-swu

The output is
``tmp/deploy/images/<machine>/cargt-image-dev-swu-<machine>.rootfs.swu``.
The same applies to ``cargt-image-core-swu``, ``cargt-image-chrome-swu``,
``cargt-image-demo-swu``, ``cargt-image-stress-test-swu`` and, in the
real-time build, ``cargt-image-rt-swu``.

To customize an update, copy the ``-swu`` recipe and its per-machine
``sw-description`` and ``update.sh`` files from
``meta-imx-cargt/recipes-support/swupdate`` into your own layer.

An Update, Step by Step
~~~~~~~~~~~~~~~~~~~~~~~

This example is from an i.MX 93 00363 on the 00428 carrier, installing the
published ``cargt-image-dev`` update from a file in ``/data``.

Before the update, the board runs from partition 1:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /proc/cmdline
   console=ttyLP0,115200 earlycon root=/dev/mmcblk0p1 rootwait rw
   root@imx93-cargt-00363-00428:~# fw_printenv mmcpart
   mmcpart=1

Install the update. The end of the output:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# swupdate -v -i /data/cargt-image-dev-swu-imx93-cargt-00363-00428.rootfs.swu
   ...
   [TRACE] : SWUPDATE running :  [check_hw_compatibility] : Hardware compatibility verified
   ...
   [TRACE] : SWUPDATE running :  [install_raw_file] : Installing file cargt-image-dev-imx93-cargt-00363-00428.rootfs.tar.zst on /data/swupdate/update.tar.zst
   ...
   [INFO ] : SWUPDATE running :  Installation in progress
   [TRACE] : SWUPDATE running :  [__run_cmd] : /tmp/scripts/update.sh   command returned 0
   [INFO ] : SWUPDATE successful ! SWUPDATE successful !

``update.sh`` logged each step:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /data/swupdate/log.txt
   ******Update started*********
   get_current_root_device=/dev/mmcblk0p1
   get_current_part=1
   get_update_part=2
   get_update_device=/dev/mmcblk0p2
   format_update_device=/dev/mmcblk0p2
   tar --zstd -xf /data/swupdate/update.tar.zst -C /data/swupdate/mnt
   ******Update complete*********
   root@imx93-cargt-00363-00428:~# fw_printenv mmcpart
   mmcpart=2

After a reboot, the board runs from partition 2, and partition 1 is mounted
under ``/run/media``:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /proc/cmdline
   console=ttyLP0,115200 earlycon root=/dev/mmcblk0p2 rootwait rw
   root@imx93-cargt-00363-00428:~# lsblk | grep mmcblk0p
   |-mmcblk0p1  179:1    0    6G  0 part /run/media/mmcblk0p1
   |-mmcblk0p2  179:2    0    6G  0 part /
   `-mmcblk0p3  179:3    0    2G  0 part /data

To go back to the previous root file system by hand, select it and reboot.
Clearing ``upgrade_available`` too ends a trial that is still running:

.. code-block:: bash

   fw_setenv upgrade_available 0
   fw_setenv mmcpart 1
   reboot

Things to know after an update:

- **SSH host keys change.** The board's SSH host keys are part of the root
  file system, so each root partition has its own. SSH clients warn that
  the host key has changed after an update (and after going back). To
  keep the same keys, store them in ``/data`` from your own layer.
- **The update archive stays in /data.** ``update.sh`` leaves the root file
  system archive in ``/data/swupdate/update.tar.zst`` (about 440 MB for
  ``cargt-image-dev``). Delete it once the new root file system works:

  .. code-block:: bash

     rm -rf /data/swupdate

SWUpdate Methods
~~~~~~~~~~~~~~~~

Web Server
^^^^^^^^^^

Cargt images include the SWUpdate web interface (``swupdate-www``). On a
connected host computer, open ``http://<target_ip>:8080/`` in a web browser,
and drag the ``.swu`` file onto the page. When the update succeeds, the board
reboots into the new root file system by itself: ``swupdate-progress``,
which Cargt images run as a service (``swupdate-progress -r -w``), reboots
it.

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

The ``swupdate`` service starts the web server at boot. To run it by hand,
for example on a different port, stop the service first:

.. code-block:: bash

   systemctl stop swupdate.socket swupdate.service
   swupdate -w "-r /www -p 8081"

USB Drive, microSD or Local File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install a ``.swu`` file that is already on the board, for example on a USB
drive or microSD card (mounted under ``/run/media``) or copied with ``scp``.
This also works before networking is set up:

.. code-block:: bash

   swupdate -v -i /run/media/<device>/cargt-image-dev-swu-<machine>.rootfs.swu
   reboot

To install updates automatically when a USB drive is inserted, add the
``swupdate-usb`` package to your image. It installs every ``.swu`` file in
the root directory of the drive.

Downloading from a Server or hawkBit
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cargt images build SWUpdate without its downloader (``-d``) and without
suricatta, its hawkBit client. To add them, put a configuration fragment
in a ``swupdate`` bbappend in your own layer, the same way
``meta-imx-cargt`` adds ``cargt-swupdate-mods.cfg``.

.. warning::

   The ``swupdate.cfg`` that Cargt images install already has a
   ``suricatta`` section with ``enable = true``, pointing at a Cargt test
   server. It does nothing while suricatta is not built in, but as soon as
   you enable ``CONFIG_SURICATTA``, the board starts polling that server.
   Install your own ``swupdate.cfg`` from your layer, with a ``suricatta``
   section for your own hawkBit server (``url``, ``tenant``, ``id`` and
   your token), or with ``enable = false``.

The configuration fragment:

.. code-block:: text

   CONFIG_CURL=y
   CONFIG_DOWNLOAD=y
   CONFIG_SURICATTA=y

With the downloader enabled, SWUpdate can download and install in one step:

.. code-block:: bash

   swupdate -v -d "-u http://<host_ip>:8000/<update_file>.swu"

RAUC A/B Updates (STM32MP2)
---------------------------

STM32MP2 00395 designs use RAUC with a dual-bank (A/B) partition layout
instead of SWUpdate. Updates install to the inactive bank, and a bank that
fails to boot falls back to the previous one automatically. See
:doc:`rauc-ota-updates`.

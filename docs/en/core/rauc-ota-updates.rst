.. _rauc-ota-updates:

RAUC A/B OTA Updates — STM32MP2 (00395-01-00365 / 00395-02-00365)
====================================================================

.. note::

   **Verified on:** ``stm32mp25-cargt-00395-01-00365`` and
   ``stm32mp25-cargt-00395-02-00365``, ``cargt-image-dev``, Yocto
   scarthgap, on eMMC and SD card. RAUC support is in the public
   `meta-st-cargt <https://github.com/cargt/meta-st-cargt>`__ and
   `meta-cargt-stm32mp-addons <https://github.com/cargt/meta-cargt-stm32mp-addons>`__
   ``scarthgap`` branches (merged October 2026). The pre-built 00395
   images on `yocto.cargt.com <https://yocto.cargt.com/images/scarthgap/>`__
   include a matching ``.raucb`` bundle. See :ref:`rauc-testing-status`
   for what has been tested.

This page describes the RAUC-based remote update mechanism Cargt uses on
STM32MP2 (OpenSTLinux) boards. Both 00395 boards use the same mechanism and
partition layout, each with its own machine configuration and bundle.

Overview
--------

Cargt's STM32MP2 (OpenSTLinux) boards use **RAUC** for remote firmware
updates, with a **dual-bank (A/B) atomic-swap** model: every updatable
partition exists as two copies (``bootfs-a``/``bootfs-b``,
``vendorfs-a``/``vendorfs-b``, ``rootfs-a``/``rootfs-b``,
``fip-a``/``fip-b``). An update is written entirely to the *inactive* copy
while the device keeps running normally from the active one; only on the
next reboot does the device switch over. An interrupted update therefore
never leaves a half-written copy selected as the boot bank.

.. important::

   If a newly installed bank fails to boot, the device falls back to the
   previous bank automatically. See :ref:`rauc-rollback-safety`.

Theory of Operation
--------------------

Partition layout
~~~~~~~~~~~~~~~~~

Several different kinds of "two copies" show up on the device, and it
matters which is which: **redundant pairs** (``TF-A``, ``Metadata``) hold
*identical* data kept twice, as separate partitions, purely for fault
tolerance; **A/B banks** (``fip``, ``bootfs``, ``vendorfs``, ``rootfs``)
are genuinely *versioned* across two separate partitions — the two copies
can differ, and that's the whole update mechanism; and ``u-boot-env`` is a
redundant pair too, but implemented as two copies *inside one partition*
rather than as two partitions (see below). The table below is in physical
device order, left to right:

.. list-table:: Partition layout (physical device order)
   :header-rows: 1
   :widths: 16 22 16 14 10

   * - Partition
     - Copies
     - Scheme
     - RAUC slot
     - FS
   * - ``TF-A``
     - 2
     - Redundant pair
     - No
     - raw
   * - ``Metadata``
     - ``metadata1``/``2``
     - Redundant pair
     - No
     - raw
   * - ``fip``
     - ``fip-a``/``-b``
     - A/B bank
     - raw
     - raw
   * - ``u-boot-env``
     - 1 partition, 2 env copies
     - Redundant, in-place
     - No
     - env
   * - ``bootfs``
     - ``bootfs-a``/``-b``
     - A/B bank
     - ext4
     - ext4
   * - ``vendorfs``
     - ``vendorfs-a``/``-b``
     - A/B bank
     - ext4
     - ext4
   * - ``rootfs``
     - ``rootfs-a``/``-b``
     - A/B bank
     - ext4
     - ext4
   * - ``userfs``
     - 1
     - Single, shared
     - No
     - ext4

- **fip-a / fip-b** — the FIP (Firmware Image Package: BL31 + U-Boot +
  U-Boot DTB) for each bank.
- **metadata1 / metadata2** — TF-A firmware-update (FWU) metadata. Records
  which bank is active/previous and each bank's accept/trial state.
- **bootfs-a / bootfs-b** — kernel Image + DTB + boot config, one per bank.
- **vendorfs-a / vendorfs-b** — vendor partition, one per bank.
- **rootfs-a / rootfs-b** — the root filesystem, one per bank. This is
  what most of a bundle's size actually is.
- **userfs** — a single partition, **not** duplicated. Shared, persistent
  application/user data that survives every OTA update untouched (grown to
  fill remaining eMMC/SD space on first boot).
- **u-boot-env** — U-Boot's environment. A single *partition*, but not a
  single copy: U-Boot's environment tooling keeps two environment copies
  at different offsets within that one partition, each tagged with a
  sequence number, so a write that's interrupted mid-way can't corrupt
  the only copy — the tooling always has a known-good fallback to read.
  This is separate from, and doesn't participate in, the A/B bank
  mechanism; it's not RAUC-managed.

The ``-b`` slot of each A/B partition starts **empty** at first flash/build;
it's populated by the very first ``rauc install``.

**Minimum media size**: the fixed-size A/B partitions alone (not counting
``userfs``, which just fills whatever space is left) add up to roughly
**6.6 GiB**. Budget **~8-10 GiB** in practice
to leave real room for persistent application data on top of that floor.
This is the number to check against before considering smaller eMMC or SD
card hardware. This partition layout, and the size guidance above, is
identical across both supported boards.

Boot flow and bank selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. **TF-A BL2** reads the FWU metadata (stock upstream logic, no
   customization needed) and boots into the selected bank's FIP → U-Boot.
#. **U-Boot** runs its boot command. In the OpenSTLinux ecosystem version
   this platform is on (6.1), TF-A's bank choice is **not** automatically
   propagated into U-Boot's own partition selection — U-Boot has to be
   told separately which bank to boot next. Cargt handles this with a
   small custom RAUC bootloader-backend script that, whenever a new bank
   is committed, persistently rewrites U-Boot's boot command so U-Boot
   picks the correct bank on the next power-on (see `Update flow`_).
#. U-Boot loads that bank's boot config and boots the kernel with a
   device-specific ``root=`` path and ``rauc.slot=A|B`` on the cmdline —
   both patched into that slot's boot config at install time (see
   `Update flow`_).
#. **Linux boots**; ``rauc.slot=`` on ``/proc/cmdline`` tells RAUC and
   every other consumer which bank is currently running.
#. **Trial/good-boot**: a newly-installed bank boots in *trial* state,
   with a bootcount-based retry limit armed (see
   :ref:`rauc-rollback-safety`). RAUC's built-in mark-good service calls
   ``rauc status mark-good`` after a successful boot, which flips the
   bank to Accepted in the FWU metadata, resyncs U-Boot's boot command to
   match, and disarms the retry limit — whether the bank is good because
   the fresh install simply booted fine, or because the retry/fallback
   mechanism already reverted to it automatically.

.. _rauc-rollback-safety:

Rollback safety: automatic fallback on a failed boot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If a newly-installed bank fails to boot at all — bad kernel, corrupted
bootfs, a crash before reaching a health checkpoint — the device
recovers automatically, with no manual intervention. Getting here required
two things working together, and it's worth understanding both if you're
building something similar:

- **A boot-attempt counter with a limit**, armed only while a bank is on
  trial. Each boot attempt increments the counter; once it passes the
  limit, the boot loader gives up on the new bank and falls back to the
  previous known-good one instead. A successful boot resets and disarms
  the counter.
- **A hardware watchdog that's actually free to act.** A boot-attempt
  counter alone isn't sufficient if the failure mode is a hang rather
  than a clean error — something still has to notice the hang and force
  a reset so the next attempt (or the fallback) can happen. On this
  platform that meant making sure the OS doesn't silently keep the
  bootloader-armed watchdog fed during an early hang that happens before
  the OS itself has taken real ownership of it; without that fix, a
  hung boot attempt could sit forever rather than reset and retry.

With both pieces in place, a bank deliberately sabotaged to fail at boot
gets ``bootlimit`` (3) real attempts — each one hanging and then
correctly recovering via a watchdog reset — before automatically falling
back to the previous good bank on the fourth. On the serial console a
failed attempt and the fallback look like this:

.. code-block:: text

   Panic 'Watchdog'
   ...
   Bootlimit (3) exceeded. Using altbootcmd

After the fallback, ``bootcmd`` and ``altbootcmd`` point at the good bank
again and ``bootcount`` and ``upgrade_available`` are cleared. The
counter is only tracked while a bank is on trial
(``upgrade_available=1``), so a watchdog reset during normal operation
does not affect A/B bookkeeping.

Update flow
~~~~~~~~~~~

What ``rauc install`` actually does:

#. RAUC verifies the bundle's signature and writes each bundle slot
   (``fip``, ``bootfs``, ``vendorfs``, ``rootfs``) straight to the
   **inactive** bank's partitions.
#. A post-install step runs:

   - Patches the newly-written bank's boot config so its ``root=`` and
     ``rauc.slot=`` values point at the slot that was just installed,
     instead of the other one.
   - Updates any other partition-label references that assume the
     previously-active bank, so they now point at the newly-installed
     bank.
   - Writes FWU metadata marking the new bank as trial and the current
     bank as accepted — arming trial/bootcount mode for the new bank.

#. The custom bootloader-backend script commits the new bank as "boot
   this one next" by rewriting U-Boot's boot command.
#. Device reboots (not automatic — the caller decides when).

.. _rauc-partition-resolution:

Partition resolution across eMMC and SD card
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

eMMC and SD card carry **identically-named** partitions (the same image
gets flashed to either), but a name-based lookup is ambiguous whenever
both devices are present at once (eMMC is always present; SD card
whenever inserted), and isn't guaranteed to resolve to the device actually
being booted from. The platform resolves this by determining, early in
boot, which physical device the running root filesystem actually lives
on, then scoping every partition reference to that device only — so RAUC
and its supporting tooling always operate on the device that's actually
running, not whichever device happens to be present.

**The one exception**: the kernel's own ``root=`` cmdline argument. It's
resolved by the kernel *before* any of that device-scoping logic can run,
so it has to be a literal, per-target device path baked in at build time
rather than resolved dynamically.

**A general gotcha worth knowing if you're integrating RAUC on a
multi-media platform**: eMMC and SD card partition *names* can match
while partition *numbers* don't — an SD card commonly needs extra
boot-related partitions that eMMC doesn't, which shifts every later
partition's number. Anything that assumes a partition's name implies a
fixed number (kernel cmdline, environment config, partition-management
scripts) has to be checked for each medium rather than copied across.

Working with bundles
---------------------

An update bundle packages the four A/B slots (``fip``, ``bootfs``,
``vendorfs``, ``rootfs``) together, hashed with dm-verity per slot, and
signed against a certificate installed on the target. Development builds
are signed with a demo key/certificate pair checked into the layer — this
**must be replaced with a real key/cert pair before any production
deployment**.

Practical notes
----------------

A few platform-level behaviors worth knowing if you're maintaining or
extending this setup:

- **Inactive-slot auto-mount conflicts.** A generic partition auto-mounter
  will happily mount whichever inactive A/B partition is sitting there
  unused, which then collides with RAUC trying to write to it
  (``Device or resource busy``). A/B partitions need to be excluded from
  any such generic auto-mount policy; ``userfs`` is intentionally left
  mountable since it isn't part of the A/B scheme.
- **First-boot resize/fsck assumptions.** Stock first-boot resize/fsck
  tooling on this BSP was written for single-bank boards and originally
  tried to grow/check every ext4 partition on first boot. That's wrong
  for A/B partitions, which are fixed-size with no room to grow — only
  the shared ``userfs`` partition ever needs resizing. Left unaddressed,
  this adds unnecessary boot-time cost (a full bad-blocks filesystem
  check) to every fresh-slot first boot after an OTA update — and on a
  large ``userfs``, that check can run long enough to look identical to a
  genuinely broken boot from the rollback mechanism's point of view. A
  bank that keeps "failing to boot" and falling back is worth checking
  for a stuck first-boot resize before assuming the installed image
  itself is bad.
- **Media matters for first-boot growth.** A fixed-size ``userfs``
  partition with free space left after it on the device (typical of an SD
  card layout, where the exact card size isn't known at build time) needs
  its partition table entry itself extended before a filesystem resize
  has anything to grow into — a plain filesystem-level resize tool only
  ever fills the partition's *existing* boundary. A layout that instead
  sizes the partition to consume all remaining space at flash time
  (typical of eMMC, whose size *is* known at build time) doesn't have
  this problem.

Examples
--------

The commands below use ``stm32mp25-cargt-00395-02-00365``; substitute
``stm32mp25-cargt-00395-01-00365`` (and its own bundle recipe name) to
target the other board — everything else is identical.

Pre-built bundles
~~~~~~~~~~~~~~~~~

Each 00395 image directory on yocto.cargt.com has a bundle next to the
``.wic`` image, for example
`stm32mp25-cargt-00395-02-00365 <https://yocto.cargt.com/images/scarthgap/stm32mp25-cargt-00395-02-00365/>`__:

.. code-block:: text

   update-st-bundle-stm32mp25-cargt-00395-02-00365-stm32mp25-cargt-00395-02-00365.raucb

``BUILD-INFO.txt`` in the same directory lists the layer commits it was
built from.

Build
~~~~~

Set up the build environment as described in the :ref:`yocto-tutorial`,
with ``MACHINE`` set to the board the bundle is for (each bundle recipe sets
``COMPATIBLE_MACHINE``). Then:

.. code-block:: sh

   bitbake cargt-image-dev update-st-bundle-stm32mp25-cargt-00395-02-00365

The bundle recipe depends on its slot images, so building it alone also
builds them. The bundle is written to
``tmp-glibc/deploy/images/<machine>/update-st-bundle-<machine>-<machine>.raucb``,
with a timestamped copy next to it.

Initial flash
~~~~~~~~~~~~~

The A/B layout uses a different partition table from the older single-bank
layout, so a board on the single-bank layout **cannot** be converted by an
OTA update. Flash it once:

- **eMMC:** STM32CubeProgrammer with the
  ``FlashLayout_emmc_<CUBEMX_DTB>-optee.tsv`` flash layout. Use the main
  layout, not one of the ``-glt*`` display variants: only the main layout
  has the A/B partitions.
- **SD card:** write the ``.wic`` image, for example with
  ``bmaptool copy <image>.wic.bz2 /dev/sdX`` (``bmaptool`` uses the
  ``.wic.bmap`` file next to it).

The ``-b`` bank starts empty (eMMC) or with only a copy of the ``-a`` FIP
(SD card). The first ``rauc install`` fills it.

Push and install
~~~~~~~~~~~~~~~~~

.. code-block:: sh

   scp update-st-bundle-stm32mp25-cargt-00395-02-00365.raucb root@<DUT>:/usr/local/
   ssh root@<DUT> 'rauc install /usr/local/update-st-bundle-stm32mp25-cargt-00395-02-00365.raucb'

``rauc install`` targets whichever bank is currently inactive — no need to
specify which slot.

Reboot and confirm the switch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   ssh root@<DUT> reboot
   # ... wait for it to come back ...
   ssh root@<DUT> 'cat /proc/cmdline; rauc status --output-format=json-pretty'

Look for ``rauc.slot=B`` (or ``A``) on the cmdline matching the bank you
just installed into, and ``"boot_status": "good"`` on the now-booted slot
in ``rauc status`` output.

.. note::

   The readable-text form of ``rauc status`` wraps values in ANSI color
   codes, so prefer ``--output-format=json`` (or ``json-pretty``) for
   anything you intend to script against.

Manual bank inspection / control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: sh

   rauc status --detailed                 # read-only: never accepts or disarms anything
   rauc status mark-good                  # accept the running (trial) bank
   rauc status mark-bad other             # cancel a pending, not-yet-booted install
   rauc status mark-bad booted            # switch to the other bank on next boot
   rauc status mark-active other          # make the other bank primary (arms a trial)
   /usr/lib/rauc/st-boot-script.sh get-primary      # bank the next boot lands on
   /usr/lib/rauc/st-boot-script.sh get-state B      # good | bad
   fw_printenv bootcmd altbootcmd upgrade_available bootcount bootlimit rauc_bad

``get-primary`` reports the bank U-Boot will boot *next*, not the one that
is running now (that is ``rauc.slot=`` on ``/proc/cmdline``, or
``booted:`` in ``rauc status``). Right after ``rauc install`` it already
names the new bank. ``rauc_bad`` lists banks that failed a trial boot, were
marked bad by hand, or were left half-written by an interrupted install.

Drag-and-drop updates from a browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``cargt-image-dev`` includes ``rauc-web-updater``, a small web page on the
board for installing one bundle on one bench board:

.. code-block:: text

   http://<DUT>:8080/

Drop a ``.raucb`` file on the page (or click to browse). It uploads the
bundle, runs ``rauc install``, and shows the install log with a
**Reboot now** link. It does not reboot by itself. The same flow works from
a script:

.. code-block:: sh

   curl -s -X POST -F "bundle=@update-st-bundle-stm32mp25-cargt-00395-02-00365.raucb" http://<DUT>:8080/upload
   curl -s http://<DUT>:8080/reboot   # after checking the install log

.. warning::

   The web updater has no authentication. It is a lab convenience for a
   trusted network and is not included in production images.

Pull-based updates with hawkBit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``rauc-hawkbit-updater`` is also in ``cargt-image-dev``. The board polls an
`Eclipse hawkBit <https://eclipse.dev/hawkbit/>`__ server, then downloads
and installs whatever distribution set is assigned to it, and reboots. The
shipped configuration (``config.conf.<board>`` in
``recipes-support/rauc-hawkbit-updater``) has placeholder
``hawkbit_server`` and ``auth_token`` values. Override them in your own
layer. The ``docs/hawkbit`` directory of ``meta-st-cargt`` has a Docker
Compose file for a test server and the REST calls to register a target and
assign an update.

Cargt uses hawkBit as test infrastructure. Both 00395 boards ran more than
110 consecutive automatic update cycles (about 18 hours) with no failures,
and a later overnight run that also sabotaged a bank every fourth cycle
passed 109 consecutive cycles.

Troubleshooting
~~~~~~~~~~~~~~~~

``Device or resource busy`` writing to the inactive slot
   A generic auto-mounter mounted it first — confirm A/B partitions are
   actually excluded from auto-mount on the target (see `Practical
   notes`_).

Slot doesn't flip after install+reboot
   Check ``fw_printenv bootcmd`` — if it still says ``Boot A`` (or
   whichever was previously active) after installing into the other bank,
   bank commitment didn't run or didn't persist; this is the "no
   automatic TF-A→U-Boot hand-off" behavior described in `Boot flow and
   bank selection`_. If ``bootcmd`` names the new bank but the board came
   back on the old one, compare ``bootcount`` with ``bootlimit`` and check
   ``rauc_bad``: the new bank failed its trial and U-Boot fell back (see
   :ref:`rauc-rollback-safety`).

``Unsupported image ... .bin for slot type raw``
   The running ``rauc`` service has not picked up a rebuilt binary or
   configuration. Run ``systemctl restart rauc.service`` after updating
   any RAUC package, and make sure you are installing the newly built
   bundle.

SSH reports ``REMOTE HOST IDENTIFICATION HAS CHANGED`` after an update
   Expected: the newly installed bank generates its own SSH host key on
   first boot. Run ``ssh-keygen -R <DUT>`` before reconnecting.

Device stuck at the boot loader prompt on an otherwise-normal boot
   Separate from the failed-boot/rollback scenario above: on builds
   predating a fix for this, the boot loader's automatic partition scan
   could occasionally drift to the wrong partition, typically after a
   stale scan-state value got persisted to the environment (for example,
   from interactive debugging at the boot prompt). This has since been
   fixed at the source. On an affected/unpatched build, clearing the
   stale value (``setenv distro_bootpart`` at the U-Boot prompt, then
   ``saveenv``) restores correct automatic scanning and stays fixed
   across subsequent boots.

Enabling A/B on another machine
-------------------------------

Everything A/B-specific is enabled only when ``COMBINED_FEATURES``
contains ``rauc``: the distro sets ``DISTRO_FEATURES`` ``rauc`` and the
machine must also set ``MACHINE_FEATURES`` ``rauc``. A machine without it
keeps the single-bank layout even with the same distro. To add a board:

#. In the machine conf: ``MACHINE_FEATURES += "rauc"``,
   ``UBOOT_EXTLINUX_KERNEL_ARGS:append = " rauc.slot=A"``, a per-target
   ``UBOOT_EXTLINUX_ROOT`` (the literal ``/dev/mmcblkNpM`` of
   ``rootfs-a``; check the real partition numbers on each medium), and
   rootfs, vendorfs and bootfs sizes that fit twice.
#. A ``.wks.in`` with the ``-a``/``-b`` partitions. ``rootfs-b`` must
   immediately follow ``rootfs-a``.
#. ``recipes-core/rauc/files/<machine>/system.conf`` with a unique
   ``compatible=``.
#. ``recipes-bsp/u-boot/libubootenv/<machine>/fw_env.config`` pointing at
   ``/run/cargt-part/u-boot-env``.
#. A bundle recipe with a matching ``RAUC_BUNDLE_COMPATIBLE``, slot file
   names and ``COMPATIBLE_MACHINE``.
#. Make sure the udev auto-mount ignore list
   (``cargt-ab-partitions.ignorelist``) covers the board's A/B partition
   numbers on each medium.

To check whether the feature is active for a recipe:

.. code-block:: sh

   bitbake -e rauc-conf | grep ^COMBINED_FEATURES=

.. _rauc-testing-status:

Testing status
--------------

All tests below passed on both 00395 boards (``00395-01-00365`` and
``00395-02-00365``) unless noted otherwise.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 15 55

   * - Test
     - Media
     - Result
   * - Install, reboot and verify, A→B and B→A
     - eMMC, SD card
     - Pass. Checked with ``rauc status`` and ``/proc/cmdline``.
   * - Repeated A↔B update cycles
     - eMMC
     - Pass. More than 12 round trips per board.
   * - Rollback after a failed boot
     - eMMC
     - Pass. A bank modified to fail at boot falls back to the previous
       bank after three attempts, with no user action. More than 12 runs
       per board.
   * - hawkBit pull updates
     - eMMC
     - Pass. More than 110 consecutive automatic cycles (about 18 hours).
   * - Drag-and-drop web updater
     - —
     - Pass (``00395-02-00365``).
   * - ``userfs`` grows to fill the media on first boot
     - SD card
     - Pass.
   * - ``userfs`` is not resized again after an update
     - —
     - Pass.

Last updated October 2026, ``meta-st-cargt`` ``scarthgap`` branch.

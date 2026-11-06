.. _selinux:

SELinux (Evaluation)
====================

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX 93` :bdg-primary:`STM32MP2`

.. note::

   SELinux has been evaluated on Cargt i.MX boards with the wrynose BSP
   and on the STM32MP2 with the scarthgap BSP, but it is not supported
   yet: it is not in any Cargt layer or image, and
   it has to be turned on in your own build. This page describes what
   Cargt tested and what it found. `Contact Cargt
   <https://www.cargt.com/cargt-about/contact-us>`__ if you plan to ship
   SELinux.

SELinux (Security-Enhanced Linux) adds mandatory access control to the
kernel. Each process runs in a *domain* and each file has a *type*, and a
policy says which domains may do what to which types. Anything the policy
does not allow is denied, even for root.

Cargt tested it with ``cargt-image-dev`` and the reference policy's
``targeted`` variant on:

- an i.MX 93 00363 on the 00365 carrier, and an i.MX 93 board with an LTE
  modem (wrynose);
- an STM32MP257F 00395 on the 00365 carrier (scarthgap), installed as a
  RAUC update to the B slot.

The Cargt STM32MP2 images do not include SELinux: their kernel is built
without it and ``systemd`` reports ``-SELINUX``.

.. contents:: On this page
   :local:
   :depth: 1

Enabling SELinux in a Build
---------------------------

**Layer.** Add ``meta-selinux`` (``git.yoctoproject.org/meta-selinux``,
``wrynose`` branch for i.MX, ``scarthgap`` for the STM32MP2) to
``bblayers.conf``. It needs ``meta-oe`` and
``meta-python``, which Cargt builds already include. Adding the layer
changes nothing until ``selinux`` is in ``DISTRO_FEATURES``.

**local.conf:**

.. code-block:: bash

   DISTRO_FEATURES:append = " acl xattr pam selinux"
   PREFERRED_PROVIDER_virtual/refpolicy = "refpolicy-targeted"
   DEFAULT_ENFORCING = "permissive"

``DEFAULT_ENFORCING`` is written to ``/etc/selinux/config``; use
``"enforcing"`` once the system runs without denials (see
`Permissive First, Then Enforcing`_).

**Image.** The distro feature alone is not enough. The image recipe, or a
``.bbappend`` for it in your layer, must label the root file system and
install the policy and tools:

.. code-block:: bash

   inherit selinux-image
   IMAGE_INSTALL:append = " packagegroup-core-selinux"

``packagegroup-core-selinux`` includes the Python analysis tools
(``audit2allow``, ``sesearch``), which suit a development image. A
production image can install a smaller set.

**Kernel.** meta-selinux's kernel changes apply to ``linux-yocto`` only,
so the ``linux-imx`` and ``linux-stm32mp`` kernels need a configuration
fragment from your layer (see :doc:`yocto-development` for adding one):

.. code-block:: text

   CONFIG_AUDIT=y
   CONFIG_SECURITY=y
   CONFIG_SECURITYFS=y
   CONFIG_SECURITY_NETWORK=y
   CONFIG_SECURITY_SELINUX=y
   CONFIG_SECURITY_SELINUX_BOOTPARAM=y
   CONFIG_SECURITY_SELINUX_DEVELOP=y
   CONFIG_SECURITY_SELINUX_AVC_STATS=y
   CONFIG_NETWORK_SECMARK=y
   CONFIG_EXT4_FS_SECURITY=y
   CONFIG_TMPFS_XATTR=y
   CONFIG_LSM="landlock,lockdown,yama,loadpin,safesetid,selinux,ipe,bpf"

On the STM32MP2's 6.6 kernel, which has no ``ipe``, use
``CONFIG_LSM="landlock,lockdown,yama,loadpin,safesetid,selinux,bpf"``.

The ``CONFIG_LSM`` line matters: both kernels' defconfigs set an explicit
list of security modules to start, and without ``selinux`` in it SELinux
is built into the kernel but never starts. ``EXT4_FS_SECURITY`` and
``TMPFS_XATTR`` let the root file system and ``/run`` hold the labels.
``SECURITY_SELINUX_DEVELOP`` is what allows permissive mode; a production
kernel can leave it out so that the system is always enforcing.

To add the fragment only when SELinux is on, in your ``linux-imx``
``.bbappend``:

.. code-block:: bash

   SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'selinux', 'file://selinux.cfg', '', d)}"

The ST kernel applies only the fragments listed in
``KERNEL_CONFIG_FRAGMENTS``, so a ``linux-stm32mp`` ``.bbappend`` also
names it there:

.. code-block:: bash

   SRC_URI += "${@bb.utils.contains('DISTRO_FEATURES', 'selinux', 'file://selinux.cfg;subdir=fragments/selinux', '', d)}"
   KERNEL_CONFIG_FRAGMENTS:append = " ${@bb.utils.contains('DISTRO_FEATURES', 'selinux', '${WORKDIR}/fragments/selinux/selinux.cfg', '', d)}"

**Expect a near-full rebuild.** The distro feature changes most recipes;
in Cargt's i.MX test build 8284 of 12816 tasks ran again, and 6785 of
10332 in the STM32MP2 build. Use a separate build
directory for SELinux images.

Checking It on the Board
------------------------

``sestatus`` shows whether SELinux is running, the policy and the mode:

.. code-block:: bash

   sestatus
   ls -Z /usr/sbin/NetworkManager     # a file's label
   ps -eZ | grep NetworkManager       # a process's domain

On Cargt's test boards, ``sestatus`` reported SELinux enabled, the
``targeted`` policy loaded and permissive mode, and the active security
modules were ``capability,selinux``. ``NetworkManager``, ``sshd``,
``avahi``, ``udev``, D-Bus, ``systemd-logind`` and ``tee-supplicant`` ran
in their own domains.

What It Costs
-------------

Measured on an i.MX 93 00363, against the same image without SELinux:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 60

   * - Item
     - Cost
   * - Root file system
     - +62 MB uncompressed, +16.5 MB compressed (the tarball in an update
       package)
   * - Kernel image
     - +266 KB
   * - Policy load at boot
     - about 0.12 s
   * - RAM
     - about 6 to 10 MB (the loaded policy, its kernel structures and
       ``auditd``)

On the STM32MP257F 00395 the SELinux packages in ``cargt-image-dev`` add
up to 43 MB installed: 28 MB for the policy and 13 MB for
``python3-networkx``, which only the analysis tools use. ``systemd``
reported loading the policy in 0.30 s. Cargt has not compared the
STM32MP2's RAM use or kernel size with an image without SELinux.

Most of the root file system increase is the Python tools and the policy
store under ``/var/lib/selinux``, which is only needed to change the policy
on the board. Cargt estimates a production set without them at +10 to
15 MB.

Software Updates
----------------

Every file needs its label after an update, and how it gets one depends on
how the update writes the new slot (see :doc:`software-updates`):

- **An update that writes a raw ext4 image into the slot** keeps the labels
  the build gave the image. Nothing extra is needed. Cargt tested this on
  the i.MX 93 board with an LTE modem, including the first update from a
  slot without SELinux.
- **An update that unpacks a tarball into the slot**, as the Cargt
  ``update.sh`` does, loses the labels: the image's tarball does not carry
  them, and ``tar`` does not restore them. The update script has to label
  the new slot after unpacking it.

To label the new slot with its own policy, the update script copies the
new slot's ``file_contexts`` to ``/run``, gives the copies a type
``setfiles`` may read, and runs ``setfiles``. The plain copy and the
``chcon`` matter under enforcing mode; without them ``setfiles`` is denied
access to the new slot's unlabeled files. ``$MNT`` is where the script
mounted the new slot:

.. code-block:: bash

   if [ -f "$MNT/etc/selinux/config" ]; then
       POLTYPE=$(sed -n 's/^SELINUXTYPE=//p' "$MNT/etc/selinux/config")
       if [ -e /sys/fs/selinux/enforce ] && [ -x /sbin/setfiles ]; then
           FCDIR=$(mktemp -d /run/fc.XXXXXX) || exit 1
           # a plain copy (not -a), so the copies get a type setfiles may read
           cp -r "$MNT/etc/selinux/$POLTYPE/contexts/files/." "$FCDIR/" &&
               chcon -R -t file_context_t "$FCDIR" &&
               /sbin/setfiles -F -r "$MNT" "$FCDIR/file_contexts" "$MNT"
           rc=$?
           rm -rf "$FCDIR"
           [ $rc -eq 0 ] || exit 1
       else
           # The running system has no SELinux: label on the first boot
           : > "$MNT/.autorelabel"
       fi
   fi

- **Between two SELinux images,** ``setfiles`` labels the new slot during
  the update. On the full root file system that adds an estimated 30 to
  40 s to the update.
- **The first update from an image without SELinux** can't write labels,
  because the running kernel has no SELinux. The script creates
  ``/.autorelabel`` instead, and the new image relabels itself on its
  first boot and reboots once. On the test board that took under 25 s.

Without either step, the updated slot boots with no labels: permissive
mode logs a flood of denials, and enforcing mode is unlikely to boot.

**On the STM32MP2,** RAUC writes ext4 images into the B slot, so most
files keep their labels, but some don't. In Cargt's test, after an update
from an image without SELinux:

- the Cargt RAUC post-install script rewrites ``/sbin/mount-partitions.sh``
  in the new slot to point at that slot's partitions, and the rewritten
  file has no label;
- RAUC's ``/slot.raucs`` status file has no label;
- the ``bootfs`` and ``vendorfs`` images are built without labels, and so
  is the ``userfs`` partition at ``/usr/local``.

In permissive mode this only logs denials, mostly services that look up
``/usr/local``. ``restorecon`` fixed the files in the new slot and the
``/boot`` and ``/vendor`` partitions at runtime. A product update should
do the same as the i.MX script above: create ``/.autorelabel`` in the
new slot when the running system has no SELinux, or relabel the files
the post-install script changes when it does. The first-boot relabel was
not tried on the STM32MP2.

``/data`` is created empty and has no labels. Services without a policy of
their own don't notice, but confined ones are denied access to files
there.

Permissive First, Then Enforcing
--------------------------------

In **permissive** mode SELinux logs what it would deny but allows it.
Start there, use the board normally, including a software update, and
collect the denials:

.. code-block:: bash

   ausearch -m avc,user_avc -ts boot     # the denials since boot
   audit2why -a                          # why each was denied
   audit2allow -a -m mylocal             # allow rules for them, as a module

Review what ``audit2allow`` suggests before using it: it allows exactly
what was denied, which can be more than a service needs. Prefer a policy
boolean where one exists. To build and load the rules as a module:

.. code-block:: bash

   audit2allow -a -M mylocal     # writes mylocal.te and mylocal.pp
   semodule -i mylocal.pp

Then switch to **enforcing**, at runtime with ``setenforce 1`` to try it,
and in ``/etc/selinux/config`` (or ``DEFAULT_ENFORCING``) to keep it.

Denials Seen on Cargt Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A small set, the same on every boot. The table says which boards each
appeared on:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 35 65

   * - Service
     - Denial and fix
   * - ``sshd`` (all boards)
     - Root logins over SSH are refused under enforcing. Set the boolean
       with ``setsebool -P ssh_sysadm_login on`` before switching a board
       without a serial console to enforcing, or you lose access to it.
       On the STM32MP2, logins failed under enforcing without it and
       worked with it.
   * - NetworkManager (i.MX)
     - Its BPF use (the ``bpf`` capability and BPF maps and programs).
       Needs a small allow rule.
   * - ``tee-supplicant`` (i.MX)
     - Its own logging socket. Set the ``tee_supplicant_qtee`` boolean.
   * - ``ofono`` (i.MX)
     - Replies over D-Bus to the console user's session. Needs a small
       allow rule, or remove ``ofono`` if the product doesn't use it.
   * - ``udev`` (i.MX 93 00363 and STM32MP2)
     - The automount script writing to ``/tmp`` and creating
       ``/run/media``. Review rather than allow writes to ``/tmp``
       wholesale.
   * - ``rauc`` (STM32MP2)
     - Under enforcing, ``rauc status`` run from an SSH shell got no
       answer: the RAUC service runs in ``initrc_t``, and its D-Bus reply
       to the shell (``unconfined_t``) was denied. See
       `Services Without a Policy`_.
   * - Several services (STM32MP2)
     - ``systemd-logind``, ``sshd``, ``systemd-timesyncd`` and others
       looking up ``/usr/local``, which has no label. Label the
       partition (see `Software Updates`_).

On the board with the LTE modem, ModemManager, ``pppd``, the CMUX
multiplexer and the ``ppp0`` connection raised no denials.

Services Without a Policy
~~~~~~~~~~~~~~~~~~~~~~~~~

The reference policy covers the common system services, but not Cargt's
own or your application's. systemd starts those in ``initrc_t``, which the
``targeted`` policy leaves unconfined: Weston, Mosquitto, SWUpdate and its
web interface, ``grow-data-part``, OP-TEE storage and your own services keep
working under enforcing, but SELinux does not protect them. Confining one
means writing a policy module for it.

An unconfined service can still meet a denial when it talks to a process
in another domain. In the test, a command-line tool run from an SSH shell
(``unconfined_t``) called a custom service over D-Bus, and permissive mode
logged a denial for the service's reply (from ``initrc_t``). Under
enforcing the tool would get no answer. Fix it with an allow rule, or
better, a domain of its own for the service.

What Was Not Tested
-------------------

- Enforcing mode set at boot. Enforcing was tested at runtime, with
  ``setenforce 1``, on the i.MX 93 00363 and the STM32MP2.
- Other i.MX processors, and the real-time kernel, which has its own
  configuration.
- On the STM32MP2: the display and Weston (the test board's device tree
  has no display), the first-boot relabel, an update between two SELinux images, and
  updates through hawkBit.
- The camera applications, and any Cargt service confined by its own
  policy module.
- An update between two SELinux images with the tarball-based update; the
  labeling step was tested on its own.

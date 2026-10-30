.. _secure-boot:

Secure Boot (AHAB) on i.MX 9
============================

i.MX 91, i.MX 93 and i.MX 95 processors verify the boot image with
AHAB (Advanced High Assurance Boot), implemented by the EdgeLock Secure
Enclave (ELE). This page explains how AHAB works on Cargt SOMs and the steps
to sign an image. It does not replace NXP's documentation: the processor's
Security Reference Manual and the Code Signing Tool (CST) user guide are the
authoritative sources; see :doc:`/references/index`. U-Boot's own guide,
``doc/imx/ahab/guides/mx8ulp_9x_secure_boot.txt`` in the U-Boot source, has
the full procedure.

.. danger::

   Programming the SRK hash fuses and closing the device are **permanent**.
   A wrong SRK hash, or closing a device that does not boot a correctly
   signed image, leaves the SOM unable to boot, and it cannot be recovered.
   Practise on a SOM you can afford to lose, keep the signing keys offline,
   and contact Cargt before closing production parts.

Checking the Lifecycle
----------------------

Current Cargt U-Boot builds do not include ``ahab_status`` (see the
warning in step 2), but the lifecycle can be read on any Cargt U-Boot. On i.MX 93, bits 9:0 of the FSB register at
``0x4751041c`` hold the lifecycle (on i.MX 95 the register is at
``0x47510414``). This only reads the register. From an i.MX 93 00363 on the
00428 carrier:

.. code-block:: text

   u-boot=> md.l 0x4751041c 1
   4751041c: 04018c08                             ....

``0x04018c08 & 0x3ff`` is ``0x008``, OEM Open. The i.MX 93 values are:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 20 80

   * - Value
     - Lifecycle
   * - ``0x001``
     - Blank
   * - ``0x002``
     - Fab
   * - ``0x004``
     - NXP Provisioned
   * - ``0x008``
     - OEM Open (as shipped)
   * - ``0x020``
     - OEM Closed
   * - ``0x040``
     - Field Return OEM
   * - ``0x080``
     - Field Return NXP
   * - ``0x100``
     - OEM Locked
   * - ``0x200``
     - Bricked

The i.MX 95 uses different values (``0x010`` is OEM Open); see U-Boot's
``display_life_cycle()`` in ``arch/arm/mach-imx/ele_ahab.c``.

How AHAB Works
--------------

The boot image (``imx-boot``) is a sequence of containers, each with a
header and a signature block. On i.MX 91 and i.MX 93:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 35 35

   * - Container
     - Contents
     - Signed by, checked by
   * - 1
     - ELE firmware
     - NXP; checked by the ELE ROM
   * - 2
     - SPL (and the Cortex-M image, if any)
     - You (OEM keys); checked by the ELE firmware
   * - 3
     - ATF, OP-TEE and U-Boot proper
     - You (OEM keys); checked by SPL through the ELE

The i.MX 95 image also carries the OEI, System Manager and V2X firmware; see
the image layout in U-Boot's guide.

The OEM keys form a PKI tree. Its root is the Super Root Key (SRK) table:
up to four SRK public keys. A hash of that table is programmed once into the
SRK_HASH fuses, and the ELE compares every signed container's SRK table
against it. On i.MX 91 and i.MX 93 the hash is SHA-256 (256 bits, eight
fuse words).

.. warning::

   The i.MX 95 (B0 and later) uses AHAB 2.0, which works differently: the
   SRK hash is 512 bits, programmed into sixteen fuse words in banks 16 and
   17, and signing needs CST 4.0.1 or later, or NXP's Secure Provisioning SDK
   (SPSDK). The i.MX 91/93 steps below do not apply to it as written, and
   following them can leave an i.MX 95 SOM unable to boot once it is closed.
   Follow the i.MX 95 sections of U-Boot's guide and NXP's SPSDK example for
   the i.MX 95, and contact Cargt first.

The device lifecycle decides what happens when a check fails:

- **OEM Open** (as shipped): the image is checked and failures are logged as
  events, but the device still boots. Use this state to test signed images.
- **OEM Closed**: only correctly signed images boot. Changing to this state
  is irreversible.

Steps
-----

These steps are for i.MX 91 and i.MX 93; see the warning above for the
i.MX 95.

1. **Get the Code Signing Tool** from NXP (an NXP account is required), and
   generate the AHAB PKI tree with the scripts it provides. Then create the
   SRK table and the SRK hash fuse file with ``srktool``. Keep the private
   keys offline or in an HSM.

2. **Enable AHAB support in U-Boot.** Add ``CONFIG_AHAB_BOOT=y`` to the
   U-Boot configuration, for example with a configuration fragment in a
   ``u-boot-imx`` bbappend in your layer. This adds the ``ahab_*`` commands
   and makes SPL authenticate the U-Boot container through the ELE.

   .. warning::

      In NXP's U-Boot (``u-boot-imx`` 2026.04), ``CONFIG_AHAB_BOOT`` also
      changes ``booti``: it expects the kernel to be packaged as an AHAB OS
      container and fails with ``Authenticate OS container is failed`` for a
      plain ``Image``, even in the OEM Open lifecycle. Cargt images boot a
      plain ``Image``, so enabling ``CONFIG_AHAB_BOOT`` on its own stops the
      board from booting Linux. Enable it only together with packaging the
      kernel and device tree as an OS container (see
      `Authenticating the Kernel`_).

      Current Cargt U-Boot builds (wrynose, October 2026) do not enable
      ``CONFIG_AHAB_BOOT``, so the ``ahab_*`` and ``auth_cntr`` commands are
      not available in them.

3. **Build the boot image.** ``imx-mkimage``, run by the ``imx-boot``
   recipe, prints the container and signature block offsets that the CST
   needs. From ``imx-boot``'s ``log.do_compile`` for an i.MX 93 00363 build:

   .. code-block:: text

      Output:   u-boot-atf-container.img
      ...
      CST: CONTAINER 0 offset: 0x0
      CST: CONTAINER 0: Signature Block: offset is at 0x190
      ...
      Output:   flash.bin
      ...
      CST: CONTAINER 0 offset: 0x400
      CST: CONTAINER 0: Signature Block: offset is at 0x490
      append u-boot-atf-container.img at 348 KB, psize=1024

4. **Sign the containers** with the CST, using CSF description files that
   name your keys and the offsets from step 3. Sign
   ``u-boot-atf-container.img`` first, rebuild ``flash.bin`` with the
   signed container, then sign ``flash.bin``:

   .. code-block:: bash

      ./cst -i csf_uboot_atf.txt -o signed-u-boot-atf-container.img
      ./cst -i csf_boot_image.txt -o signed-flash.bin

   Example CSF files are in U-Boot's ``doc/imx/ahab/csf_examples``.

5. **Flash the signed image** with UUU as usual; see
   :doc:`getting-started`.

6. **Program the SRK hash fuses** (permanent). The fuse file from
   ``srktool`` holds eight 32-bit words:

   .. code-block:: bash

      od -t x4 SRK_1_2_3_4_fuse.bin

   On i.MX 93 they go in fuse bank 16, words 0 to 7, programmed from the
   U-Boot prompt with ``fuse prog 16 <word> <value>``, one command per word.
   For the i.MX 91, take the bank and words from its fuse map in the
   Security Reference Manual. Check every value twice before running these
   commands.

7. **Check for AHAB events.** Boot the signed image and run ``ahab_status``
   at the U-Boot prompt. It prints the lifecycle and the ELE's event log,
   which records authentication problems since power-on. With the SRK hash
   fused and a correctly signed image, it reports ``No Events Found!``.

   For comparison, this is an unsigned Cargt image on an i.MX 93 00363
   (00428 carrier) in the OEM Open lifecycle. The board boots, but the ELE
   logs an event for the OEM container authentication request
   (``ELE_OEM_CNTN_AUTH_REQ``):

   .. code-block:: text

      u-boot=> ahab_status
      Lifecycle: 0x00000008, OEM Open


              0x0287eed6
              IPC = MU APD (0x2)
              CMD = ELE_OEM_CNTN_AUTH_REQ (0x87)
              IND = ELE_NO_AUTHENTICATION_FAILURE_IND (0xEE)
              STA = ELE_SUCCESS_IND (0xD6)

   Any event means the device might not boot once closed. Do not continue
   until there are none. ``ahab_dump`` prints the ELE firmware's raw debug
   log, which NXP support can interpret.

8. **Close the device** (permanent, optional for development): run
   ``ahab_close`` at the U-Boot prompt and reboot. ``ahab_status`` then
   reports ``OEM Closed``.

Authenticating the Kernel
-------------------------

AHAB as described above covers the boot loader. To extend the chain of trust
to Linux, U-Boot can authenticate a signed OS container with ``auth_cntr``.
Cargt U-Boot environments include the hooks: when ``sec_boot`` is ``yes``,
``bsp_bootcmd`` loads ``os_cntr_signed.bin`` and authenticates it with
``auth_cntr`` before booting. You do not set ``sec_boot`` yourself: Cargt
U-Boot sets it at every boot, to ``yes`` when it is built with
``CONFIG_AHAB_BOOT`` and to ``no`` otherwise. See U-Boot's
``doc/imx/ahab/guides/sign_os_cntr.txt``.

For storing application keys, see :doc:`key-storage`.

Protect the U-Boot console as well; otherwise anyone with console access can
change ``bootcmd``, or ``sec_boot`` for the current boot.

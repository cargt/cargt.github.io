.. _key-storage:

Secure Key Storage (EdgeLock and OP-TEE)
========================================

i.MX 91, i.MX 93 and i.MX 95 processors have an EdgeLock Secure Enclave
(ELE), a security subsystem with its own firmware. Cargt i.MX images also run
OP-TEE, a trusted execution environment on the Cortex-A cores. Together they
let an application store keys and use them for signing and encryption
without the key material ever being readable by Linux.

The examples on this page are from an i.MX 93 00363 SOM on the 00428 carrier
with ``cargt-image-dev`` (wrynose, October 2026).

How It Fits Together
--------------------

- **ELE** verifies the boot image (see :doc:`secure-boot`), provides a
  hardware random number generator, and derives a hardware unique key (HUK)
  that is different on every SoC.
- **OP-TEE** gets its HUK from the ELE and derives the keys that encrypt its
  secure storage from it, so stored keys are bound to that SoC.
- **The OP-TEE PKCS#11 trusted application** exposes keys in secure storage
  through the standard PKCS#11 API. Linux applications use it through
  ``/usr/lib/libckteec.so.0``, and ``pkcs11-tool`` (from OpenSC) works from
  the shell.

Checking the Components
-----------------------

U-Boot prints the ELE firmware version at boot:

.. code-block:: text

   BuildInfo:
     - ELE firmware version 2.0.6-2449fe9d

The kernel log shows the ELE driver and OP-TEE:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# dmesg | grep -E "secure-enclave|optee"
   [    1.437548] fsl-se secure-enclave: INIT_WORK call for i.MX secure-enclave: hsm0.
   [    1.455346] fsl-se secure-enclave: Successfully registered ele-trng
   [    1.461662] fsl-se secure-enclave: i.MX secure-enclave: hsm0 interface to firmware, configured.
   [    1.555291] optee: probing for conduit method.
   [    1.559781] optee: revision 4.10 (37c7fbf84c40eb9e)
   [    1.560174] optee: dynamic shared memory is enabled

``tee-supplicant``, which stores OP-TEE's encrypted files for it, runs as a
service:

.. code-block:: bash

   systemctl status tee-supplicant@teepriv0

Storing and Using Keys with PKCS#11
-----------------------------------

The OP-TEE PKCS#11 trusted application provides three slots. Each slot holds
one token, which must be initialized before use:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# pkcs11-tool --module /usr/lib/libckteec.so.0 --list-slots
   Available slots:
   Slot 0 (0x0): OP-TEE PKCS11 TA - TEE UUID 52117b82-a948-5e0d-8ce0-c7c9eaaf6d94
     token state:   uninitialized
   Slot 1 (0x1): OP-TEE PKCS11 TA - TEE UUID 52117b82-a948-5e0d-8ce0-c7c9eaaf6d94
     token state:   uninitialized
   Slot 2 (0x2): OP-TEE PKCS11 TA - TEE UUID 52117b82-a948-5e0d-8ce0-c7c9eaaf6d94
     ...

In the commands below, ``M`` is set to the module path to keep them short:

.. code-block:: bash

   M=/usr/lib/libckteec.so.0

Initialize a Token
~~~~~~~~~~~~~~~~~~

Initialize the token with a label and a security officer (SO) PIN, then set
the user PIN that applications log in with. Choose your own PINs:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --slot 0 --init-token --label device --so-pin <so-pin>
   Token successfully initialized
   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device --login --so-pin <so-pin> --init-pin --pin <user-pin>
   User PIN successfully initialized

Re-initializing a token deletes every key in it.

Generate a Signing Key
~~~~~~~~~~~~~~~~~~~~~~

Generate an elliptic curve key pair inside OP-TEE:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device --login --pin <user-pin> \
       --keypairgen --key-type EC:prime256v1 --id 01 --label device-key
   Key pair generated:
   Private Key Object; EC
     label:      device-key
     ID:         1 (0x01)
     Usage:      sign, derive
     Access:     sensitive, always sensitive, never extractable, local
     uri:        pkcs11:model=OP-TEE%20TA;manufacturer=Linaro;serial=0000000000000000;token=device;id=%01;object=device-key;type=private
   Public Key Object; EC  EC_POINT 256 bits
     ...
     label:      device-key
     ID:         1 (0x01)
     Usage:      verify, derive
     Access:     local

``never extractable`` means the private key cannot be exported from the
token, even by an application that knows the PIN. It can only be used for
signing inside OP-TEE.

Sign and Verify
~~~~~~~~~~~~~~~

Sign a file with the private key, export the public key, and verify the
signature with OpenSSL:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device --login --pin <user-pin> \
       --sign --mechanism ECDSA-SHA256 --id 01 --signature-format openssl \
       --input-file msg.txt --output-file msg.sig
   Using signature algorithm ECDSA-SHA256
   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device \
       --read-object --type pubkey --id 01 --output-file device-key.der
   root@imx93-cargt-00363-00428:~# openssl pkey -pubin -inform DER -in device-key.der -out device-key.pem
   root@imx93-cargt-00363-00428:~# openssl dgst -sha256 -verify device-key.pem -signature msg.sig msg.txt
   Verified OK

The public key can be given to a server or certificate authority, for
example to create a device certificate.

Encrypt Data with a Secret Key
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a 256-bit AES key and use it to encrypt and decrypt a file. With
``AES-CBC`` the input length must be a multiple of 16 bytes; use a fresh
random IV for each file in real use:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device --login --pin <user-pin> \
       --keygen --key-type AES:32 --id 02 --label data-key
   Key generated:
   Secret Key Object; AES length 32
     label:      data-key
     ID:         2 (0x02)
     Usage:      encrypt, decrypt
     Access:     never extractable, local
   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device --login --pin <user-pin> \
       --encrypt --mechanism AES-CBC --iv 000102030405060708090a0b0c0d0e0f --id 02 \
       --input-file secret.bin --output-file secret.enc
   Using encrypt algorithm AES-CBC
   root@imx93-cargt-00363-00428:~# pkcs11-tool --module $M --token-label device --login --pin <user-pin> \
       --decrypt --mechanism AES-CBC --iv 000102030405060708090a0b0c0d0e0f --id 02 \
       --input-file secret.enc --output-file secret.dec
   Using decrypt algorithm AES-CBC

``pkcs11-tool`` prints two ``C_GetAttributeValue`` warnings for secret keys.
They are expected: the key value is sensitive and cannot be read.

``pkcs11-tool --module $M --list-mechanisms`` lists everything the token
supports, including RSA up to 4096 bits, ECDSA and EdDSA, ECDH, HMAC, and
AES in ECB, CBC, CTR, GCM and CMAC modes. ``AES-CBC-PAD`` is not supported.

Managing Keys
~~~~~~~~~~~~~

.. code-block:: bash

   pkcs11-tool --module $M --token-label device --login --pin <user-pin> --list-objects
   pkcs11-tool --module $M --token-label device --login --pin <user-pin> --delete-object --type privkey --id 01

Applications can use the same keys through the PKCS#11 API with
``libckteec``, or through OpenSSL with the ``pkcs11-provider`` package from
the Cargt package feed (see :doc:`package-management`).

Where the Keys Are Stored
-------------------------

OP-TEE secure storage on Cargt images uses the normal file system (OP-TEE's
REE FS). ``tee-supplicant`` keeps the encrypted files in ``/var/lib/tee``,
readable only by the ``teesuppl`` user. Their contents are encrypted with
keys derived from the SoC's hardware unique key, so the files are useless on
another board.

.. warning::

   - On images published so far, ``/var/lib/tee`` is on the
     root file system. A full software update (SWUpdate on i.MX) installs a
     new root file system in the other partition, so tokens and keys created
     before the update are not there afterwards. Cargt has a BSP change that
     moves the storage to ``/data/tee``, shared by both root partitions, but
     it is not yet in the published images. Until then, plan key
     provisioning around updates, or start ``tee-supplicant`` with
     ``--fs-parent-path=/data/tee`` from your own layer. Keys created in
     ``/var/lib/tee`` are not moved automatically.
   - REE FS has no rollback protection: someone with access to the file
     system can restore an older copy of the files. OP-TEE's RPMB storage on
     the eMMC protects against this but is not enabled in Cargt images.

Other ELE Features
------------------

- **Hardware random numbers:** the ELE TRNG is the kernel's hardware RNG
  (``cat /sys/class/misc/hw_random/rng_current`` shows ``ele-trng``) and
  feeds the kernel's random pool, so applications should read
  ``/dev/urandom`` as usual. Reading ``/dev/hwrng`` directly is slow, about
  3 kB/s.
- **ELE HSM API:** NXP's ``imx-secure-enclave`` library (``libele_hsm``)
  and ``nvm_daemon`` give direct access to the ELE's own key store. This
  needs application code written against NXP's HSM API; see the API
  documents in the ``imx-secure-enclave`` source.

.. danger::

   Do not run NXP's ``ele_hsm_test`` on a board you want to keep in its
   current state. Depending on how it was built, it writes test keys to
   one-time-programmable fuses, which cannot be undone.

The kernel's trusted keys (``keyctl add trusted``) are not available on
i.MX 9: Cargt kernels build them only for CAAM, which these processors do
not have.

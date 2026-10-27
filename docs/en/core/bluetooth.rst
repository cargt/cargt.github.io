.. _bluetooth:

Bluetooth
=========

Cargt SOMs with an NXP IW610 or IW612 module have Bluetooth 5 (Classic and
Low Energy). The ``btnxpuart`` driver loads the Bluetooth firmware at boot,
and BlueZ (``bluetoothd``) manages the controller. Use ``bluetoothctl`` to
control it, and ``btmon`` to watch the traffic between BlueZ and the
controller.

Checking the Controller
-----------------------

The examples on this page are from i.MX 93 00363 SOMs (IW612) on 00428
carriers. The kernel log shows the controller coming up with the firmware
the Wi-Fi driver loaded; see `Bluetooth Device Address`_:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# dmesg | grep hci0:
   [   15.943019] Bluetooth: hci0: FW already running.

Start ``bluetoothctl`` and run ``show``:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# bluetoothctl
   [bluetoothctl]> show
   Controller 00:11:22:33:44:5D (public)
           Manufacturer: 0x0025 (37)
           Version: 0x0f (15)
           Name: imx93-cargt-00363-00428
           Alias: imx93-cargt-00363-00428
           Powered: yes
           Discoverable: no
           Pairable: yes
           ...
           Roles: central
           Roles: peripheral
   Advertising Features:
           ActiveInstances: 0x00 (0)
           SupportedInstances: 0x06 (6)

Manufacturer 37 is NXP. ``Roles`` shows the controller can act as both an
LE central and an LE peripheral.

.. note::

   ``bluetoothctl`` is meant to be used interactively. Run with a single
   command on its command line (``bluetoothctl show``), it exits before it
   connects to ``bluetoothd`` and prints nothing. In scripts, pipe the
   commands into it or use the BlueZ D-Bus API, for example:

   .. code-block:: bash

      busctl get-property org.bluez /org/bluez/hci0 org.bluez.Adapter1 Address Powered

.. _bluetooth-address:

Bluetooth Device Address
------------------------

``show`` and ``hciconfig`` report the controller's address. Which address
the controller uses depends on which firmware brought Bluetooth up:

- **Combined Wi-Fi and Bluetooth firmware** (normal): the Wi-Fi driver loads
  ``nxp/sduart_nw61x_v1.bin.se``, as set in
  ``/lib/firmware/nxp/wifi_mod_para.conf``, and Bluetooth starts with it.
  The Bluetooth driver then logs ``FW already running``, and the controller
  uses the address stored in the module, which survives power cycles.
- **Bluetooth-only firmware**: if the Bluetooth driver starts first, it
  downloads ``nxp/uartspi_n61x_v1.bin.se`` itself (``FW Download Complete``
  in ``dmesg``), and the controller reports the placeholder address
  ``88:88:88:88:88:88``. Every board then has the same address, so two of
  them cannot work near each other. This was seen on an older image; newer
  Cargt BSP builds make the Wi-Fi driver load first.

.. code-block:: text

   root@imx93-cargt-00363-00428:~# dmesg | grep hci0:
   [   15.943019] Bluetooth: hci0: FW already running.

To set an address yourself, power the controller off while you change it.
The address lasts until the firmware is loaded again:

.. code-block:: text

   [bluetoothctl]> power off
   [bluetoothctl]> menu mgmt
   [mgmt]> public-addr 00:11:22:33:44:55
   [mgmt]> back
   [bluetoothctl]> power on

Scanning for Devices
--------------------

.. code-block:: text

   [bluetoothctl]> scan on          # Classic and LE
   [bluetoothctl]> scan le          # LE only
   [bluetoothctl]> scan off
   [bluetoothctl]> devices

New devices appear as ``[NEW] Device <address> <name>`` while the scan runs.

The controller uses the Bluetooth 5 extended scan commands. Older tools
that use the legacy commands, such as ``hcitool lescan``, fail with
``Set scan parameters failed: Input/output error``, and ``btmon`` shows the
controller answering ``Command Disallowed``. Use ``bluetoothctl`` instead.

LE Advertising
--------------

To make the board visible to phones and other central devices, advertise
its name:

.. code-block:: text

   [bluetoothctl]> menu advertise
   [advertise]> name on
   [advertise]> back
   [bluetoothctl]> advertise on
   hci0 advertising_added: instance 1
   [CHG] Controller 00:11:22:33:44:51 ActiveInstances: 0x01 (1)
   Advertising object registered
   [bluetoothctl]> advertise off

The ``advertise`` menu also sets service UUIDs (``uuids``), manufacturer
data (``manufacturer``), the advertising interval (``interval``) and a
timeout (``timeout``).

GATT Server and Client
----------------------

``bluetoothctl`` can publish a simple GATT service, which is enough to test
LE connections between two boards or with a phone app such as nRF Connect.
In this example, one i.MX 93 00363 board is the server (peripheral) and a
second one is the client (central).

On the server, register a service with one characteristic that supports
read, write and notify, then advertise it:

.. code-block:: text

   [bluetoothctl]> menu gatt
   [bluetoothctl]> register-service 12345678-1234-5678-1234-56789abcdef0
   [/org/bluez/app/service0] Primary (yes/no): yes
   [bluetoothctl]> register-characteristic 12345678-1234-5678-1234-56789abcdef1 read,write,notify
   [/org/bluez/app/service0/chrc0] Enter value: 0x00
   [bluetoothctl]> register-application
   [bluetoothctl]> back
   [bluetoothctl]> menu advertise
   [advertise]> name cargt-ble-demo
   [advertise]> uuids 12345678-1234-5678-1234-56789abcdef0
   [advertise]> back
   [bluetoothctl]> advertise on

To change the value, and send a notification to subscribed clients, select
the local characteristic and write it:

.. code-block:: text

   [bluetoothctl]> menu gatt
   [bluetoothctl]> select-attribute local 12345678-1234-5678-1234-56789abcdef1
   [/org/bluez/app/service0/chrc0]> write 0x15

On the client, scan, connect, and use the characteristic. The connection can
take 15 to 20 seconds while the client reads the server's services:

.. code-block:: text

   [bluetoothctl]> scan le
   [NEW] Device 00:11:22:33:44:51 cargt-ble-demo
   [bluetoothctl]> scan off
   [bluetoothctl]> connect 00:11:22:33:44:51
   Attempting to connect to 00:11:22:33:44:51
   [CHG] Device 00:11:22:33:44:51 Connected: yes
   Connection successful
   [CHG] Device 00:11:22:33:44:51 ServicesResolved: yes
   [cargt-ble-demo]> menu gatt
   [cargt-ble-demo]> select-attribute 12345678-1234-5678-1234-56789abcdef1
   [cargt-ble-demo:/service001c/char001d]> read
   [CHG] Attribute /org/bluez/hci0/dev_00_11_22_33_44_51/service001c/char001d Value:
     12                                               .
   [cargt-ble-demo:/service001c/char001d]> write 0x80
   [cargt-ble-demo:/service001c/char001d]> notify on
   Notify started
   [CHG] Attribute /org/bluez/hci0/dev_00_11_22_33_44_51/service001c/char001d Value:
     15                                               .
   [CHG] Attribute /org/bluez/hci0/dev_00_11_22_33_44_51/service001c/char001d Value:
     16                                               .
   [cargt-ble-demo:/service001c/char001d]> notify off
   Notify stopped
   [cargt-ble-demo:/service001c/char001d]> back
   [cargt-ble-demo]> disconnect 00:11:22:33:44:51

The server logs each request:

.. code-block:: text

   [/org/bluez/app/service0/chrc0 (Vendor specific)] ReadValue: 00:11:22:33:44:5D offset 0 link LE
   [/org/bluez/app/service0/chrc0 (Vendor specific)] WriteValue: 00:11:22:33:44:5D offset 0 link LE
     80                                               .
   AcquireNotify: 00:11:22:33:44:5D link LE

``list-attributes <address>`` on the client lists every service,
characteristic and descriptor the server offers.

Pairing
-------

To pair and bond with an LE device that needs it (for example one whose
characteristics require encryption), use an agent and ``pair``:

.. code-block:: text

   [bluetoothctl]> agent NoInputNoOutput
   [bluetoothctl]> default-agent
   [bluetoothctl]> pair <address>
   [bluetoothctl]> trust <address>

``agent NoInputNoOutput`` selects "just works" pairing for devices without
a display or keyboard; use ``agent KeyboardDisplay`` to confirm passkeys.

.. warning::

   LE pairing does not complete on Cargt images published up to October
   2026. ``pair`` connects, but the kernel never starts the pairing
   exchange and logs ``Bluetooth: hci0: security requested but not
   available``; ``bluetoothctl`` reports
   ``Failed to pair: org.bluez.Error.AuthenticationCanceled``. Connections
   and GATT access that do not need encryption, as in the example above,
   work; characteristics that require encryption fail with
   ``Insufficient Encryption``. Cargt has fixed this in the BSP, and pairing
   works in both directions on the fixed builds, but the fix is not yet in
   the published images.

Debugging with btmon
--------------------

``btmon`` decodes every command and event between BlueZ and the controller.
Run it in a second terminal while you reproduce a problem:

.. code-block:: bash

   btmon                        # live decoded trace
   btmon -w /tmp/bt.snoop       # save a trace (opens in Wireshark)
   btmon -r /tmp/bt.snoop       # read a saved trace

``journalctl -u bluetooth`` shows the ``bluetoothd`` log.

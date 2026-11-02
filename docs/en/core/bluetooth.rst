.. _bluetooth:

Bluetooth
=========

Cargt SOMs with an NXP IW610 or IW612 module have Bluetooth 5 (Classic and
Low Energy). On i.MX images, the Wi-Fi driver loads the module's combined
Wi-Fi and Bluetooth firmware at boot. ``nxp-bluetooth.service`` then loads
the ``btnxpuart`` Bluetooth driver, which attaches to the running firmware,
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

``trust`` lets the device reconnect later without asking. To use a paired
device, such as a Bluetooth LE mouse or keyboard, connect to it; ``info``
shows whether it is paired, trusted and connected:

.. code-block:: text

   [bluetoothctl]> connect <address>
   [bluetoothctl]> info <address>

``remove <address>`` deletes the pairing.

Bluetooth on Your Own Carrier
-----------------------------

The Bluetooth half of the IW610 and IW612 modules is connected to the
processor over a UART with hardware flow control (RTS and CTS). The
``btnxpuart`` driver finds it through a ``bluetooth`` child node of that UART
in the device tree; no ``hciattach`` command is needed. In the i.MX 93 00363
SOM's device tree, the module is on ``lpuart5``:

.. code-block:: dts

   &lpuart5 { /* bluetooth */
           pinctrl-names = "default";
           uart-has-rtscts;
           pinctrl-0 = <&pinctrl_uart5>;
           status = "okay";

           bluetooth {
                   compatible = "nxp,88w8997-bt";
                   fw-init-baudrate = <3000000>;
                   max-speed = <3000000>;
           };
   };

- ``compatible``: ``nxp,88w8997-bt`` on the i.MX SOMs with the IW612, and
  ``nxp,88w8987-bt`` on the STM32MP2 00395 with the IW610.
- ``fw-init-baudrate``: the UART speed the module uses once its firmware is
  running. It is set in the module's one-time-programmable configuration
  during production, and the device tree must match it; Cargt modules are
  configured for 3000000.
- ``max-speed``: the speed the driver then runs the UART at.

These come from the SOM's device tree, so a carrier board's device tree
normally inherits them unchanged. Check the node on a running board through
the controller's device:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# readlink -f /sys/class/bluetooth/hci0/device/of_node
   /sys/firmware/devicetree/base/soc@0/bus@42000000/serial@42590000/bluetooth
   root@imx93-cargt-00363-00428:~# basename $(readlink /sys/class/bluetooth/hci0/device/driver)
   btnxpuart

Older notes for these modules attach the controller by hand with
``hciattach /dev/ttyLPx any 115200 flow`` and switch it to 3 Mbaud with a
vendor HCI command. With the ``btnxpuart`` node in place, the driver does
both, and ``hciattach`` is not needed. The i.MX 8M Plus 00377 is the
exception: its device tree has no ``bluetooth`` node, and
``nxp-bluetooth.service`` attaches the controller with ``hciattach`` on
``/dev/ttymxc0``.

Debugging with btmon
--------------------

``btmon`` decodes every command and event between BlueZ and the controller.
Run it in a second terminal while you reproduce a problem:

.. code-block:: bash

   btmon                        # live decoded trace
   btmon -w /tmp/bt.snoop       # save a trace (opens in Wireshark)
   btmon -r /tmp/bt.snoop       # read a saved trace

``journalctl -u bluetooth`` shows the ``bluetoothd`` log.

When hci0 Does Not Appear
-------------------------

Check the service that starts Bluetooth, and the kernel log:

.. code-block:: bash

   systemctl status nxp-bluetooth
   dmesg | grep -iE "btnxpuart|Bluetooth: hci0"
   hciconfig -a

On a working i.MX 93 00363, the kernel log shows the driver binding and the
controller finding the firmware the Wi-Fi driver loaded:

.. code-block:: text

   [   14.318817] btnxpuart serial0-0: supply vcc not found, using dummy regulator
   [   15.335067] Bluetooth: hci0: FW already running.

The ``supply vcc not found`` line is harmless.

**STM32MP2 00395 (IW610): frame reassembly errors.** If the kernel log shows
``hci0: Frame reassembly failed (-84)`` followed by ``Opcode 0x0c03 failed:
-110``, and ``nxp-bluetooth.service`` fails with ``Can't init device hci0:
Connection timed out``, the module's Bluetooth UART is running at a
different speed from the 3000000 in the device tree. This happens on IW610
modules whose one-time-programmable configuration was not set in
production: they run at 115200, and when reached at that speed they report
the placeholder address ``88:88:88:88:88:88`` instead of an address of
their own, such as ``00:08:EE:...`` on a correctly configured module. There is no
software fix for an unconfigured module; contact Cargt.


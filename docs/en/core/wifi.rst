.. _wifi:

Wi-Fi
=====

Cargt SOMs with an NXP IW610 or IW612 module have dual-band (2.4 and 5 GHz)
Wi-Fi 6. NetworkManager manages it, as it does Ethernet; see
:ref:`networking` for the basics of ``nmcli`` and ``nmtui``. Bluetooth on the
same module is covered in :doc:`bluetooth`.

.. contents:: On this page
   :local:
   :depth: 1

The Wi-Fi Hardware
------------------

The examples on this page are from i.MX 93 00363 SOMs (IW612) on 00428 and
00365 carriers, running wrynose images.

The IW612 is connected over SDIO. ``nxp-wifi.service`` loads NXP's ``moal``
and ``mlan`` drivers at boot with the options in
``/lib/firmware/nxp/wifi_mod_para.conf``:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# systemctl cat nxp-wifi
   # /usr/lib/systemd/system/nxp-wifi.service
   [Unit]
   Description=NXP WiFi service
   After=network.target

   [Service]
   Type=simple
   ExecStart=/usr/bin/env modprobe moal mod_para=nxp/wifi_mod_para.conf drvdbg=0x00000000
   ExecStartPost=/usr/bin/sleep 3

   [Install]
   WantedBy=multi-user.target

The service only runs ``modprobe``, so ``systemctl status nxp-wifi`` shows it
as ``inactive (dead)`` with ``status=0/SUCCESS`` once the drivers are
loaded. That is normal. ``lsmod`` shows the drivers:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# lsmod | grep -E "moal|mlan"
   moal                  901120  3
   mlan                  684032  1 moal

The ``SDIW612`` block in ``wifi_mod_para.conf`` names the firmware,
``nxp/sduart_nw61x_v1.bin.se``. It is the combined Wi-Fi and Bluetooth
firmware, so loading it also starts Bluetooth; see
:ref:`bluetooth-address`.

The driver creates three interfaces on one radio:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 20 80

   * - Interface
     - Use
   * - ``mlan0``
     - Client (station): joins an access point.
   * - ``uap0``
     - Access point. See `Access Point Mode`_.
   * - ``wfd0``
     - Wi-Fi Direct (peer to peer).

NetworkManager also lists a ``p2p-dev-`` device for each of them. ``iw dev``
shows the interfaces (MAC addresses replaced):

.. code-block:: text

   root@imx93-cargt-00363-00428:~# iw dev
   phy#0
           Interface wfd0
                   ifindex 5
                   wdev 0x3
                   addr 02:00:00:00:00:03
                   type managed
                   txpower 8.00 dBm
           Interface uap0
                   ifindex 4
                   wdev 0x2
                   addr 02:00:00:00:00:02
                   type managed
                   txpower 8.00 dBm
           Interface mlan0
                   ifindex 3
                   wdev 0x1
                   addr 02:00:00:00:00:01
                   type managed
                   txpower 8.00 dBm

``iw phy`` shows the radio's capabilities: 2.4 and 5 GHz bands with Wi-Fi 6
(HE) for client, access point and Wi-Fi Direct use. Its interface
combinations line shows that the interfaces share one channel:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# iw phy | grep -A2 "valid interface combinations"
           valid interface combinations:
                    * #{ managed, AP, monitor, P2P-client, P2P-GO } <= 4,
                      total <= 4, #channels <= 1, STA/AP BI must match, ...

Because of ``#channels <= 1``, a board that runs an access point on
``uap0`` and a client connection on ``mlan0`` at the same time uses the same
channel for both. The single radio is also why scans disturb a connected
link; see `Keeping a Wi-Fi Link Up`_.

Scanning
~~~~~~~~

``--rescan yes`` waits for a fresh scan. With example network names:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# nmcli -f SSID,CHAN,FREQ,SIGNAL,SECURITY device wifi list ifname mlan0 --rescan yes
   SSID         CHAN  FREQ      SIGNAL  SECURITY
   office-5G    44    5220 MHz  77      WPA2 802.1X
   guest        44    5220 MHz  75      WPA2
   lab-ap       56    5280 MHz  74      WPA2 WPA3
   office       2     2417 MHz  72      WPA2 WPA3
   ...

``iw dev mlan0 link`` shows the current connection, or ``Not connected.``;
there is an example of a connected link in `Access Point Mode`_.

.. _wifi-regulatory:

Regulatory Domain
~~~~~~~~~~~~~~~~~

Cargt images do not set a country, so the radio uses the world regulatory
domain (``country 00``). The kernel also logs that it has no regulatory
database (``Direct firmware load for regulatory.db failed``):

.. code-block:: text

   root@imx93-cargt-00363-00428:~# iw reg get
   global
   country 00: DFS-UNSET
           (2402 - 2472 @ 40), (6, 20), (N/A)
           (2457 - 2482 @ 20), (6, 20), (N/A), AUTO-BW, PASSIVE-SCAN
           (2474 - 2494 @ 20), (6, 20), (N/A), NO-OFDM, PASSIVE-SCAN
           (5170 - 5250 @ 80), (6, 20), (N/A), AUTO-BW, PASSIVE-SCAN
           (5250 - 5330 @ 80), (6, 20), (0 ms), DFS, AUTO-BW, PASSIVE-SCAN
           (5490 - 5730 @ 160), (6, 20), (0 ms), DFS, PASSIVE-SCAN
           (5735 - 5835 @ 80), (6, 20), (N/A), PASSIVE-SCAN
           (57240 - 63720 @ 2160), (N/A, 0), (N/A)

``PASSIVE-SCAN`` means the radio may only listen on those frequencies until
it hears an access point there; it may not start transmitting on its own.
The board can still join 5 GHz networks as a client, but only 2.4 GHz
channels 1 to 11 (2402–2472 MHz) are free of that restriction. That is why
the access point below uses 2.4 GHz.

Connecting to a Network
-----------------------

Connect to an access point with:

.. code-block:: bash

   nmcli device wifi list
   nmcli device wifi connect <ssid> password <password>

This creates a saved connection named after the SSID. The
:ref:`static address example <networking-static-ip>` also works for Wi-Fi
connections, with ``ifname mlan0``.

Joining a Network with nmtui
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In ``nmtui`` (see :ref:`networking-nmtui`), **Activate a connection** lists
the saved connections and the Wi-Fi networks in range. ``*`` marks the
active connections. Select a network and **<Activate>**; ``nmtui`` asks for
the password and saves a connection for the network. With example network
names:

.. code-block:: text

   ┌───────────────────────────────────────────────────────────┐
   │                                                           │
   │ ┌──────────────────────────────────────────┐              │
   │ │ Wired                                  ↑ │ <Deactivate> │
   │ │ * Wired connection 1                   ▮ │              │
   │ │                                        ▒ │              │
   │ │ Wi-Fi (mlan0)                          ▒ │              │
   │ │   office                         ▂▄▆█  ▒ │              │
   │ │   office-5G                      ▂▄▆█  ▒ │              │
   │ │   guest                          ▂▄▆_  ▒ │              │
   │ │   lab-ap                         ▂▄__  ▒ │              │
   ...

The same screen deactivates a connection. Deactivating the connection your
SSH session uses disconnects you.

.. _wifi-access-point:

Access Point Mode
-----------------

A board can run its own Wi-Fi network, for example so a phone or laptop can
connect to a setup page on the board in the field. On NXP IW610 and IW612
modules, run the access point on ``uap0``, the driver's access point
interface, rather than on ``mlan0``, the client interface.

``ipv4.method shared`` makes NetworkManager give ``uap0`` an address and
run a DHCP and DNS server for the devices that connect:

.. code-block:: bash

   nmcli connection add type wifi ifname uap0 con-name cargt-ap \
       ssid my-device-setup mode ap \
       wifi.band bg wifi.channel 6 \
       wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn \
       wifi-sec.pairwise ccmp wifi-sec.group ccmp \
       wifi-sec.psk "<passphrase of 8 to 63 characters>" \
       ipv4.method shared ipv4.addresses 192.168.60.1/24 \
       ipv6.method disabled
   nmcli connection up cargt-ap

The access point starts at boot from then on.

.. note::

   Use 2.4 GHz (``wifi.band bg``) for the access point; see
   `Regulatory Domain`_.

Checking it, on an i.MX 93 00363 with an IW612 on the 00365 carrier:

.. code-block:: text

   root@imx93-cargt-00363-00365:~# nmcli -f GENERAL.CONNECTION,GENERAL.STATE,IP4 device show uap0
   GENERAL.CONNECTION:                     cargt-ap
   GENERAL.STATE:                          100 (connected)
   IP4.ADDRESS[1]:                         192.168.60.1/24
   IP4.GATEWAY:                            --
   IP4.ROUTE[1]:                           dst = 192.168.60.0/24, nh = 0.0.0.0, mt = 600

   root@imx93-cargt-00363-00365:~# iw dev uap0 info
   Interface uap0
           ifindex 5
           wdev 0x2
           addr 02:50:43:02:ff:01
           ssid my-device-setup
           type AP
           wiphy 0
           channel 6 (2437 MHz), width: 20 MHz, center1: 2437 MHz
           txpower 8.00 dBm

A second Cargt board can join the access point as a client, on ``mlan0``.
Scan first (``--rescan yes`` waits for a fresh scan), then connect:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# nmcli -f SSID,CHAN,SIGNAL device wifi list ifname mlan0 --rescan yes
   SSID                            CHAN  SIGNAL
   my-device-setup                 6     100
   ...
   root@imx93-cargt-00363-00428:~# nmcli device wifi connect my-device-setup password "<passphrase>" ifname mlan0
   Device 'mlan0' successfully activated with '3bc72d89-13c9-4bb8-9280-e317f1cb1824'.
   root@imx93-cargt-00363-00428:~# nmcli -f GENERAL.CONNECTION,IP4 device show mlan0
   GENERAL.CONNECTION:                     my-device-setup
   IP4.ADDRESS[1]:                         192.168.60.149/24
   IP4.GATEWAY:                            192.168.60.1
   IP4.ROUTE[1]:                           dst = 192.168.60.0/24, nh = 0.0.0.0, mt = 600
   IP4.ROUTE[2]:                           dst = 0.0.0.0/0, nh = 192.168.60.1, mt = 600
   IP4.DNS[1]:                             192.168.60.1
   root@imx93-cargt-00363-00428:~# iw dev mlan0 link
   Connected to 02:00:00:00:00:01 (on mlan0)
           SSID: my-device-setup
           freq: 2437.0
           signal: -34 dBm
           rx bitrate: 143.3 MBit/s HE-MCS 11 HE-NSS 1 HE-GI 0 HE-DCM 0
           tx bitrate: 143.3 MBit/s HE-MCS 11 HE-NSS 1 HE-GI 0 HE-DCM 0

The client's Wi-Fi default route has metric 600, so its Ethernet connection
(metric 100) stays the preferred route. Between two i.MX 93 00363 boards a
few centimetres apart, ``iperf3`` measured about 100 Mbit/s over TCP.

On the access point, list the devices that have connected and the addresses
they were given:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# iw dev uap0 station dump | grep -E "Station|signal:"
   Station 00:11:22:33:44:55 (on uap0)
           signal:         -34 dBm
   root@imx93-cargt-00363-00428:~# cat /var/lib/NetworkManager/dnsmasq-uap0.leases
   1793130843 00:11:22:33:44:55 192.168.60.149 imx93-cargt-00363-00428 01:00:11:22:33:44:55

Devices on the access point can reach the board.

To stop the access point, or remove it:

.. code-block:: bash

   nmcli connection down cargt-ap
   nmcli connection delete cargt-ap

.. _wifi-link-up:

Keeping a Wi-Fi Link Up
-----------------------

Wi-Fi modules such as the IW610 and IW612 have a single radio (1x1) shared
by ``mlan0``, ``uap0`` and ``wfd0``. Whenever any of these interfaces
scans, the radio leaves the operating channel to listen on the others, and
traffic on the connected interface is delayed or lost until it returns. A
full scan covers 39 channels on 2.4 and 5 GHz and takes about 7.5 seconds.
For a control link that must respond quickly, prevent scans while connected.

**Unmanage the Wi-Fi interfaces you do not use.** NetworkManager treats
``uap0`` and ``wfd0`` as Wi-Fi devices, and while they are disconnected it
scans on them in the background, every 20 seconds to 2 minutes. These
scans disrupt ``mlan0`` even though nothing uses those interfaces. Tell
NetworkManager to leave them alone with a configuration file, for example
``/etc/NetworkManager/conf.d/90-unmanaged-wifi.conf``:

.. code-block:: ini

   [keyfile]
   unmanaged-devices=interface-name:uap0;interface-name:wfd0

Apply it with ``nmcli general reload conf`` or a reboot; ``nmcli device``
then shows the two interfaces as ``unmanaged``. On a board that runs an
access point on ``uap0`` and does not use the client interface, unmanage
``mlan0`` and ``wfd0`` instead. For a product, install the file from your
own layer.

**Lock the connection to one access point.** While connected,
wpa_supplicant scans for better access points to roam to. NetworkManager
configures it to scan every 30 seconds when the signal is weaker than
−70 dBm (−65 dBm when it has seen more than one access point for the
network), and once a day otherwise. Setting the access point's BSSID turns
these scans off completely:

.. code-block:: bash

   nmcli connection modify <connection> 802-11-wireless.bssid <access point MAC address>
   nmcli connection up <connection>

The board then no longer roams to another access point with the same SSID,
and the BSSID has to be updated if the access point is replaced.

Scans that something asks for still happen: ``nmcli device wifi list``,
``nmcli device wifi rescan`` and the ``nmtui`` **Activate a connection**
screen all scan. Avoid running them on a board that is in use.

Measured on two i.MX 93 00363 boards on the 00428 carrier, one running an
access point on ``uap0`` (2.4 GHz, channel 6) and the other connected to it
on ``mlan0`` at −21 dBm. One board sent a UDP packet every 10 ms and the
other echoed it, for 2 minutes per test. Because both boards have an IW612,
the change was made on both:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 15 25 20

   * - Configuration
     - Lost
     - Round trip over 50 ms
     - Longest round trip
   * - Default
     - 72 of 12,001
     - 5,062 (42%)
     - 2,044 ms
   * - Unused interfaces unmanaged
     - 0
     - 8
     - 83 ms
   * - Unused interfaces unmanaged, BSSID locked, power saving off
       (three runs)
     - 0
     - 4 to 23
     - 80 to 136 ms

With the default configuration, ``iw event -t`` on the client showed scans
on ``uap0`` and ``wfd0`` for most of the test, and none on ``mlan0``: at
this signal strength wpa_supplicant's own scans did not start. A single
requested scan on ``mlan0`` took 7.4 seconds, during which 40% of the packets
were delayed by more than 50 ms (up to 194 ms) and 4 were lost.

To see whether scans happen on your board, watch for them while it runs:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# iw event -t
   1793204657.559765: uap0 (phy #0): scan started
   1793204664.136950: uap0 (phy #0): scan finished: 2412 2417 2422 ... 5825, ""

Other settings worth considering for a control link:

- Turn off Wi-Fi power saving with
  ``nmcli connection modify <connection> 802-11-wireless.powersave 2``. In
  the tests above, at short range, it made no measurable difference.
- Keep the signal stronger than about −65 dBm.
- Make the control protocol detect a lost link, for example with
  heartbeats and a safe stop on timeout. No setting prevents every gap: the
  link can still drop and reconnect.

.. _networking:

Networking with NetworkManager
==============================

NetworkManager manages the Ethernet, Wi-Fi and cellular interfaces on Cargt
images, for both i.MX and STM32MP2. ``systemd-networkd`` is also installed,
but it is told to leave the Ethernet interfaces alone, and it only sets up
the CAN interfaces.

Use ``nmcli`` to configure NetworkManager. The images do not include
``nmtui``.

.. contents:: On this page
   :local:
   :depth: 1

Basics
------

NetworkManager has **devices** (network interfaces such as ``eth0``) and
**connections** (saved settings profiles). A device is configured by
activating a connection on it.

.. code-block:: bash

   nmcli device                    # interfaces and their state
   nmcli connection                # saved connections
   nmcli device show eth0          # addresses, gateway and DNS on eth0
   ip addr show eth0               # the same, from iproute2

Output from an i.MX 93 00363 on the 00365 carrier, with a cable in
``eth0`` only:

.. code-block:: text

   root@imx93-cargt-00363-00365:~# nmcli device
   DEVICE         TYPE      STATE                   CONNECTION
   eth0           ethernet  connected               Wired connection 1
   lo             loopback  connected (externally)  lo
   mlan0          wifi      disconnected            --
   uap0           wifi      disconnected            --
   wfd0           wifi      disconnected            --
   p2p-dev-mlan0  wifi-p2p  disconnected            --
   p2p-dev-uap0   wifi-p2p  disconnected            --
   p2p-dev-wfd0   wifi-p2p  disconnected            --
   eth1           ethernet  unavailable             --
   can0           can       unmanaged               --
   can1           can       unmanaged               --

``eth1`` is ``unavailable`` because it has no cable. The CAN interfaces are
``unmanaged`` because ``systemd-networkd`` sets them up.

When an Ethernet port has no saved connection, NetworkManager creates a
temporary DHCP connection for it, named ``Wired connection 1``,
``Wired connection 2`` and so on. That is why a new board gets an address
from DHCP with no configuration. To change a port's settings, create a
connection for it with ``nmcli connection add``, as in the examples below.
It takes the place of the temporary one.

Connections you create are saved as keyfiles in
``/etc/NetworkManager/system-connections/`` and are activated automatically
at boot.

Interface names:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 25 75

   * - Interface
     - Hardware
   * - ``eth0``, ``eth1``
     - Ethernet ports. ``eth0`` is the first port (ETH_A on OSM-L
       carriers).
   * - ``mlan0``
     - Wi-Fi station on NXP IW610 and IW612 modules. The driver also
       creates ``uap0`` (access point) and ``wfd0`` (Wi-Fi Direct).
   * - ``wwan0``, ``cdc-wdm0``
     - Cellular modem (names depend on the modem), managed through
       ModemManager

.. note::

   Saved connections are part of the root file system. A full software
   update (SWUpdate on i.MX, RAUC on STM32MP2) installs a new root file
   system, so connections created on the board with ``nmcli`` do not carry
   over. For products, install your connection files from your own Yocto
   layer; see `Including Connections in Your Image`_.

DHCP Client
-----------

Ethernet ports use DHCP by default. To make a named DHCP connection that
you can change later:

.. code-block:: bash

   nmcli connection add type ethernet ifname eth0 con-name eth0 \
       ipv4.method auto ipv6.method auto
   nmcli connection up eth0

To see the address, gateway and DNS servers NetworkManager received:

.. code-block:: text

   root@imx95-cargt-00414-00365:~# nmcli -f GENERAL.CONNECTION,IP4 device show eth0
   GENERAL.CONNECTION:                     Wired connection 1
   IP4.ADDRESS[1]:                         192.168.1.27/24
   IP4.GATEWAY:                            192.168.1.1
   IP4.ROUTE[1]:                           dst = 192.168.1.0/24, nh = 0.0.0.0, mt = 100
   IP4.ROUTE[2]:                           dst = 0.0.0.0/0, nh = 192.168.1.1, mt = 100
   IP4.DNS[1]:                             8.8.8.8
   IP4.DNS[2]:                             1.1.1.1

``nmcli -f DHCP4 device show eth0`` shows every option in the lease,
including the lease time and the DHCP server's address.

DHCP servers often hand out the same address to a device each time based on
its MAC address. A board without a fixed MAC address gets a new random one,
and so a new lease, at every boot; see :ref:`mac-addresses`.

To send a host name to the DHCP server (so it can register the board in DNS):

.. code-block:: bash

   nmcli connection modify eth0 ipv4.dhcp-hostname my-board
   nmcli connection up eth0

Static IP Address
-----------------

.. code-block:: bash

   nmcli connection add type ethernet ifname eth0 con-name eth0-static \
       ipv4.method manual \
       ipv4.addresses 192.168.1.50/24 \
       ipv4.gateway 192.168.1.1 \
       ipv4.dns "192.168.1.1 8.8.8.8" \
       ipv6.method disabled
   nmcli connection up eth0-static

The result, from an i.MX 95 00414 with a static address on ``eth1``
(no gateway):

.. code-block:: text

   root@imx95-cargt-00414-00365:~# nmcli -f GENERAL.CONNECTION,IP4 device show eth1
   GENERAL.CONNECTION:                     eth1-static
   IP4.ADDRESS[1]:                         192.168.50.1/24
   IP4.GATEWAY:                            --
   IP4.ROUTE[1]:                           dst = 192.168.50.0/24, nh = 0.0.0.0, mt = 101

NetworkManager saved it as a keyfile:

.. code-block:: text

   root@imx95-cargt-00414-00365:~# cat /etc/NetworkManager/system-connections/eth1-static.nmconnection
   [connection]
   id=eth1-static
   uuid=a6e04d07-1688-4996-be43-8824994a3b72
   type=ethernet
   interface-name=eth1

   [ethernet]

   [ipv4]
   address1=192.168.50.1/24
   method=manual

   [ipv6]
   addr-gen-mode=default
   method=disabled

   [proxy]

To change it later, use ``nmcli connection modify`` and then bring the
connection up again so the change takes effect:

.. code-block:: bash

   nmcli connection modify eth0-static ipv4.addresses 192.168.1.60/24
   nmcli connection up eth0-static

To add a second address to the same port:

.. code-block:: bash

   nmcli connection modify eth0-static +ipv4.addresses 10.0.0.50/24
   nmcli connection up eth0-static
   ip -4 addr show eth0

A port connected directly to a device with no router (a camera, a PLC or a
PC) needs only an address. Leave out ``ipv4.gateway`` and ``ipv4.dns``.

To go back to DHCP, delete the static connection. NetworkManager then
activates the automatic ``Wired connection`` on the port again:

.. code-block:: bash

   nmcli connection delete eth0-static

.. tip::

   If you are connected over SSH on the port you are changing, the session
   drops when the address changes. Make the change from the serial console,
   or over the other Ethernet port.

Running a DHCP Server on a Port
-------------------------------

A common setup is a board with ``eth0`` on the plant or office network and
``eth1`` serving addresses to equipment behind it. There are two ways to do
this.

Shared Mode (DHCP Server and NAT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``ipv4.method shared``, NetworkManager gives the port a static address,
starts its own dnsmasq instance to hand out addresses and answer DNS on that
port, and routes the devices on it to the board's other connections through
NAT.

The images also enable a standalone ``dnsmasq`` service, which by default
only forwards DNS queries for the board itself. It listens on DNS port 53
on every address, so NetworkManager's dnsmasq cannot start while it runs,
and the connection fails with this in ``journalctl -u NetworkManager``:

.. code-block:: text

   dnsmasq: failed to create listening socket for 192.168.50.1: Address already in use

Stop and disable the standalone service first:

.. code-block:: bash

   systemctl disable --now dnsmasq

Then create the shared connection:

.. code-block:: bash

   nmcli connection add type ethernet ifname eth1 con-name eth1-shared \
       ipv4.method shared \
       ipv4.addresses 192.168.50.1/24 \
       ipv6.method disabled
   nmcli connection up eth1-shared

Devices on ``eth1`` get addresses from ``192.168.50.10`` to
``192.168.50.254`` (one-hour leases) and use ``192.168.50.1`` as their
gateway and DNS server. Without ``ipv4.addresses``, NetworkManager uses
``10.42.0.1/24``.

.. _nat-kernel-options:

.. warning::

   Current Cargt i.MX images (wrynose, October 2026) build the kernel
   without ``CONFIG_NFT_REJECT``, which NetworkManager's NAT rules need.
   Shared mode still gives the port its address and runs the DHCP and DNS
   server, so devices on it can reach the board, but they cannot reach the
   network beyond it. NetworkManager logs
   ``firewall: nft ... Error: Could not process rule`` when this happens.
   To get NAT, add these options to the kernel in your layer with a
   configuration fragment:

   .. code-block:: text

      CONFIG_NFT_REJECT=m
      CONFIG_NFT_REJECT_INET=m

To set extra dnsmasq options for shared connections, such as a fixed
address for one device, add a file in
``/etc/NetworkManager/dnsmasq-shared.d/``:

.. code-block:: text

   # /etc/NetworkManager/dnsmasq-shared.d/eth1.conf
   dhcp-host=00:11:22:33:44:55,192.168.50.20

Then bring the connection up again.

Standalone dnsmasq (DHCP Server without NAT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need a DHCP server but not routing to the other network, give the
port a static address with NetworkManager and configure the image's
``dnsmasq`` service to serve it.

.. code-block:: bash

   nmcli connection add type ethernet ifname eth1 con-name eth1-static \
       ipv4.method manual ipv4.addresses 192.168.50.1/24 ipv6.method disabled
   nmcli connection up eth1-static

Create ``/etc/dnsmasq.d/eth1.conf``:

.. code-block:: text

   interface=eth1
   bind-interfaces
   dhcp-range=192.168.50.100,192.168.50.200,255.255.255.0,12h
   dhcp-host=00:11:22:33:44:55,192.168.50.20
   # Leave out the gateway and DNS server options: no router on this network
   dhcp-option=option:router
   dhcp-option=option:dns-server

Then restart dnsmasq and check its log:

.. code-block:: bash

   systemctl restart dnsmasq
   journalctl -u dnsmasq -f

Cellular Modems with ModemManager
---------------------------------

ModemManager detects USB and M.2 cellular modems and talks to them over QMI,
MBIM or AT commands. NetworkManager uses ModemManager to bring the data
connection up. Both run by default, and ``mmcli``, ``qmicli`` and
``mbimcli`` are included.

Checking the Modem
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   mmcli -L                  # list modems; note the modem number
   mmcli -m 0                # state, SIM, signal and access technology
   mmcli -m 0 --signal-get   # signal strength (enable with --signal-setup=10)
   mmcli -i 0                # SIM details

``mmcli -m 0`` shows the modem state. It should reach ``registered`` before a
data connection is possible. A modem that stays at ``locked`` needs the SIM
PIN; one that stays at ``searching`` or ``denied`` usually has an antenna,
coverage or SIM activation problem.

Creating the Data Connection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the APN from your carrier.

.. code-block:: bash

   nmcli connection add type gsm ifname '*' con-name cellular \
       gsm.apn <apn>
   nmcli connection up cellular

``ifname '*'`` lets the connection use whichever modem ModemManager finds.
If the SIM has a PIN, or the carrier needs a user name and password:

.. code-block:: bash

   nmcli connection modify cellular gsm.pin <pin>
   nmcli connection modify cellular gsm.username <user> gsm.password <password>

The connection comes up automatically at boot, and NetworkManager
reconnects it if the modem drops off the network.

Ethernet First, Cellular as Backup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When more than one connection has a gateway, NetworkManager adds a default
route for each, and the route with the lowest metric wins. For example, an
i.MX 95 00414 with both Ethernet ports on the same network:

.. code-block:: text

   root@imx95-cargt-00414-00365:~# ip route
   default via 192.168.1.1 dev eth0 proto dhcp src 192.168.1.27 metric 100
   default via 192.168.1.1 dev eth1 proto dhcp src 192.168.1.28 metric 101
   192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.27 metric 100
   192.168.1.0/24 dev eth1 proto kernel scope link src 192.168.1.28 metric 101

Traffic leaves through ``eth0``, the lower metric. NetworkManager's
defaults already prefer Ethernet (metric 100) to cellular (700). To make
the order explicit:

.. code-block:: bash

   nmcli connection modify eth0 ipv4.route-metric 100
   nmcli connection modify cellular ipv4.route-metric 700
   ip route                         # check which default route wins

To use cellular only for specific networks, and never as the default
route:

.. code-block:: bash

   nmcli connection modify cellular ipv4.never-default yes \
       +ipv4.routes "203.0.113.0/24"

Wi-Fi
-----

On SOMs with Wi-Fi, connect to an access point with:

.. code-block:: bash

   nmcli device wifi list
   nmcli device wifi connect <ssid> password <password>

This creates a saved connection named after the SSID. The static IP
example above also works for Wi-Fi connections, with ``ifname mlan0``.

Access Point Mode
~~~~~~~~~~~~~~~~~

A board can run its own Wi-Fi network, for example so a phone or laptop can
connect to a setup page on the board in the field. On NXP IW610 and IW612
modules, run the access point on ``uap0``, the driver's access point
interface, rather than on ``mlan0``, the client interface.

``ipv4.method shared`` makes NetworkManager give ``uap0`` an address and
run a DHCP and DNS server for the devices that connect. As for Ethernet
shared mode, stop the standalone ``dnsmasq`` service first:

.. code-block:: bash

   systemctl disable --now dnsmasq

   nmcli connection add type wifi ifname uap0 con-name cargt-ap \
       ssid my-device-setup mode ap \
       wifi.band bg wifi.channel 6 \
       wifi-sec.key-mgmt wpa-psk wifi-sec.proto rsn \
       wifi-sec.pairwise ccmp wifi-sec.group ccmp \
       wifi-sec.psk "<passphrase of 8 to 63 characters>" \
       ipv4.method shared ipv4.addresses 192.168.60.1/24 \
       ipv6.method disabled
   nmcli connection up cargt-ap

The access point starts at boot from then on. For a 5 GHz network, use
``wifi.band a`` and a 5 GHz channel such as ``36``.

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

Devices on the access point can reach the board. Reaching the network
beyond the board through NAT needs the kernel options in the
:ref:`warning above <nat-kernel-options>`; without them, the client above
could ping ``192.168.60.1`` but not addresses beyond the board.

To stop the access point, or remove it:

.. code-block:: bash

   nmcli connection down cargt-ap
   nmcli connection delete cargt-ap

Including Connections in Your Image
-----------------------------------

To ship a product with its network settings, create the connection on a
board, copy its keyfile from ``/etc/NetworkManager/system-connections/``,
and install it from a recipe in your own layer. Remove the ``uuid=`` line
so each board generates its own, and remove passwords you don't want in
your source tree.

.. code-block:: text

   # files/eth1-shared.nmconnection
   [connection]
   id=eth1-shared
   type=ethernet
   interface-name=eth1

   [ipv4]
   method=shared
   address1=192.168.50.1/24

   [ipv6]
   method=disabled

.. code-block:: bash

   # recipes-connectivity/my-network-config/my-network-config.bb
   SUMMARY = "Network connections for my product"
   LICENSE = "MIT"
   LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

   SRC_URI = "file://eth1-shared.nmconnection"

   do_install() {
       install -d ${D}${sysconfdir}/NetworkManager/system-connections
       install -m 0600 ${UNPACKDIR}/eth1-shared.nmconnection \
           ${D}${sysconfdir}/NetworkManager/system-connections/
   }

   FILES:${PN} = "${sysconfdir}/NetworkManager/system-connections"
   RDEPENDS:${PN} = "networkmanager"

Add ``my-network-config`` to ``IMAGE_INSTALL`` in your image. NetworkManager
ignores keyfiles that other users can read, so keep the mode at ``0600``.

On scarthgap builds, use ``${WORKDIR}`` in place of ``${UNPACKDIR}``.

Troubleshooting
---------------

.. code-block:: bash

   journalctl -u NetworkManager -b      # NetworkManager log for this boot
   journalctl -u ModemManager -b        # ModemManager log
   nmcli general logging level DEBUG domains ALL   # verbose logging until reboot
   nmcli connection show eth0-static    # every setting of one connection
   ethtool eth0                         # link speed and duplex

``nmcli device`` shows ``unavailable`` for an Ethernet port with no cable or
no link partner, and ``unmanaged`` for an interface NetworkManager has been
told to ignore.

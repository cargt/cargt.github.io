.. _networking:

Networking with NetworkManager
==============================

NetworkManager manages the Ethernet, Wi-Fi and cellular interfaces on Cargt
images, for both i.MX and STM32MP2. ``systemd-networkd`` is also installed,
but it is told to leave the Ethernet interfaces alone, and it only sets up
the CAN interfaces.

Use ``nmcli`` to configure NetworkManager from the command line or from
scripts. ``nmtui`` is a menu-driven alternative for configuring a board by
hand; see `Using nmtui`_.

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

NetworkManager and systemd-networkd
-----------------------------------

Both NetworkManager and ``systemd-networkd`` are installed and running.
Each interface must be managed by only one of them, so Cargt images divide
the work:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 70

   * - Service
     - Manages
   * - NetworkManager
     - Ethernet, Wi-Fi and cellular. Configure it with ``nmcli`` or
       ``nmtui``.
   * - ``systemd-networkd``
     - The CAN interfaces, from ``/etc/systemd/network/80-can0.network`` and
       ``81-can1.network``. ``50-eth0.network`` and ``51-eth1.network`` in the
       same directory mark the Ethernet ports ``Unmanaged=yes`` so that it
       leaves them to NetworkManager.
   * - ``systemd-resolved``
     - DNS. NetworkManager passes it the DNS servers of each connection
       (``resolvectl dns`` lists them). ``/etc/resolv.conf`` links to
       ``/run/systemd/resolve/resolv.conf``, which ``systemd-resolved``
       writes with those servers.

``networkctl`` lists the interfaces as ``systemd-networkd`` sees them. All
but the CAN interfaces show as ``unmanaged`` there, which is expected.

The CAN interfaces are brought up at 250 kbit/s. To use another bit rate,
change ``BitRate=`` in their ``.network`` files and reboot. For a product,
install your own versions of the files from your layer. ``ip link`` can
also change the bit rate until the next boot:

.. code-block:: bash

   ip link set can0 down
   ip link set can0 type can bitrate 500000
   ip link set can0 up

To manage an Ethernet port with ``systemd-networkd`` instead, remove the
``Unmanaged=yes`` file for it, add a ``.network`` file with its
configuration, and tell NetworkManager to leave the port alone with
``unmanaged-devices`` (see `Keeping a Wi-Fi Link Up`_ for the file
format).

Using nmtui
-----------

``nmtui`` edits the same connections as ``nmcli``, through text menus. It
is convenient for setting a static address or joining a Wi-Fi network on a
single board. ``nmcli`` is better for scripts and for instructions others
will follow.

.. note::

   Cargt is adding ``nmtui`` to ``cargt-image-dev``. Images published up to
   October 2026 do not include it. To add it to your own image:

   .. code-block:: bash

      IMAGE_INSTALL:append = " networkmanager-nmtui"

Run ``nmtui`` from an SSH session or the serial console. Use the arrow keys
and :kbd:`Tab` to move, :kbd:`Enter` to select and :kbd:`Space` to toggle a
check box. :kbd:`Esc` goes back one screen, and quits from the main menu.
The screens below are from an i.MX 93 00363 on the 00428 carrier, over SSH
in an 80 × 24 terminal.

.. code-block:: text

   root@imx93-cargt-00363-00428:~# nmtui

                              ┌─┤ NetworkManager TUI ├──┐
                              │                         │
                              │ Please select an option │
                              │                         │
                              │ Edit a connection       │
                              │ Activate a connection   │
                              │ Set system hostname     │
                              │ Radio                   │
                              │                         │
                              │ Quit                    │
                              │                         │
                              │                    <OK> │
                              │                         │
                              └─────────────────────────┘

Each menu item can also be opened directly: ``nmtui-edit``,
``nmtui-connect`` and ``nmtui-hostname``. ``nmtui-edit <name>`` and
``nmtui-connect <name>`` go straight to one connection.

Setting a Static Address with nmtui
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This creates the same connection as `Static IP Address`_ does with
``nmcli``.

1. Select **Edit a connection**. The list shows the saved connections,
   including the temporary ``Wired connection 1``:

   .. code-block:: text

      ┌───────────────────────────────────────┐
      │                                       │
      │ ┌─────────────────────────┐           │
      │ │ Ethernet              ↑ │ <Add>     │
      │ │   Wired connection 1  ▒ │           │
      │ │ Loopback              ▒ │ <Edit...> │
      │ │   lo                  ▒ │           │
      │ │                       ▒ │ <Delete>  │
      ...

2. Select **<Add>**, then **Ethernet** and **<Create>**.

3. Enter a **Profile name** and the **Device** (``eth0``). Set
   **IPv4 CONFIGURATION** to **<Manual>**, select **<Show>** next to it,
   and fill in the address with its prefix length, the gateway and the DNS
   servers. Use **<Add...>** to add each address or DNS server:

   .. code-block:: text

      ┌───────────────────────────┤ Edit Connection ├───────────────────────────┐
      │                                                                        ↑│
      │         Profile name static-eth0_____________________________          ▮│
      │               Device eth0____________________________________          ▒│
      │                                                                        ▒│
      │ ═ ETHERNET                                                    <Show>   ▒│
      │ ═ 802.1X SECURITY                                             <Show>   ▒│
      │                                                                        ▒│
      │ ╤ IPv4 CONFIGURATION <Manual>                                 <Hide>   ▒│
      │ │          Addresses 192.168.1.50/24__________ <Remove>                ▒│
      │ │                    <Add...>                                          ▒│
      │ │            Gateway 192.168.1.1______________                         ▒│
      │ │        DNS servers 192.168.1.1______________ <Remove>                ▒│
      │ │                    <Add...>                                          ▒│
      │ │     Search domains <Add...>                                          ▒│
      ...

4. Scroll down and select **<OK>** to save the connection.

5. The new connection does not replace the active one straight away. Go
   back to the main menu, select **Activate a connection**, and activate
   the new connection, or run ``nmcli connection up static-eth0``.

.. warning::

   If you are connected over SSH through the port you are changing, the
   session drops when the new address takes effect. Reconnect to the new
   address, or make the change from the serial console.

Joining a Wi-Fi Network with nmtui
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Activate a connection** lists the saved connections and the Wi-Fi
networks in range. ``*`` marks the active connections. Select a network and
**<Activate>**; ``nmtui`` asks for the password and saves a connection for
the network. With example network names:

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

Hostname and Radios
~~~~~~~~~~~~~~~~~~~

**Set system hostname** changes the board's hostname, the same as
``hostnamectl hostname <name>``:

.. code-block:: text

   ┌─────────────────┤ Set Hostname ├──────────────────┐
   │                                                   │
   │ Hostname imx93-cargt-00363-00428_________________ │
   │                                                   │
   │                                     <Cancel> <OK> │
   │                                                   │
   └───────────────────────────────────────────────────┘

**Radio** turns Wi-Fi and cellular (WWAN) on or off, the same as
``nmcli radio``:

.. code-block:: text

   ┌────┤ Set the radio switches status ├────┐
   │                                         │
   │ Wi-Fi                                   │
   │ Hardware: Enabled   Software: <Enabled> │
   │                                         │
   │ WWAN                                    │
   │ Hardware: Missing   Software: <Enabled> │
   │                                         │
   │                                  <Back> │
   │                                         │
   └─────────────────────────────────────────┘

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
``eth1`` serving addresses to equipment behind it. NetworkManager's shared
mode and the standalone ``dnsmasq`` service cover most cases. For full
control over the firewall and the DHCP server, run nftables and Kea
yourself; see `Routing with nftables and Kea`_.

Shared Mode (DHCP Server and NAT)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

With ``ipv4.method shared``, NetworkManager gives the port a static address,
starts its own dnsmasq instance to hand out addresses and answer DNS on that
port, and routes the devices on it to the board's other connections through
NAT.

Images published up to October 2026 also enable a standalone ``dnsmasq``
service, which by default only forwards DNS queries for the board itself.
It listens on DNS port 53 on every address, so NetworkManager's dnsmasq
cannot start while it runs, and the connection fails with this in
``journalctl -u NetworkManager``:

.. code-block:: text

   dnsmasq: failed to create listening socket for 192.168.50.1: Address already in use

On those images, stop and disable the standalone service first (newer Cargt
BSP builds leave it disabled):

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

   Cargt i.MX images published up to October 2026 (wrynose) build the
   kernel without ``CONFIG_NFT_REJECT``, which NetworkManager's NAT rules
   need. Cargt has fixed this in the BSP, but the fix is not yet in the
   published images.
   Shared mode still gives the port its address and runs the DHCP and DNS
   server, so devices on it can reach the board, but they cannot reach the
   network beyond it. NetworkManager logs
   ``firewall: nft ... Error: Could not process rule`` when this happens.
   To get NAT on those images, add these options to the kernel in your layer
   with a configuration fragment:

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

Routing with nftables and Kea
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To write your own firewall rules, or to use the ISC Kea DHCP server, give
the inside port a static address with NetworkManager and set up forwarding,
NAT and DHCP yourself. Masquerading with your own nftables rules does not
need ``CONFIG_NFT_REJECT``, so it also works on images where shared mode
cannot route (see the warning above).

The example below is from an i.MX 93 00363 on the 00428 carrier with
``cargt-image-dev`` (wrynose). The board has one Ethernet port, so the inside
network is a Wi-Fi access point on ``uap0`` (see `Access Point Mode`_),
created with ``ipv4.method manual ipv4.addresses 192.168.70.1/24`` instead
of ``shared``. A second 00428 joined it as a client. With a second Ethernet
port, use ``eth1`` in place of ``uap0``.

.. warning::

   Run a DHCP server only on a port whose network you control. A second DHCP
   server on an office or plant network hands out wrong addresses to other
   devices.

**Turn on IP forwarding.** Linux does not forward packets between
interfaces by default:

.. code-block:: bash

   sysctl -w net.ipv4.ip_forward=1                         # until reboot
   echo "net.ipv4.ip_forward = 1" > /etc/sysctl.d/90-router.conf  # at every boot

**Add the firewall and NAT rules.** Save them in a file, for example
``/etc/nftables-router.nft``. The ``forward`` chain lets the inside network
reach ``eth0`` and lets only replies back in; the ``postrouting`` chain
translates the inside addresses to the board's ``eth0`` address:

.. code-block:: text

   #!/usr/sbin/nft -f
   destroy table ip router
   table ip router {
       chain forward {
           type filter hook forward priority filter; policy drop;
           ct state established,related accept
           iifname "uap0" oifname "eth0" accept
       }
       chain postrouting {
           type nat hook postrouting priority srcnat; policy accept;
           oifname "eth0" masquerade
       }
   }

``destroy table`` removes an earlier copy of the table, so loading the file
again does not duplicate the rules. Load it with ``nft -f
/etc/nftables-router.nft`` and check it with ``nft list ruleset``.

Cargt images do not include an ``nftables`` service, so add a small unit,
``/etc/systemd/system/router-nftables.service``, to load the rules at boot:

.. code-block:: ini

   [Unit]
   Description=Router firewall and NAT rules
   Before=network-pre.target
   Wants=network-pre.target

   [Service]
   Type=oneshot
   ExecStart=/usr/sbin/nft -f /etc/nftables-router.nft
   RemainAfterExit=yes

   [Install]
   WantedBy=multi-user.target

.. code-block:: bash

   systemctl daemon-reload
   systemctl enable --now router-nftables

**Run Kea on the inside port.** Kea is in the Cargt package feed (see
:doc:`package-management`); for a product, add ``kea`` to your image
instead:

.. code-block:: bash

   apt-get update
   apt-get install kea

Replace ``/etc/kea/kea-dhcp4.conf`` with a configuration for the inside
network:

.. code-block:: json

   {
     "Dhcp4": {
       "interfaces-config": { "interfaces": [ "uap0" ] },
       "lease-database": { "type": "memfile", "persist": true, "name": "/var/lib/kea/kea-leases4.csv" },
       "valid-lifetime": 3600,
       "subnet4": [
         {
           "id": 1,
           "subnet": "192.168.70.0/24",
           "pools": [ { "pool": "192.168.70.100 - 192.168.70.199" } ],
           "option-data": [
             { "name": "routers", "data": "192.168.70.1" },
             { "name": "domain-name-servers", "data": "1.1.1.1, 8.8.8.8" }
           ]
         }
       ],
       "loggers": [ { "name": "kea-dhcp4", "output-options": [ { "output": "stdout" } ], "severity": "INFO" } ]
     }
   }

Check the file, then start the server and enable it at boot:

.. code-block:: bash

   kea-dhcp4 -t /etc/kea/kea-dhcp4.conf
   mkdir -p /var/lib/kea
   systemctl enable --now kea-dhcp4

When a device connects, Kea logs the lease and writes it to its lease
file (the client's MAC address is replaced here):

.. code-block:: text

   root@imx93-cargt-00363-00428:~# journalctl -u kea-dhcp4 | grep LEASE_ALLOC
   ... DHCP4_LEASE_ALLOC [hwtype=1 <client MAC>], cid=[01:<client MAC>], tid=0x48bcbd2: lease 192.168.70.100 has been allocated for 3600 seconds
   root@imx93-cargt-00363-00428:~# cat /var/lib/kea/kea-leases4.csv
   address,hwaddr,client_id,valid_lifetime,expire,subnet_id,fqdn_fwd,fqdn_rev,hostname,state,user_context,pool_id
   192.168.70.100,<client MAC>,01:<client MAC>,3600,1793221540,1,0,0,imx93-cargt-00363-00428,0,,0

**Check the routing.** On the client, the default route over Wi-Fi points
at the router, and pings to the internet get answers:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# ip route get 1.1.1.1 oif mlan0
   1.1.1.1 via 192.168.70.1 dev mlan0 src 192.168.70.100 uid 0
   root@imx93-cargt-00363-00428:~# ping -I mlan0 -c 3 1.1.1.1
   PING 1.1.1.1 (1.1.1.1): 56 data bytes
   64 bytes from 1.1.1.1: seq=0 ttl=56 time=5.944 ms
   ...
   3 packets transmitted, 3 packets received, 0% packet loss

On the router, ``tcpdump`` shows the same pings on both sides: from the
client's address on ``uap0``, and from the router's own address on ``eth0``
after NAT:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# tcpdump -n -i uap0 icmp
   20:05:57.963729 IP 192.168.70.100 > 1.1.1.1: ICMP echo request, id 793, seq 0, length 64
   20:05:57.966107 IP 1.1.1.1 > 192.168.70.100: ICMP echo reply, id 793, seq 0, length 64
   root@imx93-cargt-00363-00428:~# tcpdump -n -i eth0 icmp and host 1.1.1.1
   20:05:57.963828 IP <eth0 address> > 1.1.1.1: ICMP echo request, id 793, seq 0, length 64
   20:05:57.966070 IP 1.1.1.1 > <eth0 address>: ICMP echo reply, id 793, seq 0, length 64

``tcpdump`` is in the package feed (``apt-get install tcpdump``).

With a Wi-Fi access point as the inside network, unmanage the Wi-Fi
interfaces you do not use on both the router and the clients (see
`Keeping a Wi-Fi Link Up`_). In this test, their background scans caused
up to 60% packet loss over a few seconds; with them unmanaged, there was
none.

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
shared mode, stop the standalone ``dnsmasq`` service first on images that
enable it:

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

The access point starts at boot from then on.

.. note::

   Use 2.4 GHz for the access point on current Cargt images. Their
   regulatory domain is the world default (``iw reg get`` shows
   ``country 00``), which does not allow an access point on 5 GHz. With
   ``wifi.band a`` and ``wifi.channel 36``, the activation fails, and the
   log shows ``uap0: Failed to start AP functionality``. ``iw reg set``
   does not change the domain on the IW612; the country has to be set in
   the Wi-Fi driver's configuration.

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

Keeping a Wi-Fi Link Up
~~~~~~~~~~~~~~~~~~~~~~~

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

Capturing Packets
~~~~~~~~~~~~~~~~~

Install ``tcpdump`` from the package feed (``apt-get install tcpdump``) and
capture on the board, or stream the capture to Wireshark on your computer
over SSH. ``-U -w -`` writes each packet to the SSH connection as it
arrives, and ``not port 22`` leaves out the SSH traffic itself:

.. code-block:: bash

   ssh root@<board-ip> tcpdump -i uap0 -U -w - not port 22 | wireshark -k -i -

The same pipe works with ``tshark -i -`` for a text view, or redirected to a
file (``> capture.pcap``) to open later. From a Linux computer, streaming
pings that crossed the router above:

.. code-block:: text

   $ ssh root@<board-ip> tcpdump -i uap0 -U -w - not port 22 | tshark -i -
       1   0.000000 192.168.70.100 → 1.1.1.1      ICMP 98 Echo (ping) request  id=0x0339, seq=0/0, ttl=64
       2   0.002490      1.1.1.1 → 192.168.70.100 ICMP 98 Echo (ping) reply    id=0x0339, seq=0/0, ttl=56 (request in 1)
       3   0.991422 192.168.70.100 → 1.1.1.1      ICMP 98 Echo (ping) request  id=0x0339, seq=1/256, ttl=64
       4   0.993351      1.1.1.1 → 192.168.70.100 ICMP 98 Echo (ping) reply    id=0x0339, seq=1/256, ttl=56 (request in 3)

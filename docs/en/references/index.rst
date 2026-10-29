References
==========

Yocto Development for NXP i.MX Application Processors
-----------------------------------------------------

- `NXP i.MX Yocto Project User's Guide (UG10164) <https://www.nxp.com/docs/en/user-guide/UG10164.pdf>`_ – Official guide for building Linux images for NXP i.MX processors using Yocto.
- `NXP GitHub – meta-imx <https://github.com/nxp-imx/meta-imx>`_ – BSP layers and machine configurations for i.MX platforms.
- `NXP i.MX Porting Guide (UG10165) <https://www.nxp.jp/docs/en/user-guide/UG10165.pdf>`_ – Guide for customizing U-Boot for NXP i.MX processors.

NXP Product Documentation
-------------------------

Fact Sheets
~~~~~~~~~~~

- `i.MX 8M Plus Applications Processor Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/IMX8MPIECFS.pdf>`_ – Overview of features and architecture.
- `i.MX 91 Applications Processor Family Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/IMX91FAMFS.pdf>`_ – Overview of features and architecture.
- `i.MX 93 Applications Processor Family Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/iMX93FAMFS.pdf>`_ – Key features and block diagram.
- `i.MX 95 Applications Processor Family Fact Sheet <https://www.nxp.com/docs/en/fact-sheet/IMX95FS.pdf>`_ – Overview of cores, NPU, and safety features.

Datasheets and Reference Manuals for i.MX 8M Plus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. dropdown::
    :open:

    - `i.MX 8M Plus Applications Processor Family Overview <https://www.nxp.com/docs/en/fact-sheet/IMX8MPLUSFAMFS.pdf>`_ – Key features and block diagram.
    - `i.MX 8M Plus Applications Processor Datasheet (Commercial) <https://www.nxp.com/docs/en/preview/PREVIEW_IMX8MPEC.pdf>`_ – Electrical characteristics and package details.
    - `i.MX 8M Plus Applications Processor Datasheet (Industrial) <https://www.nxp.com/docs/en/preview/PREVIEW_IMX8MPIEC.pdf>`_ – Electrical characteristics and package details.
    - `i.MX 8M Plus Applications Processor Reference Manual <https://www.nxp.com/docs/en/preview/PREVIEW_IMX8MPRM.pdf>`_ – Functional description and register maps.


Datasheets and Reference Manuals for i.MX 91, i.MX 93, and i.MX 95
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. dropdown::
    :open:

    - `i.MX 91 Applications Processors Data Sheet (Commercial) <https://www.nxp.com/docs/en/data-sheet/IMX91CEC.pdf>`_ – Electrical specifications and functional details.
    - `i.MX 91 Applications Processors Data Sheet (Industrial) <https://www.nxp.com/docs/en/data-sheet/IMX91IEC.pdf>`_ – Industrial-grade specifications.
    - `i.MX 93 Applications Processors Data Sheet (Commercial) <https://www.nxp.com/docs/en/data-sheet/IMX93CEC.pdf>`_ – Electrical specifications and functional details.
    - `i.MX 93 Applications Processors Data Sheet (Automotive) <https://www.nxp.com/docs/en/data-sheet/IMX93AEC.pdf>`_ – Automotive-grade specifications.
    - `i.MX 93 Applications Processors Data Sheet (Industrial) <https://www.nxp.com/docs/en/data-sheet/IMX93IEC.pdf>`_ – Industrial-grade specifications.
    - `i.MX 91 Applications Processor Reference Manual <https://www.nxp.com/docs/en/reference-manual/RM12173.pdf>`_ – Functional description and register maps.
    - `i.MX 93 Applications Processor Reference Manual <https://www.nxp.com/docs/en/reference-manual/RM12175.pdf>`_ – Functional description and register maps.
    - `i.MX 95 Product Page <https://www.nxp.com/products/i.MX95>`_ – Detailed product information and resources.

SWUpdate
--------

- `SWUpdate Documentation <https://sbabic.github.io/swupdate/>`_ – Detailed instructions for implementing secure software updates on embedded devices.
- `SWUpdate GitHub <https://github.com/sbabic/swupdate>`_ – Source code and examples for SWUpdate.

RAUC
----

- `RAUC Documentation <https://rauc.readthedocs.io/>`_ – Reference for RAUC bundles, slot configuration and bootloader integration.

Yocto Project
-------------

- `Yocto Project Reference Manual <https://docs.yoctoproject.org/ref-manual/>`_ – Comprehensive reference for Yocto build system, metadata, and configuration.

BitBake
-------

- `BitBake User Manual <https://docs.yoctoproject.org/bitbake/>`_ – Guide to BitBake tasks, recipes, and advanced build options.

dnsmasq
-------

- `dnsmasq Man Page <https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html>`_ – Official documentation for DNS/DHCP server configuration and options.

Teleport SSH
------------

- `Teleport Documentation <https://goteleport.com/docs/>`_ – Instructions for secure remote access and reverse SSH tunneling.

nftables
--------

- `nftables Wiki <https://wiki.nftables.org/>`_ – Tutorials and examples for Linux firewall configuration using nftables.
- `netfilter.org nftables Project <https://www.netfilter.org/projects/nftables/index.html>`_ – Official project page with technical details and updates.

NXP Documentation for Secure Boot (AHAB) on i.MX Processors
-----------------------------------------------------------

AHAB secure boot on i.MX 91, i.MX 93 and i.MX 95 is described in each
processor's Security Reference Manual and in the NXP Code Signing Tool (CST)
user guide. NXP distributes both from the **Documentation** and
**Design Tools** tabs of the processor's product page after you sign in to an
NXP account; some documents require a signed NDA.

See :doc:`/core/secure-boot` for an overview of AHAB on Cargt SOMs.

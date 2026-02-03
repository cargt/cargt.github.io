References
==========

Yocto Development for NXP i.MX Application Processors
-----------------------------------------------------

- `NXP Yocto Project User's Guide (UG10164) <https://www.nxp.com/docs/en/fact-sheet/IMX91FAMFS.pdf>`_ – Official guide for building Linux images for NXP i.MX processors using Yocto.
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

- `Teleport Server Access Guide <https://goteleport.com/docs/ssh-access/guides/server-access/>`_ – Instructions for secure remote access and reverse SSH tunneling.

nftables
--------

- `nftables Wiki <https://wiki.nftables.org/>`_ – Tutorials and examples for Linux firewall configuration using nftables.
- `netfilter.org nftables Project <https://www.netfilter.org/projects/nftables/index.html>`_ – Official project page with technical details and updates.

NXP Documentation for Secure Boot (AHAB) on i.MX Processors
-----------------------------------------------------------

- `NXP i.MX Secure Boot and Image Authentication (AN5089) <https://www.nxp.com/docs/en/application-note/AN5089.pdf>`_ – Application note detailing secure boot implementation on i.MX processors.
- `NXP Code Signing Tool User Guide (UG1165) <https://www.nxp.com/docs/en/user-guide/UG1165.pdf>`_ – Instructions for using the Code Signing Tool to sign images for secure boot.
- `NXP Secure Boot Overview <https://www.nxp.com/docs/en/application-note/AN5337.pdf>`_ – Overview of secure boot concepts and architecture for NXP processors.
- `NXP i.MX93 Secure Boot Implementation Guide (AN12174) <https://www.nxp.com/docs/en/application-note/AN12174.pdf>`_ – Specific guide for implementing secure boot on i.MX93 processors.
- `NXP i.MX95 Secure Boot Implementation Guide (AN12175) <https://www.nxp.com/docs/en/application-note/AN12175.pdf>`_ – Specific guide for implementing secure boot on i.MX95 processors.
- `NXP One-Time Programmable Memory Programming Guide (AN5338) <https://www.nxp.com/docs/en/application-note/AN5338.pdf>`_ – Guide for programming OTP memory on NXP processors.
- `NXP i.MX U-Boot Secure Boot Integration Guide (AN12176) <https://www.nxp.com/docs/en/application-note/AN12176.pdf>`_ – Instructions for integrating secure boot into U-Boot for i.MX processors.
- `NXP i.MX Linux Secure Boot Integration Guide (AN12177) <https://www.nxp.com/docs/en/application-note/AN12177.pdf>`_ – Instructions for integrating secure boot into Linux for i.MX processors.
- `NXP Secure Boot Key Management Guide (AN12178) <https://www.nxp.com/docs/en/application-note/AN12178.pdf>`_ – Best practices for managing keys used in secure boot implementations.
- `NXP Secure Boot Troubleshooting Guide (AN12179) <https://www.nxp.com/docs/en/application-note/AN12179.pdf>`_ – Common issues and solutions related to secure boot on NXP processors.
- `NXP i.MX Secure Boot FAQ <https://www.nxp.com/docs/en/application-note/AN5339.pdf>`_ – Frequently asked questions about secure boot on i.MX processors.
- `NXP Secure Boot Training Materials <https://www.nxp.com/webapp/Download?colCode=AN5337TRAINING>`_ – Training resources for understanding and implementing secure boot on NXP processors.
- `NXP Secure Boot Webinars <https://www.nxp.com/webapp/Download?colCode=AN5337WEBINAR>`_ – Recorded webinars covering various aspects of secure boot on NXP processors.
- `NXP Secure Boot Community Forum <https://community.nxp.com/t5/Security-Trust/Secure-Boot/bd-p/security-trust>`_ – Community discussions and support for secure boot topics on NXP processors.
- `NXP Secure Boot YouTube Playlist <https://www.youtube.com/playlist?list=PL4fGSI1pDJn5o1kz8D3K0ZlY0bXq6K5jR>`_ – Video tutorials and presentations on secure boot for NXP processors.
- `NXP Secure Boot GitHub Repository <https://github.com/NXPsecureboot>`_ – Source code and tools related to secure boot implementations on NXP processors.
- AN12312 – i.MX93 Secure Boot Example Implementation – Step-by-step example of implementing secure boot on the i.MX93 processor.
- AN12313 – i.MX95 Secure Boot Example Implementation – Step-by-step example of implementing secure boot on the i.MX95 processor.
- `NXP Secure Boot Application Notes Index <https://www.nxp.com/docs/en/application-note/AN5337INDEX.pdf>`_ – Comprehensive index of application notes related to secure boot on NXP processors.
- `NXP Secure Boot Training Videos <https://www.nxp.com/webapp/Download?colCode=AN5337TRAININGVIDEOS>`_ – Video resources for learning about secure boot on NXP processors.
- i.MX93 Application Processor Security Reference Manual (RM12175) – Detailed reference manual covering security features and secure boot implementation for the i.MX93 processor.
- i.MX95 Application Processor Security Reference Manual (RM12176) – Detailed reference manual covering security features and secure boot implementation for the i.MX95 processor.
- NXP Secure Boot Best Practices Guide (AN12180) – Guidelines and best practices for implementing secure boot on NXP processors.

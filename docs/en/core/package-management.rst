Package Management on a Cargt design
====================================

Cargt Package Repository
------------------------

Updating and Installing Packages using the Cargt Package Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      apt-get update
      apt-get install <package_name>

Listing Installed Packages
~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      apt list --installed

Using a Downloaded Package File
-------------------------------

Updating using a downloaded ``.deb`` package file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code-block:: bash

      dpkg -i /<path_to_downloaded_package>/<package_file>.deb

Using your Own Package Repository
---------------------------------

Generating a Package Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   In your Yocto build environment, run:

   .. code-block:: bash

      bitbake package-index

   Then navigate to ``<build_dir>/tmp/deploy/deb/<machine>/`` to find the generated ``.deb`` repository files.

Simple Package Repository Hosting using Python HTTP Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   On your development host, navigate to the package repository directory (as above) and start a simple HTTP server:

   .. code-block:: bash

      cd <path_to_package_repo>
      python3 -m http.server <chosen_port_number>
      python3 -m http.server 8081

   .. note::

      Ensure that the chosen port number is open in your firewall settings.
      Choose a port number > 1024 and that is not already in use by another service such as SWUpdate (default port 8080).
      Open example:5678

Configuring the Target to use your Package Repository
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   On the target device, add your repository to the APT sources list:

   .. code-block:: bash

      echo "deb [trusted=yes] http://<your_server_ip>:<port_number>/ ./" >> /etc/apt/sources.list.d/my-custom-repo.list
      apt-get update
      apt-get install <package_name>

Advanced
~~~~~~~~

   You can list all of the packages in your repository by navigating to ``http://<your_server_ip>:<port_number>/`` in a web browser.

   Bitbake produces multiple directories such as ``armv8a``, ``all``, ``<machine-name>`` etc.
   If you add each directory as a separate line in the sources list, APT will be able to find more packages.
   Then the package server can be run from the ``<build_dir>/tmp/deploy/deb/`` directory.

   To do it at build time, add the following lines to your ``local.conf`` file on the development machine:

   .. code-block:: bash

      PACKAGE_FEED_URIS += " http://<your_server_ip>:<port_number>/ "
      PACKAGE_FEED_ARCHS = "all armv8a"
      Depending on your package repo, you may also need to specify:
      PACKAGE_FEED_BASE_PATHS = "deb"

   Further information: https://docs.yoctoproject.org/ref-manual/variables.html#term-PACKAGE_FEED_ARCHS

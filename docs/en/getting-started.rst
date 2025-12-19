Getting Started
===============

This guide will help you get started with the cargt project documentation.

Prerequisites
-------------

To build the documentation locally, you need:

* Python 3.7 or later
* pip (Python package installer)

Installation
------------

1. Clone the repository:

.. code-block:: bash

   git clone https://github.com/cargt/cargt.github.io.git
   cd cargt.github.io

2. Install documentation dependencies:

.. code-block:: bash

   pip install -r docs/requirements.txt

Building Documentation
----------------------

To build the documentation locally:

.. code-block:: bash

   cd docs/en
   sphinx-build -b html . ../_build/html

The built documentation will be available in ``docs/_build/html/``.

Viewing Documentation
---------------------

Open the generated documentation in your browser:

.. code-block:: bash

   # On Linux/macOS
   open docs/_build/html/index.html
   
   # On Windows
   start docs/_build/html/index.html

Deployment
----------

The documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch. The deployment is handled by GitHub Actions.

Writing Documentation
---------------------

Documentation files are written in reStructuredText format (.rst). Here are some basic formatting examples:

Headers
~~~~~~~

Use underlines with ``=``, ``-``, ``~``, etc. to create headers of different levels.

**Bold text** and *italic text*
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: rst

   **Bold text** and *italic text*

Code Blocks
~~~~~~~~~~~

.. code-block:: python

   def hello_world():
       print("Hello, World!")

Links
~~~~~

`External link <https://www.example.com>`_

Lists
~~~~~

* Item 1
* Item 2
* Item 3

For more information on reStructuredText syntax, see the `Sphinx documentation <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_.

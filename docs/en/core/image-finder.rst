.. _image-finder:

Image Finder
============

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

Pick a release, a board and an image to get the pre-built files from the
nightly builds on `yocto.cargt.com <https://yocto.cargt.com/images/>`__,
with the flashing and update commands filled in for those files. The page
also lists the device trees and every package in the image.

.. raw:: html

   <div id="image-finder-app" data-src="../_static/data/yocto">
     <p>The Image Finder needs JavaScript. Browse the images directly at
     <a href="https://yocto.cargt.com/images/">yocto.cargt.com/images</a>,
     or use the table in <a href="releases.html">Releases and Downloads</a>.</p>
   </div>
   <script src="../_static/image-finder.js" defer></script>

About the Images
----------------

- **They are nightly development builds.** Most boards have
  ``cargt-image-dev``, which includes debug tools, SSH and root login. To
  build a product image, start from :doc:`yocto`.
- **Only the latest build is kept.** Each nightly replaces the files from the
  one before, and older builds are not published. Keep a copy of the files you
  flash or ship.
- **A folder can hold files from more than one nightly.** Each file is the
  latest build of that file, so a disk image and an update file in the same
  folder can have different dates. The finder warns when they do, and shows
  each file's date.
- **The list is refreshed once a day.** This page reads a copy of the
  yocto.cargt.com listings made when the site was last built (the time is
  shown above the results). The download links go to yocto.cargt.com itself.

Every release and ``MACHINE`` is also listed in :doc:`releases`. For first-time
setup, flashing tools and logging in, see :doc:`getting-started`.

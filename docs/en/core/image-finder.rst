.. _image-finder:

Image Finder
============

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX` :bdg-primary:`STM32MP2`

The Image Finder covers every image in the nightly builds on
`yocto.cargt.com <https://yocto.cargt.com/images/>`__. Pick a board and an
image to get:

- its files: disk image, bootloader or flash layout, update file, SBOM and
  package list, with each file's date and size
- the commands to flash a board with it and to update a running board, filled
  in with those file names
- its device trees and package feeds
- what is inside it: every package, what each one needs and what needs it,
  what each top-level package costs in installed size, and what adding a
  package from the board's feed would pull in

.. button-link:: ../image-finder/index.html
   :color: primary

   Open the Image Finder

About the Images
----------------

- **They are nightly development builds.** Most boards have
  ``cargt-image-dev``, which includes debug tools, SSH and root login. To
  build a product image, start from :doc:`yocto`. The Image Finder's size
  chart shows which packages to leave out first.
- **Only the latest build is kept.** Each nightly replaces the files from the
  one before, and older builds are not published. Keep a copy of the files you
  flash or ship.
- **A folder can hold files from more than one nightly.** Each file is the
  latest build of that file, so a disk image and an update file in the same
  folder can have different dates. The Image Finder shows each file's date and
  says when they differ.
- **The lists are refreshed on a schedule.** File names and dates are read
  from yocto.cargt.com daily. Installed sizes and dependencies are measured
  weekly from the published root filesystems and package feeds, so they can be
  a few days older than the files. The download links always go to
  yocto.cargt.com itself.

Every release and ``MACHINE`` is also listed in :doc:`releases`. For first-time
setup, flashing tools and logging in, see :doc:`getting-started`.

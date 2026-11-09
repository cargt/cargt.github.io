.. _benchmarks:

SOM Benchmarks
==============

.. rst-class:: cargt-applies-to

**Applies to:** :bdg-primary:`i.MX 95` :bdg-primary:`i.MX 8M Plus` :bdg-primary:`i.MX 93` :bdg-primary:`i.MX 91` :bdg-primary:`STM32MP2`

Which Cargt SOM is fast enough for your product? This page runs the same
tests on each SOM: CPU, memory, eMMC, boot time, GPU, NPU, Ethernet,
scheduling latency and web browser speed. Cargt measured every number on its own boards in
November 2026, with the tools and commands listed under
`How It Was Measured`_, so you can run the same tests on your board.

For browser frame rates, memory and image size, see :doc:`web-browsers`. For how hot each
SOM runs and when it needs a heatsink, see :doc:`thermal-characterization`.

.. contents:: On this page
   :local:
   :depth: 1

Summary
-------

.. list-table:: Results at a glance (higher is better unless marked)
   :class: wrap-cells
   :header-rows: 1
   :stub-columns: 1
   :widths: 16 14 14 14 14 14 14

   * - Test
     - :ref:`00414 <00414>` i.MX 95
     - :ref:`00377 <00377>` i.MX 8M Plus
     - :ref:`00363-93 <00363-93>` i.MX 93
     - :ref:`00324 <00324>` i.MX 93
     - :ref:`00363-91 <00363-91>` i.MX 91
     - :ref:`00395 <00395>` STM32MP257F
   * - CPU cores
     - 6 × Cortex-A55, 1.8 GHz
     - 4 × Cortex-A53, 1.6 GHz
     - 2 × Cortex-A55, 1.7 GHz
     - 2 × Cortex-A55, 1.7 GHz
     - 1 × Cortex-A55, 1.4 GHz
     - 2 × Cortex-A35, 1.5 GHz
   * - RAM on the tested board
     - 16 GB
     - 4 GB
     - 2 GB
     - 1 GB
     - 2 GB
     - 2 GB
   * - CoreMark, one core
     - 7,014
     - 5,446
     - 6,599
     - 6,596
     - 5,413
     - 3,780
   * - CoreMark, all cores
     - 42,044
     - 21,475
     - 13,174
     - 13,091
     - 5,400
     - 7,416
   * - Memory copy (memcpy), MB/s
     - 4,624
     - 2,556
     - 2,846
     - 3,029
     - 1,816
     - 1,863
   * - eMMC sequential read / write, MB/s
     - 350 / 146
     - 325 / 38
     - 269 / 123
     - Reads only; see `Storage`_
     - 352 / 128
     - 89 / 79
   * - eMMC random 4 KB read / write, IOPS
     - 5,522 / 9,942
     - 6,274 / 8,618
     - 5,826 / 15,462
     - Reads only; see `Storage`_
     - 6,250 / 6,639
     - 3,673 / 2,747
   * - Kernel start to login prompt, s (lower is better)
     - 12.8
     - 12.3
     - 11.8
     - 11.1
     - 17.1
     - 21.4
   * - GPU, glmark2 score
     - 689 (Mali-G310)
     - 722 (GC7000UL)
     - No 3D GPU
     - No 3D GPU
     - No 3D GPU
     - 549 (GCNanoUltra)
   * - MobileNet v1 on the NPU, ms (lower is better)
     - Not measured; see `NPU`_
     - 3.4
     - 3.9
     - Not measured
     - No NPU
     - Not measured; see `NPU`_
   * - MobileNet v1 on all CPU cores, ms (lower is better)
     - 12.9
     - 47.6
     - 33.1
     - 32.9
     - 77.5
     - Not measured
   * - Gigabit Ethernet, TCP send / receive, Mbit/s
     - 943 / 941
     - 942 / 941
     - 943 / 941
     - 942 / 941
     - 940 / 941
     - 942 / 941
   * - Worst scheduling latency under load, µs (lower is better)
     - 332
     - 359
     - 391
     - 557
     - 250
     - 1,184
   * - Speedometer 3.1, WPE WebKit / Chromium
     - 1.29 / 1.54 (one run)
     - 1.15 / 1.41
     - 0.696 / 0.921
     - Not measured
     - Not measured
     - 0.838 / no Chromium

What the results show:

- **CPU:** one Cortex-A55 core on the i.MX 95 or i.MX 93 is 20 to 30%
  faster than one Cortex-A53 core on the 8M Plus, and almost twice as fast as
  one Cortex-A35 core on the STM32MP257F. With all cores busy, the six-core
  i.MX 95 does about twice the work of the four-core 8M Plus, three times
  that of the i.MX 93 and almost six times that of the STM32MP257F. The
  single-core i.MX 91, at 1.4 GHz, matches one 8M Plus core.
- **Memory:** the i.MX 95 copies memory at least 50% faster than the others.
- **eMMC:** results depend on the eMMC chip and the bus mode as much as on
  the SoC (see `Storage`_). The STM32MP257F image runs its eMMC in HS200
  mode at 100 MHz, so it reads about three times slower than the i.MX 93
  with the same eMMC chip.
- **NPU:** on the 8M Plus and i.MX 93, the NPU runs MobileNet v1 8 to 14
  times faster than all CPU cores together. On its six cores, the i.MX 95
  CPU alone takes 12.9 ms.
- **Ethernet:** every SOM sends and receives at Gigabit line rate, so
  Ethernet does not set them apart.
- **Web browsers:** Chromium scores 19 to 32% higher than WPE WebKit on
  Speedometer 3.1 on every i.MX SOM. The i.MX 95 is the fastest, and the
  i.MX 93, with no 3D GPU, the slowest. See `Web Browsers`_.
- **The two i.MX 93 SOMs** (00363 OSM and 00324 SODIMM) perform the same,
  as expected for the same SoC.

The :ref:`00359 <00359>` i.MX 93 LGA SOM is not
measured because no board was available; its i.MX 93 results should match the
two i.MX 93 SOMs above.

Charts
------

The charts show the main results. Every number is in the `Summary`_ table and
under `Results by Test`_.

.. figure:: /_static/images/charts/img-bench-coremark.svg
   :width: 100%
   :alt: Bar chart of CoreMark iterations per second. One core: i.MX 95 7,014, i.MX 8M Plus 5,446, i.MX 93 00363 6,599, i.MX 93 00324 6,596, i.MX 91 5,413, STM32MP257F 3,780. All cores: 42,044, 21,475, 13,174, 13,091, 5,400 and 7,416.

   CoreMark on one core and on all cores.

.. figure:: /_static/images/charts/img-bench-memory.svg
   :width: 100%
   :alt: Bar chart of tinymembench memcpy and memset bandwidth in MB/s. memcpy: i.MX 95 4,624, i.MX 8M Plus 2,556, i.MX 93 00363 2,846, i.MX 93 00324 3,029, i.MX 91 1,816, STM32MP257F 1,863. memset: 15,559, 12,110, 5,099, 5,125, 4,237 and 6,012.

   Memory bandwidth measured with tinymembench.

.. figure:: /_static/images/charts/img-bench-emmc-seq.svg
   :width: 100%
   :alt: Bar chart of eMMC sequential throughput in MB/s. Read: i.MX 95 350, i.MX 8M Plus 325, i.MX 93 269, i.MX 91 352, STM32MP257F 89. Write: 146, 38, 123, 128 and 79.

   eMMC sequential read and write, 1 MB blocks.

.. figure:: /_static/images/charts/img-bench-emmc-random.svg
   :width: 100%
   :alt: Bar chart of eMMC random 4 KB IOPS. Read: i.MX 95 5,522, i.MX 8M Plus 6,274, i.MX 93 5,826, i.MX 91 6,250, STM32MP257F 3,673. Write: 9,942, 8,618, 15,462, 6,639 and 2,747.

   eMMC random read and write, 4 KB blocks.

.. figure:: /_static/images/charts/img-bench-boot.svg
   :width: 100%
   :alt: Bar chart of seconds from kernel start to the login prompt: i.MX 95 12.8, i.MX 8M Plus 12.3, i.MX 93 00363 11.8, i.MX 93 00324 11.1, i.MX 91 17.1, STM32MP257F 21.4.

   Time from kernel start to the login prompt. The STM32MP257F and i.MX 91
   were on a first boot; see `Boot Time`_.

.. figure:: /_static/images/charts/img-bench-glmark2.svg
   :width: 100%
   :alt: Bar chart of glmark2-es2-wayland scores: i.MX 95 689, i.MX 8M Plus 722, STM32MP257F 549.

   glmark2 score at 800×600. The i.MX 93 and i.MX 91 have no 3D GPU.

.. figure:: /_static/images/charts/img-bench-mobilenet.svg
   :width: 100%
   :alt: Log-scale bar chart of MobileNet v1 inference time in ms. NPU: i.MX 8M Plus 3.4, i.MX 93 3.9. CPU one core: i.MX 95 54.2, i.MX 8M Plus 161.6, i.MX 93 60.2, i.MX 91 77.5. CPU all cores: 12.9, 47.6, 33.1 and 77.5.

   MobileNet v1 inference time on the NPU and on the CPU (log scale). The
   i.MX 95 and STM32MP257F NPUs are not measured yet; see `NPU`_.

.. figure:: /_static/images/charts/img-bench-latency.svg
   :width: 100%
   :alt: Bar chart of the worst cyclictest latency in microseconds under stress-ng load: i.MX 95 332, i.MX 8M Plus 359, i.MX 93 00363 391, i.MX 93 00324 557, i.MX 91 250, STM32MP257F 1,184.

   Worst scheduling latency in 60 seconds under full load, standard kernel.

The Speedometer and MotionMark charts are under `Web Browsers`_.

Results by Test
---------------

The boards and images tested:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 18 30 52

   * - SOM
     - Carrier and display
     - Image
   * - :ref:`00414 <00414>` i.MX 95
     - 00365, 10.1" LVDS panel
     - ``cargt-image-webkit``, wrynose, kernel 6.18
   * - :ref:`00377 <00377>` i.MX 8M Plus
     - 00365, HDMI output, no monitor. Passive heatsink fitted
       (ATS-CPX045045025).
     - ``cargt-image-stress-test``, wrynose, kernel 6.18
   * - :ref:`00363-93 <00363-93>` i.MX 93
     - 00365, no panel
     - A wrynose development image, kernel 6.18
   * - :ref:`00324 <00324>` i.MX 93
     - 00326 SODIMM carrier, no panel
     - A wrynose image with kernel 6.18
   * - :ref:`00363-91 <00363-91>` i.MX 91
     - 00365, no panel
     - ``cargt-image-dev``, wrynose, kernel 6.18, freshly flashed
   * - :ref:`00395 <00395>` STM32MP257F
     - 00365, 5.5" MIPI panel
     - ``cargt-image-webkit``, scarthgap (OpenSTLinux), kernel 6.6

All boards ran their default CPU frequency governor (``ondemand`` on i.MX,
``schedutil`` on STM32MP2) and no application load.

CPU
~~~

`CoreMark <https://github.com/eembc/coremark>`__ was built from source on each
board with ``-O2``: once for one core and once with one thread per core
(``-DMULTITHREAD=<cores> -DUSE_PTHREAD``). The i.MX boards built it with GCC
15.2 and the STM32MP257F with GCC 13.3, the compiler in its image.
``sysbench cpu`` (prime numbers to 20,000, 30 seconds) gives the same ranking.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 28 18 18 18 18

   * - SOM
     - CoreMark, 1 core
     - CoreMark, all cores
     - sysbench, 1 thread (events/s)
     - sysbench, all threads (events/s)
   * - 00414 i.MX 95
     - 7,014
     - 42,044
     - 345
     - 2,073
   * - 00377 i.MX 8M Plus
     - 5,446
     - 21,475
     - 305
     - 1,207
   * - 00363-93 i.MX 93
     - 6,599
     - 13,174
     - 325
     - 650
   * - 00324 i.MX 93
     - 6,596
     - 13,091
     - 325
     - 645
   * - 00363-91 i.MX 91
     - 5,413
     - 5,400
     - 265
     - 268
   * - 00395 STM32MP257F
     - 3,780
     - 7,416
     - 263
     - 517

Memory
~~~~~~

`tinymembench <https://github.com/ssvb/tinymembench>`__ copy and fill
bandwidth, and ``mbw`` (memcpy of a 256 MiB buffer, average of five runs).

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 28 18 18 18 18

   * - SOM
     - memcpy (MB/s)
     - memset (MB/s)
     - NEON copy (MB/s)
     - mbw memcpy (MiB/s)
   * - 00414 i.MX 95
     - 4,624
     - 15,559
     - 4,626
     - 4,559
   * - 00377 i.MX 8M Plus
     - 2,556
     - 12,110
     - 2,686
     - 2,471
   * - 00363-93 i.MX 93
     - 2,846
     - 5,099
     - 2,857
     - 2,714
   * - 00324 i.MX 93
     - 3,029
     - 5,125
     - 3,033
     - 2,821
   * - 00363-91 i.MX 91
     - 1,816
     - 4,237
     - 1,824
     - 1,728
   * - 00395 STM32MP257F
     - 1,863
     - 6,012
     - 1,889
     - 1,733

Storage
~~~~~~~

``fio`` with direct I/O and 16 requests in flight, on a 512 MB file in an
ext4 partition on the eMMC, 30 seconds per test. The results depend on the
eMMC chip fitted and on the bus mode the image uses, so the table lists both.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 22 22 14 14 14 14

   * - SOM
     - eMMC chip and bus mode
     - Sequential read (MB/s)
     - Sequential write (MB/s)
     - Random read (IOPS)
     - Random write (IOPS)
   * - 00414 i.MX 95
     - IN032G, HS400 enhanced strobe, 200 MHz
     - 350
     - 146
     - 5,522
     - 9,942
   * - 00377 i.MX 8M Plus
     - TS0A32, HS400 enhanced strobe, 200 MHz
     - 325
     - 38
     - 6,274
     - 8,618
   * - 00363-93 i.MX 93
     - AS032G, HS400 enhanced strobe, 200 MHz
     - 269
     - 123
     - 5,826
     - 15,462
   * - 00324 i.MX 93
     - AS032G, HS400 enhanced strobe, 200 MHz
     - 344 (raw device)
     - Not measured
     - 10,820 (raw device)
     - Not measured
   * - 00363-91 i.MX 91
     - IN032G, HS400 enhanced strobe, 200 MHz
     - 352
     - 128
     - 6,250
     - 6,639
   * - 00395 STM32MP257F
     - AS032G, HS200, 100 MHz
     - 89
     - 79
     - 3,673
     - 2,747

The 00324 was only tested read-only, on the raw eMMC device rather than a
file, so its numbers are not directly comparable with the others and are not
in the charts.

The STM32MP257F has the same eMMC chip as the i.MX 93 boards but runs it in
HS200 mode at 100 MHz, which limits its throughput. The 8M Plus's slow
sequential writes come from its eMMC chip.

Boot Time
~~~~~~~~~

``systemd-analyze`` measures from kernel start; the boot ROM, bootloader and
U-Boot time before it are not included. The table gives the kernel time, the
time to the login prompt (``getty.target``), and the total that
``systemd-analyze`` reports, which waits for every service.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 14 18 16 28

   * - SOM
     - Kernel (s)
     - Kernel start to login prompt (s)
     - ``systemd-analyze`` total (s)
     - Slowest service
   * - 00414 i.MX 95
     - 5.5
     - 12.8
     - 18.9
     - Waiting for the network, 6.1 s
   * - 00377 i.MX 8M Plus
     - 5.1
     - 12.3
     - 49.1
     - Waiting for the network, 28.1 s
   * - 00363-93 i.MX 93
     - 4.8
     - 11.8
     - 131.2
     - ``systemd-networkd-wait-online``, 120 s timeout
   * - 00324 i.MX 93
     - 2.5
     - 11.1
     - 130.2
     - ``systemd-networkd-wait-online``, 120 s timeout
   * - 00363-91 i.MX 91
     - 2.4
     - 17.1
     - 33.0
     - Growing the data partition on first boot, 19.9 s
   * - 00395 STM32MP257F
     - 5.0
     - 21.4
     - 29.6
     - Bluetooth setup, 10.3 s

The two i.MX 93 images run both NetworkManager and systemd-networkd, and
``systemd-networkd-wait-online`` waits for its full two-minute timeout. That
delays only services that wait for the network, not the login prompt or
Weston. Measure your own image with ``systemd-analyze critical-chain`` and
``systemd-analyze blame``. The STM32MP257F was measured on its first boot
after an update, which includes one-time work such as generating SSH keys and
resizing a partition. The i.MX 91 was also on its first boot, just after
flashing, which includes growing the data partition.

GPU
~~~

``glmark2-es2-wayland --off-screen -s 800x600``, run under Weston, so that the
panel size and refresh rate do not affect the score. The i.MX 93 and
i.MX 91 have no 3D GPU.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 40 30

   * - SOM
     - GPU and OpenGL ES version
     - glmark2 score
   * - 00414 i.MX 95
     - Arm Mali-G310, OpenGL ES 3.2
     - 689
   * - 00377 i.MX 8M Plus
     - Vivante GC7000UL, OpenGL ES 3.1
     - 722
   * - 00395 STM32MP257F
     - Vivante GCNanoUltra, OpenGL ES 3.1
     - 549

NPU
~~~

The MobileNet v1 1.0 224 quantized model that comes with TensorFlow Lite,
timed with its ``benchmark_model`` tool (100 to 200 runs). The CPU results
run the same model without a delegate.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 24 16 18 18

   * - SOM
     - NPU and delegate
     - NPU (ms)
     - CPU, 1 core (ms)
     - CPU, all cores (ms)
   * - 00414 i.MX 95
     - eIQ Neutron, ``libneutron_delegate.so``
     - Not measured
     - 54.2
     - 12.9
   * - 00377 i.MX 8M Plus
     - VeriSilicon, ``libvx_delegate.so``
     - 3.4
     - 161.6
     - 47.6
   * - 00363-93 i.MX 93
     - Arm Ethos-U65, ``libethosu_delegate.so``
     - 3.9
     - 60.2
     - 33.1
   * - 00324 i.MX 93
     - Arm Ethos-U65, ``libethosu_delegate.so``
     - Not measured
     - 59.4
     - 32.9
   * - 00363-91 i.MX 91
     - No NPU
     - No NPU
     - 77.5
     - 77.5 (one core)
   * - 00395 STM32MP257F
     - VeriSilicon, ST X-LINUX-AI
     - Not measured
     - Not measured
     - Not measured

Cargt images do not turn on the i.MX 93 NPU (see :doc:`npu`). Its NPU time is
from an earlier measurement for :doc:`npu`, on an 00363 i.MX 93 on the 00428
carrier with the NPU turned on, using the same model and tool.

The i.MX 95 NPU runs only models converted with NXP's eIQ Neutron converter
(part of the eIQ Toolkit), which is not in the Cargt package feeds. With the
unconverted model, the Neutron delegate leaves every operation on the CPU.
The STM32MP257F NPU needs ST's X-LINUX-AI packages, which are not in the
tested image. Neither NPU is measured yet. The i.MX 91 has no NPU.

On the CPU, a Cortex-A55 core runs the quantized model about three times
faster than the 8M Plus's Cortex-A53; the Cortex-A55 has dot-product
instructions for 8-bit integers, which the Cortex-A53 lacks.

Ethernet
~~~~~~~~

``iperf3`` TCP for 20 seconds in each direction between the board and a
Linux PC on the same Gigabit switch. Every SOM reached Gigabit line rate:

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 30 30

   * - SOM
     - Board sends (Mbit/s)
     - Board receives (Mbit/s)
   * - 00414 i.MX 95
     - 943
     - 941
   * - 00377 i.MX 8M Plus
     - 942
     - 941
   * - 00363-93 i.MX 93
     - 943
     - 941
   * - 00324 i.MX 93
     - 942
     - 941
   * - 00363-91 i.MX 91
     - 940
     - 941
   * - 00395 STM32MP257F
     - 942
     - 941

Wi-Fi throughput is not measured yet: it depends heavily on the access point
and the radio environment. See :doc:`wifi` to connect.

Scheduling Latency
~~~~~~~~~~~~~~~~~~

``cyclictest`` with one thread per core at priority 90, a 1 ms interval, for
60 seconds, while ``stress-ng`` loaded every core, memory and disk I/O. These
are standard (``PREEMPT``) kernels, not real-time kernels.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 40 30 30

   * - SOM
     - Average (µs)
     - Worst (µs)
   * - 00414 i.MX 95
     - 13 to 18
     - 332
   * - 00377 i.MX 8M Plus
     - 13 to 16
     - 359
   * - 00363-93 i.MX 93
     - 20
     - 391
   * - 00324 i.MX 93
     - 21 to 27
     - 557
   * - 00363-91 i.MX 91
     - 32
     - 250
   * - 00395 STM32MP257F
     - 18 to 19
     - 1,184

For bounded latency, use a real-time kernel. On the i.MX 95, the Cargt
real-time build keeps the worst case near 100 µs under the same kind of load;
see :doc:`real-time-linux`. By the end of this test the i.MX 95 had reached
87 °C and the 8M Plus, with its heatsink, 38 °C; see
:doc:`thermal-characterization`.

Web Browsers
~~~~~~~~~~~~

`Speedometer 3.1 <https://browserbench.org/Speedometer3.1/>`__ measures how
fast a browser runs typical web-app work: JavaScript, DOM changes and layout.
`MotionMark 1.3.1 <https://browserbench.org/MotionMark1.3.1/>`__ measures
how much animated graphics a browser can draw while holding its frame rate.
Both ran on ``cargt-image-webkit`` under Weston, with one browser full-screen
at a time. WPE WebKit and Chromium took turns, with a 60-second pause between
runs. Each score is the median of the runs listed, with the lowest and
highest run in brackets.

The i.MX 95 and STM32MP257F boards are the ones in the table above. The
8M Plus and i.MX 93 runs used other boards with the same SOMs: the 8M Plus on
the 00365 carrier with a 1280×800 LVDS panel, and the i.MX 93 on the 00428
carrier.

.. figure:: /_static/images/charts/img-bench-speedometer.svg
   :width: 100%
   :alt: Bar chart of Speedometer 3.1 scores, the median with the lowest and highest run. i.MX 95: WPE WebKit 1.29, Chromium 1.54 (one run each). i.MX 8M Plus: WPE WebKit 1.15 (1.14 to 1.16), Chromium 1.41 (1.40 to 1.42). i.MX 93: WPE WebKit 0.696 (0.691 to 0.700), Chromium 0.921 (0.905 to 0.929). STM32MP257F: WPE WebKit 0.838 (0.831 to 0.843); no Chromium in the image.

   Speedometer 3.1, the median of five to eight runs, with whiskers from the
   lowest to the highest run. The i.MX 95 results are single runs.

.. figure:: /_static/images/charts/img-bench-motionmark.svg
   :width: 100%
   :alt: Bar chart of MotionMark 1.3.1 scores, the median with the lowest and highest run. i.MX 95: not measured. i.MX 8M Plus: not measured, because the GPU driver hung. i.MX 93: WPE WebKit 1.99 (1.61 to 2.03), Chromium 29.0 (22.1 to 33.3). STM32MP257F: WPE WebKit 65.3 (64.6 to 65.4); no Chromium in the image.

   MotionMark 1.3.1, the median of three runs, with whiskers from the lowest
   to the highest run.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 22 22 18 18 20

   * - SOM and display
     - Browser
     - Speedometer 3.1
     - MotionMark 1.3.1
     - Runs
   * - 00414 i.MX 95, 1280×800, Mali-G310
     - WPE WebKit 2.52.6
     - 1.29
     - Not measured
     - 1 Speedometer
   * -
     - Chromium 142
     - 1.54
     - Not measured
     - 1 Speedometer
   * - 00377 i.MX 8M Plus, 1280×800, GC7000UL
     - WPE WebKit 2.52.6
     - 1.15 (1.14 to 1.16)
     - Not measured
     - 5 Speedometer
   * -
     - Chromium 142
     - 1.41 (1.40 to 1.42)
     - Not measured
     - 5 Speedometer
   * - 00363-93 i.MX 93, 720×1280, no 3D GPU
     - WPE WebKit 2.52.6
     - 0.696 (0.691 to 0.700)
     - 1.99 (1.61 to 2.03)
     - 8 Speedometer, 3 MotionMark
   * -
     - Chromium 142
     - 0.921 (0.905 to 0.929)
     - 29.0 (22.1 to 33.3)
     - 8 Speedometer, 3 MotionMark
   * - 00395 STM32MP257F, 720×1280, GCNanoUltra
     - WPE WebKit 2.54.2
     - 0.838 (0.831 to 0.843)
     - 65.3 (64.6 to 65.4)
     - 8 Speedometer, 3 MotionMark

On Speedometer, runs on the same board differed by less than 2%. Chromium 142
scored higher than WPE WebKit 2.52 on every i.MX SOM: 19% on the i.MX 95, 23%
on the 8M Plus and 32% on the i.MX 93. The STM32MP257F, with WPE WebKit 2.54,
lands between the i.MX 93 and the 8M Plus.

On the i.MX 93, both browsers draw on the CPU. WPE WebKit scored about 2 on
MotionMark, the bottom of its scale, and Chromium 29. On the STM32MP257F, WPE
WebKit draws with the GPU and scored 65 at 45 frames per second.

MotionMark was not measured on the 8M Plus. During the series, the Vivante GPU
driver (``galcore``) locked up: Weston and both browsers hung and could not be
stopped, and only a reboot cleared it. Only the Speedometer runs before the
hang are counted. MotionMark was not run on the i.MX 95.

For frame rates on real pages, memory use and how to pick a browser for each
SoC, see :doc:`web-browsers`.

How It Was Measured
-------------------

Every test ran over SSH on a booted board with no application load. The tools are in the Cargt package feeds (see
:doc:`package-management`): ``sysbench``, ``tinymembench``, ``mbw``, ``fio``,
``iperf3``, ``rt-tests`` (``cyclictest``), ``stress-ng``, ``glmark2`` and
``libtensorflow-lite2.19.0``. Install them with ``apt-get install``, or add
them to your image with ``IMAGE_INSTALL``. CoreMark is built from source on
the board, which needs a development image with ``gcc``.

CPU:

.. code-block:: bash

   git clone https://github.com/eembc/coremark.git && cd coremark
   SRC="core_list_join.c core_main.c core_matrix.c core_state.c core_util.c posix/core_portme.c"
   gcc -O2 -Iposix -I. -DFLAGS_STR='"-O2"' -DPERFORMANCE_RUN=1 -DITERATIONS=0 \
       $SRC -o coremark-1 -lrt
   gcc -O2 -Iposix -I. -DFLAGS_STR='"-O2 -lpthread"' -DPERFORMANCE_RUN=1 -DITERATIONS=0 \
       -DMULTITHREAD=$(nproc) -DUSE_PTHREAD $SRC -o coremark-n -lrt -lpthread
   ./coremark-1 0x0 0x0 0x66 0 7 1 2000 | grep Iterations/Sec
   ./coremark-n 0x0 0x0 0x66 0 7 1 2000 | grep Iterations/Sec

   sysbench cpu --cpu-max-prime=20000 --threads=1 --time=30 run
   sysbench cpu --cpu-max-prime=20000 --threads=$(nproc) --time=30 run

Memory:

.. code-block:: bash

   tinymembench
   mbw -q -n 5 -t0 256

Storage. Use a directory on an eMMC partition. On Cargt images ``/tmp`` and
``/var/tmp`` are in RAM, so a test there measures RAM, not the eMMC. The test
writes a 512 MB file; delete it afterwards.

.. code-block:: bash

   cd /home/root        # or another directory on the eMMC
   for t in "write 1M" "read 1M" "randwrite 4k" "randread 4k"; do
       set -- $t
       fio --name=$1 --filename=fio.tmp --size=512M --rw=$1 --bs=$2 --direct=1 \
           --ioengine=libaio --iodepth=16 --runtime=30 --time_based
   done
   rm fio.tmp

   # Bus mode and clock of the eMMC (mmc0 on most i.MX boards)
   mount -t debugfs none /sys/kernel/debug 2>/dev/null
   cat /sys/kernel/debug/mmc0/ios

Boot time, after a normal (not first) boot:

.. code-block:: bash

   systemd-analyze
   systemd-analyze critical-chain getty.target
   systemd-analyze blame | head

GPU, from an SSH session while Weston runs (on the STM32MP2, Weston runs as
the ``weston`` user, so use ``XDG_RUNTIME_DIR=/run/user/1000``):

.. code-block:: bash

   XDG_RUNTIME_DIR=/run/user/0 WAYLAND_DISPLAY=wayland-0 \
       glmark2-es2-wayland --off-screen -s 800x600

NPU (here with the i.MX 8M Plus delegate; see :doc:`npu` for the i.MX 93):

.. code-block:: bash

   cd /usr/bin/tensorflow-lite-2.19.0/examples
   ./benchmark_model --graph=mobilenet_v1_1.0_224_quant.tflite \
       --external_delegate_path=/usr/lib/libvx_delegate.so --num_runs=200
   ./benchmark_model --graph=mobilenet_v1_1.0_224_quant.tflite \
       --num_threads=$(nproc) --num_runs=100

On the 8M Plus, the first inference takes about 3 seconds while the delegate
compiles the model for the NPU; ``benchmark_model`` reports it separately
from the average.

Ethernet, with ``iperf3 -s`` running on a PC on the same network:

.. code-block:: bash

   iperf3 -c <pc-address> -t 20        # board sends
   iperf3 -c <pc-address> -t 20 -R     # board receives

Scheduling latency:

.. code-block:: bash

   stress-ng --cpu $(nproc) --vm 1 --vm-bytes 128M --io 1 --timeout 75s &
   sleep 5
   cyclictest -m -S -p 90 -i 1000 -D 60 -q
   wait

Web browsers, on a board running Weston with the browser full-screen. Open
each page, let it run to the end and read the score from the page:

.. code-block:: text

   https://browserbench.org/Speedometer3.1/?startAutomatically=true
   https://browserbench.org/MotionMark1.3.1/

Close the browser between runs, and give the board a minute to cool down.

Caveats
-------

- **One board per SOM.** Except for the browser scores, each result is one
  run on one board. Expect a few percent of variation between runs and
  boards.
- **The images are not identical.** The boards ran the images listed under
  `Results by Test`_; the STM32MP257F runs OpenSTLinux (scarthgap, kernel
  6.6), the i.MX boards wrynose with kernel 6.18.
- **Short runs.** The CPU tests run 15 to 30 seconds, too short for the SOMs
  to throttle. For sustained load, see :doc:`thermal-characterization`.
- **Power** was not measured.

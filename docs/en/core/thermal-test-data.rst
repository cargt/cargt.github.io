.. _thermal-test-data:

Thermal Test Data
=================


.. rst-class:: cargt-wide-page

Every test behind :doc:`thermal-characterization`, one row per test, including repeats,
4-hour soaks and the burn-in. The same data is available as a spreadsheet:
:download:`all test results (CSV) </_static/data/thermal-test-data.csv>`.

How the tests ran
-----------------

- Each test first lets the SOM settle at idle, then runs one load at fixed
  settings (CPU governor and frequency cap, GPU frequency cap).
- A test ends when the die temperature is steady: the mean of the last minute
  is within 0.3 °C of the mean five minutes earlier (0.15 °C for the
  enclosure, application and NPU tests, because enclosure air warms slowly).
  A test runs at least 20 minutes (40 minutes in an enclosure). Soaks run
  4 hours and the burn-in 9 hours regardless.
- Temperatures are means over the last five minutes of the load. The die
  temperature is the higher of the SoC's die sensors.
- **ΔT** is the die temperature minus the room air. **Max ambient** is the
  SOM's design limit (10 °C below its throttle point) minus ΔT. A test that
  throttled has no max ambient.
- **CPU MHz** is the mean CPU frequency over the last five minutes; **CPU /
  GPU busy** are the mean CPU and GPU load over the whole load period.
- **Performance** is the throughput of the load itself: stress-ng operations
  per second (CPU and memory), glmark2 frames per second (GPU), the UI and
  video frame rates, and NPU inferences per second.


i.MX 95 (00414)
---------------


Open air, no heatsink
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C)
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load) (ondemand)
     - 1800 / 1000
     - 20
     - 21.7
     - 45.7 / 49.3
     - 24.1
     - 71
     - 851, 5 / –
     - –
   * - Idle (no load) (performance)
     - 1800 / 1000
     - 21
     - 22.3
     - 48.4 / 52.7
     - 26.1
     - 69
     - 1800, 6 / –
     - –
   * - CPU, all cores at 50% (ondemand)
     - 900 / 1000
     - 20
     - 22.7
     - 51.2 / 53.6
     - 28.5
     - 67
     - 837, 62 / –
     - cpu 25 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1404 / 1000
     - 20
     - 23.1
     - 55.5 / 59.2
     - 32.4
     - 63
     - 1326, 58 / –
     - cpu 38 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1800 / 1000
     - 20
     - 23.3
     - 60.3 / 64.8
     - 37.1
     - 58
     - 1776, 57 / –
     - cpu 48 ops/s
   * - CPU, all cores at 50% (performance)
     - 900 / 1000
     - 21
     - 23.1
     - 51.8 / 54.3
     - 28.8
     - 66
     - 900, 61 / –
     - cpu 26 ops/s
   * - CPU, all cores at 50% (performance)
     - 1404 / 1000
     - 20
     - 22.9
     - 55.5 / 59.5
     - 32.6
     - 62
     - 1404, 57 / –
     - cpu 38 ops/s
   * - CPU, all cores at 50% (performance)
     - 1800 / 1000
     - 20
     - 22.9
     - 59.9 / 64.9
     - 37.0
     - 58
     - 1800, 57 / –
     - cpu 48 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 900 / 1000
     - 20
     - 22.7
     - 54.6 / 55.6
     - 31.9
     - 63
     - 900, 100 / –
     - cpu 45 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1404 / 1000
     - 20
     - 23.2
     - 62.3 / 62.5
     - 39.0
     - 56
     - 1404, 100 / –
     - cpu 70 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1800 / 1000
     - 21
     - 23.0
     - 69.6 / 69.8
     - 46.6
     - 48
     - 1800, 100 / –
     - cpu 87 ops/s
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 500
     - 20
     - 22.5
     - 53.3 / 54.6
     - 30.8
     - 64
     - 969, 6 / 54
     - glmark2 43 fps
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 800
     - 20
     - 22.5
     - 56.4 / 57.8
     - 33.9
     - 61
     - 1084, 8 / 61
     - glmark2 66 fps
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 1000
     - 20
     - 22.5
     - 58.3 / 59.0
     - 35.9
     - 59
     - 1100, 8 / 57
     - glmark2 81 fps
   * - CPU + GPU + memory (performance)
     - 900 / 1000
     - 23
     - 22.8
     - 65.6 / 66.5
     - 42.8
     - 52
     - 900, 95 / 58
     - cpu 31 ops/s, vm 11098 ops/s, glmark2 62 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 1000
     - 20
     - 22.8
     - 73.0 / 73.9
     - 50.2
     - 45
     - 1404, 90 / 52
     - cpu 49 ops/s, vm 17353 ops/s, glmark2 78 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 1000
     - 240 (4 h soak)
     - 21.6
     - 71.8 / 73.7
     - 50.2
     - 45
     - 1404, 90 / 85
     - cpu 48 ops/s, vm 17364 ops/s, glmark2 78 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 21
     - 23.1
     - 81.3 / 82.4
     - 58.2
     - 37
     - 1800, 93 / 56
     - cpu 56 ops/s, vm 20951 ops/s, glmark2 77 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 240 (4 h soak)
     - 22.4
     - 80.8 / 82.6
     - 58.4
     - 37
     - 1800, 90 / 88
     - cpu 60 ops/s, vm 21376 ops/s, glmark2 79 fps


Open air, passive heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C)
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load) (ondemand)
     - 1800 / 1000
     - 20
     - 21.6
     - 38.5 / 41.3
     - 16.9
     - 78
     - 790, 6 / –
     - –
   * - Idle (no load) (performance)
     - 1800 / 1000
     - 20
     - 21.6
     - 39.7 / 41.9
     - 18.1
     - 77
     - 1800, 6 / –
     - –
   * - CPU, 1 thread (matrixprod) (performance)
     - 900 / 1000
     - 20
     - 20.1
     - 37.6 / 38.2
     - 17.4
     - 78
     - 900, 18 / –
     - cpu 9 ops/s
   * - CPU, 1 thread (matrixprod) (performance)
     - 1404 / 1000
     - 20
     - 20.0
     - 38.6 / 39.3
     - 18.6
     - 76
     - 1404, 18 / –
     - cpu 15 ops/s
   * - CPU, 1 thread (matrixprod) (performance)
     - 1800 / 1000
     - 20
     - 20.0
     - 39.9 / 40.5
     - 19.9
     - 75
     - 1800, 18 / –
     - cpu 19 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 900 / 1000
     - 21
     - 21.7
     - 41.5 / 42.9
     - 19.8
     - 75
     - 829, 61 / –
     - cpu 26 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1404 / 1000
     - 21
     - 21.9
     - 44.3 / 46.6
     - 22.4
     - 73
     - 1326, 58 / –
     - cpu 38 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1800 / 1000
     - 20
     - 21.9
     - 45.7 / 50.0
     - 23.8
     - 71
     - 1313, 54 / –
     - cpu 47 ops/s
   * - CPU, all cores at 50% (performance)
     - 900 / 1000
     - 20
     - 22.1
     - 41.8 / 43.3
     - 19.6
     - 75
     - 900, 55 / –
     - cpu 26 ops/s
   * - CPU, all cores at 50% (performance)
     - 1404 / 1000
     - 20
     - 22.2
     - 44.9 / 47.0
     - 22.7
     - 72
     - 1404, 58 / –
     - cpu 39 ops/s
   * - CPU, all cores at 50% (performance)
     - 1800 / 1000
     - 20
     - 22.2
     - 46.8 / 50.3
     - 24.6
     - 70
     - 1800, 52 / –
     - cpu 49 ops/s
   * - CPU, all cores at 50% (schedutil)
     - 900 / 1000
     - 20
     - 19.7
     - 38.5 / 40.3
     - 18.9
     - 76
     - 725, 54 / –
     - cpu 26 ops/s
   * - CPU, all cores at 50% (schedutil)
     - 1404 / 1000
     - 20
     - 19.6
     - 41.0 / 43.1
     - 21.5
     - 74
     - 1392, 52 / –
     - cpu 39 ops/s
   * - CPU, all cores at 50% (schedutil)
     - 1800 / 1000
     - 20
     - 19.5
     - 43.3 / 46.6
     - 23.8
     - 71
     - 1730, 52 / –
     - cpu 48 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 500 / 1000
     - 20
     - 19.3
     - 38.6 / 38.8
     - 19.3
     - 76
     - 500, 100 / –
     - cpu 29 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 900 / 1000
     - 20
     - 22.3
     - 44.5 / 44.6
     - 22.1
     - 73
     - 900, 100 / –
     - cpu 50 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1404 / 1000
     - 20
     - 22.3
     - 48.8 / 49.0
     - 26.5
     - 69
     - 1404, 100 / –
     - cpu 74 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1800 / 1000
     - 20
     - 22.3
     - 53.2 / 53.4
     - 30.9
     - 64
     - 1800, 100 / –
     - cpu 90 ops/s
   * - CPU, all cores (all methods) (performance)
     - 1800 / 1000
     - 20
     - 19.8
     - 50.3 / 50.8
     - 30.5
     - 65
     - 1800, 100 / –
     - cpu 525 ops/s
   * - Memory (vm, 2 workers, 50% RAM) (ondemand)
     - 1800 / 1000
     - 20
     - 19.9
     - 43.7 / 45.1
     - 23.8
     - 71
     - 1800, 35 / –
     - vm 43935 ops/s
   * - CPU + memory (performance)
     - 1800 / 1000
     - 20
     - 19.7
     - 51.9 / 53.0
     - 32.2
     - 63
     - 1800, 100 / –
     - cpu 61 ops/s, vm 43377 ops/s
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 500
     - 20
     - 22.3
     - 44.3 / 46.8
     - 21.9
     - 73
     - 1099, 9 / 54
     - glmark2 43 fps
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 800
     - 20
     - 22.3
     - 45.4 / 47.2
     - 23.1
     - 72
     - 1009, 9 / 64
     - glmark2 66 fps
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 1000
     - 20
     - 22.1
     - 46.4 / 47.4
     - 24.3
     - 71
     - 1074, 8 / 58
     - glmark2 81 fps
   * - CPU + GPU + memory (performance)
     - 500 / 1000
     - 20
     - 19.4
     - 44.5 / 45.2
     - 25.1
     - 70
     - 500, 95 / 60
     - cpu 19 ops/s, vm 6687 ops/s, glmark2 74 fps
   * - CPU + GPU + memory (performance)
     - 900 / 1000
     - 20
     - 22.4
     - 50.8 / 51.4
     - 28.4
     - 67
     - 900, 92 / 62
     - cpu 33 ops/s, vm 11267 ops/s, glmark2 77 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 500
     - 20
     - 19.4
     - 48.4 / 49.1
     - 29.0
     - 66
     - 1404, 88 / 62
     - cpu 49 ops/s, vm 17583 ops/s, glmark2 43 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 800
     - 20
     - 19.3
     - 50.2 / 51.1
     - 30.9
     - 64
     - 1404, 90 / 53
     - cpu 49 ops/s, vm 17407 ops/s, glmark2 65 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 1000
     - 20
     - 22.4
     - 55.3 / 56.0
     - 32.9
     - 62
     - 1404, 91 / 52
     - cpu 48 ops/s, vm 17353 ops/s, glmark2 78 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 1000
     - 240 (4 h soak)
     - 20.2
     - 53.0 / 54.3
     - 32.7
     - 62
     - 1404, 90 / 90
     - cpu 49 ops/s, vm 17372 ops/s, glmark2 78 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 21
     - 22.4
     - 59.7 / 60.5
     - 37.3
     - 58
     - 1800, 90 / 54
     - cpu 59 ops/s, vm 21284 ops/s, glmark2 79 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 240 (4 h soak)
     - 20.9
     - 58.4 / 60.7
     - 37.5
     - 58
     - 1800, 90 / 88
     - cpu 59 ops/s, vm 21474 ops/s, glmark2 63 fps
   * - CPU + GPU + memory, verified (burn-in) (performance)
     - 1800 / 1000
     - 540 (9 h burn-in)
     - 23.5
     - 61.6 / 62.9
     - 38.2
     - 57
     - 1800, 90 / 90
     - cpu 59 ops/s, vm 21532 ops/s, glmark2 79 fps
   * - CPU + GPU + memory, verified (burn-in) (performance)
     - 1800 / 1000
     - 540 (9 h burn-in)
     - 20.5
     - 57.8 / 62.2
     - 37.3
     - 58
     - 1800, 90 / 92
     - cpu 60 ops/s, vm 21428 ops/s, glmark2 79 fps
   * - CPU + GPU + memory, verified (burn-in) (performance)
     - 1800 / 1000
     - 540 (9 h burn-in)
     - 22.5
     - 60.7 / 61.5
     - 38.2
     - 57
     - 1800, 90 / 92
     - cpu 60 ops/s, vm 21439 ops/s, glmark2 79 fps
   * - CPU + GPU + memory, verified (burn-in) (performance)
     - 1800 / 1000
     - 540 (9 h burn-in)
     - 22.1
     - 60.1 / 63.3
     - 38.0
     - 57
     - 1800, 90 / 92
     - cpu 60 ops/s, vm 21451 ops/s, glmark2 79 fps


Enclosure (Polycase WA Series WA-42\*16), passive heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C) / enclosure air
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load) (ondemand)
     - 1800 / 1000
     - 40
     - 23.6 / 26.9
     - 47.0 / 50.9
     - 23.4
     - 72
     - 791, 7 / –
     - –
   * - CPU, all cores at 50% (ondemand)
     - 900 / 1000
     - 41
     - 23.2 / 26.3
     - 49.4 / 51.0
     - 26.2
     - 69
     - 873, 61 / –
     - cpu 26 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1404 / 1000
     - 40
     - 22.9 / 26.4
     - 51.9 / 54.5
     - 29.0
     - 66
     - 1207, 58 / –
     - cpu 38 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1800 / 1000
     - 40
     - 23.4 / 26.8
     - 55.4 / 58.6
     - 32.0
     - 63
     - 1726, 57 / –
     - cpu 48 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 900 / 1000
     - 40
     - 23.1 / 26.3
     - 51.6 / 51.8
     - 28.5
     - 66
     - 900, 100 / –
     - cpu 45 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1404 / 1000
     - 40
     - 23.1 / 26.6
     - 56.6 / 56.7
     - 33.5
     - 62
     - 1404, 100 / –
     - cpu 68 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1800 / 1000
     - 40
     - 22.6 / 26.4
     - 61.5 / 61.7
     - 38.9
     - 56
     - 1800, 100 / –
     - cpu 84 ops/s
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 1000
     - 40
     - 22.8 / 26.5
     - 55.5 / 58.0
     - 32.8
     - 62
     - 1113, 14 / 86
     - glmark2 81 fps
   * - CPU + GPU + memory (performance)
     - 900 / 1000
     - 40
     - 22.8 / 26.6
     - 59.0 / 59.6
     - 36.2
     - 59
     - 900, 97 / 62
     - cpu 30 ops/s, vm 10878 ops/s, glmark2 74 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 1000
     - 240 (4 h soak)
     - 24.0 / 28.8
     - 66.8 / 67.8
     - 42.7
     - 52
     - 1404, 93 / 84
     - cpu 47 ops/s, vm 16857 ops/s, glmark2 75 fps
   * - CPU + GPU + memory (performance)
     - 1404 / 1000
     - 41
     - 22.9 / 26.9
     - 64.4 / 65.2
     - 41.5
     - 54
     - 1404, 95 / 76
     - cpu 46 ops/s, vm 16601 ops/s, glmark2 76 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 240 (4 h soak)
     - 24.1 / 29.2
     - 72.3 / 73.2
     - 48.3
     - 47
     - 1800, 91 / 85
     - cpu 59 ops/s, vm 21118 ops/s, glmark2 77 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 43
     - 22.8 / 27.2
     - 69.9 / 70.8
     - 47.0
     - 48
     - 1800, 93 / 84
     - cpu 57 ops/s, vm 20509 ops/s, glmark2 77 fps
   * - Chromium kiosk HMI (charts at 60 fps) (ondemand)
     - 1800 / 1000
     - 40
     - 22.4 / 26.1
     - 53.0 / 54.6
     - 30.6
     - 64
     - 1669, 38 / 40
     - UI 49 fps
   * - Video playback, 1080p30 H.264 (VPU) (ondemand)
     - 1800 / 1000
     - 40
     - 23.4 / 26.3
     - 47.8 / 50.6
     - 24.4
     - 71
     - 999, 10 / –
     - video 30 fps
   * - Video decode, max rate, 1080p H.264 (VPU) (ondemand)
     - 1800 / 1000
     - 40
     - 23.7 / 26.8
     - 50.5 / 53.0
     - 26.8
     - 68
     - 1151, 13 / –
     - video 359 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 900 / 1000
     - 40
     - 24.1 / 27.6
     - 52.5 / 52.9
     - 28.4
     - 67
     - 900, 42 / 37
     - UI 39 fps, video 30 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 1404 / 1000
     - 40
     - 24.1 / 27.7
     - 54.1 / 54.8
     - 30.0
     - 65
     - 1373, 37 / 42
     - UI 49 fps, video 30 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 1800 / 1000
     - 40
     - 23.4 / 27.4
     - 54.6 / 55.3
     - 31.2
     - 64
     - 1649, 34 / 44
     - UI 50 fps, video 30 fps
   * - NPU inference, MobileNet v1 (Neutron) (ondemand)
     - 1800 / 1000
     - 40
     - 23.0 / 26.3
     - 56.2 / 60.2
     - 33.2
     - 62
     - 1112, 8 / –
     - NPU 821 inferences/s
   * - NPU object detection, SSD MobileNet (Neutron + CPU) (ondemand)
     - 1800 / 1000
     - 40
     - 23.4 / 26.8
     - 53.6 / 56.6
     - 30.2
     - 65
     - 1197, 15 / –
     - NPU 194 inferences/s
   * - Chromium HMI + 1080p30 video + NPU detection (ondemand)
     - 1800 / 1000
     - 41
     - 23.4 / 27.7
     - 63.7 / 64.2
     - 40.2
     - 55
     - 1752, 48 / 45
     - UI 48 fps, video 30 fps, NPU 216 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1404 / 1000
     - 52
     - 24.3 / 29.2
     - 73.9 / 74.3
     - 49.6
     - 45
     - 1404, 94 / 79
     - cpu 44 ops/s, vm 15691 ops/s, glmark2 70 fps, NPU 671 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1404 / 1000
     - 240
     - 23.2 / 28.6
     - 73.8 / 74.3
     - 50.6
     - 44
     - 1404, 94 / 83
     - cpu 44 ops/s, vm 14913 ops/s, glmark2 70 fps, NPU 667 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1800 / 1000
     - 46
     - 23.7 / 29.2
     - 79.5 / 80.1
     - 55.9
     - 39
     - 1800, 93 / 77
     - cpu 52 ops/s, vm 19665 ops/s, glmark2 70 fps, NPU 699 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1800 / 1000
     - 240
     - 23.5 / 29.2
     - 80.2 / 81.2
     - 56.7
     - 38
     - 1800, 93 / 88
     - cpu 53 ops/s, vm 19730 ops/s, glmark2 71 fps, NPU 694 inferences/s


Throttle tests (throttle point lowered): enclosure (Polycase WA Series WA-42\*16), passive heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Throttle point (°C)
     - Test (min)
     - Room air (°C) / enclosure air
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - CPU, all cores (matrixprod) (performance)
     - 1800 / 1000
     - 55
     - 40
     - 23.4 / 27.6
     - 55.1 / 56.1
     - 31.6
     - throttled after 6 s (99 %)
     - 1076, 100 / –
     - cpu 61 ops/s
   * - GPU (glmark2 terrain) (ondemand)
     - 1800 / 1000
     - 50
     - 40
     - 23.4 / 27.0
     - 51.9 / 52.3
     - 28.5
     - throttled after 8 s (100 %)
     - 644, 9 / 68
     - glmark2 54 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 65
     - 40
     - 24.3 / 28.4
     - 63.9 / 67.0
     - 39.6
     - throttled after 324 s (63 %)
     - 1169, 91 / 66
     - cpu 49 ops/s, vm 15600 ops/s, glmark2 77 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 60
     - 41
     - 23.9 / 28.2
     - 61.9 / 63.0
     - 38.1
     - throttled after 26 s (97 %)
     - 980, 92 / 77
     - cpu 38 ops/s, vm 12505 ops/s, glmark2 76 fps
   * - CPU + GPU + memory (performance)
     - 1800 / 1000
     - 55
     - 40
     - 24.1 / 27.9
     - 56.3 / 58.6
     - 32.2
     - throttled after 4 s (100 %)
     - 707, 92 / 84
     - cpu 26 ops/s, vm 8303 ops/s, glmark2 50 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 1800 / 1000
     - 50
     - 40
     - 23.5 / 27.0
     - 51.0 / 51.9
     - 27.5
     - throttled after 6 s (100 %)
     - 631, 46 / 30
     - UI 25 fps, video 30 fps


i.MX 8M Plus (00377)
--------------------


Open air, no heatsink
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C)
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load) (ondemand)
     - 1600 / –
     - 20
     - 23.2
     - 42.2 / 43.0
     - 18.9
     - 66
     - 1221, 1 / 0
     - –
   * - Idle (no load) (ondemand)
     - 1600 / –
     - 20
     - 22.6
     - 40.3 / 42.0
     - 17.7
     - 67
     - 1213, 1 / 0
     - –
   * - Idle (no load) (performance)
     - 1600 / –
     - 21
     - 23.3
     - 42.3 / 44.0
     - 19.0
     - 66
     - 1600, 1 / 0
     - –
   * - CPU, all cores at 50% (ondemand)
     - 1200 / –
     - 20
     - 22.7
     - 45.4 / 48.0
     - 22.6
     - 62
     - 1200, 53 / 0
     - cpu 21 ops/s
   * - CPU, all cores at 50% (ondemand)
     - 1600 / –
     - 20
     - 23.0
     - 48.1 / 52.0
     - 25.1
     - 60
     - 1481, 52 / 0
     - cpu 27 ops/s
   * - CPU, all cores at 50% (performance)
     - 1200 / –
     - 20
     - 23.1
     - 45.6 / 48.0
     - 22.5
     - 62
     - 1200, 53 / 0
     - cpu 21 ops/s
   * - CPU, all cores at 50% (performance)
     - 1600 / –
     - 20
     - 23.1
     - 48.3 / 52.0
     - 25.2
     - 60
     - 1600, 52 / 0
     - cpu 27 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1200 / –
     - 20
     - 23.2
     - 49.0 / 49.0
     - 25.8
     - 59
     - 1200, 100 / 0
     - cpu 40 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1600 / –
     - 20
     - 23.2
     - 53.8 / 54.0
     - 30.6
     - 54
     - 1600, 100 / 0
     - cpu 52 ops/s
   * - GPU (glmark2 terrain) (ondemand)
     - 1600 / –
     - 20
     - 23.0
     - 48.0 / 49.0
     - 25.1
     - 60
     - 1208, 3 / 10
     - glmark2 19 fps
   * - CPU + GPU + memory (performance)
     - 1200 / –
     - 20
     - 23.2
     - 52.8 / 54.0
     - 29.6
     - 55
     - 1200, 78 / 9
     - cpu 20 ops/s, vm 13298 ops/s, glmark2 17 fps
   * - CPU + GPU + memory (performance)
     - 1600 / –
     - 20
     - 23.1
     - 56.5 / 58.0
     - 33.4
     - 52
     - 1600, 78 / 10
     - cpu 25 ops/s, vm 16529 ops/s, glmark2 17 fps
   * - Video playback, 1080p30 H.264 (VPU) (ondemand)
     - 1600 / –
     - 20
     - 22.9
     - 41.7 / 42.0
     - 18.7
     - 66
     - 1205, 4 / 0
     - video 30 fps
   * - Video decode, max rate, 1080p H.264 (VPU) (ondemand)
     - 1600 / –
     - 20
     - 22.5
     - 42.7 / 44.0
     - 20.3
     - 65
     - 1219, 10 / 0
     - video 249 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 1200 / –
     - 20
     - 22.6
     - 46.2 / 47.0
     - 23.6
     - 61
     - 1200, 48 / 29
     - UI 30 fps, video 30 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 1600 / –
     - 20
     - 22.8
     - 48.2 / 50.0
     - 25.3
     - 60
     - 1595, 45 / 24
     - UI 33 fps, video 30 fps
   * - NPU inference, MobileNet v1 (VIP8000) (ondemand)
     - 1600 / –
     - 20
     - 22.9
     - 51.8 / 52.0
     - 28.9
     - 56
     - 1227, 10 / 0
     - NPU 289 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1600 / –
     - 20
     - 22.3
     - 62.7 / 64.0
     - 40.4
     - 45
     - 1600, 88 / 10
     - cpu 23 ops/s, vm 15943 ops/s, glmark2 16 fps, NPU 209 inferences/s


Enclosure (Polycase WA Series WA-42\*16), no heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C) / enclosure air
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load) (ondemand)
     - 1600 / –
     - 41
     - 22.8 / 27.3
     - 46.8 / 50.0
     - 24.0
     - 61
     - 1230, 2 / 0
     - –
   * - CPU, all cores at 50% (ondemand)
     - 1600 / –
     - 40
     - 22.9 / 28.0
     - 53.5 / 57.0
     - 30.6
     - 54
     - 1549, 53 / 0
     - cpu 27 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1200 / –
     - 42
     - 23.1 / 28.4
     - 54.5 / 55.0
     - 31.4
     - 54
     - 1200, 100 / 0
     - cpu 40 ops/s
   * - CPU, all cores (matrixprod) (performance)
     - 1600 / –
     - 40
     - 22.9 / 28.9
     - 60.0 / 60.0
     - 37.1
     - 48
     - 1600, 100 / 0
     - cpu 51 ops/s
   * - GPU (glmark2 terrain) (ondemand)
     - 1600 / –
     - 40
     - 23.6 / 29.5
     - 56.9 / 59.0
     - 33.2
     - 52
     - 1235, 4 / 10
     - glmark2 19 fps
   * - CPU + GPU + memory (performance)
     - 1200 / –
     - 40
     - 23.2 / 29.4
     - 61.7 / 63.0
     - 38.4
     - 47
     - 1200, 80 / 9
     - cpu 20 ops/s, vm 13170 ops/s, glmark2 18 fps
   * - CPU + GPU + memory (performance)
     - 1600 / –
     - 41
     - 23.0 / 29.7
     - 65.8 / 67.0
     - 42.7
     - 42
     - 1600, 79 / 10
     - cpu 25 ops/s, vm 16310 ops/s, glmark2 17 fps
   * - CPU + GPU + memory (performance)
     - 1600 / –
     - 40
     - 23.7 / 27.4
     - 65.8 / 67.0
     - 42.1
     - 43
     - 1600, 79 / –
     - cpu 25 ops/s, vm 16483 ops/s, glmark2 16 fps
   * - Video playback, 1080p30 H.264 (VPU) (ondemand)
     - 1600 / –
     - 41
     - 23.7 / 29.0
     - 49.1 / 51.0
     - 25.4
     - 60
     - 1223, 5 / 0
     - video 30 fps
   * - Chromium kiosk HMI + 1080p30 video (ondemand)
     - 1600 / –
     - 40
     - 23.3 / 29.6
     - 57.0 / 58.0
     - 33.7
     - 51
     - 1591, 46 / 25
     - UI 32 fps, video 30 fps
   * - NPU inference, MobileNet v1 (VIP8000) (ondemand)
     - 1600 / –
     - 40
     - 23.8 / 30.0
     - 60.9 / 62.0
     - 37.1
     - 48
     - 1235, 11 / 0
     - NPU 288 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1200 / –
     - 40
     - 23.3 / 26.7
     - 68.8 / 70.0
     - 45.5
     - 39
     - 1200, 89 / –
     - cpu 18 ops/s, vm 12309 ops/s, glmark2 14 fps, NPU 207 inferences/s
   * - CPU + GPU + memory + NPU (performance)
     - 1600 / –
     - 41
     - 23.5 / 27.5
     - 73.9 / 76.0
     - 50.3
     - 35
     - 1600, 89 / –
     - cpu 22 ops/s, vm 15387 ops/s, glmark2 15 fps, NPU 211 inferences/s


i.MX 93 (00363)
---------------


Open air, no heatsink
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C)
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load)
     - – / –
     - 20
     - 22.7
     - 35.4 / 36.4
     - 12.8
     - 72
     - –, 3 / –
     - –
   * - Idle (no load)
     - – / –
     - 20
     - 23.0
     - 35.8 / 36.9
     - 12.8
     - 72
     - –, 3 / –
     - –
   * - CPU, all cores at 50%
     - – / –
     - 20
     - 22.9
     - 39.3 / 41.9
     - 16.5
     - 69
     - –, 54 / –
     - cpu 16 ops/s
   * - CPU, all cores (matrixprod)
     - – / –
     - 20
     - 22.9
     - 42.3 / 42.9
     - 19.3
     - 66
     - –, 100 / –
     - cpu 29 ops/s
   * - CPU, all cores (matrixprod)
     - – / –
     - 20
     - 22.6
     - 42.1 / 42.4
     - 19.5
     - 65
     - –, 100 / –
     - cpu 29 ops/s
   * - CPU + memory
     - – / –
     - 20
     - 23.0
     - 43.3 / 43.9
     - 20.3
     - 65
     - –, 100 / –
     - cpu 14 ops/s, vm 18667 ops/s
   * - CPU + memory
     - – / –
     - 20
     - 22.9
     - 43.3 / 44.4
     - 20.4
     - 65
     - –, 100 / –
     - cpu 14 ops/s, vm 18743 ops/s
   * - CPU + memory
     - – / –
     - 20
     - 22.7
     - 43.4 / 44.4
     - 20.7
     - 64
     - –, 100 / –
     - cpu 14 ops/s, vm 18769 ops/s
   * - Chromium kiosk HMI (charts at 60 fps)
     - – / –
     - 20
     - 22.5
     - 42.5 / 43.4
     - 20.0
     - 65
     - –, 83 / –
     - UI 13 fps


Enclosure (Polycase WA Series WA-42\*16), no heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Test (min)
     - Room air (°C) / enclosure air
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - Idle (no load)
     - – / –
     - 41
     - 23.1 / 24.6
     - 39.1 / 40.4
     - 16.1
     - 69
     - –, 4 / –
     - –
   * - CPU, all cores at 50%
     - – / –
     - 40
     - 23.1 / 25.0
     - 42.7 / 44.9
     - 19.7
     - 65
     - –, 54 / –
     - cpu 15 ops/s
   * - CPU, all cores (matrixprod)
     - – / –
     - 40
     - 23.4 / 25.4
     - 45.9 / 46.4
     - 22.5
     - 63
     - –, 100 / –
     - cpu 28 ops/s
   * - CPU + memory
     - – / –
     - 40
     - 23.3 / 25.6
     - 47.2 / 47.9
     - 23.9
     - 61
     - –, 100 / –
     - cpu 13 ops/s, vm 18305 ops/s
   * - CPU + memory
     - – / –
     - 41
     - 23.4 / 26.0
     - 47.4 / 48.4
     - 24.0
     - 61
     - –, 100 / –
     - cpu 13 ops/s, vm 18477 ops/s
   * - Chromium kiosk HMI (charts at 60 fps)
     - – / –
     - 40
     - 23.5 / 25.8
     - 46.7 / 47.4
     - 23.2
     - 62
     - –, 85 / –
     - UI 12 fps


Throttle tests (throttle point lowered): open air, no heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 24 9 7 7 9 9 6 9 10 20

   * - Load (governor)
     - CPU / GPU cap (MHz)
     - Throttle point (°C)
     - Test (min)
     - Room air (°C)
     - Die steady / max (°C)
     - ΔT (°C)
     - Max ambient (°C)
     - CPU MHz, CPU / GPU busy %
     - Performance
   * - CPU + memory
     - – / –
     - 42
     - 20
     - 22.9
     - 41.0 / 42.9
     - 18.1
     - throttled after 16 s (60 %)
     - –, 100 / –
     - cpu 12 ops/s, vm 15252 ops/s
   * - CPU + memory
     - – / –
     - 39
     - 20
     - 22.8
     - 39.4 / 41.4
     - 16.6
     - throttled after 4 s (100 %)
     - –, 100 / –
     - cpu 10 ops/s, vm 13425 ops/s

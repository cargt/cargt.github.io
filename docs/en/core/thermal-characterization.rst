.. _thermal-characterization:

Thermal Characterization of Cargt SOMs
======================================

Will your product need a heatsink? This page answers that for Cargt SOMs. We
ran each SOM under a range of loads, CPU frequency caps and cooling options,
in open air and in a sealed plastic enclosure, until its temperature stopped
changing. From each test we report the warmest air the setup can run in
without the processor reaching its design limit.

.. list-table:: SOMs covered
   :class: wrap-cells
   :header-rows: 1
   :widths: 18 22 60

   * - SOM
     - Processor
     - Status
   * - :ref:`00414 <00414>`
     - i.MX 95
     - Tested: open air and enclosure, no heatsink and passive heatsink,
       stress, application and NPU loads
   * - :ref:`00377 <00377>`
     - i.MX 8M Plus
     - Tested: open air and enclosure, no heatsink, stress, application and
       NPU loads. Passive heatsink testing planned
   * - :ref:`00363-93 <00363-93>`
     - i.MX 93
     - Tested: open air and enclosure, no heatsink, stress and application
       loads. NPU testing planned

Results for each SOM are added here as testing completes. Every test, with
its full measurements, is listed in :doc:`thermal-test-data`.

How to read the results
-----------------------

Each test runs one load until the die temperature is steady, which takes
20 minutes to 4 hours. Two numbers come out of it:

- **ΔT** is the steady die temperature minus the surrounding air temperature.
  It depends on the load, the CPU frequency cap and the cooling, but hardly on
  the room temperature.
- **Maximum ambient** is the design limit minus ΔT: the warmest surrounding
  air the setup can run in without the die passing the design limit.

The **design limit** is 10 °C below the temperature at which the processor
starts to throttle (its passive trip point). Below it, the SOM runs at full
speed with margin to spare. For the i.MX 95 the passive trip is 105 °C, so
the design limit is **95 °C**. For the i.MX 8M Plus the passive trip is
95 °C, so the design limit is **85 °C**, and the same holds for the i.MX 93.

.. note::

   The maximum ambient figures come from tests in a 19–24 °C room. Leakage
   current rises with temperature, so ΔT grows somewhat at high ambient, and
   figures above about 50 °C are extrapolations. Temperature chamber tests
   to confirm them are planned.

Summary
-------

For the i.MX 95 (00414):

- **With the passive heatsink, the SOM suits indoor products in a sealed
  plastic enclosure**, even at full load. The worst case we tested, CPU, GPU,
  memory and NPU all fully loaded at 1.8 GHz, still allows 38 °C room air
  (44 °C with the CPU capped at 1.4 GHz). A touchscreen UI with video
  playback allows about 64 °C.
- **Without a heatsink, the worst case allows only 37 °C** air in open air at
  1.8 GHz (45 °C at 1.4 GHz). That is enough for light loads but not for
  sustained full load in an enclosure.
- **Capping the CPU frequency is the most effective setting.** Each step
  between 900, 1404 and 1800 MHz changes ΔT by 4–8 °C under load.
- **Real application loads run much cooler than stress tests.** A
  touchscreen UI with 1080p30 video runs about 17 °C cooler than CPU, GPU and
  memory fully loaded.
- **The NPU is a significant heat source.** At 50–60 % busy it adds about
  9–10 °C of ΔT.
- **When the SOM does throttle, it degrades gracefully.** The kernel holds
  the die 1–3 °C under the throttle point by lowering the CPU and then the GPU
  frequency; video playback keeps its frame rate.

For the i.MX 8M Plus (00377):

- **In open air, the SOM needs no heatsink.** The worst case we tested, CPU,
  GPU, memory and NPU all fully loaded at 1.6 GHz, allows 45 °C room air;
  without the NPU, 52 °C. A touchscreen UI with video playback allows about
  60 °C.
- **It runs much cooler than the i.MX 95.** Under the same full CPU, GPU and
  memory load it rises 33 °C above the room, against 58 °C for the i.MX 95
  without a heatsink, so it allows 7–15 °C warmer air despite its lower
  design limit.
- **In a sealed plastic enclosure, it needs no heatsink unless the NPU runs
  flat out with everything else.** Without the NPU, every load allows at
  least 42 °C room air; a touchscreen UI with video allows 51 °C. With CPU,
  GPU, memory and NPU all fully loaded it allows 35 °C at 1.6 GHz and 39 °C
  at 1.2 GHz.
- **The NPU is again the largest single heat source**, adding 7–10 °C of ΔT.

For the i.MX 93 (00363):

- **It needs no heatsink, in open air or in a sealed plastic enclosure.**
  Under full CPU and memory load it rises only 20 °C above the room in open
  air and 24 °C in the enclosure, so it allows 64 °C and 61 °C room air.
- **It runs much cooler than the i.MX 8M Plus**: with all CPU cores loaded it
  rises 19 °C above the room, against 31 °C for the i.MX 8M Plus at 1.6 GHz.
- **The enclosure costs only about 3 °C of ambient.** The air inside it ran
  2–3 °C above the room.

i.MX 95 (00414) results
-----------------------

Test setup
~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :widths: 25 75

   * - Hardware
     - 00414 i.MX 95 OSM-L SOM on the 00365 carrier board, no display
       connected
   * - Software
     - Cargt Linux BSP (NXP lf-6.18.20). CPU governor: performance for the
       full-load tests, ondemand for the others.
   * - CPU frequency caps
     - 900, 1404 and 1800 MHz. The i.MX 95 Cortex-A55 cores have no 1.2 GHz
       operating point; 1404 MHz is the nearest.
   * - Die temperature
     - The higher of the i.MX 95 ANA and A55 thermal sensors
   * - Ambient
     - Dracal USB-PTH450 sensors: one in the room and, for enclosure tests,
       one in the enclosure air
   * - Passive heatsink
     - Advanced Thermal Solutions ATS-CPX045045025-162-C2-R0 (45 × 45 × 25 mm)
       with its pre-applied phase-change interface material, fastened to the
       00365 carrier with ATS-HK91-R0 hardware
   * - Enclosure
     - Polycase WA Series WA-42*16 (12 × 9 × 3 in), lid sealed, no vents

Loads:

- **Stress loads:** ``stress-ng`` on the CPU (all cores, half load, or a single
  thread) and memory; ``glmark2`` on the GPU; and all of them at once ("CPU +
  GPU + memory").
- **Application loads:**

  - a Chromium kiosk touchscreen UI, with three scrolling charts at the
    display rate, live value tiles and an event list;
  - 1080p30 H.264 video playback on the VPU.

- **NPU loads:** TensorFlow Lite inference on the eIQ Neutron NPU:

  - MobileNet v1 image classification;
  - SSD MobileNet object detection.

Open air: no heatsink and passive heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 34 14 14 14 24

   * - Load
     - CPU cap (MHz)
     - ΔT, no heatsink (°C)
     - ΔT, passive (°C)
     - Maximum ambient, no heatsink → passive
   * - CPU + GPU + memory
     - 1800
     - 58.4
     - 37.5
     - 37 → 58 °C
   * - CPU + GPU + memory
     - 1404
     - 50.2
     - 32.7
     - 45 → 62 °C
   * - CPU + GPU + memory
     - 900
     - 42.8
     - 28.4
     - 52 → 67 °C
   * - CPU, all cores
     - 1800
     - 46.6
     - 30.9
     - 48 → 64 °C
   * - GPU only
     - 1800
     - 35.9
     - 24.3
     - 59 → 71 °C
   * - CPU, all cores at 50 %
     - 1800
     - 37.1
     - 23.8
     - 58 → 71 °C
   * - Idle
     - 1800
     - 24.1
     - 16.9
     - 71 → 78 °C

- The passive heatsink lowers ΔT by 30–36 %, which allows 7–21 °C warmer air.
  The gain is largest under the heaviest loads.
- No test throttled. The hottest die reading was 82.6 °C, at full load with no
  heatsink.
- The CPU governor (ondemand, performance or schedutil) changed temperatures
  by less than 1 °C at the same cap and load. A governor does not replace a
  frequency cap.
- Reducing the GPU frequency cap from 1000 to 500 MHz lowers ΔT by only
  2–4 °C.

Sealed enclosure, passive heatsink
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 14 18 14 24

   * - Load
     - CPU cap (MHz)
     - ΔT, open air → enclosure (°C)
     - Enclosure air above room (°C)
     - Maximum ambient, open air → enclosure
   * - CPU + GPU + memory
     - 1800
     - 37.5 → 48.3
     - 5.2
     - 58 → **47 °C**
   * - CPU + GPU + memory
     - 1404
     - 32.7 → 42.7
     - 4.7
     - 62 → **52 °C**
   * - CPU + GPU + memory
     - 900
     - 28.4 → 36.2
     - 3.7
     - 67 → 59 °C
   * - CPU, all cores
     - 1404
     - 26.5 → 33.5
     - 3.4
     - 69 → 62 °C
   * - GPU only
     - 1800
     - 24.3 → 32.8
     - 3.7
     - 71 → 62 °C
   * - Idle
     - 1800
     - 16.9 → 23.4
     - 3.2
     - 78 → 72 °C

- The enclosure costs 6.5–11 °C of maximum ambient. Only 3–5 °C of that is
  the enclosure air warming up. The rest is the heatsink working less well in
  still air.
- An enclosure takes several hours to settle. The 4-hour tests ran about
  1.3 °C warmer than 40-minute tests at the same settings. The CPU + GPU +
  memory rows above are from 4-hour tests.
- No test throttled. The hottest die reading was 73.2 °C.

Application and NPU loads in the enclosure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All with the passive heatsink, CPU capped at 1800 MHz unless stated.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 36 12 16 36

   * - Load
     - ΔT (°C)
     - Maximum ambient
     - Performance
   * - Idle
     - 23.4
     - 72 °C
     - –
   * - 1080p30 video playback
     - 24.5
     - 71 °C
     - 30 fps, no dropped frames
   * - Touchscreen UI
     - 30.6
     - 64 °C
     - 49 fps
   * - Touchscreen UI + 1080p30 video
     - 31.2
     - 64 °C
     - UI 50 fps, video 30 fps
   * - Touchscreen UI + video, CPU at 1404 MHz
     - 30.0
     - 65 °C
     - UI 49 fps, video 30 fps
   * - Touchscreen UI + video, CPU at 900 MHz
     - 28.4
     - 67 °C
     - UI 39 fps, video 30 fps
   * - Object detection on the NPU
     - 30.2
     - 65 °C
     - 194 inferences/s
   * - Image classification on the NPU
     - 33.2
     - 62 °C
     - 821 inferences/s (1.2 ms each)
   * - Touchscreen UI + video + object detection
     - 40.2
     - 55 °C
     - UI 48 fps, video 30 fps, 216 inferences/s
   * - CPU + GPU + memory + NPU (4 hours)
     - 56.7
     - **38 °C**
     - all at full load
   * - CPU + GPU + memory + NPU, CPU at 1404 MHz (4 hours)
     - 50.6
     - **44 °C**
     - CPU −16 %, memory −24 %, NPU −4 %, GPU unchanged

- **Video playback costs almost nothing:** the VPU adds about 1 °C to ΔT.
- **For a UI, 1404 MHz costs nothing:** the UI keeps its frame rate and the
  chip runs 1.2 °C cooler than at 1800 MHz. At 900 MHz the UI frame rate
  drops 22 % for only 1.6 °C more.
- **The NPU adds 9–10 °C of ΔT** at 50–60 % busy, whatever else is running.
  MobileNet runs in 1.2 ms per inference on the NPU, against 13 ms on the CPU.
- **CPU + GPU + memory + NPU is the worst case tested.** It allows 38 °C room
  air in the enclosure, against about 47 °C for the same load without the
  NPU. Over 4 hours it settled under 1 °C hotter than in a 1-hour run.
- **A 1404 MHz CPU cap recovers 6 °C** of that worst case, to 44 °C. It costs
  16 % of CPU and 24 % of memory throughput; the NPU loses only 4 % and the
  GPU nothing.

Throttling behavior
~~~~~~~~~~~~~~~~~~~

No real test throttled, so we lowered the throttle point (passive trip) to
make the SOM throttle at room temperature and see how it behaves. All runs
were in the enclosure with the passive heatsink, capped at 1800 MHz.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 14 16 40

   * - Load
     - Throttle point
     - CPU MHz while throttled
     - Performance while throttled
   * - CPU + GPU + memory
     - 65 °C
     - 1169
     - CPU −18 %, memory −27 %, GPU unchanged
   * - CPU + GPU + memory
     - 60 °C
     - 980
     - CPU −35 %, memory −41 %, GPU unchanged
   * - CPU + GPU + memory
     - 55 °C
     - 707
     - CPU −57 %, memory −61 %, GPU −35 %
   * - Touchscreen UI + video
     - 50 °C
     - 631
     - UI 50 → 25 fps; video still 30 fps

- Throttling is orderly. The kernel holds the die 1–3 °C under the throttle
  point by stepping the CPU down first and the GPU only when that is not
  enough.
- The SOM ran steadily for over 40 minutes while throttled, with no
  oscillation, errors or crashes.
- The cost grows with how far the load overshoots: 5 °C over costs 20–35 % of
  CPU performance, 15 °C or more costs over half.

Long-term stability
~~~~~~~~~~~~~~~~~~~

- **36 hours at full load:** CPU + GPU + memory at 1800 MHz with the passive
  heatsink in open air, using ``stress-ng --verify``. There were no errors and
  no throttling. Throughput stayed constant: CPU 59.4–60.0 operations/s, GPU
  79 fps.
- **Consistent results:** 4-hour tests matched the 20-minute tests within
  0.2 °C in open air. Over the 36 hours the room varied by 3 °C while ΔT
  stayed within 1 °C.

.. _thermal-00377:

i.MX 8M Plus (00377) results
----------------------------

Test setup
~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :widths: 25 75

   * - Hardware
     - 00377 i.MX 8M Plus OSM-L SOM on the 00365 carrier board, no
       heatsink, in open air on a desk and in a sealed Polycase WA-42*16
       plastic enclosure. For the UI and video tests the HDMI output was
       enabled with no monitor connected.
   * - Software
     - Cargt Linux BSP (NXP lf-6.18.20). CPU governor: performance for the
       full-load tests, ondemand for the others.
   * - CPU frequency caps
     - 1200 and 1600 MHz, the two Cortex-A53 operating points of this part.
       The GC7000UL GPU has no frequency levels to cap.
   * - Die temperature
     - The higher of the i.MX 8M Plus CPU and SoC thermal sensors, which
       report whole degrees
   * - Ambient
     - A Dracal USB-PTH450 sensor in the room, 22–24 °C. In the enclosure, a
       second sensor measured the air inside it.

The loads are those used for the i.MX 95, with the NPU loads running on the
VIP8000 NPU through the TensorFlow Lite VX delegate. Every test ran to a
steady die temperature and none throttled.

Open air, no heatsink
~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 34 12 12 14 28

   * - Load
     - CPU cap MHz
     - ΔT °C
     - Max ambient
     - Performance
   * - CPU + GPU + memory + NPU
     - 1600
     - 40.4
     - **45 °C**
     - 209 inferences/s, CPU 23 ops/s, GPU 16 fps
   * - CPU + GPU + memory
     - 1600
     - 33.4
     - **52 °C**
     - CPU 25 ops/s, GPU 17 fps
   * - CPU + GPU + memory
     - 1200
     - 29.6
     - 55 °C
     - CPU −19 %, memory −20 %, GPU unchanged
   * - CPU, all cores
     - 1600
     - 30.6
     - 54 °C
     - 52 ops/s
   * - CPU, all cores
     - 1200
     - 25.8
     - 59 °C
     - 40 ops/s (−22 %)
   * - Image classification on the NPU
     - 1600
     - 29.0
     - 56 °C
     - 289 inferences/s
   * - CPU at 50 %
     - 1600
     - 25.2
     - 60 °C
     - –
   * - GPU only
     - 1600
     - 25.1
     - 60 °C
     - 19 fps
   * - Touchscreen UI + 1080p30 video
     - 1600
     - 25.3
     - 60 °C
     - UI 33 fps, video 30 fps
   * - Touchscreen UI + 1080p30 video
     - 1200
     - 23.6
     - 61 °C
     - UI 30 fps, video 30 fps
   * - 1080p video decode, maximum rate
     - 1600
     - 20.3
     - 65 °C
     - 249 fps
   * - 1080p30 video playback
     - 1600
     - 18.7
     - 66 °C
     - 30 fps, no dropped frames
   * - Idle
     - 1600
     - 18–19
     - 66 °C
     - –

- **No heatsink is needed in open air**, even at full load: the hottest die
  reading in any test was 64 °C.
- **The NPU adds 7–10 °C of ΔT**, about as on the i.MX 95. With everything
  running, the NPU rate drops 28 % against the NPU alone.
- **Capping the CPU at 1200 MHz saves 4–5 °C** under CPU load and costs about
  20 % of CPU and memory throughput. For the UI it costs 8 % of the frame
  rate for under 2 °C.
- **Video costs almost nothing:** the VPU adds about 1 °C at 30 fps.
- **The UI is limited by the GPU, not temperature:** the touchscreen UI runs
  at 30–33 fps on the GC7000UL, against 49 fps on the i.MX 95.
- **The governor makes no difference:** ondemand and performance give the
  same temperature within 0.3 °C at the same cap and load.

Enclosure, no heatsink
~~~~~~~~~~~~~~~~~~~~~~

The same loads inside the sealed enclosure. ΔT is still measured against the
room air outside the enclosure. Each test ran about 40 minutes to settle.

.. list-table::
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 10 14 12 34

   * - Load
     - CPU cap MHz
     - ΔT °C (open air → enclosure)
     - Max ambient
     - Performance
   * - CPU + GPU + memory + NPU
     - 1600
     - 40.4 → 50.3
     - **35 °C**
     - 211 inferences/s, CPU 22 ops/s, GPU 15 fps
   * - CPU + GPU + memory + NPU
     - 1200
     - 45.5
     - **39 °C**
     - 207 inferences/s, CPU −20 %, GPU 14 fps
   * - CPU + GPU + memory
     - 1600
     - 33.4 → 42.7
     - **42 °C**
     - CPU 25 ops/s, GPU 17 fps
   * - CPU + GPU + memory
     - 1200
     - 29.6 → 38.4
     - 47 °C
     - CPU −20 %, GPU unchanged
   * - CPU, all cores
     - 1600
     - 30.6 → 37.1
     - 48 °C
     - 51 ops/s
   * - CPU, all cores
     - 1200
     - 25.8 → 31.4
     - 54 °C
     - 40 ops/s (−22 %)
   * - Image classification on the NPU
     - 1600
     - 29.0 → 37.1
     - 48 °C
     - 288 inferences/s
   * - Touchscreen UI + 1080p30 video
     - 1600
     - 25.3 → 33.7
     - 51 °C
     - UI 32 fps, video 30 fps
   * - GPU only
     - 1600
     - 25.1 → 33.2
     - 52 °C
     - 19 fps
   * - CPU at 50 %
     - 1600
     - 25.2 → 30.6
     - 54 °C
     - –
   * - 1080p30 video playback
     - 1600
     - 18.7 → 25.4
     - 60 °C
     - 30 fps
   * - Idle
     - 1600
     - 18–19 → 24.0
     - 61 °C
     - –

- **No test throttled.** The hottest die reading was 76 °C, with everything
  loaded at 1600 MHz: 9 °C under the design limit.
- **The enclosure costs 5–10 °C of ambient:** about 5 °C at idle and under
  light loads, 8–10 °C under heavy ones. The air inside the enclosure ran
  3–7 °C above the room.
- **Only the NPU worst case may need a heatsink.** CPU, GPU, memory and NPU
  all fully loaded allow 35 °C room air at 1600 MHz. Capping the CPU at
  1200 MHz raises that to 39 °C, at a cost of 20 % of CPU throughput; the NPU
  rate is unchanged. For warmer rooms this case needs a heatsink.

i.MX 93 (00363) results
-----------------------

Test setup
~~~~~~~~~~

.. list-table::
   :class: wrap-cells
   :widths: 25 75

   * - Hardware
     - 00363 i.MX 93 OSM-L SOM on the 00365 carrier board, no heatsink, in
       open air on a desk and in the same sealed Polycase WA-42*16 enclosure,
       mounted as the i.MX 8M Plus was. The display output was enabled with
       no panel connected.
   * - Software
     - Cargt Linux BSP (NXP lf-6.18.20)
   * - CPU frequency
     - The two Cortex-A55 cores run at a fixed 1.7 GHz; the i.MX 93 has no
       CPU frequency levels to cap or governor to choose. It has no 3D GPU or
       video decoder, so the touchscreen UI is drawn by the CPU and there are
       no GPU or video tests.
   * - Die temperature
     - The i.MX 93 CPU thermal sensor
   * - Ambient
     - A Dracal USB-PTH450 sensor in the room, 22–24 °C. In the enclosure, a
       second sensor measured the air inside it.

The loads are those used for the other SOMs, without the GPU. Every test ran
to a steady die temperature and none throttled. The open-air tests of CPU and
memory, all CPU cores and idle were repeated two or three times; repeats
agreed within 0.5 °C, and the tables give their mean. NPU tests on the
Ethos-U65 are planned.

.. list-table:: Open air and enclosure, no heatsink
   :class: wrap-cells
   :header-rows: 1
   :widths: 30 16 16 16 22

   * - Load
     - ΔT °C (open air → enclosure)
     - Max ambient, open air
     - Max ambient, enclosure
     - Performance (open air → enclosure)
   * - CPU + memory
     - 20.5 → 24.0
     - **64 °C**
     - **61 °C**
     - CPU 14 → 13 ops/s, memory 18,700 → 18,400 ops/s
   * - CPU, all cores
     - 19.4 → 22.5
     - 66 °C
     - 63 °C
     - 29 → 28 ops/s
   * - Touchscreen UI (drawn by the CPU)
     - 20.0 → 23.2
     - 65 °C
     - 62 °C
     - 13 → 12 fps
   * - CPU at 50 %
     - 16.5 → 19.7
     - 69 °C
     - 65 °C
     - –
   * - Idle
     - 12.8 → 16.1
     - 72 °C
     - 69 °C
     - –

- **No heatsink is needed** in open air or in the enclosure: the hottest die
  reading in any test was 48 °C, 37 °C under the design limit.
- **The enclosure costs about 3 °C of ambient.** The air inside it ran
  1.6 °C above the room at idle and 2.6 °C at full load.
- **The touchscreen UI loads the CPU almost fully**, because the i.MX 93 has
  no 3D GPU: it runs about as warm as the CPU stress test, at 12–13 fps.
- **Throttling works as on the other SOMs.** With the throttle point lowered
  to test it, the kernel held the die at the throttle point by idling the
  CPU, at a cost of 18–30 % of CPU throughput.

Choosing cooling for your product
---------------------------------

To estimate the cooling a product needs:

1. Find the row closest to your product's load and CPU frequency cap.
2. Take the maximum ambient for your environment and cooling.
3. Compare it with the warmest air your product will see. Allow for the
   inside of your enclosure being warmer than the room: 2–7 °C in the sealed
   enclosure tested here.

For example, an indoor i.MX 95 product in a sealed plastic enclosure, with
the CPU capped at 1404 MHz and the passive heatsink, allows 52 °C room air at
the worst-case stress load. That is a margin of about 20 °C over a 30 °C room.

These results come from one SOM of each type in one orientation on the
00365 carrier board. A different carrier, enclosure, mounting orientation or airflow
changes them. Treat them as a starting point and verify your final design.
For help choosing cooling for your product,
`contact Cargt <https://www.cargt.com/contact/>`__.

Test data
---------

:doc:`thermal-test-data` lists every test behind this page, with its
temperatures, clock frequencies, loads and performance, and has them as a
CSV file to download.

.. toctree::
    :hidden:

    thermal-test-data

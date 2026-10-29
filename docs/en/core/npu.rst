.. _npu:

Machine Learning on the i.MX 93 NPU
===================================

The i.MX 93 has an Arm Ethos-U65 neural processing unit (NPU) for running
quantized TensorFlow Lite models. Cargt images do not turn it on, because
on the i.MX 93 the NPU is driven through the Cortex-M33 core, and many
products use the M33 for their own firmware instead. This page shows how to
turn the NPU on yourself.

The examples on this page are from an i.MX 93 00363 SOM on an 00428 carrier
with the 5.5" display, running a wrynose image.

How It Works
------------

When an application opens ``/dev/ethosu0``, Linux starts the M33 through
remoteproc with the firmware in ``/lib/firmware/ethosu_firmware``. The M33
then runs the inferences that the ``ethosu`` kernel driver sends it over
RPMsg.

.. warning::

   While the NPU is turned on, the M33 belongs to Linux and cannot run your
   own firmware. Turn the NPU on only if your product does not need the M33
   for anything else.

The kernel driver (``CONFIG_ETHOSU``) and the M33 firmware are already in
Cargt images. To use the NPU you need:

1. A device tree that turns on the M33 remoteproc and the NPU.
2. The TensorFlow Lite packages and the Ethos-U delegate in your image.
3. A model compiled for the NPU with Vela.

The NPU needs a 256 MB memory region at 0xc0000000, so it needs a SOM with
2 GB of RAM.

Turning On the NPU in the Device Tree
-------------------------------------

Save this include file as ``imx93-cargt-00363-npu.dtsi``. It adds the NPU
memory region, turns on the M33 remoteproc with its mailboxes and RPMsg
buffers, and adds the ``ethosu`` device. The buffer regions it refers to are
already reserved in the 00363 SOM device tree.

.. code-block:: dts

   // SPDX-License-Identifier: (GPL-2.0+ OR MIT)
   /* Enable the Arm Ethos-U65 NPU on a Cargt i.MX 93 00363 SOM. */

   / {
   	reserved-memory {
   		ethosu_mem: ethosu_region@c0000000 {
   			compatible = "shared-dma-pool";
   			reusable;
   			reg = <0x0 0xc0000000 0x0 0x10000000>;
   		};
   	};

   	ethosu {
   		compatible = "arm,ethosu";
   		fsl,cm33-proc = <&cm33>;
   		memory-region = <&ethosu_mem>;
   		power-domains = <&mlmix>;
   	};
   };

   &cm33 {
   	mbox-names = "tx", "rx", "rxdb";
   	mboxes = <&mu1 0 1>,
   		 <&mu1 1 1>,
   		 <&mu1 3 1>;
   	memory-region = <&vdevbuffer>, <&vdev0vring0>, <&vdev0vring1>,
   			<&vdev1vring0>, <&vdev1vring1>, <&rsc_table>;
   	fsl,startup-delay-ms = <500>;
   	status = "okay";
   };

Then make a device tree for your board that includes your normal board
device tree followed by the NPU include file. For an 00428 carrier with the
5.5" display, save this as
``imx93-cargt-00363-00428-glt0557201280is1-npu.dts``:

.. code-block:: dts

   // SPDX-License-Identifier: (GPL-2.0+ OR MIT)
   /* 00363 + 00428 with the 5.5" display and the NPU turned on */

   #include "imx93-cargt-00363-00428-glt0557201280is1.dts"
   #include "imx93-cargt-00363-npu.dtsi"

Building the Device Tree in Your Layer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In your own layer (see :ref:`application-development`), put both files in
``recipes-kernel/linux/files/`` and add
``recipes-kernel/linux/linux-imx_%.bbappend``:

.. code-block:: text

   FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

   SRC_URI += " \
       file://imx93-cargt-00363-npu.dtsi \
       file://imx93-cargt-00363-00428-glt0557201280is1-npu.dts \
   "

   do_patch:append() {
       cp ${UNPACKDIR}/imx93-cargt-00363-npu.dtsi \
          ${UNPACKDIR}/imx93-cargt-00363-00428-glt0557201280is1-npu.dts \
          ${S}/arch/arm64/boot/dts/freescale/
       echo 'dtb-$(CONFIG_ARCH_MXC) += imx93-cargt-00363-00428-glt0557201280is1-npu.dtb' \
           >> ${S}/arch/arm64/boot/dts/freescale/Makefile
   }

   KERNEL_DEVICETREE:append = " freescale/imx93-cargt-00363-00428-glt0557201280is1-npu.dtb"

The kernel package then installs the new device tree in ``/boot`` with the
others.

Selecting the Device Tree
~~~~~~~~~~~~~~~~~~~~~~~~~

Point ``fdtfile`` at the new device tree and reboot:

.. code-block:: bash

   fw_setenv fdtfile boot/imx93-cargt-00363-00428-glt0557201280is1-npu.dtb
   reboot

``fdtfile`` is shared by both root file system slots. If you switch slots,
for example with a software update, make sure the other slot also has the
device tree, or set ``fdtfile`` back first.

After the reboot, ``/dev/ethosu0`` exists and the M33 shows up in remoteproc.
It stays ``offline`` until the first application opens the NPU:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# ls -l /dev/ethosu0
   crw------- 1 root root 510, 0 Oct 29 15:13 /dev/ethosu0
   root@imx93-cargt-00363-00428:~# cat /sys/class/remoteproc/remoteproc0/name /sys/class/remoteproc/remoteproc0/state
   imx-rproc
   offline
   root@imx93-cargt-00363-00428:~# dmesg | grep -iE "ethosu|remoteproc"
   [    0.000000] OF: reserved mem: initialized node ethosu_region@c0000000, compatible id shared-dma-pool
   [    0.000000] OF: reserved mem: 0x00000000c0000000..0x00000000cfffffff (262144 KiB) map reusable ethosu_region@c0000000
   [    1.509823] ethosu ethosu: assigned reserved memory node ethosu_region@c0000000
   [    3.867400] remoteproc remoteproc0: imx-rproc is available

Adding the Machine Learning Packages
------------------------------------

Add TensorFlow Lite, the Ethos-U delegate and the Ethos-U driver stack to
your image, for example in your image recipe or ``local.conf``:

.. code-block:: text

   IMAGE_INSTALL:append:mx93-nxp-bsp = " tensorflow-lite tensorflow-lite-ethosu-delegate ethos-u-driver-stack"

The layers that provide them are already part of the Cargt BSP. The
delegate also installs ``vela``, the model compiler, on the board.

Compiling a Model with Vela
---------------------------

The NPU runs only models compiled by Vela, and the model must be fully
quantized to 8-bit integers. Operations the NPU cannot run fall back to the
CPU. The ``vela`` on the board already targets the i.MX 93's NPU, so it
needs no extra options. This compiles the MobileNet example model that comes
with TensorFlow Lite:

.. code-block:: bash

   cd /usr/bin/tensorflow-lite-2.19.0/examples
   vela mobilenet_v1_1.0_224_quant.tflite --output-dir /tmp/npu

It takes a few seconds on the board. The start of Vela's summary shows how
many operators run on the NPU; here all of them do:

.. code-block:: text

   Network summary for mobilenet_v1_1.0_224_quant
   Accelerator configuration               Ethos_U65_256
   System configuration               Ethos_U65_High_End
   Memory mode                      Dedicated_Sram_384KB
   Accelerator clock                                1000 MHz
   Design peak SRAM bandwidth                      14.90 GB/s
   Design peak DRAM bandwidth                       3.49 GB/s

   Total SRAM used                                370.94 KiB
   Total DRAM used                               3590.67 KiB

   CPU operators = 0 (0.0%)
   NPU operators = 56 (100.0%)

Vela writes the compiled model and a summary file:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# ls -l /tmp/npu
   total 3172
   -rw-r--r-- 1 root root    1603 Oct 29 15:14 mobilenet_v1_1.0_224_quant_summary_Ethos_U65_High_End.csv
   -rw-r--r-- 1 root root 3241472 Oct 29 15:14 mobilenet_v1_1.0_224_quant_vela.tflite

Running a Model on the NPU
--------------------------

Pass the Ethos-U delegate to TensorFlow Lite to run the compiled model on
the NPU:

.. code-block:: bash

   cd /usr/bin/tensorflow-lite-2.19.0/examples
   ./label_image -m /tmp/npu/mobilenet_v1_1.0_224_quant_vela.tflite \
       -i grace_hopper.bmp -l labels.txt \
       --external_delegate_path=/usr/lib/libethosu_delegate.so

``Applied EXTERNAL delegate`` shows that the model runs on the NPU:

.. code-block:: text

   INFO: Loaded model /tmp/npu/mobilenet_v1_1.0_224_quant_vela.tflite
   INFO: resolved reporter
   INFO: Ethosu delegate: device_name set to /dev/ethosu0.
   INFO: Ethosu delegate: cache_file_path set to .
   INFO: Ethosu delegate: timeout set to 60000000000.
   INFO: Ethosu delegate: enable_cycle_counter set to 0.
   INFO: Ethosu delegate: enable_profiling set to 0.
   INFO: Ethosu delegate: profiling_buffer_size set to 2048.
   INFO: Ethosu delegate: pmu_event0 set to 0.
   INFO: Ethosu delegate: pmu_event1 set to 0.
   INFO: Ethosu delegate: pmu_event2 set to 0.
   INFO: Ethosu delegate: pmu_event3 set to 0.
   INFO: EXTERNAL delegate created.
   INFO: EthosuDelegate: 1 nodes delegated out of 1 nodes with 1 partitions.
   INFO: Ethosu delegate: zero-copy disabled, export ETHOSU_ENABLE_ZERO_COPY=1 to enable
   INFO: Applied EXTERNAL delegate.
   INFO: invoked
   INFO: average time: 3.8 ms
   INFO: 0.780392: 653 military uniform
   INFO: 0.105882: 907 Windsor tie
   INFO: 0.0156863: 458 bow tie
   INFO: 0.0117647: 466 bulletproof vest
   INFO: 0.00784314: 835 suit

The first run starts the M33, and ``remoteproc0`` then stays ``running``:

.. code-block:: text

   root@imx93-cargt-00363-00428:~# cat /sys/class/remoteproc/remoteproc0/state
   running
   root@imx93-cargt-00363-00428:~# dmesg | grep -iE "remoteproc|rpmsg"
   ...
   [   37.822462] remoteproc remoteproc0: Booting fw image ethosu_firmware, size 157176
   [   38.354603] virtio_rpmsg_bus virtio0: rpmsg host is online
   [   38.381583] virtio_rpmsg_bus virtio1: rpmsg host is online
   [   38.384357] virtio_rpmsg_bus virtio1: creating channel rpmsg-ethosu-channel addr 0x1e
   [   38.401802] remoteproc remoteproc0: remote processor imx-rproc is now up

To measure the speed, run ``benchmark_model`` with the same delegate. The
last line gives the average time per inference in microseconds:

.. code-block:: text

   root@imx93-cargt-00363-00428:/usr/bin/tensorflow-lite-2.19.0/examples# ./benchmark_model \
       --graph=/tmp/npu/mobilenet_v1_1.0_224_quant_vela.tflite \
       --external_delegate_path=/usr/lib/libethosu_delegate.so --num_runs=200
   ...
   INFO: Inference timings in us: Init: 33384, First inference: 3954, Warmup (avg): 3838.47, Inference (avg): 3921.67

To compare with the CPU, run the original model without the delegate, for
example ``--num_threads=2``. For MobileNet v1 (224x224, quantized):

.. list-table::
   :header-rows: 1
   :widths: 60 40

   * - Where it runs (``benchmark_model``)
     - Time per inference
   * - NPU (Ethos-U delegate)
     - 3.9 ms
   * - CPU, 1 thread
     - 61 ms
   * - CPU, 2 threads (both Cortex-A55 cores)
     - 33 ms

On the example image, ``label_image`` gives the same top five results on the
CPU and on the NPU, with ``653 military uniform`` first (0.76 on the CPU,
0.78 on the NPU).

Each run may log these messages. They are harmless: the driver tries to
load the firmware every time the NPU is opened, and the M33 is already
running.

.. code-block:: text

   imx-rproc remoteproc-cm33: can't change firmware while running
   ethosu ethosu: can't change firmware or remote processor is running

Turning the NPU Off Again
-------------------------

Point ``fdtfile`` back at your normal device tree and reboot:

.. code-block:: bash

   fw_setenv fdtfile boot/imx93-cargt-00363-00428-glt0557201280is1.dtb
   reboot

``/dev/ethosu0`` and the M33 remoteproc are then gone, and the M33 is free
for your own firmware again.

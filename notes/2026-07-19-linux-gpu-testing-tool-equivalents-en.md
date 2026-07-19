---
audio: false
generated: true
image: false
lang: en
layout: post
title: Linux GPU Testing Tool Equivalents
translated: false
type: note
---

Question: **What are Linux GPU testing tools like FurMark, GPU-Z, 3DMark, etc.? What are the Linux equivalents?**

Answer:

On Windows, people usually use:

* **GPU-Z** → hardware information / monitoring
* **FurMark** → extreme GPU stress test ("burn-in")
* **3DMark** → gaming benchmark
* **OCCT** → stability + power testing

Linux has equivalents, but the ecosystem is more fragmented.

## 1. GPU information tools (GPU-Z equivalent)

### `nvidia-smi` (NVIDIA)

For RTX 3090 / 4070 / A100 etc:

```bash
nvidia-smi
```

Example:

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 575.xx       Driver Version: 575.xx      CUDA Version: 12.x      |
| GPU  Name        Memory-Usage  Temp  Power |
| RTX 3090         10000MiB     70C   320W |
+-----------------------------------------------------------------------------+
```

Monitor continuously:

```bash
watch -n 1 nvidia-smi
```

More detailed:

```bash
nvidia-smi -q
```

Equivalent to GPU-Z:

* VRAM usage
* temperature
* power
* clocks
* PCIe link
* ECC errors (professional cards)

---

### `nvtop` (Linux GPU htop)

Install:

Ubuntu:

```bash
sudo apt install nvtop
```

Run:

```bash
nvtop
```

Looks like:

```
GPU  RTX 3090
Util: 99%
Mem: 23GB/24GB
Temp: 72C
Power: 350W
```

Supports:

* NVIDIA
* AMD
* Intel

Very useful for AI workloads.

---

## 2. FurMark equivalent (GPU stress test)

FurMark is basically:

> "maximize GPU shader load + heat output"

Linux options:

---

### GPU Burn (closest FurMark)

For NVIDIA:

[https://github.com/wilicc/gpu-burn](https://github.com/wilicc/gpu-burn)

Build:

```bash
git clone https://github.com/wilicc/gpu-burn
cd gpu-burn
make
```

Run:

```bash
./gpu_burn 600
```

Meaning:

600 seconds stress test.

Example:

```
GPU 0: RTX 3090
Time: 600 sec
Performance: 35000 Gflop/s
```

During test:

```bash
watch nvidia-smi
```

You check:

* temperature
* power stability
* crashes
* driver reset

For used RTX 3090 from Xianyu, this is one of the first tests I would run.

---

### `stress-ng`

CPU/GPU stress:

```bash
sudo apt install stress-ng

stress-ng --gpu 1 --timeout 10m
```

Less GPU-specific.

---

## 3. 3DMark equivalent

3DMark measures gaming performance:

* DirectX
* ray tracing
* rasterization
* FPS

Linux does not have official 3DMark.

Alternatives:

---

### Unigine Heaven

Classic Linux GPU benchmark.

Unigine Heaven Benchmark

Example:

```bash
./heaven
```

Measures:

* FPS
* GPU load
* stability

Good for comparing:

RTX 3090 vs RX 7900 XT.

---

### Unigine Superposition

More modern:

Unigine Superposition Benchmark

Tests:

* Vulkan
* OpenGL
* heavy scenes

---

### Phoronix Test Suite

Linux benchmark framework:

Phoronix Test Suite

Install:

```bash
sudo apt install phoronix-test-suite
```

Example:

```bash
phoronix-test-suite benchmark unigine-superposition
```

It can benchmark:

* GPU
* CPU
* memory
* storage

---

## 4. AI workload GPU test (probably more relevant for you)

Since your use case is LLM training/inference, gaming benchmarks are less meaningful.

I would test:

### CUDA bandwidth

```bash
nvidia-smi --query-gpu=memory.total,memory.free --format=csv
```

---

### PyTorch CUDA test

```python
import torch

print(torch.cuda.get_device_name())

x=torch.randn(
    (10000,10000),
    device="cuda"
)

for i in range(100):
    y=x@x

print("OK")
```

This stresses:

* CUDA cores
* VRAM
* memory controller

---

### LLM inference test

Example:

```bash
python -m vllm.entrypoints.openai.api_server \
 --model Qwen/Qwen3-30B \
 --tensor-parallel-size 2
```

Then measure:

* tokens/sec
* VRAM usage
* stability

For your 2×3090 idea, this is much more meaningful than FurMark.

---

## Used GPU checking workflow (RTX 3090 / 7900 XT)

If buying second-hand:

### Step 1: Check identity

NVIDIA:

```bash
nvidia-smi
```

AMD:

```bash
rocminfo
```

---

### Step 2: Stress

```bash
./gpu_burn 600
```

Watch:

```bash
nvtop
```

Look for:

* temperature < 85°C
* no driver crash
* stable power

---

### Step 3: VRAM test

NVIDIA:

```bash
gpu-burn
```

or:

```bash
memtest_vulkan
```

VRAM problems are common on used mining GPUs.

---

### Step 4: Real AI workload

Run:

```bash
llama.cpp
```

or:

```bash
vllm
```

Load a large model until VRAM is nearly full.

---

For your case (buying used RTX 3090 / RX 7900 XT for AI), my priority would be:

1. `nvidia-smi` / `nvtop` → identify card
2. `gpu-burn 10min` → thermal + power
3. VRAM stress test → memory health
4. LLM inference → practical AI stability

FurMark/3DMark are more for gamers; AI users care more about **VRAM correctness + CUDA/ROCm stability under long tensor workloads**.

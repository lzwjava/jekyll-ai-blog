---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD ROCm FLUX.1-schnell Optimization
translated: false
type: note
---

Question: How to optimize this stable-diffusion.cpp FLUX.1-schnell GGUF workflow on AMD GPUs with ROCm?

Answer:

Your current setup is optimized for **RTX 4070 CUDA**:

```
sd-cli
 ├── diffusion=cuda
 ├── vae=cuda
 ├── clip=cpu
 └── t5xxl=cpu
```

For AMD ROCm, the optimization path is different. The key is:

1. Build `stable-diffusion.cpp` with HIP/ROCm backend.
2. Move more components to GPU if VRAM allows.
3. Tune memory offloading.
4. Use ROCm-specific kernels/build flags.

---

## 1. Build stable-diffusion.cpp with ROCm/HIP

`stable-diffusion.cpp` uses the same ggml backend style as llama.cpp.

Clone:

```bash
git clone https://github.com/leejet/stable-diffusion.cpp
cd stable-diffusion.cpp
```

Build with HIP:

```bash
cmake -B build \
  -DSD_USE_HIPBLAS=ON \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build -j$(nproc)
```

Check:

```bash
./build/bin/sd-cli --help
```

You should see HIP backend support.

Verify:

```bash
rocminfo | grep gfx
```

Example:

```
gfx1100   # RDNA3
gfx1030   # RDNA2
gfx90a    # MI250/MI300
```

---

## 2. Change backend from CUDA to HIP

Your current:

```python
self._backend = "diffusion=cuda,clip=cpu,vae=cuda,t5xxl=cpu"
```

Change:

```python
self._backend = "diffusion=hip,clip=cpu,vae=hip,t5xxl=cpu"
```

Example:

```bash
--backend diffusion=hip,clip=cpu,vae=hip,t5xxl=cpu
```

---

## 3. VRAM placement strategy

FLUX is heavy.

Your model:

```
flux1-schnell-Q4_0.gguf
~8-9GB
```

Other files:

```
vae.safetensors
~300MB

clip_l
~235MB

t5xxl_fp16
~9.8GB
```

Total FP16:

```
diffusion     8GB
T5XXL         10GB
VAE           0.3GB
CLIP          0.2GB

≈18-20GB VRAM
```

So your current:

```
diffusion GPU
vae GPU
clip CPU
t5 CPU
```

is reasonable for 12GB.

---

### AMD 16GB GPU

Example:

RX 7900 XT:

```
24GB
```

or MI50:

```
16GB
```

You can try:

```bash
--backend diffusion=hip,vae=hip,clip=hip,t5xxl=cpu
```

Better:

```
GPU:
 diffusion
 VAE
 CLIP

CPU:
 T5XXL
```

---

### AMD 24GB+

Example MI300X:

```
192GB HBM
```

Move everything:

```bash
--backend diffusion=hip,vae=hip,clip=hip,t5xxl=hip
```

The speed difference is huge.

---

## 4. Enable ROCm environment tuning

Before running:

```bash
export HSA_OVERRIDE_GFX_VERSION=<your gfx>
export PYTORCH_ROCM_ARCH=<your gfx>
```

Example:

RX 7900:

```bash
export HSA_OVERRIDE_GFX_VERSION=11.0.0
```

MI300:

```bash
export HSA_OVERRIDE_GFX_VERSION=9.4.2
```

---

## 5. Use rocBLAS tuning

ROCm has kernel selection overhead.

Run:

```bash
rocblaslt-bench
```

or enable:

```bash
export ROCBLAS_LAYER=4
```

For production:

```bash
export ROCBLAS_TENSILE_LIBPATH=/opt/rocm/lib/rocblas/library
```

---

## 6. Compile with aggressive optimization

For RDNA3:

```bash
cmake -B build \
  -DSD_USE_HIPBLAS=ON \
  -DCMAKE_BUILD_TYPE=Release \
  -DAMDGPU_TARGETS=gfx1100
```

For MI300:

```bash
cmake -B build \
  -DSD_USE_HIPBLAS=ON \
  -DAMDGPU_TARGETS=gfx942
```

---

## 7. Use Vulkan backend as alternative

For AMD consumer GPUs, Vulkan can sometimes beat ROCm.

Build:

```bash
cmake -B build \
  -DSD_USE_VULKAN=ON
```

Run:

```bash
--backend diffusion=vulkan
```

Advantages:

```
ROCm:
+ better compute
+ tensor kernels
- driver complexity

Vulkan:
+ works everywhere
+ no ROCm install
- sometimes slower
```

For RX 6000/7000 cards I would benchmark both.

---

## 8. Your Python code change

Make backend configurable:

```python
if self._backend is None:
    if os.environ.get("AMD_GPU"):
        self._backend = (
            "diffusion=hip,"
            "clip=cpu,"
            "vae=hip,"
            "t5xxl=cpu"
        )
    else:
        self._backend = (
            "diffusion=cuda,"
            "clip=cpu,"
            "vae=cuda,"
            "t5xxl=cpu"
        )
```

Then:

AMD:

```bash
AMD_GPU=1 python app.py
```

NVIDIA:

```bash
python app.py
```

---

## 9. Biggest performance wins

For FLUX.1-schnell:

| Optimization               |     Speed impact |
| -------------------------- | ---------------: |
| GPU VAE                    |           10-20% |
| GPU CLIP                   |            5-10% |
| GPU T5XXL                  |             2-3x |
| Q8/Q6 diffusion instead Q4 | quality + slower |
| Vulkan vs HIP benchmark    |             ±20% |
| Persistent process         |           20-30% |

Your current architecture:

```
spawn sd-cli
load GGUF
generate
exit
```

has a hidden cost.

A persistent server would be faster:

```
Python
 |
 v
sd-cpp daemon
 |
 GPU resident model
```

similar to vLLM.

For many images:

```
current:
10 images
10 model loads

optimized:
10 images
1 model load
```

could easily save minutes.

---

For your hardware direction:

* RTX 4070 12GB → keep CUDA.
* RX 7900 XTX 24GB → ROCm is interesting.
* MI300X → full GPU FLUX pipeline, massive speed.
* MI50 16GB → possible but ROCm support is old and not ideal.

For AMD image generation today, I would benchmark:

```
stable-diffusion.cpp HIP
        vs
stable-diffusion.cpp Vulkan
        vs
ComfyUI ROCm
```

because FLUX performance depends heavily on backend kernels.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: ROCm gfx900 PyTorch needs Docker
translated: false
type: note
---

## Done — ROCm userspace installed and verified

Here's the final state:

### Installed & working

| Component | Package | Verified |
|-----------|---------|----------|
| GPU enumeration | `rocminfo` | ✅ `gfx900`, `AMD Radeon Pro WX 9100`, 64 CUs, 16 GB |
| Monitoring | `rocm-smi` | ✅ Device `0x6861`, GFX `gfx900` |
| Kernel thunk | `libhsakmt1` | ✅ |
| HSA runtime | `libhsa-runtime64-1` | ✅ (ROCk module loaded) |
| HIP runtime + compiler | `libamdhip64-7`, `hipcc` (clang-21) | ✅ compiled & **ran a real vec-add kernel on GPU** |
| OpenCL | `rocm-opencl-icd` | ✅ `clinfo`: gfx900, OpenCL 2.0, 64 CUs |

I also added your user to the `render` and `video` groups (ACLs already allowed access; re-login to make the group membership effective).

### Confirmed limitation (proven, not assumed)
ROCm **7.1's rocBLAS has no gfx900 kernels**, so any rocBLAS-based workload fails:

```
Device ID 0 : AMD Radeon Pro WX 9100 gfx900:xnack-
rocBLAS error: Cannot read .../TensileLibrary.dat ... for GPU arch : gfx900
```

This means **PyTorch from the Ubuntu repo (`python3-torch-rocm`) will not work on this GPU.** Custom HIP kernels and OpenCL do work.

### For actually training nanoGPT on this card
gfx900 needs a **ROCm 5.7** stack (the last release with full Vega 10 support). The clean way is a container, since the host kernel driver + `/dev/kfd` are all it needs:

```bash
docker run -it --device=/dev/kfd --device=/dev/dri \
  --group-add video --group-add render \
  rocm/pytorch:rocm5.7_ubuntu22.04_py3.10_pytorch_2.0.1
```

Your system has **neither docker nor podman**, and the system Python is **3.14** (too new for the ROCm 5.7 PyTorch wheels), so the container route is the practical one.

---

**Next step — shall I:**
1. **Install docker (or podman) and pull the `rocm/pytorch` ROCm 5.7 image**, then verify `torch.cuda` sees the GPU and run a quick nanoGPT smoke test? *(recommended)*
2. Leave it as-is — you'll handle the PyTorch setup yourself?
3. Also **remove** the `librocblas5`/`librocblas5-bench` packages I installed purely for the verification test? (They're harmless but unused.)

Which do you want?
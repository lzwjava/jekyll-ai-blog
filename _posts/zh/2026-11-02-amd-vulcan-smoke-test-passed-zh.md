---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Vulcan 冒烟测试通过
translated: true
type: note
---

烟雾测试通过。以下是总结：

## 结果

生成的图像：`smoke-out/fox_512_vulkan1.png` (512×512, 20步)，在 **AMD Radeon Pro WX 9100** 上通过 Vulkan 生成。

## 操作步骤

1. **找到构建文件** — `build/bin/sd-cli` 已经使用 `SD_VULKAN=ON` 构建完成。
2. **检测 GPU** — `--list-devices`：
   - `Vulkan0` Intel HD Graphics 530 (iGPU)
   - `Vulkan1` AMD Radeon Pro WX 9100（独立 GPU，16 GB）
   - `CPU` Intel i5-6500
3. **修复模型** — `models/sd15-q4_0.gguf` 是一个不完整的下载文件（缺失 48 MB，导致 `tensor ... extends beyond its model file`）。已从 `second-state/stable-diffusion-v1-5-GGUF` 恢复完整文件，大小为 1,566,768,416 字节。
4. **运行烟雾测试** — 在全部三个后端上进行了测试。

## 有效的 GPU 命令

```bash
GGML_VK_DISABLE_FUSION=1 ./build/bin/sd-cli \
  -m models/sd15-q4_0.gguf \
  -p "a red fox in a snowy forest, highly detailed, cinematic lighting" \
  -n "blurry, low quality" \
  -W 512 -H 512 --steps 20 --seed 42 --cfg-scale 7.0 \
  --backend "diffusion=vulkan1,vae=vulkan1,te=vulkan1" \
  -o smoke-out/fox_512_vulkan1.png
```

**性能：** 11.51 秒采样时间 + 1.13 秒 VAE 解码时间 = **12.98 秒**（20步，512×512）。

## 重要发现

当 ggml Vulkan **融合功能**（默认开启）启用时，AMD GPU **会因 Vulkan device-lost 错误而崩溃**（`vk::Queue::submit: ErrorDeviceLost`）。设置 `GGML_VK_DISABLE_FUSION=1` 可使其稳定。这是 RADV/Vega10 的驱动程序问题，而非项目缺陷。

已验证的其他后端：
- `Vulkan0`（Intel iGPU）：无需环境变量即可正常工作，但速度较慢（约 4.2 秒/步，AMD 约 0.6 秒/步）。
- `CPU`：正常工作，256×256 下约 3.9 秒/步。

输出文件位于 `smoke-out/` 目录：`fox_512_vulkan1.png`、`smoke_vulkan1.png`、`smoke_vulkan0.png`、`smoke_cpu.png`。源代码文件未作任何修改。
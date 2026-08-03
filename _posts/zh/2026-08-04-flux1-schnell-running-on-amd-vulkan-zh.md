---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX.1-schnell在AMD Vulkan上运行
translated: true
type: note
---

全部验证通过。以下是完整总结：

## ✅ 完成 — FLUX.1-schnell 已通过 stable-diffusion.cpp (Vulkan) 在 AMD 机器上运行

### 配置详情

| 组件 | 详细说明 |
| --- | --- |
| **项目** | `/root/amd-hackathon-lzwjava/` — 可编辑 pip 安装至 `/opt/venv`，`fluxreel` CLI 可用 |
| **sd.cpp** | 使用 **Vulkan 后端** 构建了 `sd-cli` + `sd-server`（该网络环境下 GitHub 被屏蔽，从 PyPI 的 `stable-diffusion-cpp-python` 0.4.7 sdist 获取了内置源码） |
| **模型（17.2GB）** | `flux1-schnell-Q4_0.gguf`（6.8GB，unsloth）、`t5xxl_fp16.safetensors`（9.8GB）、`clip_l.safetensors`、`ae.safetensors` — 通过 **hf-mirror.com** 并使用你的 HF token 下载（连接断开后需恢复一次） |
| **配置** | `~/.config/fluxreel/.env` → `SDCPP_BIN`、`SDCPP_MODEL_DIR=/root/models`、`SDCPP_BACKEND=`（省略 `--backend`；新版 sd.cpp 已编译后端），960×720，4 步 |
| **额外工具** | 已安装 `ffmpeg` 用于视频生成管线 |

### 代码修复（已提交为 `fd713aa`）

1. **`cli.py`** — `main()` 中从未调用 `load_env()`，导致 `.env` 配置被忽略。已修复连接。
2. **`sd_cpp_provider.py`** — 硬编码了 `--backend "diffusion=cuda,..."`，新版 sd.cpp 不支持。添加了 `SDCPP_BACKEND` 环境变量覆盖（空值 → 省略标志 → 自动使用 Vulkan；未设置 → 保留原 CUDA 默认值以兼容原始配置）。

### 验证 — 运行成功 🎉

- **直接使用 sd-cli**：512×512 猫图，4 步 → **5.6 秒**（AMD Radeon，RADV NAVI31，Vulkan 1.4，51.5GB VRAM）
- **`fluxreel img`**：`"a cyberpunk city at night, neon reflections, rain"` → 960×720 PNG 耗时 **28.5 秒**（含 16 秒模型加载），保存至 `/root/fluxreel_test.png`
- **从 Mac 执行 `fluxreel -p 31329 info`**：显示 ROCm GPU、PyTorch 2.9.1 + HIP 7.2、2.9TB 可用磁盘、128 核心

### 注意事项

- 该机器上无法直接访问 GitHub；hf-mirror.com 表现良好（连接稳定时约 3 分钟下载 10GB）。
- 管理命令（`info`/`download`/`tunnel`）需 **从 Mac 端** 通过端口 **31329** 执行（`fluxreel -p 31329 ...`）；在机器本地上，`fluxreel img` 为本地生成路径。
- `gen-video --provider sdcpp` 将使用本地 Vulkan FLUX 生成场景图像；LLM 故事板步骤默认使用 OpenRouter（需配置你的 API key）。

远程执行示例命令：

```bash
/opt/venv/bin/fluxreel img "a dragon on a castle tower" --width 1024 --height 1024 --output /root/dragon.png
```

---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 10个成功落地的项目
translated: true
type: note
---

全部 10 个项目已克隆、编译并构建成功。🎉

## 构建报告 (`~/projects`)

| # | 项目 | 说明 | 构建 | 产物 | 验证 |
| --- | ------ | ------ | ------ | ------ | ------ |
| 1 | **fmt** | C++ 格式化库 | ✅ 9秒 | `libfmt.a` | 小程序运行 → `fmt works: 42` |
| 2 | **spdlog** | 快速 C++ 日志库 | ✅ 10秒 | `libspdlog.a` | 库文件存在 |
| 3 | **nlohmann/json** | C++ JSON 库 | ✅ 2秒 | `single_include/` | 头文件就绪 |
| 4 | **yaml-cpp** | YAML 解析器 | ✅ 11秒 | `libyaml-cpp.a` | 库文件存在 |
| 5 | **libjpeg-turbo** | SIMD JPEG 编解码器 | ✅ 46秒 | `libjpeg.so.62.4.0` | `cjpeg` v3.2.1 |
| 6 | **zstd** | Zstandard 压缩 | ✅ 28秒 | `zstd` (1.1M) | v1.6.0 |
| 7 | **redis** | 内存数据存储 | ✅ 132秒 | `redis-server`/`redis-cli` | 服务器报告版本号 |
| 8 | **libgit2** | Git 库 | ✅ 34秒 | `libgit2.so.2.0.0` | 库文件存在 |
| 9 | **whisper.cpp** | 语音转文本 (GGML) | ✅ 82秒 | `whisper-cli`, `whisper-server` | 二进制文件已构建 |
| 10 | **stable-diffusion.cpp** | 图像生成 (GGML) | ✅ ~300秒 | `sd-cli` (43M), `sd-server` (45M) | `sd-cli` 报告版本号 |

**总磁盘占用：** ~1.75 GB · 全部使用 `-j4` 在此设备上构建。

### 备注

- **9/10 一次性构建成功。** `stable-diffusion.cpp` 首次失败是因为浅克隆跳过了其 **ggml 子模块** — 通过 `git submodule update --init --recursive` 修复，然后重新构建。
- 所有构建均为 **仅 CPU 版本**。`whisper.cpp` 和 `stable-diffusion.cpp` 均支持我们用于 llama.cpp 的相同 ROCm/HIP 路径（`-DGGML_HIP=ON -DGGML_CUDA_FORCE_MMQ=ON -DAMDGPU_TARGETS=gfx900`），如需 GPU 加速可启用。
- 工具链：gcc 15 / make / cmake 4.4.4 (uv)。此设备未安装 autotools/Rust/Go，因此我选择了基于 CMake/Make 的项目。如需，可 `apt install` 这些工具链并添加 Rust/Go 经典项目（ripgrep、fzf、tmux）。

是否需要我 **用 HIP/gfx900 重新构建 whisper.cpp + stable-diffusion.cpp**，或添加另一批项目（例如 OpenCV、DuckDB、ffmpeg、Lua、sqlite）？

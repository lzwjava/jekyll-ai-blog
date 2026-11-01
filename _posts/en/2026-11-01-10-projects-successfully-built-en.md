---
audio: false
generated: true
image: false
lang: en
layout: post
title: 10 Projects Successfully Built
translated: false
type: note
---

All 10 projects cloned, compiled, and built successfully. 🎉

## Build Report (`~/projects`)

| # | Project | What it is | Build | Artifact | Verify |
| --- | --------- | ----------- | ------- | ---------- | -------- |
| 1 | **fmt** | C++ format library | ✅ 9s | `libfmt.a` | tiny program ran → `fmt works: 42` |
| 2 | **spdlog** | fast C++ logging | ✅ 10s | `libspdlog.a` | lib present |
| 3 | **nlohmann/json** | JSON for C++ | ✅ 2s | `single_include/` | header ready |
| 4 | **yaml-cpp** | YAML parser | ✅ 11s | `libyaml-cpp.a` | lib present |
| 5 | **libjpeg-turbo** | SIMD JPEG codec | ✅ 46s | `libjpeg.so.62.4.0` | `cjpeg` v3.2.1 |
| 6 | **zstd** | Zstandard compression | ✅ 28s | `zstd` (1.1M) | v1.6.0 |
| 7 | **redis** | in-memory data store | ✅ 132s | `redis-server`/`redis-cli` | server reports version |
| 8 | **libgit2** | git library | ✅ 34s | `libgit2.so.2.0.0` | lib present |
| 9 | **whisper.cpp** | speech-to-text (GGML) | ✅ 82s | `whisper-cli`, `whisper-server` | binaries built |
| 10 | **stable-diffusion.cpp** | image gen (GGML) | ✅ ~300s | `sd-cli` (43M), `sd-server` (45M) | `sd-cli` reports version |

**Total disk:** ~1.75 GB · all built with `-j4` on this box.

### Notes

- **9/10 built on first try.** `stable-diffusion.cpp` initially failed because the shallow clone skipped its **ggml submodule** — fixed with `git submodule update --init --recursive`, then rebuilt.
- All builds are **CPU-only**. `whisper.cpp` and `stable-diffusion.cpp` both support the same ROCm/HIP path we used for llama.cpp (`-DGGML_HIP=ON -DGGML_CUDA_FORCE_MMQ=ON -DAMDGPU_TARGETS=gfx900`) if you want GPU offload.
- Toolchain: gcc 15 / make / cmake 4.4.4 (uv). No autotools/Rust/Go on the box, which is why I picked CMake/Make-based projects. If you want, I can `apt install` those toolchains and add Rust/Go classics (ripgrep, fzf, tmux).

Want me to **rebuild whisper.cpp + stable-diffusion.cpp with HIP/gfx900**, or add another batch (e.g. OpenCV, DuckDB, ffmpeg, Lua, sqlite)?

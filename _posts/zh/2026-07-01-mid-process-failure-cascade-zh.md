---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 过程中途失效级联
translated: true
type: note
---

处理过程中出现了几个问题：

1. sglang 0.4.x 硬性锁定 torch==2.7.1  
   我们原计划使用 torch 2.5.1+cu124 + triton 3.1.0。但 sglang 0.4.10 的 `[srt]` 额外依赖中精确锁定了 `torch==2.7.1`。编译好的内核（sgl-kernel 0.2.8，flashinfer 0.2.9rc2）是基于 2.7.1 构建的。因此，在 sglang 0.4.x 下无法使用 torch 2.5.1。

2. cu124 的 wheel 包在 torch 2.6.0 之后停止发布  
   PyTorch 在 2.6.0 之后不再发布 cu124 的 wheel 包。torch 2.7.1 仅提供 cu126/cu128/cu130 版本。我们不得不从最初的“cu124”方案转向 cu126。

3. sglang 的依赖解析器与我们的 torch 锁定冲突  
   当我们运行 `pip install sglang[all]` 时，pip 的解析器检测到 sglang 依赖中的 `torch==2.7.1`，并试图安装它，这会覆盖我们精心锁定的 cu124 torch。我们不得不先使用 `--no-deps`，然后单独安装依赖。

4. pip 下载 torch 时超时（两次）  
   torch+cu124 和 torch+cu126 的 wheel 包约 800MB。SSH 连接在 300 秒后超时。我们不得不改用 `nohup` 后台安装。

5. 工作站在非交互式 SSH 下无法访问 HuggingFace  
   代理（127.0.0.1:7890）已通过 `start_proxy` 配置在 `.bashrc` 中，但在非交互式 SSH 中不会激活。我们必须显式导出 HTTP_PROXY/HTTPS_PROXY，然后编写了一个启动脚本。

6. ninja 不在 PATH 中  
   sglang 会生成 `ninja` 子进程用于 JIT 编译。pip 安装的 ninja 包位于 venv bin 目录，但 sglang 的子进程找不到它。我们必须将 venv bin 添加到 PATH。

7. 僵尸进程导致 OOM  
   首次成功启动时因端口绑定（30000 已被占用）而崩溃。第二次启动时发生 OOM，因为第一个 sglang 进程仍持有 8.65 GB 的 GPU 内存。我们不得不 `pkill -9` 终止所有进程，并等待 GPU 释放。

最大的概念性障碍：原方案（torch 2.5.1+cu124+triton 3.1.0）与 sglang 0.4.x 精确锁定的 torch 不兼容。最终发现 torch 2.7.1+cu126 + triton 3.3.1 才是实际可行的组合——triton 版本（3.3.1）比计划的新，但仍足够旧以避免 3.5/3.6 的段错误。

---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 调试 Mini-SGLang 多进程
translated: true
type: note
---

现在我理解了该项目。以下是调试 Mini-SGLang 的方法：

## 关键事实：该项目是多进程的

`launch_server()` (`python/minisgl/server/launch.py`) 通过 `multiprocessing` 使用 `spawn` 方式生成**独立的 OS 进程**：

| 进程 | 执行内容 |
| --- | --- |
| 主进程 | FastAPI/uvicorn API 服务器 (`api_server.py`) |
| 每个 TP rank 一个 | 调度器 (`_run_scheduler` → `scheduler/scheduler.py`) |
| N+1 | 分词器/逆分词器工作进程 (`tokenize_worker`) |

它们通过 ZMQ 通信。这一点很重要，因为**主进程中的断点不会命中在子进程中运行的代码**，而且 `spawn` 方式意味着子进程会从头重新导入所有内容。

另请注意：调试器必须使用与 `run_python.sh` **相同的解释器** (`/usr/bin/python3.12 -s`)，因为用户 site-packages 中的 torch 2.11.0 会破坏 `sgl_kernel`。`debugpy` **尚未安装**——除了纯 `pdb` 之外，你需要它来进行调试。

---

## 选项 1 — 最简单：调试离线的 `LLM` API（单进程）

`python/minisgl/llm/llm.py` 公开了一个 `Scheduler` 子类，该子类在**单进程**中运行所有内容——没有多进程，没有 ZMQ，没有服务器。这是逐步调试调度/预填充/解码逻辑的最佳方式：

```python
# /tmp/debug_llm.py
import sys; sys.path.insert(0, "/mnt/data/mini-sglang/python")
from minisgl.llm import LLM

llm = LLM("/path/to/model", dtype=torch.bfloat16)  # 在 Scheduler.__init__ 中设置断点
out = llm.generate("Hello, my name is")             # 在 scheduler.py / prefill.py 中设置断点
print(out)
```

使用 pdb 或 VS Code 调试器运行：

```bash
/usr/bin/python3.12 -s /tmp/debug_llm.py          # 直接运行
/usr/bin/python3.12 -s -m pdb /tmp/debug_llm.py   # pdb 命令行
```

或者直接在 `scheduler.py` 等文件中插入 `breakpoint()`（等同于 `pdb.set_trace()`）。注意：调度器在 `torch.inference_mode()` 内运行，这对 pdb 来说没问题。

## 选项 2 — 调试服务器（主进程 + 生成的子进程）

调试生成的子进程唯一可靠的方法是使用 `debugpy` 进行**远程附加**（安装在系统 python 中，这样它就能免受 `-s` 标志的影响）：

```bash
/usr/bin/python3.12 -s -m pip install debugpy
```

然后在 `launch.py` 中的子进程目标函数（例如在 `_run_scheduler` 中）顶部添加如下代码：

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))   # 每个生成的进程监听同一端口；VS Code 会显示一个选择器
debugpy.wait_for_client()
```

正常启动服务器，然后在 VS Code 中使用 "Python Debugger: Attach" 配置——VS Code 会询问你要附加到哪个进程（主 uvicorn 进程、`minisgl-TP0-scheduler`、分词器）。附加到你设置了断点的那个进程。

**断点放置建议：**

- HTTP 层 → `server/api_server.py`（主进程）
- 调度循环 → `scheduler/scheduler.py` (`run_forever`)、`prefill.py`、`decode.py`（子进程）
- 分词 → `tokenizer/`（子进程）

## 选项 3 — VS Code launch.json

```jsonc
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "附加到 minisgl 进程",
      "type": "debugpy",
      "request": "attach",
      "connect": { "host": "127.0.0.1", "port": 5678 },
      "processId": "${command:pickProcess}" // 允许选择调度器/分词器进程
    },
    {
      "name": "运行离线 LLM（单进程）",
      "type": "debugpy",
      "request": "launch",
      "program": "/tmp/debug_llm.py",
      "python": "/usr/bin/python3.12",
      "args": ["-s"] // 复制 run_python.sh 的 -s 参数（禁用用户 site-packages）
    }
  ]
}
```

## 选项 4 — PyCharm（该项目有 `.idea/` 目录）

- 打开项目，将解释器设置为 `/usr/bin/python3.12`（系统解释器——避免损坏的用户站点 torch 2.11.0）。
- PyCharm 自动支持使用 `spawn` 方式的 `multiprocessing`：当你从运行配置启动 `python -m minisgl` 时，子进程会自动连接到同一个调试器（无需 `debugpy` 代码）。运行配置：模块 `minisgl`，添加来自 `--help` 的 CLI 参数（例如 `--model-path ... --tp-size 1`），并设置 `PYTHONUNBUFFERED=1`。

---

## 注意事项

1. **CUDA 内核**（`sgl_kernel`、`flashinfer`、JIT 编译的注意力内核）无法单步调试——断点仅适用于 Python 代码。
2. 调试时使用 `--tp-size 1`；多 GPU 会增加 N 个需要处理的调度器进程。
3. `mp.set_start_method("spawn", force=True)` —— 子进程会重新导入模块，因此请将 debugpy 监听代码放在子进程的*目标函数*中，而不是模块顶层。
4. `run_api_server` 直接运行 `uvicorn.run(...)`，因此如果你附加到主进程，`api_server.py` 中的断点将会命中。

需要我为你设置 `.vscode/launch.json` 或向 `launch.py` 添加一个 debugpy 钩子吗？

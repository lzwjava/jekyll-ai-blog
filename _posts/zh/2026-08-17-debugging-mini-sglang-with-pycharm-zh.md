---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 PyCharm 调试 Mini-SGLang
translated: true
type: note
---

下面是根据你仓库中的验证结果给出的完整解释。

## 为什么解释器很重要（`run_python.sh` 的故事）

你的 `run_python.sh` 的存在是有原因的：

```bash
exec /usr/bin/python3.12 -s "$@"
```

`-s` 标志**禁用了用户 site-packages**（`~/.local/lib/python3.12/site-packages`），其中包含 torch 2.11.0。该版本会导致 `sgl_kernel` 出现 `undefined symbol: c10_cuda_check_implementation` 错误。而*系统* site-packages（`/usr/lib/python3/dist-packages`）中安装了可正常工作的 torch 2.9.1 + sgl_kernel 0.3.21 + flashinfer 0.6.16。

好消息是：**你的 `.idea/minisgl.iml` 已经指向了 `/usr/bin/python3.12`**（`<orderEntry type="jdk" jdkName="/usr/bin/python3.12" .../>`），所以 PyCharm 的解释器已经是正确的。如果你切换了解释器，就会出问题。在 PyCharm 中验证：*设置 → 项目: mini-sglang → Python 解释器* → 应该显示 `/usr/bin/python3.12`，并且包列表应该显示 **torch 2.9.x，而不是 2.11.0**。

**一个细节：** PyCharm 默认不会传递 `-s`，但你可以在运行配置的 *解释器选项* 字段中复制该行为（见下文）。如果没有这个选项，PyCharm 可能会导入用户-site 的 torch 2.11.0，并抛出同样的 `undefined symbol` 错误导致崩溃。检查 *运行 → 编辑配置 → 解释器选项* — 需要添加 `-s`。

## PyCharm 的多进程调试如何工作（你询问的神奇机制）

PyCharm 的调试器（`pydevd`）不需要在你的项目中添加任何 `debugpy.listen()` 代码。其机制如下：

1. 当你按下 **调试** 按钮时，PyCharm 会启动主进程，并附带修改过的 `PYTHONPATH`/环境变量以及 `sitecustomize` 钩子，这些钩子会自动启动连接到 IDE 的 `pydevd`。同时还会设置 `PYCHARM_HOSTED=1` 和 `PYDEVD_*` 等环境变量。
2. **关键技巧：** 这些环境变量存在于被调试进程的 `os.environ` 中。
3. 当 `launch.py` 调用 `mp.Process(target=..., ...)`（针对调度器、分词器和反分词器）时，`multiprocessing` 模块会将**父进程的环境变量继承**到每个子进程。使用 `spawn` 方式时，子进程会重新导入 `__main__` / 目标模块，而该导入会触发 `sitecustomize` → 检测到 `PYCHARM_HOSTED` → 自动附加第二个 `pydevd` 连接到 IDE，并在调试工具窗口中注册为一个新的"Python 进程"。
4. 你的断点会**自动传播**：在 `scheduler/scheduler.py` 中设置一个断点，每个导入该文件的进程（主进程 + 每个 TP 调度子进程）都会获得该断点。当子进程触发断点时，整个进程树会**一同暂停**（PyCharm 默认的"挂起所有线程"/"挂起所有进程"设置）。

因此，这里之所以能正常工作，是因为 `launch.py` 使用被调试进程中的标准 `multiprocessing` API 创建子进程。如果某个子进程使用不同的解释器执行 `os.execv` 或后台守护化，自动附加就会失败——但这里不是这种情况。

## 逐步创建运行配置（附你的机器实际值）

我检查了你的 GPU（`RTX 4070, 12GB`）和本地模型。**DeepSeek-V2-Lite 需要 30GB — 无法加载。** 位于 `/mnt/data/sec-edgar-gpt-124m-model/` 的 626MB GPT-2 是合适的调试目标。

*运行 → 编辑配置 → ➕ → Python*：

| 字段 | 值 |
|---|---|
| 名称 | `minisgl-debug` |
| **模块名** | `minisgl`（不是"脚本路径"——使用下拉菜单） |
| 解释器选项 | `-s` |
| 工作目录 | `/mnt/data/mini-sglang` |
| 参数 | `--model-path /mnt/data/sec-edgar-gpt-124m-model --tp-size 1 --port 1919 --dtype float32` |
| 环境变量 | `PYTHONUNBUFFERED=1`（通过环境变量编辑器添加） |
| 使用 Python 控制台运行 | 取消勾选（保持标准调试器） |

参数说明：
- `--model-path ...` 是唯一**必需的**参数（`args.py` 中的 `parser.add_argument(..., required=True)`）。
- `--tp-size 1` → 只创建**一个**调度器子进程，而不是 N 个。多 GPU 调试会使进程树成倍增加。
- `--dtype float32` → 124M GPT-2 使用 fp32 没问题，可以避免在首次调试过程中触发 dtype 转换相关的代码路径。（之后可以切换到 `--dtype bfloat16`。）
- `--num-tokenizer 0` 是默认值（共享分词器/反分词器）——保留此设置；进程更少。
- `--shell-mode` 会运行交互式提示符而不是 uvicorn——这不是你想要的 API 调试方式，但如果你想在 REPL 中调试请求处理，会很方便。

然后按下 **调试**。调试工具窗口将显示进程树：

```
minisgl-debug (主进程)                          ← api_server.py (FastAPI/uvicorn, 端口 1919)
├── minisgl-TP0-scheduler                     ← scheduler/scheduler.py, 引擎, kvcache
├── minisgl-tokenizer-0                       ← tokenizer/
└── minisgl-detokenizer-0                     ← tokenizer/ (反分词路径)
```

你可以从进程树中暂停/终止单个进程，还有一个"恢复所有进程"的开关，这样你可以在一个子进程上调试时，让其他进程继续运行。

## 具体调试工作流程

1. 在 `python/minisgl/scheduler/prefill.py` 中设置断点（第一个请求），并在 `decode.py` 中设置一个断点。
2. 通过运行配置启动服务器；使用 curl 发送请求：
   ```bash
   curl http://127.0.0.1:1919/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt2","messages":[{"role":"user","content":"你好！"}],"max_tokens":16}'
   ```
3. 执行在 **TP0-scheduler** 进程中停止。你可以：
   - **评估** `len(seq_ids)`、`batch.seq_lens` — 张量会在变量窗格中显示为 shape/dtype（PyCharm 原生渲染 torch 张量）。
   - 单步跳过 CUDA 内核调用（FlashInfer/sgl_kernel）——你无法单步*进入*这些调用（编译后的 C++），所以在这些行使用*跳过*。
   - 使用**评估表达式**（`⌥F8`）查看 `tensor.shape`、`isinstance(x, torch.Tensor)`。
4. 如果要调试 HTTP 层，在 `server/api_server.py` 中设置断点——这将触发**主进程**中的断点。

## 该项目的特定注意事项

- **`mp.set_start_method("spawn", force=True)`** 没问题——PyCharm 的自动附加功能通过环境变量继承机制可以在 spawn 方式下正常工作。唯一需要避免的是：*永远不要*在使用 PyCharm 调试器的同时添加你自己的 `debugpy`/`pdb` 调用——两个调试器附加到同一个进程会导致冲突（端口/文件锁定问题）。
- **CUDA 内核是不透明的**：FlashAttention/FlashInfer/sgl_kernel JIT C++ 无法单步进入；围绕它们的 Python 断点可以正常工作。
- **`torch.inference_mode()`** 在 `_run_scheduler` 内部处于活动状态——张量的自动求导历史被关闭，因此你无法检查 `grad_fn`。这是预期行为。
- **GPU 内存**：12GB 的显卡还需要容纳 KV 缓存；GPT-2 124M 大约剩余 11GB 空闲，非常充足。如果你以后使用 DeepSeek-V2-Lite，则需要 `--tp-size 2` 跨两块 GPU 运行，否则会面临 OOM（内存不足）。
- **在生成的子进程内使用 `breakpoint()`** 会将子进程的标准输入附加到中断点——在 PyCharm 运行调试的情况下，不要混用。

需要我帮你编写 PyCharm 运行配置的 XML 文件（`.idea/runConfigurations/minisgl_debug.xml`），让它自动出现在你的运行配置下拉菜单中吗？
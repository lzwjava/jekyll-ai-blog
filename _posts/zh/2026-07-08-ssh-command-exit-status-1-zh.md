---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH 命令退出状态 1
translated: true
type: note
---

问题：这个 SSH 命令是干什么的，为什么它以状态 1 退出？

答案：

**它的作用**

这是一个通过 SSH 对 AMD Dev Cloud（或其他 GPU 机器）执行的单次远程诊断运行，针对 `nanochat` 项目的虚拟环境：

```bash
ssh root@<IP_ADDRESS> -p 30520 -i ~/.ssh/id_ed25519 -o StrictHostKeyChecking=no \
  "source /workspace/nanochat/.venv/bin/activate && \
   echo '=== FA3 check ===' && python3 -c '...' && \
   echo '=== triton test ===' && python3 -c '...'"
```

它运行两个检查：

1. **FA3 检查** — 从 `nanochat.flash_attention` 导入 `HAS_FA3` 和 `flash_attn`，打印 FlashAttention-3 是否已编译进去，然后在 CUDA 上执行一个微小的 `[1,1,32,128]` bf16 注意力前向传递，以确认内核实际运行。
2. **Triton 测试** — 执行一个简单的 CUDA 张量加法，然后定义并 JIT 编译一个 Triton `add_kernel`，以确认机器上的 Triton 代码生成/编译正常工作。

两部分通过 `&&` 串联，因此如果任一个 Python 调用返回非零值，整个命令就会以非零退出——这就是你看到的（`exit 1`）。

**失败原因**

仔细看 Triton 内核体：

```python
@triton.jit
def add_kernel(x_ptr, y_ptr, output_ptr, n, BLOCK_SIZE: triton.literal):
    pid = triton.program_id(0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + triton.arange(0, BLOCK_SIZE)
    mask = offsets < n
    x = triton.load(x_ptr + offsets, mask=mask)
    y = triton.load(y_ptr + offsets, mask=mask)
    triton.store(output_ptr + offsets, x + y, mask=mask)
```

在 `@triton.jit` 函数内部，所有语言原语都位于 `triton.language`（通常导入为 `tl`），**而不是**在顶层 `triton` 模块上：

- `triton.literal` → 不存在；应该是 `tl.constexpr`
- `triton.program_id` → 应该是 `tl.program_id`
- `triton.arange` → 应该是 `tl.arange`
- `triton.load` / `triton.store` → 应该是 `tl.load` / `tl.store`

在 JIT 编译时，Triton 前端会对函数进行 AST 遍历并尝试解析这些属性引用——`triton.literal` 等会在编译时引发 `AttributeError`（或类型解析失败），因此 `add_kernel[grid](...)` 会抛出异常，你的 `except Exception as e: print(...)` 会捕获并打印 `Triton JIT failed: ...`，但关键是 **Python 进程本身如果只打印的话可能仍会以 0 退出**——所以 exit 1 更可能来自第一个代码块（FA3 检查），除非外层 shell 引号出了问题。

实际上，考虑到该命令已经被压平成一个单一的 `ssh "..."` 字符串，exit 1 更可能的原因在于：你原本的 heredoc 风格 Python 代码（包含真实换行和 4 空格缩进）在被序列化为一个 shell 字符串时发生了换行/重新引号化。如果任何缩进或引号转义在传输过程中被损坏（例如嵌套在双引号 SSH 命令中的单引号），那么在 `try/except` 逻辑运行之前就会引发 `SyntaxError`/`IndentationError`——这会导致立即以 1 退出，并解释为什么你在粘贴的内容中根本看不到 `=== FA3 check ===` 或 `=== triton test ===` 输出（值得检查：你实际看到过这些 echo 行打印吗？还是输出直接以 traceback 开始？）。

**如何正确调试（不要纠结于引号）**

将真正的脚本推送到远程机器，而不是通过嵌套的 SSH 引号内联 Python：

```python
# fa3_triton_check.py
from nanochat.flash_attention import HAS_FA3, flash_attn
import torch
import triton
import triton.language as tl

print(f"FA3 available: {HAS_FA3}")
print(f"flash_attn module: {flash_attn.__module__}")

q = torch.randn(1, 1, 32, 128, dtype=torch.bfloat16, device="cuda")
k = torch.randn(1, 1, 32, 128, dtype=torch.bfloat16, device="cuda")
v = torch.randn(1, 1, 32, 128, dtype=torch.bfloat16, device="cuda")
try:
    out = flash_attn(q, k, v)
    print(f"FA test: OK, output shape {out.shape}")
except Exception as e:
    print(f"FA test FAILED: {e}")

x = torch.randn(100, 100, device="cuda")
y = x + x
print(f"Basic cuda ops OK: {y.shape}")

@triton.jit
def add_kernel(x_ptr, y_ptr, output_ptr, n, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    block_start = pid * BLOCK_SIZE
    offsets = block_start + tl.arange(0, BLOCK_SIZE)
    mask = offsets < n
    a = tl.load(x_ptr + offsets, mask=mask)
    b = tl.load(y_ptr + offsets, mask=mask)
    tl.store(output_ptr + offsets, a + b, mask=mask)

grid = lambda meta: (triton.cdiv(100, meta["BLOCK_SIZE"]),)
try:
    out = torch.empty_like(x)
    add_kernel[grid](x, y, out, 100, BLOCK_SIZE=32)
    print("Triton JIT compile: OK")
except Exception as e:
    print(f"Triton JIT failed: {e}")
```

然后：

```bash
scp -P 30520 -i ~/.ssh/id_ed25519 fa3_triton_check.py root@<IP_ADDRESS>:/workspace/nanochat/
ssh root@<IP_ADDRESS> -p 30520 -i ~/.ssh/id_ed25519 \
  "source /workspace/nanochat/.venv/bin/activate && python3 /workspace/nanochat/fa3_triton_check.py"
```

另请注意：`grid` 需要通过 `meta`/kwargs 传递 `BLOCK_SIZE`（`meta["BLOCK_SIZE"]` 或显式传递 `BLOCK_SIZE=32`）——一个忽略 `meta` 的裸 `triton.cdiv(100, 32)` 网格 lambda 也可以工作，但一旦后续加入自动调优就会变得脆弱。

这样做消除了引号转义这一变量，提供了真正的 traceback 而非被吞掉的退出码，并且与你将来实际驱动远程 nanochat/FA3 实验的方式一致（推送脚本、scp、运行、`cat` 日志回来）。

---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 优化CLI代理的性能权衡
translated: true
type: note
---

**问题：** 对于一个最小的 OpenCode/Claude Code CLI 代理，Python 与 Rust 的速度差异可以忽略不计，因为瓶颈在于 LLM API 延迟——但我们是否仍然应该进行性能分析？而对于数据密集型（大型 Excel）或计算密集型工作负载，Rust 可能明显更快，对吧？

**回答：**

是的，你说得完全正确。让我详细分解一下。

## 瓶颈层级

对于一个 LLM 代理 CLI，延迟栈如下：

```
LLM API 调用：        2,000 – 30,000 ms   ← 占据主导地位
网络 I/O：            50 – 500 ms
文件 I/O：            1 – 50 ms
JSON 解析：           0.1 – 5 ms
Python 启动：         50 – 150 ms         ← 在 CLI 上实际可见！
Rust 启动：           1 – 5 ms
```

因此，对于 Claude Code 风格的工具，**Python 启动延迟是唯一的实际差距**——而且仅当你在紧密循环中成百上千次调用该二进制文件时才会感觉到（例如在 shell 循环中按文件调用代理）。

---

## Rust 真正获胜的地方

### 1. 大型 Excel / 数据处理

Python 中通过 `openpyxl` 处理 Excel 文件在大型工作表上众所周知地慢：

```python
# Python: openpyxl 读取 10 万行——可能需要 10-30 秒
import openpyxl
wb = openpyxl.load_workbook("big.xlsx")  # 慢，内存占用高
```

Rust 使用 `calamine` crate 在 <1 秒内读取相同内容：

```rust
use calamine::{open_workbook, Reader, Xlsx};

let mut wb: Xlsx<_> = open_workbook("big.xlsx").unwrap();
let sheet = wb.worksheet_range("Sheet1").unwrap();
for row in sheet.rows() {
    // 在 ~200ms 内处理 10 万行
}
```

Python 的变通方法：使用 `pandas` + `openpyxl` 引擎，或者更好的 `polars`（基于 Rust）：

```python
import polars as pl
df = pl.read_excel("big.xlsx")  # polars 底层使用 Rust
```

因此，对于 DataFrame，Python 结合 Polars 基本弥补了差距。但如果你在处理**自定义的逐行逻辑**，Rust 仍然占优。

### 2. 计算密集型（正则扫描、AST 解析、文件搜索）

Claude Code 的杀手锏是快速的代码库索引。如果你要扫描 5 万个文件查找符号：

```
Python 类似 grep 的扫描 5 万个文件：   ~8 秒
Rust 类似 ripgrep 的扫描：             ~0.3 秒
```

这就是 `ripgrep` 存在的原因，也是 `ast-grep` 等工具使用 Rust 编写的原因。Rust 的并行性加上零拷贝字符串扫描是其优势所在。

### 3. 并行工具调用

如果你的代理同时运行多个工具调用（读取 10 个文件，执行 3 个 shell 命令），Python 的 GIL 限制了真正的 CPU 并行性。Rust 的 `tokio` + `rayon` 能同时提供异步 I/O 和 CPU 并行性。

---

## 如何实际进行性能分析

不要靠猜测。以下是 CLI 代理的最小性能分析设置：

**Python —— 分析代理中非 LLM 的时间：**

```python
import cProfile
import pstats
import io

pr = cProfile.Profile()
pr.enable()

# 在此处放置代理的工具使用/文件处理代码
result = process_repo("./my_project")

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(20)
print(s.getvalue())
```

或者使用 `py-spy` 对运行中的进程进行零开销采样：

```bash
py-spy record -o profile.svg -- python agent.py
```

**Rust —— 使用 criterion 进行 `cargo bench`：**

```rust
use criterion::{criterion_group, criterion_main, Criterion};

fn bench_file_scan(c: &mut Criterion) {
    c.bench_function("scan_repo", |b| {
        b.iter(|| scan_repository("./test_repo"))
    });
}

criterion_group!(benches, bench_file_scan);
criterion_main!(benches);
```

**整个代理循环的实际时间比较：**

```bash
# 测量除 LLM 时间之外的所有内容
hyperfine \
  'python agent.py --dry-run --no-llm' \
  './target/release/agent --dry-run --no-llm' \
  --warmup 3
```

`hyperfine` 会给出均值、标准差以及清晰的比较表格。

---

## 针对你的用例的实际决策矩阵

| 工作负载 | Python 是否足够好？ | Rust 是否值得？ |
|---|---|---|
| LLM API 编排 | ✅ 总是 | 杀鸡用牛刀 |
| 小文件读取（<1k 文件） | ✅ | 否 |
| 大型 Excel（>5 万行，自定义逻辑） | ⚠️ 使用 polars | ✅ 是 |
| 完整代码库索引（>1 万个文件） | ❌ 慢 | ✅ 是 |
| 大规模正则/AST 扫描 | ❌ | ✅ 是 |
| API 响应的 JSON 解析 | ✅ | 边际收益 |
| 紧密循环中的 CLI 启动 | ⚠️ 100ms 开销 | ✅ 5ms |

---

## 我对你情况的建议

对于你的 `ww`/`zz`/`iclaw` 风格的 CLI 代理：**先用 Python 开始，用 `py-spy` 分析，只有当分析显示非 LLM 代码占用了超过 10% 的实际时间时，才重写 Rust 热路径。**

我会立即用 Rust 开始的唯一情况是：如果你正在构建类似代码库索引器、文件监视器或大型仓库上的语义搜索工具——这些场景 Rust 从第一天起就有价值。`ast-grep`、`ripgrep` 和 `oxc`（JS 解析器）这类工具的存在正是因为这个原因。

对于纯 LLM 代理编排（比如一个最小化的 Claude Code 克隆），Python 配合 `asyncio` 就足够了——`await anthropic.messages.create()` 会吞噬其他所有开销。
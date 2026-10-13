---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python floor 语义已实现
translated: true
type: note
---

完成。这是全貌。

## 我改进的内容

**1. `//` 和 `%` 现在符合 Python 的 floor 语义（README 的 #1 路线图项目）**

`wei` 自称与 Python 类似，但除法是 C 风格的：LLVM 的 `sdiv`/`srem` 向零截断，而 `frem`/`fdiv` 在负数情况下与 Python 不同。因此 `-7 // 2` 输出 `-3`，`7 % -2` 输出 `1`，`-7.0 % 3` 输出 `-1` — 这些与 CPython 的结果（分别为 `-4`、`-1`、`2`）不一致。

该规则使 wei 在算术方面真正功能完备（测试断言恒等式 `a == (a//b)*b + a%b`）：

* `-7 // 2  -> -4`（向下取整除法，而非 C 截断）— 同时使用 `sdiv` + `srem`，在符号不同时进行调整
* `-7 % 2   -> 1`（结果采用**除数的符号**，而不是被除数）
* `-9.0 % 4 -> 3`、`7.0 % -3 -> -2`（浮点数通过对商使用 `llvm.floor` 实现）
* 整数 `/`、`//`、`%` **除以零** 现在会打印 `ZeroDivisionError: division by zero` 并以状态 1 退出（之前是 `-4617182418800017408` 这样的垃圾值）。
* 浮点数保留 IEEE 的 `inf`/`nan` 用于 `/`，已记录。

文件：`wei/codegen.py`、`wei/compiler.py`（`build_source`）、`README.md`。

**2. `wei build -O2` 现在在这台机器上开箱即用**

它依赖于 `$OPT`/`$LLVM_BIN`，而这两个变量无法从 PATH 中获取（Homebrew 的 `llvm` 不在 PATH 中）。新增了 Homebrew 发现机制（`/opt/homebrew/opt/llvm/bin/opt`，带版本的 Cellar）。还**清理了 `compiler.py` 中未使用的导入**（`ast.Module`、无用的 `ast.is_numeric` 辅助函数、未使用的 `tokenize`/`ParseError`/`LexError`）。

**3. 通过真正的 guard 来强化正确性**

```python
def _guard_div_zero(self, divisor, op, node):
    """insert a runtime ZeroDivisionError check before integer div/rem"""
    is_zero = self.builder.icmp_signed("==", divisor, ir.Constant(I64, 0))
    with self.builder.if_then(is_zero):
        ...printf + exit(1)
```

## 还可以改进的地方（后续步骤，按价值/工作量排序）

这里没有任何根本性的阻塞 — 语言很干净，在它声称的方面是正确的，并且 `46 passed`。优先级：

1. **`wei` REPL（路线图）** — 一个功能丰富的交互式循环成本最低（JIT 路径已经齐全：`compile_source` + `run_module`）。这将大幅提高“感觉像 Python”的标准。
2. **类型检查器作为独立的遍** — 提供带有*列*信息的真实语义错误消息（AST 从不记录列，所以 `print(10+ )` 的错误会宽泛地指向整行）。这可以干净地分解为一个在代码生成之前遍历 AST 的检查器。
3. **字符串作为可增长的缓冲区（`+=`、`len`、`substr`、比较）** — 路线图项目；`str` 目前是 `i8*`，因此是静态大小的；需要堆分配器（`libc` 的 `malloc`/`realloc`）。
4. **列表/数组 + 切片** — 路线图；需要堆 + GC 策略（首次尝试可以使用 bump allocator）。
5. **`io` 的 current_function 名称打印、`read_float`、`print` 的 stdin** — 轻而易举的胜利。

**我注意到但没有处理的小问题（低风险）：**

* 没有功能上的阻塞。测试很全面（`46 passed`），错误信息带有源码 caret，IR 很干净。

接下来真正要构建的是 **REPL** — 它直接重用 `run_module`，只需一次小重构（编译一次，在重新定义函数时保留模块），这将让 wei 立刻变得生动起来。我会从那里开始。需要我现在实现 REPL 吗？

## 总结

**已实现（全部 `46 passed`）：**

1. **Python floor 除法/取余语义**（路线图项目已完成） — `//` 和 `%` 现在在负数操作数上遵循 CPython：`-7 // 2 == -4`、`7 % -2 == -1`、`-7.0 % 3 == 2`，并通过恒等式 `a == (a//b)*b + a%b` 验证。
2. **运行时 `ZeroDivisionError`** — 整数除/取余除以零现在会打印消息并以状态 1 退出（之前是像 `-4617182418800017408` 这样的静默垃圾值）；浮点操作保持 IEEE（`inf`/`nan`）。
3. **`wei build -O2` 之前只有显式设置 `$OPT` 才能在此工作** — 新增了 Homebrew `opt` 的自动发现（`/opt/homebrew/opt/llvm/bin/opt`，带版本的 Cellar）；还清理了未使用的导入（`tokenize`、`ParseError`、`LexError`、无用的 `ast.is_numeric`）。

**接下来我会做：REPL**（价值/努力比最高 — 它通过一次小重构就重用了 `compile_source` + `run_module`：在重新定义时保持模块存活）。之后：一个真正的类型检查器遍，为多 token 表达式提供源码列错误。

涉及的文件：`wei/codegen.py`、`wei/compiler.py`、`README.md`、`tests/test_e2e.py`。

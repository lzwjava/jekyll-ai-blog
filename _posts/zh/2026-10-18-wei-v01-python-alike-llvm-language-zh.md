---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Wei v0.1 类似Python的LLVM语言
translated: true
type: note
---

完成！**wei v0.1** 是一种使用 LLVM 编译的可运行的类 Python 语言——全部 42 个测试通过，已提交到 git。

## 构建内容

```
wei/
├── wei/lexer.py     tokenizer with Python-style indentation (INDENT/DEDENT)
├── wei/ast.py       AST node definitions
├── wei/parser.py    recursive-descent parser (precedence ladder, if/elif/else…)
├── wei/codegen.py   AST → LLVM IR via llvmlite (bundled LLVM 22)
├── wei/compiler.py  pipeline driver (JIT runner + AOT linker)
├── wei/cli.py       `wei run | build | ir | check`
├── examples/        hello, control, fib, fizzbuzz, math
└── tests/           lexer + parser + 20 end-to-end tests
```

## 这种语言

```python
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)     # recursion works (functions are hoisted)

answer = 42                            # type inferred: int = i64
pi: float = 3.14159
for k in range(10, 1, -2):             # indentation blocks, Python style
    print(k, answer, pi)
n = read_int()
print("n + 1 =", n + 1)                # print → variadic libc printf
```

## 端到端验证

- **JIT**：`wei run fib.wei` → MCJIT，输出 `fib(20) = 6765`
- **AOT**：`wei build fizzbuzz.wei -o prog` → `.o` + clang 链接 → 原生二进制
- **中间端**：`wei build fib.wei -O2` → 运行系统 LLVM `opt` 流水线
- **互操作**：生成的 IR 通过 `opt -passes=verify` 验证，可在 `lli` 下执行
- **类型**：`i64`/`double`/`i1`/`i8*`，int→float 自动提升，Python 风格 `/`（真除法），通过 `llvm.pow.f64` 实现 `**`，带 `phi` 的短路 `and`/`or`，链式比较

## 过程中发现并修复的几个真实 bug

1. 在值计算完成之前将变量初始化器存储在 `entry` 块中
2. LLVM 的规则：**块 #0 是函数入口**（allocas 必须位于其中）
3. 在消费空白字符之前计算缩进 → 产生虚假的 `DEDENT`/`INDENT` 对
4. Python 中 `"" in "eE"` 为 `True` → 在 EOF 时越界
5. UTF-8 字符串全局变量按字符而非字节计算大小

试试看：`.venv/bin/wei run examples/fib.wei`，或者 `echo 100 | wei run - <<< 'n = read_int()...'`。

自然的后续步骤（见 README 路线图）：一个合适的类型检查器阶段、字符串操作、列表/结构体，或者 REPL——我接下来可以处理其中任何一个。

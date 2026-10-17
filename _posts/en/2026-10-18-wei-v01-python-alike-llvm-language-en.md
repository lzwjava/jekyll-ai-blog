---
audio: false
generated: true
image: false
lang: en
layout: post
title: Wei v0.1 Python-alike LLVM language
translated: false
type: note
---

Done! **wei v0.1** is a working Python-alike language compiled with LLVM — all 42 tests pass, committed to git.

## What got built

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

## The language

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

## Verified end-to-end

- **JIT**: `wei run fib.wei` → MCJIT, prints `fib(20) = 6765`
- **AOT**: `wei build fizzbuzz.wei -o prog` → `.o` + clang link → native binary
- **Middle-end**: `wei build fib.wei -O2` → runs the system LLVM `opt` pipeline
- **Interop**: emitted IR verified by `opt -passes=verify`, executes under `lli`
- **Types**: `i64`/`double`/`i1`/`i8*`, int→float auto-promotion, Python-style `/` (true division), `**` via `llvm.pow.f64`, short-circuit `and`/`or` with `phi`, chained comparisons

## A few real bugs found & fixed along the way

1. Storing variable initializers in the `entry` block before the value was computed
2. LLVM's rule that **block #0 is the function entry** (allocas must live there)
3. Indentation computed before consuming whitespace → spurious `DEDENT`/`INDENT` pairs
4. `"" in "eE"` being `True` in Python → out-of-bounds at EOF
5. UTF-8 string globals sized by chars instead of bytes

Try it: `.venv/bin/wei run examples/fib.wei`, or `echo 100 | wei run - <<< 'n = read_int()...'`.

Natural next steps (in the README roadmap): a proper type-checker pass, string ops, lists/structs, or a REPL — I can take any of those next.

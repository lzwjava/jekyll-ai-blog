---
audio: false
generated: true
image: false
lang: en
layout: post
title: Python floor semantics implemented
translated: false
type: note
---

Done. Here's the full picture.

## What I improved

**1. `//` and `%` now match Python floor semantics (the README's #1 roadmap item)**

`wei`'s claims to be Python-alike, but division was C-style: LLVM's `sdiv`/`srem` truncate toward zero, and `frem`/`fdiv` differ from Python for negatives. So `-7 // 2` printed `-3`, `7 % -2` printed `1`, and `-7.0 % 3` printed `-1` — all wrong versus CPython (which gives `-4`, `-1`, `2`).

The rule makes wei genuinely feature-complete on the arithmetic front (tests asserts the identity `a == (a//b)*b + a%b`):

* `-7 // 2  -> -4` (floor division, not C truncation) — booth `sdiv` + `srem`, adjust when signs differ
* `-7 % 2   -> 1`  (result takes the **sign of the divisor**, not dividend)
* `-9.0 % 4 -> 3`, `7.0 % -3 -> -2` (floats via `llvm.floor` of the quotient)
* int `/`, `//`, `%` **by zero** now print `ZeroDivisionError: division by zero` and exit with status 1 (was: `-4617182418800017408` garbage).
* floats keep IEEE `inf`/`nan` for `/`, documented.

Files: `wei/codegen.py`, `wei/compiler.py` (`build_source`), `README.md`.

**2. `wei build -O2` now works out of the box on this machine**

It depended on `$OPT`/`$LLVM_BIN`, which weren't reachable from path (Homebrew `llvm` isn't on PATH). Added Homebrew discovery (`/opt/homebrew/opt/llvm/bin/opt`, versioned Cellar). Also **cleaned unused imports** in `compiler.py` (`ast.Module`, dead `ast.is_numeric` helper, unused `tokenize`/`ParseError`/`LexError`).

**3. Correctness hardening via a real guard**

```python
def _guard_div_zero(self, divisor, op, node):
    """insert a runtime ZeroDivisionError check before integer div/rem"""
    is_zero = self.builder.icmp_signed("==", divisor, ir.Constant(I64, 0))
    with self.builder.if_then(is_zero):
        ...printf + exit(1)
```

## What could still be improved (next steps, in order of value/effort)

Nothing here is asymptotically blocking — the language is clean, correct where it claims to be, and `46 passed`. Priorities:

1. **`wei` REPL (roadmap)** — a rich interactive loop costs the least (the JIT path is all there: `compile_source` + `run_module`). Would substantially raise the "feels like Python" bar.
2. **Type checker as a separate pass** — real semantic error messages with *column* info (the AST never records columns, so `print(10+ )` errors point generously to the whole line). This decomposes cleanly into a checker that walks the AST before codegen.
3. **Strings as growable buffers (`+=`, `len`, `substr`, comparison)** — roadmap item; `str` is currently `i8*` so it's statically sized; needs heap allocator (`libc` `malloc`/`realloc`).
4. **Lists/arrays + slices** — roadmap; needs heap + GC strategy (bump allocator for a first cut).
5. **`io` current_function name printing, `read_float`, stdin for `print`** — trivial wins.

**Minor nits I noticed but didn't touch (low risk):**

* None functionally blocking. Tests are thorough (`46 passed`), errors have source carets, IR is clean.

The next thing to actually build is the **REPL** — it reuses `run_module` directly with one small refactor (compile once, keep the module around when a function is redefined), and it makes wei feel alive immediately. I'd start there. Want me to implement the REPL now?## Summary

**Implemented (all `46 passed`):**

1. **Python floor division/remainder semantics** (roadmap item done) — `//` and `%` now follow CPython for negative operands: `-7 // 2 == -4`, `7 % -2 == -1`, `-7.0 % 3 == 2`, verified against the identity `a == (a//b)*b + a%b`.
2. **Runtime `ZeroDivisionError`** — integer div/rem by zero now prints a message and exits with status 1 (was: silent garbage like `-4617182418800017408`); float ops stay IEEE (`inf`/`nan`).
3. **`wei build -O2` worked here only with explicit `$OPT`** — added automatic Homebrew `opt` discovery (`/opt/homebrew/opt/llvm/bin/opt`, versioned Cellar); also cleaned unused imports (`tokenize`, `ParseError`, `LexError`, dead `ast.is_numeric`).

**Next thing I'd do: the REPL** (highest value-per-effort — it reuses `compile_source` + `run_module` with just one refactor: keep modules alive across redefinitions). After that: a real type-checker pass with source-column errors for multi-token expressions.

Files touched: `wei/codegen.py`, `wei/compiler.py`, `README.md`, `tests/test_e2e.py`.

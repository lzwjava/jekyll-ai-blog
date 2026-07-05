---
audio: false
generated: true
image: false
lang: en
layout: post
title: XeLaTeX vs Other TeX Compilers
translated: false
type: note
---

**Question:** Compare XeLaTeX with other TeX compilers (pdfLaTeX, LuaLaTeX, etc.) — what are the differences and when should each be used?

**Answer:**

## The engine landscape

There are four engines you'll actually encounter. All of them run the same macro layer (LaTeX) on top — the "compiler" difference is the *engine* underneath.

| Engine | Output | Fonts | Unicode | Speed | Extensibility |
|---|---|---|---|---|---|
| pdfTeX (`pdflatex`) | PDF directly | Legacy (Type1/TFM, 8-bit) | No (workarounds via `inputenc`) | Fastest | microtype (protrusion + expansion) |
| XeTeX (`xelatex`) | PDF via `xdvipdfmx` | System fonts (OpenType/TrueType via `fontspec`) | Native UTF-8 | Medium | Limited; protrusion only, no font expansion |
| LuaTeX (`lualatex`) | PDF directly | System fonts via `fontspec` (loaded in Lua) | Native UTF-8 | Slowest cold start | Lua scripting inside the engine — full node-list access |
| (u)pTeX / classic `latex`+`dvips` | DVI → PS/PDF | Legacy | No (pTeX: Japanese-specific) | Fast | Niche (Japanese typesetting, PSTricks) |

## First-principles: what actually differs

The core divergence is **how text becomes glyphs**.

**pdfTeX** is 8-bit at heart. Every "character" is a byte; UTF-8 input is faked by `\usepackage[utf8]{inputenc}` decoding multi-byte sequences into macro calls. Fonts are the old TFM metric + Type1 world — you can't just point at `PingFang.ttc` on your Mac; someone has to have packaged the font for TeX (that's what packages like `lmodern`, `newtx` are).

**XeTeX**'s big idea: delegate text shaping to the OS-adjacent stack. It reads native UTF-8, and uses HarfBuzz (formerly ICU) to shape OpenType fonts — ligatures, contextual forms, CJK, Arabic, Devanagari all just work. Internally it still produces an extended DVI (`.xdv`) which `xdvipdfmx` converts to PDF — that indirection is why some pdfTeX-specific PDF primitives don't exist in XeTeX.

**LuaTeX** took the opposite approach: instead of bolting an external shaper onto TeX, it rewrote the engine with an embedded Lua interpreter and exposed TeX's internals (node lists, callbacks, font loader) as Lua APIs. Font loading is done *in Lua* (`luaotfload`), so it's programmable — you can intercept the paragraph builder, mutate glyph nodes, generate content at typesetting time. This is why LuaLaTeX is now the officially recommended "modern" engine for LaTeX development; the LaTeX team's new features (e.g., tagged/accessible PDF) target it first.

## Practical decision tree

```
Need Lua scripting, advanced microtype, or cutting-edge LaTeX features?  → lualatex
Need CJK/Arabic/system fonts, and lualatex is too slow for you?          → xelatex
Pure English/Latin doc, journal template, want max speed + microtype?   → pdflatex
Journal/arXiv forces a specific engine?                                  → do what they say
```

Concrete cases:

- **Chinese documents**: `ctex` package supports both, but `xelatex` has historically been the default for `ctexart` and is battle-tested with CJK. `lualatex` + `luatexja` also works well now.
- **arXiv / many journals**: pdfLaTeX is still the safest submission target; XeLaTeX support on arXiv exists but is fussier.
- **Beamer with custom brand fonts**: XeLaTeX or LuaLaTeX (you need `fontspec`).
- **Resume/CV with system fonts**: XeLaTeX is the classic choice (most CV templates like moderncv/awesome-cv assume it).

## Minimal working examples

pdfLaTeX (legacy font world):

```latex
\documentclass{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}  % no-op on modern LaTeX, kept for clarity
\usepackage{lmodern}
\usepackage{microtype}       % full power only on pdftex/luatex
\begin{document}
Hello, world.
\end{document}
```

XeLaTeX / LuaLaTeX (same source works for both):

```latex
\documentclass{article}
\usepackage{fontspec}
\setmainfont{Source Serif 4}       % any installed OpenType font
% CJK:
% \usepackage{xeCJK}               % xelatex
% \setCJKmainfont{PingFang SC}
\begin{document}
Hello, 你好, مرحبا — all native UTF-8.
\end{document}
```

Engine detection in a portable preamble:

```latex
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}\usepackage{lmodern}
\else
  \usepackage{fontspec}
\fi
```

Build commands (on your M2 Air, `brew install --cask mactex-no-gui`):

```bash
latexmk -pdf doc.tex          # pdflatex
latexmk -xelatex doc.tex
latexmk -lualatex doc.tex
```

## Gotchas worth knowing

- **Speed**: pdfLaTeX ≈ 2–5× faster than LuaLaTeX on cold compile; LuaLaTeX's Lua font loader dominates startup. For CI pipelines rebuilding docs constantly, this matters. `lualatex --luaonly` caching and `luahbtex` (the default binary since TeX Live 2020, HarfBuzz shaping) narrowed the gap.
- **microtype**: font expansion (subtle glyph stretching for better justification) works on pdfTeX and LuaTeX but *not* XeTeX — XeTeX only gets character protrusion. If you care about typographic gray, LuaLaTeX > XeLaTeX.
- **`\special`/PDF primitives**: packages doing low-level PDF tricks (some tikz externalization setups, `pdfpages` edge cases, media embedding) behave differently on XeTeX due to the `.xdv` → PDF indirection.
- **XeTeX's future**: it's in maintenance mode — stable, but new development energy (LaTeX3, tagged PDF, `luametatex`/ConTeXt) is on the Lua side. For new long-lived projects, prefer LuaLaTeX unless you have a XeTeX-specific need like `xeCJK` muscle memory.
- **Tectonic**: worth a look for your CLI-agent workflows — a Rust-wrapped XeTeX with automatic dependency fetching, single binary, reproducible builds. `brew install tectonic; tectonic doc.tex` and it downloads only the packages it needs. Great for automation, no 5GB TeX Live install.

## TL;DR for your setup

For your blog/notes PDF pipelines: **LuaLaTeX** if starting fresh (future-proof, scriptable — you can even generate content from Lua, which fits your automation style), **XeLaTeX** if you're doing Chinese docs with existing `xeCJK` templates, **pdfLaTeX** only when a journal or arXiv forces it. **Tectonic** if you want the whole thing as a clean CLI dependency in an agent pipeline.

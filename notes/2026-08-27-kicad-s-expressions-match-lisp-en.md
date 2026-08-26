---
audio: false
generated: true
image: false
lang: en
layout: post
title: KiCad S-expressions match Lisp
translated: false
type: note
---

**Question:** Is KiCad's S-expression format the same as Lisp/Scheme S-expressions?

**Answer:**

Yes, exactly the same concept — KiCad's format is directly inspired by Lisp/Scheme S-expressions. Here's the breakdown:

**What they share**

The core syntax is identical in spirit:
- Parentheses for grouping: `(key value value ...)`
- Nested/recursive structure
- Atoms (symbols, numbers, strings)

A KiCad schematic snippet looks like:
```lisp
(kicad_sch
  (version 20230121)
  (symbol (lib_id "Device:R")
    (at 100.0 50.0 0)
    (property "Reference" "R1"
      (at 101.5 48.5 0)))
  (wire
    (pts (xy 100 50) (xy 110 50))))
```

That's pure S-expression — a Lisp programmer would feel right at home reading it.

**Where it differs from Lisp/Scheme**

| Feature | Lisp/Scheme | KiCad S-expr |
|---|---|---|
| Purpose | Code + data | Data only |
| Evaluation | Executed by interpreter | Parsed as config |
| `car`/`cdr` semantics | Yes | No |
| Macros / lambdas | Yes | No |
| Strings | `"..."` | `"..."` same |
| Comments | `;` semicolon | `#` hash (KiCad-specific!) |

KiCad's format is essentially **S-expressions used purely as a data serialization format** — like JSON but with parens instead of braces. No evaluation, no functions.

**Historical context**

This pattern has precedent — Emacs config files, GNOME's GConf, and many EDA tools have used S-expressions as a human-readable, VCS-friendly alternative to XML or JSON. KiCad switched from its old custom format to S-expressions around v5/v6 specifically because they're easy to diff, parse, and generate programmatically.

**For AI/LLM purposes**

Because it's regular and recursive like Lisp, you can:
- Parse it with any Lisp reader (Common Lisp, Racket, Guile all work out of the box)
- Parse it in Python with a simple recursive descent parser or `sexpdata` library
- Feed it directly to an LLM — the structure is self-documenting

So yes — if you know Lisp or Scheme, you already understand KiCad's file format at a structural level.

**References:**
- [KiCad File Format Docs](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/)
- [Wikipedia: S-expression](https://en.wikipedia.org/wiki/S-expression)

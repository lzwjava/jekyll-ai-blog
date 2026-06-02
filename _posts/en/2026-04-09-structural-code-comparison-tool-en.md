---
audio: false
generated: true
image: false
lang: en
layout: post
title: Structural Code Comparison Tool Introduction
translated: false
type: note
---

I'll search for information about ydiff and provide you with a comprehensive introduction.Question: What is a comprehensive introduction to ydiff from the GitHub repository yinwang0/ydiff?

Answer:

## Overview

ydiff is a structural comparison tool developed by Yin Wang primarily for Lisp family languages, with experimental support for C++ and JavaScript. Unlike traditional diff tools that perform line-by-line text comparisons, ydiff parses programs into abstract syntax trees (ASTs) to provide structural, language-aware comparisons.

## Key Features

### 1. Language-Aware Parsing
ydiff parses programs and understands basic language constructs, avoiding nonsensical comparisons such as comparing a string "10000" with an integer 10000 even though they appear similar. It attempts to match functions with the same name before comparing functions with different names.

### 2. Format Insensitive
The comparison results are not affected by differences in whitespace, line breaks, or indentation. For instance, ydiff will not produce a large diff simply because you surrounded a block of code with an if condition.

### 3. Moved Code Detection
ydiff can identify refactored code—whether it has been renamed, moved, reordered, wrapped, lifted, combined, or fragmented—regardless of how deep the changes are within the program structure.

### 4. Human-Friendly Output
The output is designed for human understanding, with an interactive UI that helps users navigate and understand changes efficiently. The left and right windows in the interface are always locked in their relative positions.

## Implementation Details

ydiff is implemented in Racket, a Scheme-based programming language. The tool was developed as part of Yin Wang's vision for structural programming, where programs would be stored directly as data structures rather than text, eliminating the need for parsing.

## Language Support

While ydiff originally aimed to support multiple languages, the developer found parsers tedious to implement and decided to focus primarily on the Lisp family. Current support includes:

- **Primary Support**: Lisp family languages (Scheme, Clojure, Emacs Lisp)
- **Experimental Support**: C++ and JavaScript
- **Separate Implementation**: Python (through a tool called "PyDiff")

The C++ parser was created as a demonstration of how a mostly-correct parser could be constructed within two days of work.

## Installation and Usage

### Building ydiff

To build the tool:

1. Navigate to the directory containing the source code
2. Run `make`
3. This compiles several executables such as diff-lisp, diff-cpp, and diff-js
4. Copy these executables to a directory in your PATH

### Running ydiff

Example usage:
```bash
diff-lisp demos/mk1.ss demos/mk2.ss
```

This produces an HTML file named "mk1-mk2.html" in the current directory. The HTML file requires support files nav.js and diff.css to be present in the same directory.

## Use Cases

ydiff is helpful for understanding code changes and may also be used for detecting plagiarism in programming classes or copyright infringement. For large-scale plagiarism detection, MOSS might be more suitable, but ydiff is fundamentally more accurate because it parses programs.

## Demonstrations

The project includes various demonstrations showing ydiff's capabilities:

- Comparing different versions of ydiff's own algorithm
- Comparing the original miniKanren with a modified version supporting a negation operator
- Comparing two versions (v20 and v23) of paredit-mode for Emacs
- Comparing different commits of Typed Clojure

## License

ydiff is free software licensed under the GNU General Public License version 3 or later.

References:

- [https://github.com/yinwang0/ydiff](https://github.com/yinwang0/ydiff)
- [https://yinwang0.wordpress.com/2012/01/03/ydiff/](https://yinwang0.wordpress.com/2012/01/03/ydiff/)
- [https://yinwang0.substack.com/p/ydiff](https://yinwang0.substack.com/p/ydiff)

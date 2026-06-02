---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Angular NGCC Ivy Compatibility Bridge
translated: false
type: note
---

**Question:** What does NGCC in Angular do?

**Answer:**

**NGCC** stands for **Angular Compatibility Compiler**.

It was a tool in Angular (mainly used from **Angular 9** to **Angular 15**) that helped applications using the new **Ivy** rendering engine consume older Angular libraries that were still compiled with the previous **View Engine** (the old rendering system before Ivy).

### What NGCC actually did

- When you installed an Angular library from npm that was published in **View Engine** format (common before ~2020–2021),
- NGCC would **automatically transform** that library's code into Ivy-compatible format **during your project's build** (or sometimes post-install via `node_modules` processing).
- This transformation happened by converting the library's metadata and rendering instructions so Ivy could understand and use them correctly.

Without NGCC, an Ivy-based application would fail to compile or run when depending on a non-Ivy (View Engine) library.

### Important historical context

- Angular 9 (2020) → Ivy became the **default** renderer, but NGCC was added for backward compatibility.
- Angular 12 → View Engine was removed from the framework itself (only libraries still needed NGCC).
- **Angular 16** (May 2023) → **NGCC was completely removed**.
  → View Engine libraries no longer work at all.
  → All libraries must now be published in Ivy format (most popular libraries have been updated since 2021–2022).

### Today (2026)

- If you're using **Angular 16 or newer**, you no longer see or need NGCC.
- If your build fails with messages about View Engine or missing NGCC → it means you're depending on a very old / unmaintained library that was never migrated to Ivy.
- Solution in such cases: update or replace the problematic dependency.

In short:
NGCC was a **temporary bridge** that allowed a smooth ecosystem transition from View Engine → Ivy between 2020–2023. It is now obsolete and has been removed since Angular 16.

**References:**

- [Angular Update Guide - v16](https://update.angular.dev/?v=15.0-16.0)
- [Angular Changelog](https://github.com/angular/angular/blob/main/CHANGELOG.md)
- [Blog: The Removal of Angular Compatibility Compiler (ngcc) in Angular 16](https://katsuba.dev/articles/the-removal-of-angular-compatibility-compiler-ngcc-in-angular-16)
- [Official Angular blog on library distribution improvements](https://blog.angular.dev/upcoming-improvements-to-angular-library-distribution-76c02f782aa4)

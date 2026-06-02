---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Angular Core Packages Explained Simply
translated: false
type: note
---

The Angular ecosystem has several key packages that work together. Here's how they relate:

**@angular/core** is the fundamental package that contains the core framework functionality - things like components, directives, dependency injection, change detection, and the component lifecycle. Every Angular app needs this.

**@angular/compiler** translates your Angular templates (the HTML with Angular-specific syntax) into JavaScript code that browsers can execute. This happens in two ways:
- Just-in-time (JIT): compilation happens in the browser at runtime
- Ahead-of-time (AOT): compilation happens during the build process (preferred for production)

**@angular/cli** (Angular CLI) is the command-line tool for development. It helps you create projects, generate components/services/modules, run the dev server, build for production, run tests, and more. When you run `ng serve` or `ng build`, you're using the CLI. It orchestrates the compiler and other build tools behind the scenes.

**@angular/compiler-cli** is the CLI's interface to the compiler, used during the build process for AOT compilation.

**Think of it this way:**
- `@angular/core` = the engine of your car
- `@angular/compiler` = translates your Angular code into something the browser understands
- `@angular/cli` = your toolbox and control panel for building and managing Angular apps
- `@angular/compiler-cli` = connects the CLI to the compiler for builds

There are also many other `@angular/*` packages like `@angular/common`, `@angular/router`, `@angular/forms`, etc. that provide additional functionality, but these three you asked about form the foundational build and runtime architecture.

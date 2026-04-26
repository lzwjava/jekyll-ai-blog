---
audio: false
generated: true
image: false
lang: en
layout: post
title: Exam Tools for C and C++ Programming
translated: false
type: note
---

Question:

Can Pintia ([https://pintia.cn/home](https://pintia.cn/home)) be used like GitHub/GCC environment for C/C++ exams, and can I use tools like GCC, g++, Dev-C++, or VSCode for my “计算机程序设计基础” practical exam at GDUFS?

Answer:

Yes, you’re basically describing a **standard C/C++ programming exam environment**, and your understanding is mostly correct—but there are a few important clarifications.

### 1. What Pintia actually is

PTA (Pintia) is an **online programming judging system** used by many universities in China.

It typically:

* Provides problem statements
* Lets you submit code (C / C++)
* Compiles and runs your code on server-side
* Checks output automatically

So it is **not GitHub** (no repo/version control), but more like:

> “Online judge + submission system (like LeetCode for exams)”

---

### 2. Compiler environment (GCC / g++)

Yes—your mental model is correct.

Most C/C++ exam systems (including PTA) ultimately compile your code using:

* **gcc (for C)**
* **g++ (for C++)**

So this is the real backend behavior:

* Your code → sent to server → compiled by GCC/G++ → tested

You don’t see the compiler directly, but it is there.

---

### 3. Local tools in exam room (Dev-C++ / VSCode)

In many university practical exams like “计算机程序设计基础”:

You may see:

* Dev-C++ (common in Chinese exams)
* Visual Studio Code (sometimes allowed)
* GCC/G++ installed locally

Your thinking is correct:

#### VSCode advantages

* Familiar editing experience
* Better indentation, search, copy/paste
* Easier debugging mentally
* Input method (Sogou Pinyin / 双拼) works smoothly

#### Dev-C++ advantages

* One-click compile & run
* Preconfigured compiler
* Less setup risk during exam

---

### 4. What usually matters in exams

In these exams, the key is NOT the tool—it is:

* Correct input/output format
* Correct algorithm logic
* Fast implementation under time pressure

So:

> VSCode is fine for editing, but make sure you can compile/run quickly in the exam environment.

---

### 5. Practical strategy (very important)

A good workflow for your situation:

#### Option A (safe exam approach)

* Use Dev-C++ to compile/run (zero setup risk)
* Use VSCode only if allowed and stable

#### Option B (your preference)

* Write in VSCode
* Compile using terminal:

```bash
g++ main.cpp -o main
./main
```

But only do this if:

* GCC is available
* You are confident under exam pressure

---

### 6. Input method (Sogou / 双拼)

Yes, totally fine.

Just be careful:

* Don’t accidentally switch input modes during exam
* Make sure punctuation is correct (very important in PTA)

---

### 7. Key insight

Your real advantage is not the IDE.

It is:

> “Can you translate problem → algorithm → correct code quickly under time constraints?”

Tools only help reduce friction.

---

If you want, I can also help you:

* Build a **Pintia exam survival template (C/C++)**
* Or give you **common exam problem patterns (100% scoring strategy)**
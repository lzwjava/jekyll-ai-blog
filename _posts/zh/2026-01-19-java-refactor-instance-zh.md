---
audio: false
generated: true
image: false
lang: zh
layout: post
model: google/gemini-3-flash-preview
title: 将 Java 静态成员重构为基于实例的成员
translated: true
type: note
---

Question: 如何重构这段 Java 代码以避免使用 static methods，并改为使用 `Main` class 的一个 instance？

Answer: 要将代码重构为基于 instance 的形式，你应该将 `BufferedReader` 和 `PrintWriter` 移动到 instance fields 中，并在 `main` method 内部通过创建 `Main` 的新 instance 来调用 `solve()` method。

以下是更新后的代码：

```java
package com.lzw.solutions.codeforces.p2190B1;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class Main {
    // 使用 instance fields 代替 static fields
    private final BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    private final PrintWriter out = new PrintWriter(System.out, true);

    // Instance method (没有 'static' 关键字)
    private void solve() throws IOException {
        String line = in.readLine();
        if (line == null) return;

        int t = Integer.parseInt(line.trim());
        while (t-- > 0) {
            int n = Integer.parseInt(in.readLine().trim());
            String s = in.readLine();
            // 在 production 中通常更倾向于使用标准的 if-check 或 logging 而非 assert，
            // 但根据你的逻辑暂时保留：
            assert (s.length() == n);
            out.println(s);
        }
    }

    public static void main(String[] args) {
        try {
            // 创建一个 instance 并调用 instance method
            new Main().run();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // 用于管理 instance 生命周期的 helper
    private void run() throws IOException {
        try {
            solve();
        } finally {
            out.close();
            in.close();
        }
    }
}

```

### Key Changes Made

* **移除了 `static`：** 字段 `in` 和 `out` 以及 method `solve()` 不再使用 `static` 修饰符。它们现在属于该 class 的特定 instance。
* **Object Instantiation：** 在 `main` method 中，使用 `new Main().run()` 从 static context 跳转到 instance context。
* **Resource Management：** 添加了一个带有 `finally` block 的 `run()` method，以确保即使在执行过程中发生 exception，`PrintWriter` 和 `BufferedReader` 也能被正确关闭。

需要我向你展示如何在这个基于 instance 的结构中实现一个更快的自定义 `Scanner` class 吗？

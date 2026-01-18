---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Java 简洁算法竞赛模板
translated: true
type: note
---

Question: 如何让我用于 competitive programming 的 Java 模板变得更整洁一些？

Answer:

这里有一些整洁且实用的改进建议，它们在保持你原始结构的同时，使代码更具可读性、可维护性，并带有一些现代感——且不涉及过于复杂的 ultra-fast input/output 领域。

### 整理后的版本（推荐的平衡方案）

```java
package com.lzw.solutions.sample.pjava_sample_buf;

import java.io.*;

public class Main {

    private final BufferedReader in;
    private final PrintWriter out;

    public Main() {
        in = new BufferedReader(new InputStreamReader(System.in));
        out = new PrintWriter(System.out, true); // 启用 auto-flush
    }

    // ─── Basic readers ────────────────────────────────────────────────

    private int readInt() throws IOException {
        return Integer.parseInt(in.readLine().trim());
    }

    private long readLong() throws IOException {
        return Long.parseLong(in.readLine().trim());
    }

    private String readLine() throws IOException {
        return in.readLine();
    }

    // ─── Core logic ───────────────────────────────────────────────────

    private void solve() throws IOException {
        // 解题逻辑写在这里
        // 例如：
        // int n = readInt();
        // out.println(n * 2);
    }

    // ─── Cleanup ──────────────────────────────────────────────────────

    private void close() throws IOException {
        in.close();
        out.close();
    }

    // ─── Entry point ──────────────────────────────────────────────────

    public static void main(String[] args) {
        try {
            Main main = new Main();
            main.solve();
            main.close();
        } catch (IOException e) {
            System.err.println("IO Error: " + e.getMessage());
            System.exit(1);
        }
    }
}
```

### 包含的主要整洁性改进：

- 字段定义为 `private final`（构造后不可变——良好的习惯）。
- 构造函数使用 `PrintWriter(..., true)` → 启用 **auto-flush**（减少手动调用 `flush()` 的次数）。
- 读取方法设为 `private`（封装性）。
- 在 `readInt`/`readLong` 中加入了 `trim()`（更好地处理意外的空格）。
- 增加了 `readLong()`，因为在 Java CP 中几乎总是需要它。
- `main` 方法使用 try-catch 而不是 `throws Exception`（调试时可以获得更清晰的 stack trace）。
- 统一命名：使用 `in` / `out` 而不是混合风格。
- 使用美观的分隔符添加了清晰的板块注释。
- 删除了不必要的 `if (in != null)` 检查（在这里 BufferedReader/PrintWriter 永远不会为 null）。

### 如果你偏好更简短，这里有一个更精简的版本：

```java
import java.io.*;

public class Main {
    private static final BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    private static final PrintWriter out = new PrintWriter(System.out, true);

    private static void solve() throws IOException {
        // 代码写在这里
    }

    public static void main(String[] args) throws IOException {
        solve();
        out.close();
    }
}
```

### 你可能会喜欢的可选整洁辅助方法（选 1–2 个即可）：

```java
// 快速读取数字（在整洁模板中非常常见）
private static int ni() throws IOException { return Integer.parseInt(in.readLine().trim()); }
private static long nl() throws IOException { return Long.parseLong(in.readLine().trim()); }

// 或者 one-liner 风格
private static int nextInt() throws IOException { return Integer.parseInt(in.readLine()); }

// 非常简洁的输出工具
private static void println(Object x) { out.println(x); }
private static void print(Object x)   { out.print(x);   }
```

选择任何让你感觉最自然的风格。

第一个版本（包含构造函数 + 独立的 readers + try-catch）可能是最整洁的，同时也非常接近你原有的代码结构。

References:

- 无（基于常见现代 Java CP 模式的风格/整洁度建议）
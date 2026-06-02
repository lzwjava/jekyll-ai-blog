---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Codeforces Java 中避免包声明
translated: true
type: note
---

**Question:** 如果我在向 Codeforces 提交 Java 解答时，在顶部包含类似 `package com.lzw.solutions.codeforces.p2190B1;` 的 package 声明会发生什么？这会导致 runtime error 吗？

**Answer:**

是的 —— **它会导致 compilation error**，而不是 runtime error。

Codeforces **不允许**在提交的 Java 解答中包含 package 声明。

当你提交以下代码开头的内容时：

```java
package com.lzw.solutions.codeforces.p2190B1;
```

Codeforces 编译器将拒绝它，并显示类似以下的信息：

- Compilation error
- 或者直接提示：**"package statement is not allowed"**
- 或者：**"class Main is public, should be declared in a file named Main.java"**

### 为什么会这样

Codeforces 以一种非常简单的方式编译你的 Java 代码：

- 他们将**你提交的全部代码**放入一个名为 `Main.java` 的文件中
- 使用以下命令编译：`javac Main.java`
- 然后运行：`java Main`

因此：

- 文件名是固定的 → `Main.java`
- public class **必须**命名为 `Main`
- **不允许使用 `package ...;` 语句**（因为这要求文件必须位于与包名匹配的文件夹中，例如 `com/lzw/solutions/codeforces/p2190B1/Main.java`）

### 正确版本（你应该提交的内容）

只需**删除 package 行**：

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class Main {

    private BufferedReader in;
    private PrintWriter out;

    public Main() {
        in = new BufferedReader(new InputStreamReader(System.in));
        out = new PrintWriter(System.out);
    }

    public static void main(String[] args) throws IOException {
        Main m = new Main();
        m.solve();
        m.close();
    }

    private void close() {
        out.flush();
        out.close();
    }

    private void solve() throws IOException {
        int t = Integer.parseInt(in.readLine());
        while (t-- > 0) {
            int n = Integer.parseInt(in.readLine());
            String s = in.readLine();
            // assert (s.length() == n);   ← 在实际提交中删除或注释掉
            out.println(s);
        }
    }
}
```

### 快速总结 —— Codeforces Java 提交注意事项

- 不要包含 `package ...;`
- Public class 必须命名为 `Main`
- 如果需要，请使用 fast input/output（你目前的模板没问题）
- 移除 `assert` 语句（如果在评测机中启用了 assertions，它们可能会抛出 Error）

祝你在 Codeforces 解题顺利！

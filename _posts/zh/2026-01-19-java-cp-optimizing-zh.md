---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 优化 Java 算法竞赛模板
translated: true
type: note
---

Question: 如何改进我的 Competitive Programming Java 模板？

Answer:

你目前的模板简洁明了，但它存在一些局限性，可能会导致在 **Codeforces**、**AtCoder** 或 **CodeChef** 等平台上出现 **TLE** (Time Limit Exceeded) —— 尤其是在处理大数据量输入（N ≤ 10⁶、多组测试用例或 1-2 秒的严苛时限）的问题时。

以下是最重要的改进建议，大致按影响程度排序：

### 1. Fast Input (Java 出现 TLE 的首要原因)

你目前的版本使用 `readLine()` **一次读取一行**。当输入包含 10⁵–10⁶ 个数字时，这种方式非常慢。

**推荐方案**（按从最快到最易用的顺序）：

**2024–2025 年最快且最常用** — BufferedReader + StringTokenizer (或自定义 FastScanner)

```java
import java.io.*;
import java.util.*;

public class Main {
    static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    static StringTokenizer st;

    static String next() throws IOException {
        while (st == null || !st.hasMoreTokens()) {
            st = new StringTokenizer(br.readLine());
        }
        return st.nextToken();
    }

    static int nextInt() throws IOException {
        return Integer.parseInt(next());
    }

    static long nextLong() throws IOException {
        return Long.parseLong(next());
    }

    static double nextDouble() throws IOException {
        return Double.parseDouble(next());
    }

    static String nextLine() throws IOException {
        return br.readLine();
    }

    // ────────────────────────────────────────

    static void solve() throws IOException {
        // 你的代码
    }

    public static void main(String[] args) throws IOException {
        // int t = nextInt();
        // while (t-- > 0) solve();

        solve();
        br.close();           // 良好的习惯
    }
}
```

甚至更好：许多 Codeforces 上的顶尖 Java 选手使用 **自定义 FastScanner** 类（带有字符缓冲区或直接读取字节），但上述版本通常足以应对 Div. 2 C–D 和许多 Div. 1 A–B 题目。

### 2. Fast Output

`PrintWriter` 已经不错了，但你可以让它更快：

- 选项 A：保留 `PrintWriter`（最方便）
- 选项 B：使用 `BufferedOutputStream` + 手动字节转换（更快，但代码较乱）
- 选项 C（流行的折中方案）：

```java
static PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));
```

然后务必记得调用 `out.flush()` 或让 `close()` 来执行。

现在很多人这样做：

```java
static final PrintWriter out = new PrintWriter(System.out);
```

并接受那点微小的开销 —— 通常都能通过测试。

### 3. 多组测试用例支持 (非常常见的模式)

在 `main` 函数中添加以下内容：

```java
int t = nextInt();
while (t-- > 0) {
    solve();
}
```

或者更好 —— 仅在题目有多个测试用例时读取 `t`（现在很多题目使用单次测试 + 第一行为 n 的形式）。

### 4. 其他强烈推荐的补充

添加这些辅助方法（你会经常用到它们）：

```java
static long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }
static long lcm(long a, long b) { return a / gcd(a, b) * b; }   // 注意溢出

static boolean isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return false;
    return true;
}

// 在对 Pair / 对象排序时非常有用
static class Pair implements Comparable<Pair> {
    long first; int second;
    Pair(long f, int s) { first = f; second = s; }
    public int compareTo(Pair o) {
        if (first != o.first) return Long.compare(first, o.first);
        return Integer.compare(second, o.second);
    }
}
```

### 5. 现代且整洁的风格 (2025 年流行)

许多高分 Java 选手使用的实用强力模板：

```java
import java.io.*;
import java.util.*;

public class Main {
    static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    static StringTokenizer st;
    static PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));

    static String next() throws IOException {
        while (st == null || !st.hasMoreTokens())
            st = new StringTokenizer(br.readLine());
        return st.nextToken();
    }

    static int ni() throws IOException { return Integer.parseInt(next()); }
    static long nl() throws IOException { return Long.parseLong(next()); }
    static double nd() throws IOException { return Double.parseDouble(next()); }

    static void solve() throws IOException {
        // ───── 你的代码 ─────
        out.println("answer");
    }

    public static void main(String[] args) throws IOException {
        // int t = ni();
        // while (t-- > 0) solve();
        solve();
        out.flush();
        // out.close();   // 如果你信任 flush 则可选
    }
}
```

### 快速清单 – 根据你的水平添加内容

- 初学者 → 只需添加 StringTokenizer + nextInt() / nextLong()
- 中级 → 添加 PrintWriter 配合 BufferedOutputStream + 多组测试支持
- 进阶 → 自定义 FastScanner (逐字节处理)，必要时使用 BigInteger，带有本地文件输入的 debug 模式

你目前的模板是一个很好的精简基础 —— 只需升级输入读取方式，你就能避免 Java 中 70–80% 的 TLE 问题。

祝你好运，继续努力！

参考资料：

- [Fast data input-output for competitive programming in Java 11](https://codeforces.com/blog/entry/97203)
- [Java Template for Competitive Coding](https://codeforces.com/blog/entry/77287)
- [Java Template / Snippet for Competitive Programming](https://codeforces.com/blog/entry/144375)

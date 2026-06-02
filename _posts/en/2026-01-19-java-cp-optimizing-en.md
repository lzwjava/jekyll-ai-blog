---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Optimizing Java Competitive Programming Templates
translated: false
type: note
---

Question: How can my competitive programming Java template be improved?

Answer:

Your current template is clean and simple, but it has several limitations that can cause **TLE** (Time Limit Exceeded) on platforms like **Codeforces**, **AtCoder**, or **CodeChef** — especially on problems with large input (N ≤ 10⁶, many test cases, or tight time limits ~1–2 seconds).

Here are the most important improvements, roughly ordered by impact:

### 1. Fast Input (the #1 reason Java gets TLE)

Your current version reads **one line at a time** with `readLine()`. This is very slow when the input has 10⁵–10⁶ numbers.

**Recommended approaches** (from fastest to easiest):

**Fastest & most used in 2024–2025** — BufferedReader + StringTokenizer (or custom FastScanner)

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
        // your code here
    }

    public static void main(String[] args) throws IOException {
        // int t = nextInt();
        // while (t-- > 0) solve();

        solve();
        br.close();           // good habit
    }
}
```

Even better: many top Java users on Codeforces use a **custom FastScanner** class (with char buffer or direct byte reading), but the above version is usually enough for Div. 2 C–D and many Div. 1 A–B.

### 2. Fast Output

`PrintWriter` is already good, but you can make it faster:

- Option A: Keep `PrintWriter` (most convenient)
- Option B: Use `BufferedOutputStream` + manual byte conversion (faster, but ugly)
- Option C (popular compromise):

```java
static PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));
```

Then always remember to call `out.flush()` or let `close()` do it.

Many people now do:

```java
static final PrintWriter out = new PrintWriter(System.out);
```

and accept the small overhead — it usually passes.

### 3. Multiple test cases support (very common pattern)

Add this in `main`:

```java
int t = nextInt();
while (t-- > 0) {
    solve();
}
```

Or even better — read t only if the problem has multiple tests (many problems now use single test + first line = n or something).

### 4. Other highly recommended additions

Add these helper methods (you'll use them very often):

```java
static long gcd(long a, long b) { return b == 0 ? a : gcd(b, a % b); }
static long lcm(long a, long b) { return a / gcd(a, b) * b; }   // be careful with overflow

static boolean isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return false;
    return true;
}

// Very useful for sorting pairs / objects
static class Pair implements Comparable<Pair> {
    long first; int second;
    Pair(long f, int s) { first = f; second = s; }
    public int compareTo(Pair o) {
        if (first != o.first) return Long.compare(first, o.first);
        return Integer.compare(second, o.second);
    }
}
```

### 5. Modern & clean style (popular in 2025)

A realistic strong template used by many high-rated Java coders:

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
        // ───── your code ─────
        out.println("answer");
    }

    public static void main(String[] args) throws IOException {
        // int t = ni();
        // while (t-- > 0) solve();
        solve();
        out.flush();
        // out.close();   // optional if you trust flush
    }
}
```

### Quick checklist – what to add depending on your level

- Beginner → just add StringTokenizer + nextInt() / nextLong()
- Intermediate → add PrintWriter with BufferedOutputStream + multiple test support
- Advanced → custom FastScanner (byte by byte), BigInteger when needed, debug mode with local file input

Your current template is a good minimal base — just upgrade the input reading and you'll avoid 70–80% of TLEs in Java.

Good luck & keep practicing!

References:

- [Fast data input-output for competitive programming in Java 11](https://codeforces.com/blog/entry/97203)
- [Java Template for Competitive Coding](https://codeforces.com/blog/entry/77287)
- [Java Template / Snippet for Competitive Programming](https://codeforces.com/blog/entry/144375)

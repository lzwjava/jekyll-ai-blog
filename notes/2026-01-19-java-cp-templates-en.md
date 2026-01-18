---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Clean Java Competitive Programming Templates
translated: false
type: note
---

Question: How can I make my competitive programming Java template a bit cleaner?

Answer: 

Here are several clean, practical improvements that keep your original structure while making the code more readable, maintainable, and slightly more modern — without going into ultra-fast input/output territory.

### Cleaned-up version (recommended balance)

```java
package com.lzw.solutions.sample.pjava_sample_buf;

import java.io.*;

public class Main {

    private final BufferedReader in;
    private final PrintWriter out;

    public Main() {
        in = new BufferedReader(new InputStreamReader(System.in));
        out = new PrintWriter(System.out, true); // auto-flush enabled
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
        // Your solution goes here
        // Example:
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

### Main cleanliness improvements included

- Fields are `private final` (immutable after construction — good habit)
- Constructor uses `PrintWriter(..., true)` → enables **auto-flush** (less manual `flush()` calls)
- Reader methods are `private` (encapsulation)
- Added `trim()` to `readInt`/`readLong` (handles accidental spaces better)
- Added `readLong()` because you almost always need it
- `main` method uses try-catch instead of `throws Exception` (cleaner stack trace for debugging)
- Consistent naming: `in` / `out` instead of mixing styles
- Clear section comments with nice-looking separators
- No unnecessary `if (in != null)` checks (BufferedReader/PrintWriter are never null here)

### Even smaller / more minimal clean version (if you prefer brevity)

```java
import java.io.*;

public class Main {
    private static final BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    private static final PrintWriter out = new PrintWriter(System.out, true);

    private static void solve() throws IOException {
        // your code here
    }

    public static void main(String[] args) throws IOException {
        solve();
        out.close();
    }
}
```

### Optional clean additions you might like (pick 1–2)

```java
// Quick number readers (very common in clean templates)
private static int ni() throws IOException { return Integer.parseInt(in.readLine().trim()); }
private static long nl() throws IOException { return Long.parseLong(in.readLine().trim()); }

// Or one-liner style
private static int nextInt() throws IOException { return Integer.parseInt(in.readLine()); }

// Very clean output helpers
private static void println(Object x) { out.println(x); }
private static void print(Object x)   { out.print(x);   }
```

Pick whichever style feels most natural to you.

The first version (with constructor + separate readers + try-catch) is probably the cleanest while still being very close to your original code.

References:  

- None (style/cleanliness suggestions based on common modern Java CP patterns)
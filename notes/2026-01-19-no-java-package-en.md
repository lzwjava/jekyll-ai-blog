---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Avoid Package Declarations in Codeforces Java
translated: false
type: note
---

**Question:** What happens if I include a package declaration like `package com.lzw.solutions.codeforces.p2190B1;` at the top when submitting a Java solution to Codeforces? Will it cause a runtime error?

**Answer:**

Yes — **it will cause a compilation error**, not a runtime error.

Codeforces **does not allow** package declarations in submitted Java solutions.

When you submit code that starts with:

```java
package com.lzw.solutions.codeforces.p2190B1;
```

Codeforces compiler will reject it with a message similar to:

- Compilation error
- or sometimes directly: **"package statement is not allowed"**
- or: **"class Main is public, should be declared in a file named Main.java"**

### Why this happens

Codeforces compiles your Java code in a very simple way:

- They put **your entire submitted code** into a file named `Main.java`
- They compile it with: `javac Main.java`
- Then run: `java Main`

Because of this:

- The file name is fixed → `Main.java`
- The public class **must** be named `Main`
- **No `package ...;` statement is allowed** (because that would require the file to be inside a folder matching the package name, e.g. `com/lzw/solutions/codeforces/p2190B1/Main.java`)

### Correct version (what you should submit)

Just **remove the package line**:

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
            // assert (s.length() == n);   ← remove or comment out in real submission
            out.println(s);
        }
    }
}
```

### Quick summary — what to remember for Codeforces Java submissions

- No `package ...;`
- Public class must be named `Main`
- Use fast input/output if needed (your current template is fine)
- Remove `assert` statements (they may throw Error in some judges if assertions are enabled)

Good luck with your Codeforces problems!

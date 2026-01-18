---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-flash-preview
title: Refactoring Java Static to Instance Based
translated: false
type: note
---

Question: How can I refactor this Java code to avoid using static methods and instead use an instance of the `Main` class?

Answer: To refactor your code to be instance-based, you should move the `BufferedReader` and `PrintWriter` into instance fields and call the `solve()` method on a new instance of `Main` created inside the `main` method.

Here is the updated code:

```java
package com.lzw.solutions.codeforces.p2190B1;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class Main {
    // Instance fields instead of static fields
    private final BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
    private final PrintWriter out = new PrintWriter(System.out, true);

    // Instance method (no 'static' keyword)
    private void solve() throws IOException {
        String line = in.readLine();
        if (line == null) return;
        
        int t = Integer.parseInt(line.trim());
        while (t-- > 0) {
            int n = Integer.parseInt(in.readLine().trim());
            String s = in.readLine();
            // Using standard if-check or logging is often preferred over assert 
            // in production, but keeping it per your logic:
            assert (s.length() == n);
            out.println(s);
        }
    }

    public static void main(String[] args) {
        try {
            // Create an instance and call the instance method
            new Main().run();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Helper to manage the lifecycle of the instance
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

### Key Changes Made:

* **Removed `static`:** The fields `in` and `out` and the method `solve()` no longer use the `static` modifier. They now belong to a specific instance of the class.
* **Object Instantiation:** In the `main` method, `new Main().run()` is used to jump from the static context into the instance context.
* **Resource Management:** Added a `run()` method with a `finally` block to ensure that your `PrintWriter` and `BufferedReader` are closed properly, even if an exception occurs during execution.

Would you like me to show you how to implement a faster custom `Scanner` class within this instance-based structure?
---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: IntelliJ Redirect Input Using Macros Title
translated: false
type: note
---

**Question:** In IntelliJ IDEA, how can I redirect input from `resources/p2190A/1.in` for the class `com.lzw.solutions.codeforces.p2190A.Main`, and use a macro/variable so that `p2190A` becomes easy to change (reusable for other problems)?

**Answer:**

Here are the most practical & commonly used ways in 2025–2026 among competitive programmers using IntelliJ:

### Recommended Solution 1: Run Configuration + $Prompt$ macro (most flexible)

1. Create / edit Run Configuration for your Main class
2. In **Program arguments** (or **VM options** — both work), write:

```text
$Prompt$
```

3. In **Working directory**, use one of these styles:

   Style A (recommended):

   ```
   $MODULE_DIR$/src/main/resources
   ```

   Style B (if you like problem-code folders):

   ```
   $MODULE_DIR$/src/main/resources/$Prompt$
   ```

4. Every time you run (Shift+F10), IntelliJ will ask you:

   What to input?

   You just type:  `p2190A`  →  Enter

   → it will read from `resources/p2190A/1.in`

### Recommended Solution 2: Use File Template + Live Template (semi-automatic)

Create a **live template** (Settings → Editor → Live Templates):

Abbreviation: `cf`

```text
-Dfile.input=$MODULE_DIR$/src/main/resources/$problemCode$/$fileName$.in

// press Tab to jump between variables
```

Then in **VM options** field of run configuration write:

```
cf
```

and press Tab → type problem folder name → Tab → type filename (usually `1`)

### Quick & Dirty Solution 3: Hardcode but with easy replace

VM options:

```
-Dfile.input=$MODULE_DIR$/src/main/resources/p2190A/1.in
```

When you want to change problem →
press **Ctrl+Shift+R** → **Replace in File** → replace `p2190A` → very fast

### Most Popular Modern Way (2025+) — Solution 4: One run config per contest + folder macro

Many people now do:

Run configuration name:    Codeforces Round 952 (Div. 4)

Program arguments:

```
$Prompt$
```

Working directory:

```
$MODULE_DIR$
```

And in main you do something like:

```java
public static void main(String[] args) throws Exception {
    String folder = args.length > 0 ? args[0] : "p2190A";
    String file   = args.length > 1 ? args[1] : "1";

    System.setIn(new FileInputStream(
        "src/main/resources/" + folder + "/" + file + ".in"
    ));
    // or use Paths.get(...) if you prefer
    ...
}
```

Then you run → type `p2190A` → Enter

Very clean and reusable.

### Summary – choose one

| Method                     | Flexibility | Typing effort | Recommended for |
|----------------------------|-------------|---------------|------------------|
| $Prompt$ in args           | ★★★★★       | low           | most people      |
| $Prompt$ in working dir    | ★★★★        | very low      | folder structure |
| Live Template + VM options | ★★★★        | medium        | power users      |
| args[0] = folder name      | ★★★★★       | low           | long-term        |
| Just replace string        | ★★          | high          | quick & dirty    |

Most Codeforces/AtCoder users in IntelliJ nowadays use **method 1** or **method 4**.

Good luck & fast AC!

**References:**

- None required for this answer (IntelliJ macros behavior is standard across recent versions)

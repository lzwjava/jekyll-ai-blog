---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: VS Code Java Input Redirection Guide
translated: false
type: note
---

**Question:** How to configure input redirection for a Java program in VS Code launch.json (e.g. redirect from file like 1.in)?

**Answer:**

In VS Code's `launch.json` for Java, there are several correct ways to redirect standard input (`System.in`) from a file. Here are the most commonly used and reliable methods in 2025:

### Recommended Method 1 – Using `args` with `<` redirection (most popular)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "java",
            "name": "Current File (with input redirect)",
            "request": "launch",
            "mainClass": "${file}",
            "args": "< \"${workspaceFolder}/src/main/resources/uva/${problem}/1.in\"",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

**Note:** Use **double quotes** around the path if it contains spaces.
This is the most widely used method in competitive programming communities.

### Method 2 – Using `redirector` (old style – still works in many setups)

```json
{
    "type": "java",
    "name": "Current File with input file",
    "request": "launch",
    "mainClass": "${file}",
    "redirector": {
        "input": "${workspaceFolder}/src/main/resources/uva/${problem}/1.in"
    }
}
```

**Important:**
This format only works if your Java extension supports the `redirector` attribute (older versions did, newer ones sometimes ignore it or require different syntax).

### Method 3 – Cleanest & most reliable in recent VS Code + Java Extension (2024–2026)

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "java",
            "name": "Launch with input redirection",
            "request": "launch",
            "mainClass": "${file}",
            "args": [
                "<",
                "${workspaceFolder}/src/main/resources/uva/${problem}/1.in"
            ],
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

This format avoids shell quoting issues on Windows/macOS/Linux.

### Bonus: Dynamic problem name using input prompt

```json
{
    "type": "java",
    "name": "UVa - Ask problem number",
    "request": "launch",
    "mainClass": "${file}",
    "args": "< \"${workspaceFolder}/src/main/resources/uva/${input:problemNumber}/1.in\"",
    "inputs": [
        {
            "id": "problemNumber",
            "type": "promptString",
            "description": "Enter UVa problem number (e.g. 100, 101, 10410)",
            "default": "100"
        }
    ]
}
```

### Quick summary – what to use in 2025/2026

| Method                             | Reliability | Windows | macOS/Linux | Recommended? |
|------------------------------------|-------------|---------|-------------|--------------|
| `args: "< \"path\""`               | ★★★★★       | Yes     | Yes         | Yes (most popular) |
| `args: ["<", "path"]`              | ★★★★☆       | Yes     | Yes         | Yes (clean) |
| `redirector: { "input": "..." }`   | ★★☆☆☆       | partial | partial     | Avoid if possible |
| `console": "externalTerminal"` + manual < | ★★★☆☆    | Yes     | Yes         | Fallback |

**Most people today just use:**

```json
"args": "< \"${workspaceFolder}/src/main/resources/uva/${problem}/1.in\""
```

Good luck with UVa / competitive programming!

**References:**

- None needed for this configuration question (common VS Code Java setup pattern)

---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: VS Code Java 输入重定向指南
translated: true
type: note
---

**Question:** 如何在 VS Code 的 launch.json 中为 Java 程序配置输入重定向（例如从 1.in 文件重定向）？

**Answer:**

在 VS Code 的 Java `launch.json` 中，有几种正确的方法可以将标准输入 (`System.in`) 从文件重定向。以下是 2025 年最常用且可靠的方法：

### 推荐方法 1 – 使用带有 `<` 重定向符号的 `args`（最流行）

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

**注意：** 如果路径包含空格，请在路径周围使用 **双引号**。
这是算法竞赛（Competitive Programming）社区中使用最广泛的方法。

### 方法 2 – 使用 `redirector`（旧式 – 在许多配置中仍然有效）

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

**重要提示：**
此格式仅在你的 Java extension 支持 `redirector` 属性时有效（旧版本支持，新版本有时会忽略它或需要不同的语法）。

### 方法 3 – 在最新的 VS Code + Java Extension (2024–2026) 中最整洁且可靠的方法

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

这种格式可以避免 Windows/macOS/Linux 上的 shell 引用（quoting）问题。

### 额外技巧：使用输入提示动态获取题目名称

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

### 快速总结 – 2025/2026 年该使用哪种方案

| Method | Reliability | Windows | macOS/Linux | Recommended? |
| :--- | :--- | :--- | :--- | :--- |
| `args: "< \"path\""` | ★★★★★ | Yes | Yes | Yes (most popular) |
| `args: ["<", "path"]` | ★★★★☆ | Yes | Yes | Yes (clean) |
| `redirector: { "input": "..." }` | ★★☆☆☆ | partial | partial | Avoid if possible |
| `console": "externalTerminal"` + manual < | ★★★☆☆ | Yes | Yes | Fallback |

**现在大多数人只需使用：**

```json
"args": "< \"${workspaceFolder}/src/main/resources/uva/${problem}/1.in\""
```

祝你在 UVa / 算法竞赛中取得好成绩！

**References:**

- 此配置问题不需要额外参考资料（属于 VS Code Java 设置的常见模式）
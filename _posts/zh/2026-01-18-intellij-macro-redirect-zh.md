---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用宏重定向 IntelliJ 输入标题
translated: true
type: note
---

**Question:** 在 IntelliJ IDEA 中，如何为类 `com.lzw.solutions.codeforces.p2190A.Main` 重定向来自 `resources/p2190A/1.in` 的输入，并使用宏/变量使得 `p2190A` 易于更改（以便在其他题目中复用）？

**Answer:**

以下是 2025–2026 年间在 IntelliJ 中进行 competitive programming 的程序员最实用且常用的方法：

### 推荐方案 1：Run Configuration + $Prompt$ 宏（最灵活）

1. 为你的 Main 类创建/编辑 Run Configuration
2. 在 **Program arguments**（或 **VM options** —— 两者皆可）中输入：

```text
$Prompt$
```

3. 在 **Working directory** 中，使用以下风格之一：

   风格 A（推荐）：

   ```
   $MODULE_DIR$/src/main/resources
   ```

   风格 B（如果你喜欢针对题号的文件夹结构）：

   ```
   $MODULE_DIR$/src/main/resources/$Prompt$
   ```

4. 每次运行（Shift+F10）时，IntelliJ 都会弹出对话框询问：

   What to input?

   你只需输入：`p2190A` → Enter

   → 它将从 `resources/p2190A/1.in` 中读取

### 推荐方案 2：使用 File Template + Live Template（半自动）

创建一个 **live template** (Settings → Editor → Live Templates):

Abbreviation: `cf`

```text
-Dfile.input=$MODULE_DIR$/src/main/resources/$problemCode$/$fileName$.in

// 按 Tab 在变量间跳转
```

然后在 run configuration 的 **VM options** 字段中输入：

```
cf
```

并按 Tab → 输入题目文件夹名称 → Tab → 输入文件名（通常是 `1`）

### 快速省事方案 3：硬编码但易于替换

VM options:

```
-Dfile.input=$MODULE_DIR$/src/main/resources/p2190A/1.in
```

当你想要更改题目时 →
按 **Ctrl+Shift+R** → **Replace in File** → 替换 `p2190A` → 速度非常快

### 2025+ 最流行的现代方式 —— 方案 4：每个 contest 一个 run config + folder 宏

现在很多人这样做：

Run configuration name: Codeforces Round 952 (Div. 4)

Program arguments:

```
$Prompt$
```

Working directory:

```
$MODULE_DIR$
```

在 main 函数中，你可以这样写：

```java
public static void main(String[] args) throws Exception {
    String folder = args.length > 0 ? args[0] : "p2190A";
    String file   = args.length > 1 ? args[1] : "1";

    System.setIn(new FileInputStream(
        "src/main/resources/" + folder + "/" + file + ".in"
    ));
    // 或者如果你更喜欢使用 Paths.get(...)
    ...
}
```

然后运行 → 输入 `p2190A` → Enter

非常整洁且可复用。

### 总结 – 选择其一

| 方法 | 灵活性 | 输入工作量 | 推荐人群 |
|----------------------------|-------------|---------------|------------------|
| args 中的 $Prompt$ | ★★★★★ | 低 | 大多数人 |
| working dir 中的 $Prompt$ | ★★★★ | 极低 | 固定文件夹结构 |
| Live Template + VM options | ★★★★ | 中等 | 高级用户 |
| args[0] = folder name | ★★★★★ | 低 | 长期方案 |
| 直接替换字符串 | ★★ | 高 | 临时方案 |

如今在 IntelliJ 中大多数 Codeforces/AtCoder 用户使用 **方法 1** 或 **方法 4**。

祝你好运，快速 AC！

**References:**

- 此答案不需要特定引用（IntelliJ 宏的行为在最近的版本中是标准的）

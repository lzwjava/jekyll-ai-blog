---
audio: false
generated: true
lang: zh
layout: post
title: 修复Jekyll的YAML与文件错误
translated: true
type: note
---

输出信息显示存在两类错误：

1.  **YAML 异常**：这表明您 Markdown 文件中的 Front Matter（文件顶部的 YAML 块）存在问题：
      * `/Users/lzwjava/projects/lzwjava.github.io/notes/2025-06-25-company-valuation-comparison-en.md`
      * `/Users/lzwjava/projects/lzwjava.github.io/notes/2025-06-25-top-companies-evolve-en.md`
        错误信息 "在解析块映射时，第 2 行第 1 列未找到预期的键" 表明这些文件中的 YAML 语法不正确，很可能是 Front Matter 中缺少某个键或存在缩进问题。

2.  **`Errno::ENOENT: No such file or directory @ rb_sysopen - /Users/lzwjava/projects/lzwjava.github.io/wandb/debug-internal.log`**：此错误表明 Jekyll 正尝试访问一个不存在的文件或目录，具体是 `/wandb/debug-internal.log`。这可能是一个临时文件，或是 Jekyll 尝试处理的来自其他工具（如 Weights & Biases - `wandb`）的依赖文件。

关于如何让 Jekyll 忽略某些目录，您可以在 `_config.yml` 文件中使用 `exclude` 配置选项。

具体操作如下：

1.  **打开您的 `_config.yml` 文件**（位于 Jekyll 项目的根目录）。

2.  **添加或修改 `exclude` 指令。** 此指令接受一个路径（文件或目录）数组，Jekyll 在构建过程中将忽略这些路径。

    例如，要忽略 `wandb` 目录以及任何其他您想排除的目录，请在 `_config.yml` 中添加以下内容：

    ```yaml
    exclude:
      - wandb/
      - some_other_directory/
      - another_file_to_ignore.md
    ```

    **重要提示：**

      * 对于目录，请确保包含尾部斜杠 (`/`)，以保证其内的所有内容都被忽略。
      * 路径是相对于您 Jekyll 项目的根目录。

**针对您的具体错误使用 `exclude`：**

  * **针对 `wandb` 目录错误：** 在 `_config.yml` 的 `exclude` 列表中添加 `wandb/` 应能阻止 Jekyll 尝试读取其中的文件，从而解决 `wandb/debug-internal.log` 的 `No such file or directory` 错误。

  * **针对 YAML 异常：** `exclude` 指令无法修复您 Markdown 文件中的 YAML 错误。您需要**手动更正** `notes/2025-06-25-company-valuation-comparison-en.md` 和 `notes/2025-06-25-top-companies-evolve-en.md` 文件中的 Front Matter。

    **典型的 Jekyll Front Matter 结构：**

    ```yaml
    ---
    layout: post
    title: "我的精彩文章"
    date: 2025-07-02 10:00:00 +0800
    categories: [notes, tech]
    tags: [jekyll, markdown]
    ---

    您的内容从这里开始。
    ```

    请仔细检查 YAML 异常中提到的文件，确保它们遵循此结构，尤其注意缩进和正确的键值对。错误信息 "在解析块映射时，第 2 行第 1 列未找到预期的键" 表明您的 Front Matter 开头部分存在问题，可能是缺少键或在应有键的位置存在多余空格。

在对 `_config.yml` 进行这些更改并修正您的 Markdown 文件后，请再次尝试运行 Jekyll 构建或服务命令。

---
audio: false
generated: true
lang: zh
layout: post
title: 在Zed中启用软换行
translated: true
type: note
---

与许多现代文本编辑器一样，Zed 采用“软换行”的概念来实现行包裹。这意味着文本行会在编辑器中显示为换行，但不会在文件中实际插入换行符。

以下是在 Zed 中启用行包裹的方法：

1.  **打开 Zed 设置：**

      * 按下 `Command + Shift + P`（macOS）或 `Ctrl + Shift + P`（Windows/Linux）打开命令面板。
      * 输入 "local" 并选择 "zed: Open Local Settings"。这将打开您的 `settings.json` 文件。

2.  **添加 `soft_wrap` 设置：**

      * 在 `settings.json` 文件中，添加或修改 `"soft_wrap"` 设置。您有几个选项：

          * **`"editor_width"`：** 这是最常见且通常推荐的选项。它会根据当前编辑器窗口的宽度进行换行。
            ```json
            {
              "soft_wrap": "editor_width"
            }
            ```
          * **`"preferred_line_length"`：** 这将根据指定的 `preferred_line_length`（例如 80 个字符）进行换行。您还需要定义 `preferred_line_length`。
            ```json
            {
              "soft_wrap": "preferred_line_length",
              "preferred_line_length": 80
            }
            ```
          * **`"bounded"`：** 此选项提供更高级的换行行为，但对于大多数用户而言，`editor_width` 或 `preferred_line_length` 通常已足够。
          * **`"none"`：** 此选项禁用行包裹。

3.  **保存文件：**

      * 按下 `Command + S`（macOS）或 `Ctrl + S`（Windows/Linux）保存 `settings.json` 文件。

Zed 现在会根据您选择的设置进行行包裹。

**重要提示：**

  * **项目级设置：** 您也可以在项目级别启用自动换行，方法是在项目目录中创建一个 `.zed` 文件夹，并在其中放置一个包含所需 `soft_wrap` 配置的 `settings.json` 文件。这将覆盖您在该特定项目的全局设置。
  * **语言特定设置：** 您甚至可以针对特定语言配置 `soft_wrap`。例如，要为 Markdown 文件设置软换行：
    ```json
    {
      "languages": {
        "Markdown": {
          "soft_wrap": "editor_width"
        }
      }
    }
    ```
  * **“Rewrap”命令：** 如果您在寻找“硬换行”文本（实际插入换行符）而非仅视觉包裹的命令，Zed 也提供了一个“Rewrap”命令（通常绑定到 `Alt-Q` 或 `Alt-W`）。这对于格式化注释或长文本行非常有用。

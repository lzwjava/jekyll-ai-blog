---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Notes子命令仍使用--input-dir
translated: true
type: note
---

以下是对 Markdown 文本的简体中文翻译：

=== 对话子命令：`--input-dir` 与位置参数 file 的对比 ===

提交 7f3f368 将 `ww conversation generate` 从 `--input-dir`（批量处理目录中所有 JSON 文件）更改为位置参数 `file`（单个文件）。以下是所有 5 个子命令的状态：

1. json     (json.py)     - 位置参数 `filename`  ✅ 无 `--input-dir`
2. generate (generate.py) - 位置参数 `file`      ✅ 已在 7f3f368 中修复
3. notes    (notes.py)    - 仍使用 `--input-dir`  ⚠️ 见下文
4. to-video (video.py)    - 位置参数 file (sys.argv)  ✅ 无 `--input-dir`
5. to-image (image.py)    - 位置参数 file (sys.argv)  ✅ 无 `--input-dir`

=== 只有 `notes` 仍在使用 `--input-dir` ===

notes.py 第 78-82 行：
    parser.add_argument("--input-dir", default="scripts/conversation", ...)

但这可以说是有意为之——`notes` 会遍历目录中所有 .json 文件，并将每个文件转换为 markdown 笔记。这是一个天生为批量处理设计的命令。

然而，如果你希望与 `generate` 保持一致（使用单个文件参数），它可以重构为接受单个文件或目录。`generate` 命令在 7f3f368 之前也具有“处理目录中所有文件”的批量模式，但你去掉了它。

=== video.py 有一个名为 `input_dir` 的局部变量，但它不是 CLI 标志 ===

video.py 第 139 行：`input_dir = os.path.dirname(input_path) or "."`
这只是从位置参数 file 中提取父目录。没有 `--input-dir` 标志。✅ 没问题。

=== 总结 ===

目前只有 `ww conversation notes` 使用了 `--input-dir` 模式。其他子命令都使用位置参数 file。需要我重构 `notes` 以使其匹配——即接受单个文件或目录作为位置参数吗？
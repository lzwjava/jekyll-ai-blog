---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练可见，输出缓冲
translated: true
type: note
---

IMPORTANT: 翻译 markdown 内容时，请确保格式正确：
- 在标题（以 # 开头的行）和表格（以 | 开头的行）之间始终添加空行
- 保持正确的 markdown 表格结构
- 保留所有原始格式和间距，除非格式规则要求更改
- 不要将整个翻译包裹在 markdown 代码块（```markdown 或 ```）中——内容将直接用于 Jekyll 与 Kramdown

TRANSLATION RULES:
- 如果不确定，不要翻译特定项目名称、公司名称或学校名称
- 对于技术术语、新词和技术概念，保留英文而非翻译
- 对于中文翻译：专有名词和技术术语使用英文而非中文音译
- 对于日语翻译：在适当情况下使用英文技术术语而非 romaji 或 katakana
- 对于所有语言：优先使用英文表示现代技术词汇、编程术语和品牌名称

找到了。训练确实在运行——检查点文件（1.49GB，更新于22:41）证明了这一点。但日志卡住了，原因是 **Python stdout buffering**。

当 Python 的 stdout 通过 `tee` 管道输出时，它不再是 TTY，因此 Python 会完全缓冲输出而不是行缓冲。`train.py` 中的 `print()` 调用停留在管道缓冲区中，从未刷新到 `/tmp/train.log`。

日志文件的最后修改时间是 21:16（只有初始警告）。该进程正在通过管道输出（`fd/1 -> pipe`），确认了缓冲问题。

**训练正常，只是输出不可见。** 要解决未来运行的问题，可以：
- 在启动命令中设置 `PYTHONUNBUFFERED=1`
- 或者添加 `-u` 标志：`python3 -u train.py ...`

检查点 `out-github-code-124m/ckpt.pt`（1.49GB）刚刚保存，因此训练正在进行。你只是在损失/指标上盲目飞行。要我终止并重新启用无缓冲输出，还是让它完成并检查检查点统计信息？
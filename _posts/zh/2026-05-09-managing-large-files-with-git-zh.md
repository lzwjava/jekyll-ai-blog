---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Git管理大文件
translated: true
type: note
---

问题：对于大于500MB的文件（如MP4录制文件和Whisper输出），我应该如何使用Git管理它们？是否只能忽略它们？

回答：

对于像你这样的媒体/转录工作流，通常的做法是：

* Git 管理：
  * 源代码
  * 脚本
  * 配置文件
  * 提示词
  * 小型元数据
  * 文档

* Git 忽略：
  * 大型视频
  * 生成的输出
  * 缓存
  * 日志
  * 临时产物

所以是的——通常 Whisper 生成的 `.mp4`、`.srt`、`.vtt`、`.json`、`.txt` 应该大部分被忽略。

一个清晰的结构例如：

```text
whisper-test/
├── src/
├── scripts/
├── prompts/
├── data/
│   ├── raw/
│   └── processed/
├── outputs/
├── logs/
├── .gitignore
└── README.md
```

推荐的 `.gitignore`：

```gitignore
# 大型媒体
*.mp4
*.mkv
*.mov
*.avi

# Whisper 输出
*.srt
*.vtt
*.tsv
*.json
*.txt

# 日志
*.log

# 临时/缓存
.cache/
tmp/
temp/

# Python
__pycache__/
*.pyc

# 模型
models/
*.bin
*.pt
*.gguf
```

对于你当前目录：

```text
meeting_01_2.json
meeting_01_2_refined.md
meeting_01_2.tsv
meeting_01_2.vtt
myopia.mp4
whisper.log
```

你可能希望：

| 文件                      | Git？       |
| ------------------------- | ---------- |
| `myopia.mp4`              | 忽略       |
| `meeting_01_2.tsv`        | 忽略       |
| `meeting_01_2.vtt`        | 忽略       |
| `meeting_01_2.srt`        | 忽略       |
| `meeting_01_2.txt`        | 忽略       |
| `whisper.log`             | 忽略       |
| `meeting_01_2_refined.md` | 可能保留   |
| 脚本/配置文件             | 保留       |

因为：

* 原始/生成的产物是可重复生成的
* 精炼后的 markdown 可能包含人工编辑和知识

一个非常常见的工程模式是：

```text
原始数据 -> 生成的输出 -> 精炼知识
```

只有最终的精炼知识才进入 Git。

---

如果你确实需要为大型文件进行版本管理，有几种方法。

## 1. Git LFS（大文件存储）

适用于：

* 你真正需要视频/模型的版本历史
* 团队协作需要它

安装：

```bash
git lfs install
```

跟踪 mp4：

```bash
git lfs track "*.mp4"
```

这会创建一个：

```text
.gitattributes
```

然后正常提交。

但是：

* GitHub 存储/带宽有限制
* 仓库变得更重
* 克隆更慢
* 不适用于生成的输出

通常适用于：

* ML 模型
* 数据集
* 重要的演示视频

不适用于：

* 频繁重新生成的 Whisper 输出

---

## 2. 外部存储 + Git 元数据（最实用）

在 AI/数据工程中非常常见。

将大文件存储在：

* NAS
* 外部 SSD
* 云存储
* S3
* Google Drive
* Dropbox

Git 只存储：

* 脚本
* 清单
* 哈希值
* 元数据

例如：

```text
videos/
  2026/
    meeting_01.mp4
```

Git 跟踪：

```json
{
  "file": "meeting_01.mp4",
  "sha256": "...",
  "duration": 7200
}
```

这种方式扩展性更好。

---

## 3. DVC（数据版本控制）

在 ML/数据流水线中，许多人使用：

* [DVC](https://dvc.org?utm_source=chatgpt.com)

它结合了：

* Git 用于代码
* 外部存储用于数据/模型

在以下情况下非常有用：

* 数据集巨大
* 存在 GPU 工作流
* 进行大量实验

但可能对于个人 Whisper 实验来说过于复杂。

---

## 我对你的工作流的建议

鉴于你的设置（本地 GPU + Whisper + 实验）：

### 放入 Git

```text
scripts/
prompts/
configs/
README.md
精炼的 markdown 笔记
小示例
```

### 忽略

```text
mp4
logs
srt/vtt/tsv
中间 json
缓存
模型
```

### 可选

保留一个小的演示样本：

```text
samples/demo_30sec.mp4
```

用于可重复性/测试。

---

一个实用的工作流：

```bash
# 生成
python transcribe.py myopia.mp4

# 精炼
vim meeting_01_2_refined.md

# 仅提交知识/代码
git add scripts README.md meeting_01_2_refined.md
git commit -m "精炼转录流水线"
```

这样可以保持仓库：

* 快速
* 整洁
* 可克隆
* 长期可维护

几年后非常重要——否则仓库会变成巨大的存储垃圾场，而不是工程历史记录。

参考：

* [Git LFS](https://git-lfs.com?utm_source=chatgpt.com)
* [DVC](https://dvc.org?utm_source=chatgpt.com)
* [Git Ignore 文档](https://git-scm.com/docs/gitignore?utm_source=chatgpt.com)
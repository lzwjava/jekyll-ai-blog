---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 多步骤HEIC转Markdown工作流
translated: true
type: note
---

很好的问题。你实际上是在问：如何将一个可重复的多步骤 CLI 工作流（HEIC→JPG、压缩、剥离 EXIF、注入 markdown）编码为一个可复用的技能，让 Hermes 这样的智能体能可靠地调用。

以下是我会采用的架构：

---

## 图像处理 + Markdown 注入的技能模式

在你的智能体上下文中，“技能”实际上由三部分组成：

1. **SKILL.md** — 声明式规格，供智能体读取以了解要使用的工具/步骤
2. **Shell 脚本或 Python 脚本** — 实际的可执行逻辑
3. **提示模板** — 智能体如何调用它并传入参数

---

### 步骤 1：编写可执行脚本

```bash
# ~/scripts/add_images_to_post.sh
#!/usr/bin/env bash
set -euo pipefail

# Usage: add_images_to_post.sh <heic_dir> <post_md> <section_name>
HEIC_DIR="$1"
POST_MD="$2"
SECTION="$3"
OUT_DIR="$(dirname "$POST_MD")/images/$(basename "$POST_MD" .md)"

mkdir -p "$OUT_DIR"

for heic in "$HEIC_DIR"/*.HEIC "$HEIC_DIR"/*.heic; do
  [ -f "$heic" ] || continue
  base=$(basename "$heic" | sed 's/\.[Hh][Ee][Ii][Cc]//')
  jpg="$OUT_DIR/${base}.jpg"

  # Convert HEIC → JPG
  magick "$heic" "$jpg"

  # Strip location/EXIF metadata
  exiftool -all= -overwrite_original "$jpg"

  # Compress to ~500KB (iterative quality reduction)
  quality=85
  while [ $(stat -f%z "$jpg") -gt 512000 ] && [ $quality -gt 20 ]; do
    magick "$jpg" -quality $quality "$jpg"
    quality=$((quality - 10))
  done

  echo "Processed: $jpg ($(du -sh "$jpg" | cut -f1))"
done

# Build markdown image block for section
IMG_BLOCK=""
for jpg in "$OUT_DIR"/*.jpg; do
  rel_path="${jpg#$(dirname "$POST_MD")/}"
  IMG_BLOCK+="![](${rel_path})\n\n"
done

# Inject after ## $SECTION header
python3 - <<PYEOF
import re, sys

md = open("$POST_MD").read()
section_pattern = rf"(## $SECTION\n)"
replacement = r"\1\n$IMG_BLOCK\n"
new_md = re.sub(section_pattern, replacement, md, count=1)

if new_md == md:
    # Section doesn't exist — append it
    new_md += f"\n## $SECTION\n\n$IMG_BLOCK\n"

open("$POST_MD", "w").write(new_md)
print("Injected images into $POST_MD under ## $SECTION")
PYEOF
```

依赖项：`imagemagick`、`exiftool`（均可通过 `brew install imagemagick exiftool` 安装）。

---

### 步骤 2：编写 SKILL.md

```markdown
# skill: add-images-to-post

## Purpose
Convert HEIC photos → JPG, compress to ~500KB, strip EXIF/location,
and inject them into a markdown post under a named section.

## When to use
User says: "add images to post", "insert photos", "convert HEIC to jpg for blog",
or provides a directory of images and a .md file path.

## Parameters
- heic_dir: directory containing .HEIC files (e.g. ~/Downloads/c1)
- post_md: absolute path to the markdown file
- section: section heading name to inject under (e.g. "Porridge")

## Steps
1. Run: ~/scripts/add_images_to_post.sh <heic_dir> <post_md> <section>
2. Verify output with: ls -lh <out_dir>/*.jpg
3. Show the injected markdown block to the user for confirmation
4. Optionally open the markdown file for review

## Tools required
- imagemagick (brew install imagemagick)
- exiftool (brew install exiftool)

## Output
- Converted JPGs in <post_dir>/images/<post_name>/
- Markdown file updated with image references under ## <section>
```

将此文件保存到 `/mnt/skills/user/add-images-to-post/SKILL.md`（或你的智能体加载技能的位置——请查阅你的 Hermes 配置）。

---

### 步骤 3：你的智能体如何调用它

关键在于，你的智能体（Hermes）会在相关任务开始时读取 SKILL.md。触发条件是用户意图与技能描述匹配。因此，在你的 `available_skills` 配置中注册它：

```yaml
skills:
  - name: add-images-to-post
    description: |
      Convert HEIC photos to JPG, compress, strip EXIF, inject into markdown post.
      Trigger when user mentions adding images to a blog post or converting HEIC files.
    location: ~/skills/add-images-to-post/SKILL.md
```

然后 Hermes 会：
1. 读取 SKILL.md
2. 从你的自然语言请求中提取参数
3. 以正确参数调用 shell 脚本
4. 返回结果

---

### 复合模式

一旦你有了 5–10 个这样的技能，你就可以得到：

```
用户意图 → 智能体读取技能 → 运行脚本 → 完成
```

零歧义。技能文件是规格，脚本是实现。这正是 Claude Code 内部工具的工作方式——模型读取工具描述，将意图映射到调用。

针对你的具体用例，我还会在脚本中添加一个 `--dry-run` 标志，显示它将要执行的操作而不修改文件——智能体在进行写入操作之前，非常喜欢有安全的预览步骤。

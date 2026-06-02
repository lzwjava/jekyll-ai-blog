---
audio: false
generated: true
lang: zh
layout: post
title: 优化翻译效率：段落哈希技术应用
translated: true
type: note
---

### 关于优化翻译工作流的思考

你的目标很明确：将 Jekyll 博客文章（用 Markdown 编写）翻译成 8 种语言时，通过仅重新翻译更改或新增的段落来最小化 AI 令牌使用量，同时缓存未更改的段落。你希望坚持使用 Markdown 进行编辑，避免为核心内容使用数据库/JSON/YAML，并处理特殊元素如代码块（这些不应翻译）。基于段落的方法很有意义，因为它符合你的写作和编辑方式——在这个层面上，翻译的语境准确性可能比句子级别更高。

关键挑战：

- **识别更改**：没有版本控制差异，你需要一种方法来检测哪些内容是新的/更改的/未更改的。对段落进行哈希处理（例如，对规范化的英文文本使用 SHA-256）是高效且无状态的——无需存储完整的旧版本。
- **处理 Markdown 结构**：你不能简单地按 `\n\n` 分割，因为代码块、标题、列表或其他语法可能会破坏结构。对于基本文章，简单的基于正则表达式的分割器可能有效，但使用轻量级 Markdown 解析器能更好地保持结构并跳过不可翻译部分。
- **缓存**：保持基于文件的简单缓存（例如，一个 JSON 文件或文件目录），避免使用数据库。按段落哈希、按语言缓存。
- **令牌节省**：对于长篇文章，这可以在小编辑时减少 80-90% 的使用量，因为只有受影响的段落会调用 AI API。
- **边缘情况**：新增/删除的段落（通过重新哈希处理）；微小调整（例如，拼写错误修复）将触发重新翻译，除非你规范化空格/标点；必须排除代码块或内联代码；如果段落重新排序，哈希将不匹配，但如果将其视为"新"内容，这也没问题。
- **集成**：在你的 Jekyll 工作流中将其作为预构建脚本运行（例如，通过 bash 脚本或 Git 钩子）。如果你单独生成翻译后的 Markdown 文件，则不需要 Jekyll 插件。

这种方法优于句子级别（AI 的语境准确性较低）或全文翻译（无节省）。对于写作想法来说，YAML/JSON 确实繁琐——坚持使用 Markdown。

### 建议的最佳方式：基于段落哈希的缓存和 Markdown 感知解析

使用 Python 脚本：

1. 将英文 Markdown 解析为"可翻译单元"（段落，排除代码块，如果需要也可以排除标题等）。
2. 对每个单元的英文文本进行哈希处理（规范化，例如去除多余空格）。
3. 检查基于文件的缓存中是否存在按哈希/语言存储的现有翻译。
4. 通过你的 AI 工具（例如 DeepSeek/Mistral API）翻译缺失的段落。
5. 缓存新翻译。
6. 重新组装翻译后的 Markdown 文件，保留不可翻译部分。

**为什么这是最佳方式**：

- **简单且低开销**：无需数据库，仅使用文件。除了 AI 调用外，可在本地/离线运行。
- **灵活**：通过跳过代码块来处理它们。可扩展至其他 Markdown 元素（例如，如果标题较短，则不翻译）。
- **成本效益高**：仅对新/更改的段落付费。对于一篇 10 段落的文章，编辑一段可节省约 90% 的令牌。
- **易于维护**：自然地编辑英文 Markdown；脚本处理其余部分。
- **所需工具**：Python（你可能已安装）。库：`hashlib`（内置，用于哈希处理），`markdown` 或 `mistune` 用于解析（如果需要；对于"无特殊语法"的情况，可以从简单的正则表达式开始）。

#### 分步实施

1. **设置**：
   - 创建一个 `translations_cache.json` 文件（或一个目录如 `cache/`，其中包含用于可扩展性的 hash.json 文件）。
   - 结构：`{ "hash1": { "fr": "翻译文本", "es": "...", ... }, "hash2": { ... } }`
   - 将其存储在博客仓库中（如果敏感则使用 git-ignore）或单独目录中。
   - 在脚本中列出你的 8 种语言（例如，['fr', 'es', 'de', ...]）。

2. **解析 Markdown**：
   - 对于简单情况（段落 + 代码块）：使用逐行处理来检测围栏代码块（``````` 或 `~~~`）和缩进代码（>3 个空格）。
   - 将"段落"收集为连续的非代码、非空行块。
   - 更好：使用 Python 的 `markdown` 库转换为 HTML，然后提取文本，但这对于重新组装是有损的。相反，使用 `mistune`（一个快速的 Markdown 解析器）来获取 AST（抽象语法树），这允许你遍历和修改可翻译节点（例如，'paragraph' 节点）。
   - 如果需要，安装 `mistune`（但你的环境有基础工具；假设你可以在本地 pip 安装）。

3. **哈希处理**：
   - 规范化：`text.strip().lower()` 或仅 `.strip()` 以忽略空格更改（如果希望，但这可能会错过有意编辑）。
   - 哈希：`hashlib.sha256(normalized.encode()).hexdigest()`

4. **翻译**：
   - 使用你的 AI API 包装器（例如，对于 DeepSeek：发送提示如"将此段落翻译成法语：{text}"）。
   - 如果可能，进行批处理，但由于段落较小，顺序处理也可以。

5. **重新组装**：
   - 通过将可翻译块替换为缓存/新翻译来重建 Markdown，保持代码/标题不变。

6. **脚本执行**：
   - 运行：`python translate_blog.py path/to/english.md`
   - 输出：`path/to/fr.md`、`path/to/es.md` 等。
   - 对于 Jekyll：将这些文件放在 `_posts/` 中，并加上语言前缀，或使用多语言插件如 `jekyll-polyglot` 来处理。

#### 示例 Python 脚本

这是一个使用逐行解析的基本版本（除了内置库外，无需外部库）。它假设简单的 Markdown：段落由空行分隔，围栏代码块。对于复杂语法，升级到 `mistune`。

```python
import hashlib
import json
import os
import sys
# 假设你有一个 AI 翻译函数；替换为你的 DeepSeek/Mistral API 调用
def ai_translate(text, lang):
    # 占位符：返回 API 调用结果
    return f"Translated to {lang}: {text}"  # 替换为真实 API

CACHE_FILE = 'translations_cache.json'
LANGUAGES = ['fr', 'es', 'de', 'it', 'pt', 'zh', 'ja', 'ko']  # 你的 8 种语言

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=4)

def compute_hash(text):
    normalized = text.strip()  # 自定义规范化
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def parse_markdown(md_text):
    lines = md_text.splitlines()
    blocks = []
    current_block = []
    in_code = False
    for line in lines:
        if line.strip().startswith('```') or line.strip().startswith('~~~'):
            in_code = not in_code
            if current_block:
                blocks.append(('text', '\n'.join(current_block)))
                current_block = []
            blocks.append(('code', line))
            continue
        if in_code:
            blocks.append(('code', line))
        else:
            if line.strip():  # 非空行
                current_block.append(line)
            else:
                if current_block:
                    blocks.append(('text', '\n'.join(current_block)))
                    current_block = []
    if current_block:
        blocks.append(('text', '\n'.join(current_block)))
    return blocks

def translate_post(english_md_path):
    with open(english_md_path, 'r') as f:
        md_text = f.read()

    blocks = parse_markdown(md_text)
    cache = load_cache()

    for lang in LANGUAGES:
        translated_blocks = []
        for block_type, content in blocks:
            if block_type == 'code':
                translated_blocks.append(content)
            else:  # text
                h = compute_hash(content)
                if h not in cache:
                    cache[h] = {}
                if lang not in cache[h]:
                    translation = ai_translate(content, lang)
                    cache[h][lang] = translation
                translated_blocks.append(cache[h][lang])

        # 用换行符重新组装
        translated_md = '\n\n'.join(translated_blocks)  # 根据 Markdown 格式化调整
        output_path = english_md_path.replace('.md', f'_{lang}.md')
        with open(output_path, 'w') as f:
            f.write(translated_md)

    save_cache(cache)
    print("Translations updated.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python script.py path/to/english.md")
    else:
        translate_post(sys.argv[1])
```

**如何使用**：

- 将 `ai_translate` 替换为你的 API 逻辑。
- 在编辑后对你的文章文件运行。
- 对于标题/列表：扩展 `parse_markdown` 以检测（例如，以 `#` 或 `-` 开头的行作为单独块）。
- 如果文章包含图片/链接：由于它们在文本块中，保持不变。
- 规范化提示：如果你想忽略次要标点更改，使用正则表达式在哈希处理前去除它们。

#### 增强功能

- **Git 集成**：使用 `git diff` 预先识别更改的行，但哈希更简单。
- **批量翻译**：如果 API 支持，一次性发送多个新段落。
- **错误处理**：重试失败的 API 调用；验证翻译。
- **高级解析**：Pip 安装 `mistune` 并使用其渲染器进行自定义（例如，跳过 'code_block' 节点）。
- **测试**：使用 SHA-256 时哈希冲突很少见；在示例文章上测试。

这应该可以在不使你的工作流复杂化的情况下节省令牌。如果你的 Markdown 更复杂，从此开始并迭代。如果你需要调整或 API 集成方面的帮助，请告诉我！

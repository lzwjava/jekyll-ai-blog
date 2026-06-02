---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在终端中显示Markdown
translated: true
type: note
---

问题：如何在终端CLI工具中正确显示Markdown格式的AI响应（例如`**加粗**`、`- 列表`）？我是否可以通过系统提示词来让LLM停止使用Markdown语法？

回答：

你有**两种主要方法**——在终端中精美地渲染Markdown，或者通过系统提示词从源头抑制它。以下是两种方法的完整分析。

---

## 方法1：在终端中渲染Markdown

最适合此用途的Python库是**Rich**。Rich可以渲染Markdown，并能合理地将格式转换为终端显示——包括标题、加粗、斜体、列表以及带有完整语法高亮的代码块。

### 安装Rich

```bash
pip install rich
```

### 将LLM响应渲染为Markdown

```python
from rich.console import Console
from rich.markdown import Markdown

console = Console()

# 假设这是你的LLM响应字符串
llm_response = """
# 摘要

以下是关键要点：

- **要点一**: 非常重要
- **要点二**: 同样重要

```python
print("Hello World")
```
"""

md = Markdown(llm_response)
console.print(md)
```

你也可以直接从命令行使用Markdown类——例如：`python -m rich.markdown README.md`

### 将LLM输出管道传输到`rich-cli`

如果你使用的是输出管道的CLI工具，你可以从另一个进程管道传输输出：`cat response.md | rich - --markdown --force-terminal`

---

## 方法2：通过系统提示词移除Markdown

是的，你完全可以通过指令让LLM仅以纯文本格式响应，而不使用任何Markdown语法。这是一种非常常见且有效的解决方案。

### 有效的系统提示词措辞

```
你是一个运行在终端CLI工具中的助手。
在你的回答中不要使用任何Markdown格式。
不要用加粗（**文本**）、斜体（*文本*）、标题（# 文本）、
项目符号（-）以及反引号代码块。
仅使用纯文本回答。
```

### 此方法有效的理由（及注意事项）

许多开发者都面临这个确切的问题——LLM倾向于默认使用Markdown格式。诸如在系统提示词开头加入“以纯文本无格式的方式回答”等技术可能有所帮助，但效果不一。

最近，在"o"系列模型中，OpenAI引入了默认设置，禁止生成带有Markdown格式的响应，除非明确给出“Formatting re-enabled”指令来重新启用此行为。

一个在实践中效果良好、明确且有力的系统提示词示例（源自实际使用）：

```
用户将向你提问。
请仅用纯文本回答——不要用markdown、不要用代码块、不要用项目符号（-）、不要用加粗或斜体语法。
你的输出将直接打印到终端。
```

---

## 方法3：通过编程方式移除Markdown（备选方案）

如果LLM偶尔仍会泄露Markdown语法，你可以使用像`markdownify`这样的库或简单的正则表达式清理器来移除它：

```python
import re

def strip_markdown(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)   # 加粗
    text = re.sub(r'\*(.*?)\*', r'\1', text)         # 斜体
    text = re.sub(r'#{1,6}\s?', '', text)            # 标题
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text, flags=re.DOTALL)  # 代码
    text = re.sub(r'^\s*[-*]\s+', '', text, flags=re.MULTILINE)    # 项目符号
    return text.strip()
```

---

## 总结——应使用哪种方法？

| 方法 | 最适用于 |
|---|---|
| **Rich（渲染Markdown）** | 你想要带有颜色和结构的精美格式终端输出 |
| **系统提示词（抑制Markdown）** | 你想要原始纯文本，不要装饰 |
| **编程方式移除** | 作为系统提示词不完全可靠时的安全备用方案 |

对于CLI工具，最稳健的解决方案是**结合使用两种方法**：使用系统提示词以最小化Markdown输出，并使用`rich`来渲染仍出现的任何结构化文本。

参考文献：

- [Rich Markdown 文档](https://rich.readthedocs.io/en/latest/markdown.html)
- [Rich 在 GitHub 上](https://github.com/Textualize/rich)
- [Rich-CLI 在 GitHub 上](https://github.com/Textualize/rich-cli)
- [OpenAI 社区——如何阻止 Markdown 输出](https://community.openai.com/t/how-to-prevent-gpt-from-outputting-responses-in-markdown-format/961314)

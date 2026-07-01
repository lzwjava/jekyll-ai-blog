---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新的备注和学位特征
translated: true
type: note
---

## 1. 触发了 gh-pages 工作流

在 jekyll-ai-blog 仓库上运行了 `gh workflow run gh-pages.yml`。确认已在以下地址启动：
<https://github.com/lzwjava/jekyll-ai-blog/actions/runs/27012471396>

---

## 2. `ww degree --months` 过滤器

**问题：** `ww degree` 显示所有 20 篇抓取的文章，无论时间多久。用户只关心最近 3 个月。

**更改（4 个文件）：**

- `ww/degree/degree.py` — 添加了 `from datetime import datetime, timedelta`，添加了 `--months N` 参数（默认 3，传 0 以禁用）。在获取条目后，根据日期过滤：`e["date"] >= cutoff`，其中 `cutoff` 为 `now - N*30 days`。
- `ww/main.py` — 在 Degree 部分的帮助文本中添加了 `--months`。
- `README.md` / `README-CN.md` — 在 degree 命令表格中添加了 `--months` 行。

**用法：**

```
ww degree              # 最近 3 个月（默认）
ww degree --months 6   # 最近 6 个月
ww degree --months 0   # 所有文章（不过滤）
```

**提交：** `b57960d` — `feat(degree): filter articles by --months (default 3)`
**CI：** 所有 3 个工作流均通过（Lint & Security、Unit Test、Integration Test）。

---

## 3. 重复笔记检测修复

**问题：** 在 2026-06-05 创建了两篇内容相同的笔记：

- `2026-06-05-embedding-in-english-and-ai-explained-en.md`
- `2026-06-05-embeddings-from-language-to-ai-models-en.md`

pre-commit 钩子（`test_duplicate_notes.py`）检测到了重复并阻止了提交。但一开始就不应该创建重复的笔记。

**根本原因：** 使用了两种不同的算法：

| 位置 | 算法 | 行为 |
| --- | --- | --- |
| `check_duplicate_notes.py`（生产环境） | 前 250 个字符必须*完全相等*，然后匹配 450/500 个字符 | 过于严格——漏掉了措辞稍有差异的近似重复 |
| `test_duplicate_notes.py`（pre-commit 测试） | 前 200 个字符 90% 相似度 或 后 200 个字符 90% 相似度 | 宽松——捕捉了语义重复 |

当 LLM 对同一个问题（“什么是 embedding？”）给出了两次答案，但标题/措辞略有不同时，严格的生产环境检查通过了，而宽松的 pre-commit 测试却捕捉到了重复。

**更改（3 个文件）：**

- `ww/ww/note/check_duplicate_notes.py` — 将严格算法替换为与测试相同的基于前/后 200 个字符 90% 相似度的检查。添加了 `_char_similarity()` 辅助函数。现在生产环境和测试使用相同的逻辑。
- `ww/tests/note/test_check_duplicate_notes_extended.py` — 更新了 2 个测试：
  - `test_different_first_and_last_chars_returns_false` — 更改为不同的结尾（原版本仅在开头不同，但旧算法不检查结尾）
  - `test_long_strings_with_many_differences` — 更改为预期 `True`，因为前/后 200 个字符现在匹配
- `jekyll-ai-blog/notes/2026-06-05-embeddings-from-language-to-ai-models-en.md` — 删除了重复的文件。

**提交（ww）：** `75ec6ac` — `fix(note): align duplicate detection with test algorithm`
**提交（jekyll-ai-blog）：** `fcf99761f` — `fix(notes): remove duplicate embedding note`
**CI：** 所有 35 个重复检查测试通过。pre-commit 钩子通过。

---

## 为什么重复不断发生

笔记创建流程为：hermes `/note` 插件 → 剪贴板 → `ww note` → 队列 → `ww note watch` → `create_note_from_content()`。`create_note_from_content()` 中的重复检查存在，但使用的算法过于严格——它要求前 500 个字符中几乎精确的字符级匹配。当 LLM 在不同时间对同一个问题生成相同的答案，但措辞略有不同（不同的标题、略微不同的表述）时，检查通过了，于是创建了重复。pre-commit 钩子使用了更宽容的算法，捕捉到了这些重复，这就是为什么提交一直失败。现在两者使用相同的算法。

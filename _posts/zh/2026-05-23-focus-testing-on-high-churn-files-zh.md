---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 高变更文件聚焦测试
translated: true
type: note
---

以下是数据和策略：

**变更频率数据（按提交次数排名前15的文件）：**

```
62  ww/main.py                     ← CLI入口点，遥遥领先
12  ww/note/create_normal_log.py
10  ww/note/create_note_utils.py
10  ww/note/create_log.py
 9  ww/image/screenshot.py
 8  ww/sync/remote.py
 8  ww/llm/openrouter_client.py
 8  ww/github/gitmessageai.py
 6  ww/note/note_workflow.py
 6  ww/note/create_note.py
 6  ww/note/create_note_from_clipboard.py
 6  tests/test_main.py
 5  ww/note/screenshot_log.py
 5  ww/git/git_update.py
 4  ww/search/search_*.py（4个文件）
 4  ww/git/git_squash.py、git_show_command.py等
```

**分布情况极为极端：**

- `ww/` 目录下共有721个被跟踪文件
- 45个文件拥有3次以上提交（约6%）
- 693个文件仅有1-2次提交（约94%）—— 添加后几乎未修改

**此策略有效的原因：**

1. **变更频率 = 缺陷引入面。** 频繁变更的文件是回归缺陷的高发区。一个被修改62次的文件（main.py）的缺陷引入机会，是一个仅被修改1次文件的62倍。

2. **这里的80/20法则更为极端。** 排名前45的文件（6%）占据了绝大部分提交量。测试这些文件，就覆盖了未来80%以上变更的落点。

3. **当前的覆盖率存在偏差。** 你在note/git/image/utils等模块有60-100%的覆盖率——但一些高变更频率的文件如 `main.py`（62次提交）、`create_normal_log.py`（12次提交）、`screenshot.py`（9次提交）、`remote.py`（8次提交）、`openrouter_client.py`（8次提交）可能为零或很低的覆盖率。

4. **零覆盖率的未测试模块（agent/、audio/、cloud/等）大多属于低变更频率。** 它们是一次构建后便不再修改。测试这些模块的投资回报率低——它们很少变更，因此出现缺陷的概率也小。

**行动方案：**

```
步骤1：git log --format= --name-only ww/ | sort | uniq -c | sort -rn > /tmp/churn.txt
步骤2：对排名前30%（约20-25个文件）的每个文件：
   - 是否存在对应的测试文件？（tests/*/<module>/test_<name>.py）
   - 如果存在，覆盖率是多少？（pytest --cov=<module>）
   - 如果不存在，这是一个缺口——编写测试
步骤3：优先级排序 = 变更频率 × (1 - 现有覆盖率)
```

**公式：** `优先级 = 提交次数 × (1 - 覆盖率%)` —— 这会给出一个排序列表，其中拥有62次提交和0%覆盖率的文件（main.py）得分最高，而拥有1次提交和80%覆盖率的文件得分接近零。

**核心结论：** 是的，这是正确的思考方式。优先测试高变更频率的文件，是提升实际测试质量最具杠杆效应的举措。当前12%的整体数字具有误导性——如果你能充分覆盖排名前30的高变更文件，你就是在真正关键的领域提供了保护。
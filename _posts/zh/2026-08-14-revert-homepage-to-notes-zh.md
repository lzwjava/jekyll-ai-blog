---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将首页恢复为笔记
translated: true
type: note
---

完成。现在首页显示的是笔记而非文章。

**变更**（`index.html`）：
{% raw %}
```diff
-{% include sort.html type='posts' %}
+{% include sort.html type='notes' %}

-{% include post-list.html lang='en' type='posts' %}
+{% include post-list.html lang='en' type='notes' %}
```
{% endraw %}

**验证：**
- `bundle exec jekyll build` 构建成功（目标冲突警告是预先存在的重复永久链接问题，与此变更无关）
- 生成的 `_site/index.html` 现在包含 12,507 个 `data-type="note"` 项目，且列表与 `notes-en.html` 完全相同

这实际上撤销了提交 `0653f4f2d`（"将首页从笔记改为文章"），因此 `/` 现在与笔记订阅源一致。
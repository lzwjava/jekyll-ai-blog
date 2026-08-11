---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全局设置 Git 身份
translated: true
type: note
---

已完成。Git 身份已全局设置：

```
user.name  = lzwjava
user.email = lzwjava@gmail.com
```

这将应用于任何仓库中的未来所有提交。对于刚刚失败的仓库 (`~/projects/jekyll-ai-blog`)，它会自动采用这些设置——你可以按照错误提示使用 `ww note process` 重试推送，或手动提交创建的笔记：

```bash
cd ~/projects/jekyll-ai-blog
git add notes/
git commit -m "docs: add notes on tmux fixes for terminfo and portable"
git push
```

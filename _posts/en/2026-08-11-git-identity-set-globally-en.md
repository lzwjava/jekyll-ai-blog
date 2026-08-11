---
audio: false
generated: true
image: false
lang: en
layout: post
title: Git Identity Set Globally
translated: false
type: note
---

Done. Git identity set globally:

```
user.name  = lzwjava
user.email = lzwjava@gmail.com
```

This applies to all future commits in any repo. For the repo that just failed (`~/projects/jekyll-ai-blog`), it'll pick these up automatically — you can retry the push with `ww note process` as the error suggested, or commit the created notes manually:

```bash
cd ~/projects/jekyll-ai-blog
git add notes/
git commit -m "docs: add notes on tmux fixes for terminfo and portable"
git push
```

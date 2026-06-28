---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用新 Rsync 成功备份
translated: true
type: note
---

备份完成！

```
最终：Mac Mini 上 56G（~/macbook-backup/）

projects/   21G  ✓
personal/   33G  ✓  （图片 4888/4888 原片）
config/     12K  ✓
shell/      84K  ✓
ssh/        12K  ✓
desktop/    1.0G ✓
documents/  120M ✓
joplin/     33M  ✓
openclaw/   13M  ✓
wechat/     184K ✓
docker/     8K   ✓
maven/      241M ✓
token/      4K   ✓
```

解决办法是从源码编译安装 rsync 3.4.1。旧版 macOS 自带的 rsync 2.6.9 大约每 5 分钟就会断开 SSH 连接。使用 rsync 3.4.1 后，大部分传输都能顺利完成而不中断——图片传输只用了 3 轮，而如果用 2.6.9 版则需要 10 轮以上才能完成。

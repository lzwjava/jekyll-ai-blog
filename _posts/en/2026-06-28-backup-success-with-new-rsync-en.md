---
audio: false
generated: true
image: false
lang: en
layout: post
title: Backup Success With New Rsync
translated: false
type: note
---

BACKUP COMPLETE!

```
Final: 56G on Mac Mini (~/macbook-backup/)

projects/   21G  ✓
personal/   33G  ✓  (Pictures 4888/4888 originals)
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

The fix was building rsync 3.4.1 from source. The old macOS rsync 2.6.9 was dropping SSH connections every ~5 minutes. With rsync 3.4.1, most transfers completed without drops — Pictures finished in 3 runs vs the 10+ runs it would have taken with 2.6.9.

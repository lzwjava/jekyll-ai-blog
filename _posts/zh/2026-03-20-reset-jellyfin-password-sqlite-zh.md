---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 SQLite 重置 Jellyfin 密码
translated: true
type: note
---

好的。这是我的操作步骤：

### 重置是如何工作的

**1. 停止服务** — Jellyfin 运行时无法修改数据库：
```bash
sudo systemctl stop jellyfin
```

**2. 备份数据库** — 以防万一：
```bash
sudo cp /var/lib/jellyfin/data/jellyfin.db /var/lib/jellyfin/data/jellyfin.db.bak
```

**3. 检查 schema** — 发现了 `Users` 表，并看到密码以 PBKDF2-SHA512 哈希形式存储在 `Password` 列中。

**4. 清空密码并强制重置：**
```sql
UPDATE Users SET Password='', MustUpdatePassword=1 WHERE Username='jellyfin';
```
- `Password=''` — 删除哈希，因此登录时无需密码
- `MustUpdatePassword=1` — 强制 Jellyfin 在下次登录时提示设置新密码

**5. 重新启动服务：**
```bash
sudo systemctl start jellyfin
```

就是这样。不需要 Jellyfin CLI — 只需直接编辑本地的 SQLite 数据库。

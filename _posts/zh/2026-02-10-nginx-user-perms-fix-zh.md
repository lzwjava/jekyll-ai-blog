---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Nginx 用户和权限错误
translated: true
type: note
---

**Question:** 为什么在将 user 更改为 'lzw' 后 nginx 无法启动？如何修复 `/var/log/nginx/error.log` 的 permission denied 错误以及关于 "user" 指令的 warning？

**Answer:**

Nginx 启动失败是因为你将 user 更改为了 `lzw`（一个普通的 non-root user），但 master process 仍然需要 **root privileges** 来执行以下操作：

- 绑定到端口 80（小于 1024 的 privileged port）
- 打开/写入由 root 或 www-data 拥有的日志文件（例如 `/var/log/nginx/error.log`）
- 执行其他 privileged operations

当你以 non-root user (`lzw`) 身份运行 nginx 时，它无法打开 `/var/log/nginx/error.log` → **Permission denied (13)** → emergency exit。

Warning 信息  
`the "user" directive makes sense only if the master process runs with super-user privileges, ignored`  
准确地证实了这一点：nginx 忽略了你的 `user lzw;` 配置行，因为它不是以 root 身份启动的。

### 推荐的修复方案 – 让 nginx 以 root (master) 运行，但在 worker 进程中降权为 `lzw`

这是 nginx 设计的**标准且安全**的工作方式。

1. **删除或撤销之前的 user 更改**

   如果你使用了 `systemctl edit nginx` 并添加了：

   ```ini
   [Service]
   User=lzw
   Group=lzw
   ```

   删除该 override：

   ```bash
   sudo rm /etc/systemd/system/nginx.service.d/override.conf
   sudo systemctl daemon-reload
   ```

   或者如果你编辑了 `/etc/nginx/nginx.conf` 并添加了 `user lzw lzw;`，请将其注释掉或删除：

   ```nginx
   # user lzw lzw;   ← 注释或删除此行
   ```

2. **重启 nginx (应该可以再次以 www-data 身份运行)**

   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl status nginx
   ```

3. **修复原始目录的权限问题** (确保 /movies/ 访问时不会出现 403)

   使用 group 方法 (干净且安全)：

   ```bash
   sudo chgrp -R www-data /home/lzw/qDownloads
   sudo chmod -R g+rx /home/lzw/qDownloads
   sudo chmod g+x /home/lzw               # 允许 group 遍历你的 home 目录
   ```

   然后 reload：

   ```bash
   sudo systemctl reload nginx
   ```

   测试：`http://192.168.1.36/movies/`

### 备选方案 – 完全以 user lzw 身份运行 (不推荐用于 80 端口)

如果你确实希望 nginx 完全作为 `lzw` 运行 (完全没有 root)：

- 将 listen 端口更改为大于 1024 的端口（例如 8080）
- 修复所有 log / pid 文件的权限

`/etc/nginx/nginx.conf` 中的示例配置更改：

```nginx
user lzw lzw;
...
http {
    ...
    access_log /home/lzw/nginx/access.log;
    error_log  /home/lzw/nginx/error.log;
}
```

在你的 server block 中：

```nginx
server {
    listen 8080;
    ...
}
```

然后创建日志目录并赋予所有权：

```bash
mkdir -p /home/lzw/nginx
chown lzw:lzw /home/lzw/nginx
```

但再次强调：**只有在不需要使用 80/443 端口时，这才是切实可行的**。大多数人保持默认的 root → drop-privileges 模型。

### 快速总结 – 现在的操作步骤 (适用于 99% 的情况)

```bash
# 1. 撤销错误的 systemd override
sudo rm /etc/systemd/system/nginx.service.d/override.conf
sudo systemctl daemon-reload

# 2. (可选) 确保 nginx.conf 中没有 user lzw 行
sudo nano /etc/nginx/nginx.conf   # 删除或注释 "user lzw ..."

# 3. 修复下载文件夹权限
sudo chgrp -R www-data /home/lzw/qDownloads
sudo chmod -R g+rx /home/lzw/qDownloads
sudo chmod g+x /home/lzw

# 4. 正常启动 nginx
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl status nginx
```

你应该能看到 Active: active (running) 且没有权限错误。

**References:**

- None required – 这是 nginx.org 上记录的标准 nginx privilege model 行为。
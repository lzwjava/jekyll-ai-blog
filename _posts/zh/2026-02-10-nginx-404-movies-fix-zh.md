---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Nginx 电影路径 404 错误
translated: true
type: note
---

**Question:** 访问 /movies/ 路径时，从 nginx/1.28.2 收到 404 Not Found 错误。

**Answer:**

404 错误意味着 nginx 正在运行并响应，但无法找到请求的资源。既然你使用了 `alias /home/lzw/qDownloads/;` 并开启了 `autoindex on;`，以下是最常见的原因及逐步修复方法：

### 1. URL 错误（最常见原因）
请确保你访问的是 **精确** 的路径：

- 正确：`http://localhost/movies/`（带末尾斜杠）
- 同时尝试：`http://your-server-ip/movies/` 或 `http://127.0.0.1/movies/`

如果你输入 `http://localhost/movies`（没有末尾斜杠），根据你的配置，nginx 可能会返回 404。

### 2. 目录权限 – nginx 无法读取 /home/lzw/qDownloads
这是 **第二大常见原因**。

Nginx 通常以 `www-data` (Ubuntu/Debian) 或 `nginx` (官方包) 用户运行。该用户必须能够：

- 进入每个父目录（`/home`, `/home/lzw`, `/home/lzw/qDownloads`）
- 读取文件并列出目录

快速修复 – 给其他用户赋予读取和执行权限（对于私有 home 目录设置最安全）：

```bash
sudo chmod -R o+rx /home/lzw/qDownloads
# 或者更精简的权限：
sudo chmod o+x /home/lzw
sudo chmod o+x /home/lzw/qDownloads
sudo chmod -R o+r /home/lzw/qDownloads
```

更好的长期解决方案（推荐）：

```bash
# 创建 www-data 组访问权限
sudo chgrp -R www-data /home/lzw/qDownloads
sudo chmod -R g+rx /home/lzw/qDownloads

# 允许遍历 home 目录（仅需执行位 execute bit）
sudo chmod g+x /home/lzw
```

### 3. SELinux 或 AppArmor 拦截访问（如果已启用）
在 Ubuntu 上，AppArmor 通常是处于活跃状态的。

检查 AppArmor 是否拒绝访问：

```bash
sudo aa-status
# 如果你看到 nginx 处于 complain 或 enforce 模式
```

快速临时测试 – 将 nginx 的 AppArmor 设置为 complain 模式：

```bash
sudo aa-complain /usr/sbin/nginx
sudo systemctl restart nginx
```

如果这就恢复正常了 → 那么 AppArmor 就是问题所在。你应该创建或调整 profile 而不是永久禁用它。

### 4. 配置未实际加载
确保你的配置已生效：

- 文件应位于 `/etc/nginx/sites-available/`（例如：`movies.conf`）
- 在 `/etc/nginx/sites-enabled/` 中存在软链接：
  ```bash
  sudo ln -s /etc/nginx/sites-available/movies.conf /etc/nginx/sites-enabled/
  ```
- 没有冲突的 `default` 站点：
  ```bash
  sudo rm /etc/nginx/sites-enabled/default   # 如果你不需要默认欢迎页面
  ```
- 测试并重新加载：
  ```bash
  sudo nginx -t
  sudo systemctl reload nginx
  ```

### 5. 目录为空或不存在
再次确认：

```bash
ls -la /home/lzw/qDownloads/
```

如果文件夹为空，开启了 `autoindex on` 的 nginx 仍会显示索引页面（只是提示没有文件）。

### 立即执行的诊断命令
如果仍然无法工作，请运行这些命令并查看输出：

```bash
# 1. 当前已启用的 nginx 配置文件
ls -l /etc/nginx/sites-enabled/

# 2. nginx 正在使用的完整 server block
sudo nginx -T | grep -A 15 "server_name localhost"

# 3. 查看 nginx 错误日志寻找线索
sudo tail -n 30 /var/log/nginx/error.log

# 4. 以 nginx 用户身份测试访问
sudo -u www-data ls -la /home/lzw/qDownloads/
# 如果显示 "Permission denied" → 权限问题
```

先修复最可能的问题（权限或末尾斜杠）—— 在 80–90% 的 home 目录 alias 案例中，都是这两者之一导致的。

**References:**

- 标准故障排查步骤无需特定参考文献。

---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ubuntu 上安装最新版 Nginx
translated: true
type: note
---

**Question:** 系统提示找不到 'nginx' 命令。它建议安装 nginx-core, nginx-extras 或 nginx-light。我接下来该怎么做才能让 nginx 运行起来？

**Answer:**

你使用的是 **Ubuntu** (或基于 Debian 的) 系统，目前尚未安装 nginx。以下是 2025/2026 年推荐的操作步骤：

### 最佳选择：安装现代官方 nginx 版本 (推荐)

apt 建议的版本 (`1.18.0`) **非常陈旧** (发布于 2020 年)。你肯定更希望使用更新且受支持的版本。

#### 方法 1 – 官方 nginx repository (最干净且能获取最新 stable 版本)

1. 添加官方 nginx 签名密钥和 repository：
```bash
sudo apt update
sudo apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" | sudo tee /etc/apt/preferences.d/99nginx
```

2. 安装 nginx：
```bash
sudo apt update
sudo apt install nginx
```

3. 验证：
```bash
nginx -v
# 应该显示类似：nginx version: nginx/1.26.x (或更高版本)
sudo systemctl status nginx
```

#### 方法 2 – 快速但版本较旧 (如果你只想立刻测试)

如果你不在乎是否为最新版本，只想立即运行 nginx：
```bash
sudo apt update
sudo apt install nginx
# 这通常会安装 nginx-core 或默认变体
```

无论使用哪种方法，安装完成后你原来的 config 应该可以通过以下步骤生效：
- 将其放置在 `/etc/nginx/sites-available/` (例如 `/etc/nginx/sites-available/movies`)
- 创建 symlink：`sudo ln -s /etc/nginx/sites-available/movies /etc/nginx/sites-enabled/`
- 如果需要，删除或禁用默认站点：`sudo rm /etc/nginx/sites-enabled/default`
- 测试 config：`sudo nginx -t`
- Reload：`sudo systemctl reload nginx` (或 `sudo nginx -s reload`)

### 快速总结 – 大多数人现在应该运行的命令
```bash
# 推荐 – 从官方源获取当前的 stable nginx
sudo apt update
sudo apt install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring
curl -fsSL https://nginx.org/keys/nginx_signing.key | sudo gpg --dearmor -o /usr/share/keyrings/nginx-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/ubuntu $(lsb_release -cs) nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

sudo apt update
sudo apt install nginx

nginx -v
```

完成这些步骤后，你就可以使用 `nginx` 命令，并且你在 `/movies/` 下配置的 directory listing 应该可以正常工作了。

**References:**  

- [http://nginx.org/en/linux_packages.html](http://nginx.org/en/linux_packages.html)  
- [https://nginx.org/en/docs/install.html](https://nginx.org/en/docs/install.html)
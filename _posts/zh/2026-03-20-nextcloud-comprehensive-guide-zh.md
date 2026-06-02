---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用 Nextcloud 的全面指南
translated: true
type: note
---

以下是针对 **Nextcloud** 的全面、最新（截至 2026 年 3 月）指南，涵盖服务器设置基础、客户端使用（桌面和移动）、核心功能以及支持的文件类型。Nextcloud 是一个强大的开源、自托管平台，用于文件同步、共享、协作、日历、联系人等功能。

### 1. 服务器安装和设置
Nextcloud Server 在 Linux 上运行（推荐），通过 Docker 或手动设置支持其他平台。

**推荐系统要求（2026 年）：**
- **OS**：Ubuntu 24.04 LTS（强烈推荐）、Ubuntu 22.04 LTS、Red Hat Enterprise Linux 9、Debian 12、openSUSE Leap 15.6 等（64 位以获得最佳性能）。
- **Database**：MariaDB 10.11（推荐）或 MySQL 8.4、PostgreSQL 15–17、SQLite（仅用于测试）。
- **PHP**：8.2 或 8.3（推荐 8.3）。
- **Web server**：Apache 2.4（使用 mod_php 或 php-fpm）或 Nginx + php-fpm。
- **CPU/RAM**：小型/中型使用至少 2 核和 4 GB RAM；大量协作或多用户时需要更多。

**最简单的安装方法（2025–2026 年）：**
- **Docker（推荐用于家庭/自托管用户）**：使用官方 `nextcloud` Docker 镜像和 `docker-compose`。示例基本 `docker-compose.yml`：
  ```yaml
  version: '3'
  services:
    db:
      image: mariadb:10.11
      restart: always
      command: --transaction-isolation=READ-COMMITTED --binlog-format=ROW
      volumes:
        - db:/var/lib/mysql
      environment:
        - MYSQL_ROOT_PASSWORD=yourpassword
        - MYSQL_PASSWORD=yourpassword
        - MYSQL_DATABASE=nextcloud
        - MYSQL_USER=nextcloud

    app:
      image: nextcloud:latest
      restart: always
      ports:
        - 8080:80
      links:
        - db
      volumes:
        - nextcloud:/var/www/html
      environment:
        - MYSQL_PASSWORD=yourpassword
        - MYSQL_DATABASE=nextcloud
        - MYSQL_USER=nextcloud
        - MYSQL_HOST=db

  volumes:
    db:
    nextcloud:
  ```
  使用 `docker compose up -d` 运行，然后访问 `http://your-ip:8080` 完成 Web 安装程序。

- **Ubuntu 上的手动安装**：遵循官方指南——安装 LAMP/LEMP 栈，从 nextcloud.com 下载最新 `.tar.bz2`，提取到 Web 根目录，设置权限，运行 Web 安装程序。

- 安装后：创建管理员账户，配置受信任域名，启用 HTTPS（通过 Let's Encrypt + Caddy/Nginx/Apache），设置后台任务（cron），从 Apps 商店启用 Calendar、Contacts、Talk、Text 等应用。

### 2. 客户端（桌面和移动）
Nextcloud 提供官方同步客户端，实现无缝文件访问和同步。

**桌面客户端（Windows、macOS、Linux）：**
- 下载地址：https://nextcloud.com/install/#install-clients（2026 年最新版本 ~v4.0.x）。
- 支持：Windows 10+（64 位）、macOS 12.0+（64 位）、Linux（AppImage 支持大多数发行版，例如 Ubuntu 22.04+）。
- 设置：
  1. 安装并启动客户端。
  2. 输入 Nextcloud 服务器 URL（例如 https://cloud.yourdomain.com）。
  3. 使用用户名和密码登录（或使用 app password 以提高安全性）。
  4. 选择要同步的文件夹（支持选择性同步——仅同步所需内容）。
  5. Windows/macOS 支持虚拟文件（文件本地显示但打开时下载——节省空间）。
- 功能：双向同步、冲突处理、版本控制、活动 Feed、从桌面共享。

**移动客户端（Android & iOS）：**
- 下载：“Nextcloud” 应用，从 Google Play 或 Apple App Store。
- 设置：与桌面相同——添加服务器 URL，登录。
- 主要功能：自动上传照片/视频、即时上传、离线访问、后台同步、端到端加密支持。
- 附加：Nextcloud Talk 应用用于聊天/视频通话（独立或集成）。

### 3. 核心功能和使用
- **Web 界面**：通过浏览器访问——Files 应用用于上传/下载/共享，预览多种文件类型，创建/编辑文档（使用 Text/OnlyOffice/Collabora），共享链接（密码、过期、编辑权限）。
- **共享**：内部（用户/组）、外部公共链接、联合共享（与其他 Nextcloud 实例）。
- **端到端加密 (E2EE)**：为文件夹启用——仅您能解密（客户端侧）。
- **版本和回收站**：自动文件版本控制，删除文件进入回收站（可配置保留期）。
- **Apps 生态**：数千个应用——Deck（Kanban）、Notes、Tasks、Calendar、Contacts、Mail、News、Photos（支持人脸识别）等。
- **搜索和标签**：全文搜索、智能标签、快速访问快捷方式。
- **安全性**：2FA、暴力破解保护、速率限制、审计日志。

### 4. 支持的文件类型
Nextcloud 支持几乎**任何文件类型**的存储和同步——上传无硬性限制（除管理员配置的黑名单或大小限制）。

**主要亮点：**
- **所有常见格式** 无问题：文档（.docx、.xlsx、.pptx、.odt、.ods、.pdf）、图像（.jpg、.png、.gif、.webp、.heic）、音频（.mp3、.wav、.flac、.m4a）、视频（.mp4、.mkv、.mov、.avi）、归档（.zip、.rar、.7z）、代码（.py、.js、.cpp、.md）等。
- 特殊/小众文件（例如 .sla、.story、.blend、科学格式）：完全支持存储/同步，但预览/编辑取决于安装的应用或外部工具。
- **预览和缩略图**（服务器端生成）：
  - 默认启用：图像、文本文件。
  - 可选（为性能/安全在配置中启用）：PDF、SVG、Office 文档（通过 preview providers）、视频（需要 ffmpeg）、音频波形。
  - 通过社区应用或内置工具支持多种格式（例如 LibreOffice 用于文档预览）。
- **编辑/协作**：
  - Text/Markdown → 内置 Nextcloud Text。
  - Office 文档 → 集成 OnlyOffice 或 Collabora Online（实时协同编辑）。
  - 较新功能（2025–2026 年）：内置文档转换（PDF ↔ DOCX 等）、Text 中的 LaTeX 支持、高级 XLSX 表格样式。
- **黑名单**：管理员可通过 `occ config:app:set files blacklisted_files --value="[\".htaccess\",\".htpasswd\"]"` 或类似命令阻止危险扩展（例如 .exe、.bat）。

简而言之：上传和同步任何合理文件。图像、PDF、Office 文件、视频和文本的预览/编辑效果出色。

从小规模开始（仅 Files + 客户端），然后根据需要扩展应用。社区（help.nextcloud.com、GitHub）和 docs.nextcloud.com 是优秀资源。

参考资料：

- [Nextcloud Official Documentation](https://docs.nextcloud.com/)
- [Nextcloud Download & Clients](https://nextcloud.com/install/)
- [System Requirements](https://docs.nextcloud.com/server/stable/admin_manual/installation/system_requirements.html)
- [Previews Configuration](https://docs.nextcloud.com/server/stable/admin_manual/configuration_files/previews_configuration.html)
- [Desktop Client Manual](https://docs.nextcloud.com/server/latest/user_manual/en/desktop/index.html)
- [Files & Sync](https://docs.nextcloud.com/server/latest/user_manual/en/files/desktop_mobile_sync.html)

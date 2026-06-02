---
audio: false
generated: true
image: false
lang: en
layout: post
title: Comprehensive Guide to Using Nextcloud
translated: false
type: note
---

Question: Provide a comprehensive guide to using Nextcloud, including the server, clients, and supported file types.

Answer:

Here is a comprehensive, up-to-date (as of March 2026) guide to **Nextcloud**, covering server setup basics, client usage (desktop and mobile), core features, and supported file types. Nextcloud is a powerful open-source, self-hosted platform for file sync, sharing, collaboration, calendars, contacts, and more.

### 1. Server Installation and Setup
Nextcloud Server runs on Linux (recommended), with support for other platforms via Docker or manual setup.

**Recommended system requirements (2026):**
- **OS**: Ubuntu 24.04 LTS (strongly recommended), Ubuntu 22.04 LTS, Red Hat Enterprise Linux 9, Debian 12, openSUSE Leap 15.6, etc. (64-bit only for best performance).
- **Database**: MariaDB 10.11 (recommended) or MySQL 8.4, PostgreSQL 15–17, SQLite (only for testing).
- **PHP**: 8.2 or 8.3 (8.3 recommended).
- **Web server**: Apache 2.4 (with mod_php or php-fpm) or Nginx with php-fpm.
- **CPU/RAM**: At least 2 cores and 4 GB RAM for small/medium use; more for heavy collaboration or many users.

**Easiest installation methods (2025–2026):**
- **Docker (recommended for home/self-hosted users)**: Use the official `nextcloud` Docker image with `docker-compose`. Example basic `docker-compose.yml`:
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
  Run with `docker compose up -d`, then visit `http://your-ip:8080` to complete the web installer.

- **Manual install on Ubuntu**: Follow the official guide — install LAMP/LEMP stack, download the latest `.tar.bz2` from nextcloud.com, extract to web root, set permissions, run the web installer.

- After installation: Create an admin account, configure trusted domains, enable HTTPS (via Let's Encrypt + Caddy/Nginx/Apache), set up background jobs (cron), and enable apps like Calendar, Contacts, Talk, Text, etc. from the Apps store.

### 2. Clients (Desktop and Mobile)
Nextcloud provides official sync clients for seamless file access and synchronization.

**Desktop Client (Windows, macOS, Linux):**
- Download from: https://nextcloud.com/install/#install-clients (latest ~v4.0.x in 2026).
- Supported: Windows 10+ (64-bit), macOS 12.0+ (64-bit), Linux (AppImage works on most distros, e.g., Ubuntu 22.04+).
- Setup:
  1. Install and launch the client.
  2. Enter your Nextcloud server URL (e.g., https://cloud.yourdomain.com).
  3. Log in with your username and password (or use app password for security).
  4. Choose folders to sync (selective sync available — only sync what you need).
  5. Virtual file support on Windows/macOS (files appear locally but download on open — saves space).
- Features: Two-way sync, conflict handling, versioning, activity feed, sharing from desktop.

**Mobile Clients (Android & iOS):**
- Download: "Nextcloud" app from Google Play or Apple App Store.
- Setup: Same as desktop — add server URL, login.
- Key features: Auto-upload photos/videos, instant upload, offline access, background sync, end-to-end encryption support.
- Additional: Nextcloud Talk app for chat/video calls (separate or integrated).

### 3. Core Features and Usage
- **Web Interface**: Access via browser — Files app for upload/download/share, preview many file types, create/edit documents (with Text/OnlyOffice/Collabora), share links (password, expiration, edit permissions).
- **Sharing**: Internal (users/groups), external public links, federated sharing (with other Nextcloud instances).
- **End-to-End Encryption (E2EE)**: Enable for folders — only you can decrypt (client-side).
- **Versions & Trashbin**: Automatic file versioning, deleted files go to trash (configurable retention).
- **Apps Ecosystem**: Thousands of apps — Deck (Kanban), Notes, Tasks, Calendar, Contacts, Mail, News, Photos (with face recognition), etc.
- **Search & Tags**: Full-text search, smart tags, quick access shortcuts.
- **Security**: 2FA, brute-force protection, rate limiting, audit logs.

### 4. Supported File Types
Nextcloud supports virtually **any file type** for storage and sync — there are no hard restrictions on upload (except admin-configurable blacklists or size limits).

**Key highlights:**
- **All common formats** work without issues: documents (.docx, .xlsx, .pptx, .odt, .ods, .pdf), images (.jpg, .png, .gif, .webp, .heic), audio (.mp3, .wav, .flac, .m4a), video (.mp4, .mkv, .mov, .avi), archives (.zip, .rar, .7z), code (.py, .js, .cpp, .md), etc.
- Special/niche files (e.g., .sla, .story, .blend, scientific formats): Fully supported for storage/sync, but previews/editing depend on installed apps or external tools.
- **Previews & thumbnails** (generated server-side):
  - Enabled by default: Images, text files.
  - Optional (enable in config for performance/security): PDF, SVG, Office documents (via preview providers), videos (requires ffmpeg), audio waveforms.
  - Many formats supported via community apps or built-in tools (e.g., LibreOffice for document previews).
- **Editing/Collaboration**:
  - Text/Markdown → built-in Nextcloud Text.
  - Office docs → integrate OnlyOffice or Collabora Online (real-time co-editing).
  - Newer features (2025–2026): Built-in document conversion (PDF ↔ DOCX, etc.), LaTeX support in Text, advanced XLSX table styling.
- **Blacklisting**: Admins can block dangerous extensions (e.g., .exe, .bat) via `occ config:app:set files blacklisted_files --value="[\".htaccess\",\".htpasswd\"]"` or similar.

In short: Upload and sync anything reasonable. Previews/editing shine for images, PDFs, Office files, videos, and text.

Start small (just Files + clients), then expand with apps as needed. The community (help.nextcloud.com, GitHub) and docs.nextcloud.com are excellent resources.

References:

- [Nextcloud Official Documentation](https://docs.nextcloud.com/)
- [Nextcloud Download & Clients](https://nextcloud.com/install/)
- [System Requirements](https://docs.nextcloud.com/server/stable/admin_manual/installation/system_requirements.html)
- [Previews Configuration](https://docs.nextcloud.com/server/stable/admin_manual/configuration_files/previews_configuration.html)
- [Desktop Client Manual](https://docs.nextcloud.com/server/latest/user_manual/en/desktop/index.html)
- [Files & Sync](https://docs.nextcloud.com/server/latest/user_manual/en/files/desktop_mobile_sync.html)

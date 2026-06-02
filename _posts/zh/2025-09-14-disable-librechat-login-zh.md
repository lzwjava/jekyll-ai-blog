---
audio: false
date: 2025-09-14
generated: true
image: false
lang: zh
layout: post
model: mistralai/mistral-medium-3.1
title: 禁用LibreChat登录验证
translated: true
type: note
---

要让 **LibreChat** 无需频繁登录（或完全禁用登录）即可工作，您可以调整身份验证设置。以下是解决问题的步骤：

---

### **1. 禁用身份验证（无需登录）**
如果您希望 **LibreChat 完全开放**（完全不需要登录），请修改配置：

#### **选项 A：环境变量（推荐）**
在您的 `.env` 文件（或环境变量）中设置以下内容：
```env
# 完全禁用身份验证
AUTHENTICATION=false
```
然后重启 LibreChat：
```bash
docker compose down && docker compose up -d  # 如果使用 Docker
# 或
npm run build && npm run start  # 如果在本地运行
```

#### **选项 B：修改 `config.yaml`**
如果您使用 `config.yaml` 文件，请添加：
```yaml
auth:
  enabled: false
```

---

### **2. 修复频繁退出问题（如果仍需要登录）**
如果您**希望保留身份验证**但解决频繁退出问题，请尝试以下解决方案：

#### **A. 增加会话/Cookie 过期时间**
在 `.env` 中修改会话设置：
```env
# 延长会话超时时间（以秒为单位，例如 7 天 = 604800）
SESSION_EXPIRY=604800

# 确保 Cookie 安全（如果使用 HTTPS）
COOKIE_SECURE=true  # 如果在 HTTP 上测试，设置为 false
COOKIE_SAME_SITE=lax
```

#### **B. 使用持久化会话存储**
默认情况下，LibreChat 可能使用内存会话（重启后重置）。切换到**数据库支持的会话存储**（例如 Redis 或 PostgreSQL）：

1. **安装 Redis**（如果尚未安装）：
   ```bash
   docker run -d --name redis -p 6379:6379 redis
   ```
2. 更新 `.env`：
   ```env
   SESSION_STORE=redis
   REDIS_URL=redis://localhost:6379
   ```

#### **C. 检查反向代理设置（如果使用 Nginx/Apache）**
如果您使用代理（例如 Nginx），请确保：
- Cookie 被正确转发。
- `ProxyPass` 包含 `cookie` 指令。

Nginx 配置示例：
```nginx
location / {
    proxy_pass http://localhost:3080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_cookie_path / /;  # 确保 Cookie 作用域正确
}
```

#### **D. 清除浏览器缓存并在无痕模式下测试**
有时，浏览器缓存/损坏的 Cookie 会导致问题。请尝试：
- 清除 `librechat.example.com` 的 Cookie。
- 在**无痕模式**或不同浏览器中测试。

---

### **3. 调试 Cookie 问题**
如果 Cookie 仍然无法持久化：
1. **检查浏览器开发者工具**（`F12` > **Application** > **Cookies**）查看是否设置了 `connect.sid`（或类似内容）。
2. **验证 `SameSite` 属性**（应为 `Lax`，如果是跨站则为 `None`）。
3. **确保 `Domain` 正确**（例如，子域名使用 `.example.com`）。

---

### **4. 更新 LibreChat**
如果您使用的是旧版本，新版本可能已修复错误：
```bash
git pull origin main
docker compose down && docker compose up -d --build
```

---

### **最后说明**
- **安全警告**：禁用身份验证（`AUTHENTICATION=false`）会使 LibreChat **公开可访问**。请仅在受信任/内部网络中执行此操作。
- **需要 HTTPS**：如果使用 Cookie，请确保您的站点使用 **HTTPS**（或在测试时设置 `COOKIE_SECURE=false`）。

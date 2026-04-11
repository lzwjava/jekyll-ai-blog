---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信域名验证指南
translated: true
type: note
---

问题：如何为我的博客创建并部署微信验证文件？微信在什么情况下需要这种验证？

回答：

## 1. 需要做什么

你会拿到类似这样的文件：

```
198976a221b3bd8c.txt
```

其内容为：

```
5354e
```

这是微信所需的**域名所有权验证文件**。

### ✅ 逐步操作

#### 第一步 — 在本地创建文件

进入你的代码仓库（`/Users/lzwjava/projects/lzwjava.github.io`）：

```bash
cd /Users/lzwjava/projects/lzwjava.github.io

echo "5354e" > 198976a221b3bd8c.txt
```

#### 第二步 — 放置在根目录

确保文件位于**部署站点的根目录**，而不是子文件夹内：

```
lzwjava.github.io/
├── index.html
├── 198976a221b3bd8c.txt   ✅ 必须在此处
├── ...
```

#### 第三步 — 提交并推送

```bash
git add 198976a221b3bd8c.txt
git commit -m "添加微信验证文件"
git push
```

你的 GitHub Pages 工作流程（`.github/workflows/gh-pages.yml`）会自动将其部署。

---

## 2. 验证部署

部署后，请测试：

```
https://lzwjava.github.io/198976a221b3bd8c.txt
```

它应精确返回：

```
5354e
```

⚠️ 不应有 HTML、格式问题，理想情况下也不应有换行符问题。

---

## 3. GitHub Pages 重要细节

检查你的工作流程（`gh-pages.yml`），确保：

* 它没有排除 `.txt` 文件
* 它复制**所有根目录文件**到最终的构建输出中

如果你使用静态站点生成器（如 Jekyll、Hexo 等）：

* 将文件放在：

  * `public/` (Hexo)
  * `_site/` (Jekyll 输出目录)
  * 或根静态文件夹

例如，对于 Hexo：

```bash
cp 198976a221b3bd8c.txt source/
```

---

## 4. 微信何时需要此文件？

微信在以下几种场景中需要此验证：

### 1. 微信公众号

当你：

* 将**网站域名**绑定到你的公众号
* 启用如下的功能：

  * JS-SDK（分享、支付）
  * OAuth 登录

👉 他们必须确认你**拥有该域名**

---

### 2. 微信开放平台

当配置：

* 网站应用登录
* UnionID 系统
* 第三方集成

---

### 3. 微信小程序

当使用：

* Web-view 页面
* 业务域名配置

---

### 4. 微信支付

当设置：

* 支付回调 URL
* API 端点

---

## 5. 为何采用此方法？

微信使用这种简单方法是因为：

* 无需 DNS 访问权限
* 易于验证所有权
* 类似于：

  * Google Search Console
  * Cloudflare 域名验证

---

## 6. 常见错误（非常重要）

* ❌ 将文件放在子目录中（如 `/assets/` 等）
* ❌ 文件内容不匹配（多余的空格或换行符）
* ❌ 无法公开访问（私有仓库或被阻止）
* ❌ 使用错误的域名（如 `www` 与非 `www`）
* ❌ GitHub Pages 缓存延迟（等待 1-2 分钟）

---

## 7. 快速检查清单

* 文件存在于根目录 ✅
* 内容完全匹配 ✅
* 可通过 URL 访问 ✅
* HTTPS 正常工作 ✅

---

如果你需要，我还可以：

* 检查你的 `gh-pages.yml`，确保不会删除该文件
* 帮助在 CI/CD 过程中自动化注入验证文件
* 或设置多域名验证策略（适用于通过微信类似 SEO 的分发方式扩展流量）
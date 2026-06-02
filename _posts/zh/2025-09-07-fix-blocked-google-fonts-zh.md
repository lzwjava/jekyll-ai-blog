---
audio: false
date: 2025-09-07
generated: true
image: false
lang: zh
layout: post
title: 修复被屏蔽的谷歌字体请求
translated: true
type: note
---

该请求是您的页面尝试从 Google Fonts 加载网络字体样式表：

* **它是什么：** `https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap` 是定义 **Open Sans** 字体外观的 CSS。您的主题或自定义 CSS 包含了它，以便网站可以使用 Open Sans 字体渲染。
* **为什么您看到 "Status: — / 0 B / no headers"：** 当请求被**阻止或取消**时（例如，被广告/隐私拦截器、严格的 Content-Security-Policy、不稳定的网络或国家级阻止），DevTools 会显示此状态。页面仍然*尝试*请求它，因此网络行中会有记录。

### 在 Jekyll 博客中它可能来自哪里

通常是以下情况之一：

1. **主题在 `<head>` 中包含它**
   在 `_layouts/default.html` 或 `_includes/head.html` 中（或者如果您使用 `remote_theme`，则在主题的等效文件中）查找类似这样的行：
   `<link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap" rel="stylesheet">`

2. **SCSS 导入了它**
   在 `/assets/css/*.scss` 或 `/_sass/**` 中检查是否有：
   `@import url("https://fonts.googleapis.com/css?family=Open+Sans:400,700&display=swap");`

3. **远程主题**（例如 jekyll-theme-cayman）在其 head include 中硬编码了 Google Fonts。在您的仓库中覆盖主题的 head/layout 将允许您移除它。

### 如何快速找到它

在您的站点仓库根目录下，尝试以下任一命令：

```
rg -n "fonts.googleapis.com"
rg -n "Open Sans"
rg -n "display=swap"
```

### 修复或更改它的选项

**A) 移除 Google Fonts 并使用系统字体栈（最快且对隐私友好）**

1.  删除引入 Google Fonts 的 `<link>`（或 SCSS 的 `@import`）。
2.  在您的主样式表中，设置一个系统字体栈：

    ```css
    html, body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Ubuntu,
                   "Helvetica Neue", Arial, "Noto Sans", sans-serif,
                   "Apple Color Emoji", "Segoe UI Emoji";
    }
    ```

    （在 Jekyll 中，将其放入 `assets/css/style.scss` 中，并在文件顶部包含 front-matter `---` 行。）

**B) 保留 Open Sans 但自行托管**

1.  下载 Open Sans（400 & 700）的 WOFF2 文件，并将其放在 `assets/fonts/` 目录下。
2.  添加到您的 CSS 中：

    ```css
    @font-face {
      font-family: "Open Sans";
      font-style: normal;
      font-weight: 400;
      font-display: swap;
      src: url("/assets/fonts/OpenSans-400.woff2") format("woff2");
    }
    @font-face {
      font-family: "Open Sans";
      font-style: normal;
      font-weight: 700;
      font-display: swap;
      src: url("/assets/fonts/OpenSans-700.woff2") format("woff2");
    }
    body { font-family: "Open Sans", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
    ```
3.  移除 Google Fonts 的 `<link>`/`@import`。

**C) 保持原样但阻止请求失败**

*   为您的站点禁用拦截扩展，或者放宽您的 CSP 以允许 `https://fonts.googleapis.com` 和 `https://fonts.gstatic.com`。
*   如果您所在的地区这些域名被阻止，建议选择方案 A 或 B。

### Jekyll 特定的覆盖技巧

*   **远程主题：** 将主题的 `/_includes/head.html` 或 `/_layouts/default.html` 复制到您的仓库中的相同路径，移除 Google Fonts 行，Jekyll 将使用您的覆盖版本。
*   **压缩的 head include：** 有时主题通过变量注入字体。如果是这样，将该变量设置为空或覆盖 include 以排除字体。

如果您提供您的主题名称（或您的 `_config.yml` 中的 `theme` / `remote_theme`），我可以指出需要覆盖的确切文件以及最小的差异。

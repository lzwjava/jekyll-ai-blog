---
audio: false
generated: true
lang: zh
layout: post
title: 使用组织托管多个GitHub Pages站点
translated: true
type: note
---

是的，创建 GitHub 组织确实是托管额外 GitHub Pages 站点并获取唯一 `*.github.io` 子域的有效方式，因为每个组织都可以拥有独立的 `organization.github.io` 站点，与您的个人 `username.github.io` 站点互不干扰。以下是具体操作方法和注意事项：

### 核心要点

- **个人账户限制**：每个 GitHub 用户账户只能拥有一个用户站点，托管在 `username.github.io`，且必须绑定名为 `username.github.io` 的仓库。若已使用该功能，则无法在同一账户下创建其他 `*.github.io` 子域。
- **组织站点**：每个 GitHub 组织同样可拥有组织站点，通过创建名为 `organization.github.io` 的仓库即可获得 `organization.github.io` 子域。通过设立多个组织，即可创建更多 `*.github.io` 子域。
- **项目站点**：虽然用户和组织账户均可通过其他仓库托管多个项目站点（如 `username.github.io/project` 或 `organization.github.io/project`），但这些均为子路径而非子域。若需真正的子域（如 `sub.example.github.io`），则必须使用自定义域名，因为 GitHub 不支持在 `github.io` 下创建自定义子域。

### 通过创建 GitHub 组织获取额外 `*.github.io` 子域的步骤

1. **创建 GitHub 组织**：
   - 登录 GitHub 账户
   - 点击右上角 "+" 图标选择 **New organization**
   - 按指引创建组织并设定唯一名称（如 `myorg`），该名称将决定子域名（如 `myorg.github.io`）
   - 注意：可免费创建组织，但部分功能（如私有仓库）可能需要付费计划。公开仓库的 GitHub Pages 服务在 GitHub Free 中可用

2. **创建组织的 GitHub Pages 仓库**：
   - 在新组织中创建严格命名为 `myorg.github.io` 的仓库（将 `myorg` 替换为实际组织名）
   - 此仓库将托管组织站点，可通过 `https://myorg.github.io` 访问

3. **配置 GitHub Pages**：
   - 进入 `myorg.github.io` 仓库的 **Settings** 标签页
   - 滚动至 **Pages** 区域
   - 在 **Source** 下选择要发布的分支（如 `main` 或 `gh-pages`）并保存
   - 配置完成后，站点将在几分钟内上线于 `https://myorg.github.io`

4. **添加内容**：
   - 在发布分支中添加 `index.html` 文件或使用静态站点生成器（如 Jekyll）
   - 提交并推送更改，例如：

     ```bash
     git clone https://github.com/myorg/myorg.github.io
     cd myorg.github.io
     echo "Hello World" > index.html
     git add --all
     git commit -m "Initial commit"
     git push origin main
     ```

   - 访问 `https://myorg.github.io` 验证站点是否生效

5. **重复操作获取更多子域**：
   - 创建更多组织（如 `myorg2`、`myorg3`）并重复上述流程，即可获得 `myorg2.github.io`、`myorg3.github.io` 等子域
   - 每个组织均可拥有一个 `*.github.io` 子域，只要创建足够多的组织即可获得大量子域

### 限制与注意事项

- **github.io 上的自定义子域**：无法直接通过 GitHub Pages 创建类似 `sub.myorg.github.io` 的子域。`github.io` 域名由 GitHub 管理，仅支持 `username.github.io` 或 `organization.github.io` 格式。若需使用自定义子域（如 `blog.example.com`），必须拥有自定义域名并通过 DNS 设置（CNAME 记录）指向 `myorg.github.io`
- **单仓库对应单子域**：每个 `*.github.io` 子域仅能绑定一个仓库（`username.github.io` 或 `organization.github.io`）。若需从单一仓库提供多个子域服务，必须使用自定义域名并借助额外托管或代理服务
- **管理开销**：每个组织都需要独立管理（成员、权限、计费等），请确保能够妥善管理多个组织
- **DNS 与自定义域名**：若想使用自定义域名（如 `example.com` 或 `sub.example.com`）替代 `*.github.io`，需在仓库的 **Pages** 设置中配置域名，并在 DNS 服务商处添加 CNAME 记录。例如将 `sub.example.com` 指向 `myorg.github.io`。务必验证域名以防被劫持
- **私有仓库**：私有仓库的 GitHub Pages 功能需要 GitHub Pro、Team 或 Enterprise 计划。若使用免费计划，请确保 `myorg.github.io` 仓库为公开状态

### 多子域替代方案

若需要在单一自定义域名下配置多个子域（如 `blog.example.com`、`shop.example.com`）：

1. 从域名注册商（如 Namecheap 或 GoDaddy）购买自定义域名（如 `example.com`）
2. 在组织中创建多个仓库（如 `myorg/blog`、`myorg/shop`）
3. 为每个仓库启用 GitHub Pages，并在各自的 **Pages** 设置中配置自定义域名（如 `blog.example.com` 和 `shop.example.com`）
4. 通过 DNS 服务商配置 CNAME 记录，将 `blog.example.com` 和 `shop.example.com` 均指向 `myorg.github.io`。注意：未配置独立自定义域名的仓库会以子路径形式出现在组织域名下（如 `example.com/blog`）
5. 需注意 GitHub Pages 原生不支持从单一仓库提供多子域服务，可能需要 CDN 或反向代理等外部服务

### 示例场景

- 已使用 `username.github.io` 作为个人站点
- 创建名为 `myorg` 的组织及 `myorg.github.io` 仓库，获得 `myorg.github.io`
- 创建名为 `myorg2` 的组织及 `myorg2.github.io` 仓库，获得 `myorg2.github.io`
- 若需自定义子域：拥有 `example.com` 域名后，通过 CNAME 记录设置 `blog.example.com`（指向 `myorg.github.io`）和 `shop.example.com`（指向 `myorg2.github.io`）

### 最终提醒

- 创建多个组织是获取额外 `*.github.io` 子域最直接的方式，无需自定义域名
- 若需要真实子域（如 `sub.myorg.github.io`），必须使用自定义域名并进行 DNS 配置，因为 GitHub 的 `github.io` 不原生支持此功能
- 始终验证自定义域名以避免域名被劫持等安全风险
- DNS 更改可能需长达 24 小时才能全局生效

如有更多疑问或需要具体配置帮助，欢迎随时提出！

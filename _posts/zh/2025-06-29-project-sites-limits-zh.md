---
audio: false
generated: true
lang: zh
layout: post
title: GitHub Pages 项目站点网址规则
translated: true
type: note
---

借助 GitHub Pages，除了用户站点（`username.github.io`）外，您还可以在个人账户下创建**项目站点**。不过，项目站点的 URL 格式仅限于特定模式，并非所有子域名或子路径配置都原生支持。我们来探讨您关于能否对项目站点使用 `username.github.io/project1` 或 `project1.username.github.io` 的问题。

### 关键要点
- **用户站点**：名为 `username.github.io` 的单一仓库，其内容托管在 `https://username.github.io`。
- **项目站点**：您个人账户中的任何其他仓库均可配置为项目站点，通过 `https://username.github.io/仓库名称`（子路径形式，而非子域名）访问。
- **子域名限制**：GitHub Pages 不原生支持像 `project1.username.github.io` 这样的子域名。`github.io` 域名由 GitHub 管理，只有 `username.github.io`（针对用户）或 `organization.github.io`（针对组织）可以作为顶级子域名。像 `project1.username.github.io` 这样的自定义子域名需要自定义域名和 DNS 配置。

### 能否使用 `username.github.io/project1`？
**可以**，您可以将 `username.github.io/project1` 用于项目站点。这是 GitHub Pages 处理项目站点的标准方式：
- 在您的个人账户下创建一个仓库（例如 `username/project1`）。
- 为该仓库启用 GitHub Pages：
  - 转到仓库的 **Settings** 标签页。
  - 滚动到 **Pages** 部分。
  - 在 **Source** 下，选择要发布的分支（例如 `main` 或 `gh-pages`）并保存。
- 配置完成后，站点即可通过 `https://username.github.io/project1` 访问。
- 您可以通过在更多仓库（`username/project2`、`username/project3` 等）上启用 GitHub Pages 来创建多个项目站点（例如 `username.github.io/project2`、`username.github.io/project3`）。
- **内容**：在每个仓库的发布分支中添加 `index.html` 或使用像 Jekyll 这样的静态站点生成器。

### 能否使用 `project1.username.github.io`？
**不行**，GitHub Pages 不原生支持在 `github.io` 域名下使用像 `project1.username.github.io` 这样的子域名。`github.io` 域名仅允许：
- `username.github.io` 用于用户站点。
- `organization.github.io` 用于组织站点。
- 像 `username.github.io/仓库名称` 这样的子路径用于项目站点。

要实现像 `project1.username.github.io` 这样的 URL，您需要：
1. **自定义域名**：从域名注册商（如 Namecheap 或 GoDaddy）购买一个域名（例如 `example.com`）。
2. **DNS 配置**：设置 CNAME 记录，将一个子域名（例如 `project1.example.com`）指向您的 GitHub Pages 站点（例如 `username.github.io` 或 `username.github.io/project1`）。
3. **GitHub Pages 设置**：
   - 在仓库的 **Pages** 设置中，配置自定义域名（例如 `project1.example.com`）。
   - 可选地，启用“Enforce HTTPS”以增强安全性。
4. **结果**：您可以将 `project1.example.com` 映射到 `project1` 仓库的内容，但无法映射到 `project1.username.github.io`，因为 GitHub 控制着 `github.io` 域名，不允许在其下创建自定义子域名。

### `username.github.io/project1` 的设置示例
1. 在您的账户下创建一个名为 `project1` 的仓库（`username/project1`）。
2. 添加内容（例如 `index.html`）：
   ```bash
   git clone https://github.com/username/project1
   cd project1
   echo "Hello from Project 1" > index.html
   git add --all
   git commit -m "Initial commit"
   git push origin main
   ```
3. 启用 GitHub Pages：
   - 转到 `username/project1` → **Settings** → **Pages**。
   - 将源设置为 `main`（或其他分支）并保存。
4. 访问 `https://username.github.io/project1` 查看实时站点（可能需要几分钟才能生效）。

### 使用自定义域名的自定义子域名示例
如果您想要 `project1.example.com`：
1. 拥有一个域名（例如 `example.com`）。
2. 在您的 DNS 提供商设置中，添加一条 CNAME 记录：
   - 名称：`project1`
   - 值：`username.github.io`
3. 在 `project1` 仓库的 **Pages** 设置中，将自定义域名设置为 `project1.example.com`。
4. 将内容推送到 `project1` 仓库，它将在 `project1.example.com` 上提供服务。

### 限制
- **仅支持 `github.io` 的子路径**：在没有自定义域名的情况下，项目站点始终以子路径形式（`username.github.io/project1`）提供服务，而非子域名（`project1.username.github.io`）。
- **一个用户站点**：您的 `username.github.io` 仓库专用于您的用户站点。项目站点使用其他仓库，并显示为子路径。
- **自定义子域名需要自定义域名**：要获得 `project1.something`，您需要拥有 `something`（例如 `example.com`）并配置 DNS。
- **私有仓库**：私有仓库中的项目站点需要 GitHub Pro、Team 或 Enterprise 计划。对于免费账户，仓库必须公开。

### 总结
- **使用 `username.github.io/project1`**：可以，这是原生支持的，只需创建一个仓库（`username/project1`）并启用 GitHub Pages。您可以通过这种方式创建多个项目站点（例如 `username.github.io/project2` 等）。
- **使用 `project1.username.github.io`**：不行，这在 `github.io` 下不受支持。您需要自定义域名（例如 `project1.example.com`）和 DNS 设置才能达到类似效果。
- **多个子域名**：要获得多个 `*.github.io` 子域名，可以创建 GitHub 组织（如前所述）以使用 `org1.github.io`、`org2.github.io` 等，或者使用自定义域名来创建像 `project1.example.com` 这样的子域名。

如果您需要帮助设置特定的项目站点、配置自定义域名或管理多个站点，请告诉我！

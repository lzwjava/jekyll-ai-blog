---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 配置 RubyGems 代理设置
translated: true
type: note
---

为确保 `gem`（RubyGems）在安装过程中使用您的代理（例如位于 `http://127.0.0.1:7890`），请按照以下步骤操作。根据您分享的详细输出，它*似乎已经在使用代理*——输出中的“正在连接 127.0.0.1:7890... 已连接”这一行是底层 HTTP 客户端（可能是 `net/http` 或类 `curl` 的详细模式）的明确指示。

### 1. **配置代理（如果尚未设置）**

- **选项 A：使用环境变量（推荐用于一次性或 sudo 命令）**
     这些变量会告知 `gem` 通过代理路由流量。在安装前运行：

     ```
     export http_proxy=http://127.0.0.1:7890
     export https_proxy=http://127.0.0.1:7890
     sudo -E gem install jekyll bundler --verbose
     ```

  - `-E` 标志在使用 `sudo` 时保留您的环境变量。
  - 如需持久化设置，请将 `export` 行添加到您的 `~/.bashrc` 或 `~/.profile`。

- **选项 B：在 `~/.gemrc` 中配置（用户级别，未来安装无需 sudo）**
     创建或编辑 `~/.gemrc`：

     ```
     echo 'http_proxy: http://127.0.0.1:7890' >> ~/.gemrc
     echo 'https_proxy: http://127.0.0.1:7890' >> ~/.gemrc
     ```

     然后运行 `gem install jekyll bundler --verbose`（尽可能不使用 `sudo`——`sudo` 可能会忽略用户配置）。如果必须使用 `sudo`，请坚持使用选项 A。

### 2. **验证是否使用代理**

- **使用 `--verbose` 运行（如您所做）**：查找类似以下的行：
  - `HEAD https://index.rubygems.org/` 后跟代理连接详情。
  - `正在连接 127.0.0.1:7890... 已连接。`（这确认了代理使用）。
  - 如果显示直接连接到 `rubygems.org`（例如，提及 IP 地址但没有代理信息），则表示它绕过了代理。

- **使用试运行或信息获取进行测试**：

     ```
     gem fetch jekyll --verbose --platform=ruby
     ```

     或者仅查询索引：

     ```
     gem search jekyll --verbose
     ```

     检查输出中是否有代理连接。

- **检查环境变量**：

     ```
     echo $http_proxy $https_proxy
     ```

     如果它们设置正确，`gem` 应该会继承它们。

- **使用 `gem env` 进行调试**：

     ```
     gem env
     ```

     在 "HTTP Proxy" 或 "HTTPS Proxy" 部分查找您的代理 URL。

### 故障排除

- **如果 sudo 忽略了代理**：使用 `sudo -E` 或不使用 `sudo` 运行（安装到用户目录：`gem install --user-install jekyll bundler`）。
- **没有连接信息？** 您的代理可能未启用详细模式，或者环境变量未设置。单独测试代理：`curl -v https://rubygems.org/`（应显示代理跳转）。
- **企业/严格代理？** 如果需要认证，请使用 `http://user:pass@127.0.0.1:7890`。
- **仍然失败？** 暂时禁用代理（`unset http_proxy https_proxy`）并重试——如果禁用后工作，则是配置问题；如果仍然失败，请检查您的代理服务器（例如 Clash/V2Ray 日志）。

您的安装已成功（200 OK 响应），所以您很可能没问题——只需确认下次运行时显示代理连接以安心。如果您分享更多输出，我可以进一步调试！

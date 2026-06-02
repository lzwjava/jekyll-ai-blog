---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 在 Ubuntu 系统上安装 Jekyll
translated: true
type: note
---

### 在 Ubuntu 上安装和运行 Jekyll

根据你遇到的错误（“未找到 'bundle' 命令”）以及你尝试运行的命令，看起来你需要先正确安装 Ruby、Bundler 和 Jekyll。Ubuntu 默认不包含这些工具，但按照官方 Jekyll 指南安装非常简单。我将逐步带你完成完整设置流程，然后说明如何运行你的具体命令。

#### 第一步：安装系统依赖

打开终端并运行以下命令安装 Ruby 和构建工具（这会通过 `ruby-full` 安装 Ruby 3.x）：

```bash
sudo apt update
sudo apt install ruby-full build-essential zlib1g-dev
```

- 这会设置 Ruby 环境（可通过 `ruby -v` 验证——应显示类似 3.0+ 的版本号）
- 如果你使用的是较新的 Ubuntu 系统（如 22.04+），此方法可直接使用。请尽量避免通过 Snap 安装 Ruby，可能引发路径问题

#### 第二步：设置用户 Gem 目录（推荐避免使用 Sudo）

为避免后续出现权限错误，建议在用户目录安装 gems：

```bash
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

- 验证设置：运行 `gem env`——应显示 `GEM_HOME` 为 `~/gems`

#### 第三步：安装 Jekyll 和 Bundler

现在安装核心工具：

```bash
gem install jekyll bundler
```

- 这会将 `gem`、`jekyll` 和 `bundle` 命令添加到你的路径中
- 如果遇到权限错误，请重新检查第二步或临时使用 `sudo`（但不建议长期使用）

#### 第四步：创建并运行博客

现在你可以运行代码片段中的命令了。以下是详细说明：

1. **创建新 Jekyll 站点**：

   ```bash
   jekyll new myblog
   ```

   - 这会在 `myblog` 文件夹中生成基础站点结构

2. **进入目录**：

   ```bash
   cd myblog
   ```

3. **安装依赖**（这里原本的 `bundle install` 会失败——现在应该能正常运行）：

   ```bash
   bundle install
   ```

   - 这会拉取 Jekyll 插件等 gems

4. **启动本地服务**（在 <http://127.0.0.1:4000> 启动本地服务器）：

   ```bash
   bundle exec jekyll serve
   ```

   - 在浏览器中访问该 URL 即可查看站点

5. **启用增量重建模式**（开发时更快速，仅重建更改的文件）：

   ```bash
   bundle exec jekyll serve --incremental
   ```

6. **显示草稿文章**：

   ```bash
   bundle exec jekyll serve --draft
   ```

7. **解决 "webrick" 错误**（Ruby 3+ 常见问题，因为默认未捆绑）：

   ```bash
   bundle add webrick
   ```

   - 然后重启服务：`bundle exec jekyll serve`
   - 或者将 `gem "webrick"` 添加到 `Gemfile` 后运行 `bundle install`

8. **跳过 Bundler 快速启动**：

   ```bash
   jekyll serve
   ```

   - 但在项目中建议保持使用 `bundle exec` 以确保一致性

#### 故障排除

- **仍显示“bundle 未找到”？** 确保第二步已正确加载 `~/.bashrc`（执行 `source ~/.bashrc`），然后重启终端或运行 `hash -r`。可通过 `which bundle` 检查
- **gem 权限问题？** 坚持使用第二步中的用户目录设置
- **Ruby 版本过旧？** 如果 `ruby -v` 显示版本 <3.0，建议使用 rbenv 安装新版（通过 `curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash` 安装，然后执行 `rbenv install 3.2.0`）
- **防火墙阻止 4000 端口？** Ubuntu 通常不会，但可通过 `curl http://127.0.0.1:4000` 测试
- 你的项目位于 `~/projects/blog-source`——请在该目录下运行命令或调整路径

启动服务后，可以编辑 `_posts/` 或 `_config.yml` 中的文件并保存——Jekyll 会自动重建。生产环境部署时，使用 `jekyll build` 构建后部署到 GitHub Pages 或 Netlify。

[Jekyll Ubuntu 安装指南](https://jekyllrb.com/docs/installation/ubuntu/)

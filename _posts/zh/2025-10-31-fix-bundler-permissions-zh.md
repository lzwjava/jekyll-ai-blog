---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 修复 Bundler 权限错误
translated: true
type: note
---

### 理解错误原因

这是在使用 Bundler（Ruby 的依赖管理工具）与系统安装的 Ruby（此处为 3.2.0 版本）时常见的权限问题。该错误出现的原因是 Bundler 试图在系统级的 gem 目录 `/var/lib/gems/3.2.0/cache/` 中下载并缓存 `rake` gem（可能还有其他 gem），这需要 root 级别的写入权限。您的 Bundler 本身是安装在用户本地目录（位于 `~/.local/share/gem/`），但在安装时默认使用了系统的 gem 路径。

您 `Gemfile` 中的依赖链（Jekyll + 诸如 `minima`、`jekyll-feed` 等依赖项）只是触发了对 `rake` 作为深层依赖的安装——您的设置本身没有问题，仅仅是权限问题。

### 快速解决方案（按推荐顺序排列）

1. **本地安装 Gems（推荐 - 无需 Sudo）**
   这会将所有内容保留在您的用户主目录中，完全避开系统路径。运行：

   ```
   bundle config set --local path 'vendor/bundle'
   bundle install
   ```

   - 这会在您的项目中创建一个 `vendor/bundle` 文件夹用于存放 gems。
   - 之后要运行您的 Jekyll 站点，请使用 `bundle exec jekyll serve`（`exec` 确保其使用本地 gems）。
   - 如果您希望此设置对所有项目全局生效：将 `--local` 替换为 `--global`，并使用 `~/.bundle` 作为路径。

2. **使用 Sudo（快速但非理想方案）**
   如果您需要一次性安装且不介意系统级的 gems：

   ```
   sudo bundle install
   ```

   - **警告**：这会以 root 身份全局安装 gems，可能导致后续的所有权问题（例如，将来的更新也需要 `sudo`）。如有可能请避免使用。

3. **修复系统权限（高级 - 谨慎使用）**
   如果您希望在不使用 sudo 的情况下继续使用系统 gem 目录：

   ```
   sudo chown -R $USER:$USER /var/lib/gems/3.2.0/
   ```

   - 然后重试 `bundle install`。
   - **警告**：这会更改系统 gems 的所有权，可能破坏由您的发行版（例如 Ubuntu）管理的软件包。仅在您具备排查问题的能力时执行此操作。

### 长期建议

对于 Ruby/Jekyll 开发，建议切换到用户管理的 Ruby 安装程序，如 [rbenv](https://github.com/rbenv/rbenv) 或 [RVM](https://rvm.io/)。这通过将 Ruby 和 gems 完全安装在您的用户主目录中，避免了所有权限困扰：

- 安装 rbenv：遵循[官方指南](https://github.com/rbenv/rbenv#installation)。
- 然后执行：`rbenv install 3.2.0 && rbenv global 3.2.0 && gem install bundler`。
- 重试 `bundle install`——它将顺利运行。

如果以上方法均未解决问题或您遇到其他错误，请分享 `ruby -v`、`gem env` 以及您的 `Gemfile.lock`（如果存在）的输出，以便获得更有针对性的帮助！

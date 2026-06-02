---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 使用 Ruby on Rails
translated: true
type: post
---

在 ShowMeBug 的工作期间，我参与了企业微信集成项目。这涉及将 ShowMeBug 集成到企业微信中，提供在企业微信生态系统中无缝访问技术面试工具。我使用了 Ruby、Ruby on Rails、PostgreSQL 和微信 SDK 等技术，为面试官和候选人创建了流畅的用户体验。

这篇博客文章是在 2025 年 2 月左右由 AI 协助撰写的。

---

Ruby on Rails（通常简称“Rails”）是一个强大的基于 Ruby 编程语言的 Web 开发框架。它旨在通过强调约定优于配置和 DRY（不要重复自己）原则，使构建 Web 应用程序变得快速和愉快。让我们来看看如何设置它并创建一个简单的应用程序。

#### 第 1 步：安装 Ruby 和 Rails
首先，你需要安装 Ruby，因为 Rails 是一个 Ruby gem（库）。大多数系统都没有预装 Ruby，所以这里是如何设置它的：

- **在 macOS/Linux 上：**
  - 使用版本管理器如 `rbenv` 或 `rvm` 以获得灵活性。通过 Homebrew 安装它（`brew install rbenv`），然后运行：
    ```bash
    rbenv install 3.2.2  # 截至 2025 年的稳定 Ruby 版本
    rbenv global 3.2.2
    ```
  - 安装 Rails：
    ```bash
    gem install rails
    ```

- **在 Windows 上：**
  - 使用 RubyInstaller（从 rubyinstaller.org 下载）。选择一个带有 DevKit 的版本，如 3.2.2。
  - 安装 Ruby 后，打开命令提示符并运行：
    ```bash
    gem install rails
    ```

验证安装：
```bash
ruby -v  # 应显示类似于 ruby 3.2.2 的内容
rails -v # 应显示最新的 Rails 版本，例如 7.1.x
```

#### 第 2 步：创建一个新的 Rails 项目
安装 Rails 后，生成一个新的应用程序：
```bash
rails new myapp --database=sqlite3
cd myapp
```
这将创建一个名为 `myapp` 的文件夹，其中包含完整的 Rails 结构，使用 SQLite 作为默认数据库（适合开发）。

#### 第 3 步：启动服务器
运行内置的 Rails 服务器：
```bash
rails server
```
在浏览器中打开 `http://localhost:3000`。你将看到一个欢迎页面。恭喜，你的 Rails 应用程序正在运行！

#### 第 4 步：构建一些简单的内容
让我们创建一个基本的“Posts”功能，以了解 Rails 的 MVC（模型-视图-控制器）模式。

- **生成模型和控制器：**
  ```bash
  rails generate scaffold Post title:string body:text
  ```
  这将创建一个 `Post` 模型、数据库迁移、控制器和视图——所有这些都连接在一起。

- **运行迁移：**
  ```bash
  rails db:migrate
  ```
  这将为帖子设置数据库表。

- **查看它：**
  重新启动服务器（`rails server`）并访问 `http://localhost:3000/posts`。你将看到一个 CRUD 接口，用于创建、读取、更新和删除帖子。

#### 第 5 步：探索关键概念
- **路由：**打开 `config/routes.rb`。你将看到 `resources :posts`，它自动生成 RESTful 路由，如 `/posts/new` 或 `/posts/1/edit`。
- **控制器：**查看 `app/controllers/posts_controller.rb`。它处理请求和响应。
- **视图：**检查 `app/views/posts/`。这些是 ERB 模板（带有嵌入 Ruby 的 HTML）。
- **模型：**查看 `app/models/post.rb`。它与数据库相关联，并且可以包括验证（例如，`validates :title, presence: true`）。

#### 第 6 步：自定义和部署
- 在 `app/assets/stylesheets/` 中添加一些样式的 CSS。
- 对于生产环境，切换到 PostgreSQL（`rails new myapp --database=postgresql`）并部署到 Render 或 Heroku 等平台。在 `Gemfile` 中更新 `gem "pg"` 并运行 `bundle install`。

#### 专业技巧
- 使用 `rails console` 实时实验你的模型。
- 运行 `rails generate --help` 以查看 Rails 提供的所有快捷方式。
- 利用像 `devise` 这样的 gem 进行身份验证或 `pundit` 进行授权——将它们添加到你的 `Gemfile` 中并按需配置。

就是这样！你已经有一个基本的 Rails 应用程序在运行。从这里开始，探索官方 Rails 指南（guides.rubyonrails.org）或构建一些实际的项目来巩固你的技能。你在考虑什么样的项目呢？

---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 使用 Laravel
translated: true
type: post
---

如果你正在涉足网页开发，并且想要一个既强大又易于上手的框架，Laravel 就是你的不二选择。它是一个 PHP 框架，凭借其优雅的语法、强大的功能和一个支持你的社区，迅速在开发者世界中引起了轰动。在这篇博客中，我将带你了解 Laravel 的基础知识，并向你展示为什么它值得你花时间。

#### 第 1 步：设置你的环境

在你开始使用 Laravel 构建之前，你需要正确的工具。以下是你需要的：

- **PHP**：版本 8.1 或更高（Laravel 发展迅速，所以保持更新！）。
- **Composer**：这是 PHP 的依赖管理器。从 [getcomposer.org](https://getcomposer.org/) 下载。
- **本地服务器**：像 XAMPP、WAMP 或 Laravel 内置的服务器都非常好用。
- **终端**：你将运行命令，所以熟悉你的命令行。

准备好这些后，打开你的终端并全局安装 Laravel：

```
composer global require laravel/installer
```

这将让你用一个命令创建新的 Laravel 项目。

#### 第 2 步：创建你的第一个 Laravel 项目

准备好构建一些东西了吗？在你的终端中，导航到你想要项目所在的文件夹（例如，`cd /path/to/your/folder`），然后输入：

```
laravel new my-first-app
```

几分钟后，Composer 将设置一个名为 `my-first-app` 的新 Laravel 项目。导航到它：

```
cd my-first-app
```

要看到它的运行效果，启动 Laravel 的内置服务器：

```
php artisan serve
```

打开你的浏览器并访问 `http://localhost:8000`。轰——你有一个欢迎页面！这是 Laravel 在向你问好。

#### 第 3 步：了解基础知识

Laravel 遵循 MVC（模型-视图-控制器）结构，这使你的代码保持整洁和有组织：

- **模型**：处理你的数据（例如数据库表）。
- **视图**：用户看到的前端内容（HTML、CSS 等）。
- **控制器**：连接模型和视图的粘合剂。

你可以在 `app/` 文件夹中找到这些。例如，控制器位于 `app/Http/Controllers`，视图在 `resources/views`。

#### 第 4 步：构建一个简单的页面

让我们快速创建一个“Hello, World”页面。打开 `routes/web.php`——这是你定义应用程序 URL 的地方。添加这行：

```php
Route::get('/hello', function () {
    return view('hello');
});
```

现在，在 `resources/views` 中创建一个名为 `hello.blade.php` 的文件。添加这行：

```html
<!DOCTYPE html>
<html>
<head>
    <title>Hello, Laravel</title>
</head>
<body>
    <h1>Hello, World!</h1>
</body>
</html>
```

重新启动你的服务器（或保持运行），然后访问 `http://localhost:8000/hello`。你将看到你的“Hello, World!”页面。`.blade.php` 扩展名意味着你正在使用 Laravel 的 Blade 模板引擎——对动态内容非常方便。

#### 第 5 步：与数据库玩耍

Laravel 通过其 Eloquent ORM（对象关系映射）使数据库工作变得轻而易举。首先，在 `.env` 文件中设置你的数据库（例如 MySQL、SQLite）：

```
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=your_database_name
DB_USERNAME=your_username
DB_PASSWORD=your_password
```

创建一个迁移来设置一个表。运行：

```
php artisan make:migration create_posts_table
```

在 `database/migrations` 下的新文件中定义你的表：

```php
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('body');
        $table->timestamps();
    });
}
```

运行迁移：

```
php artisan migrate
```

现在你有一个 `posts` 表！你可以用以下命令创建一个 `Post` 模型：

```
php artisan make:model Post
```

这将你的表与你可以在代码中使用的模型绑定在一起。

#### 第 6 步：继续探索

Laravel 还有很多东西可以提供——身份验证、中间件、路由和通过 Composer 的包。想要用户登录？运行：

```
php artisan make:auth
```

需要前端提升？使用 Laravel Breeze 或 Jetstream。[官方文档](https://laravel.com/docs) 是你在这里的最佳朋友。

#### 为什么使用 Laravel？

它快速、安全，并且节省了你重新发明轮子的时间。无论你是构建博客、电子商务网站还是 API，Laravel 的工具——如 artisan 命令、Blade 模板和 Eloquent——都使生活更轻松。

那么，你在等什么？从小处做起，实验，很快你就会像老手一样制作网页应用。编码愉快！

---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: PHP 命令行基础指南
translated: true
type: note
---

PHP 有几个实用的 command line 选项，可以让你运行 PHP scripts、执行 code snippets 以及配置 interpreter 的行为。以下是主要的选项：

**Basic script execution** 是最常见的用法。你可以通过 `php filename.php` 直接运行一个 PHP 文件，任何 command line arguments 都会通过 `$argv` 数组传递给你的 script（其中 `$argv[0]` 是 script 名称本身）。

**`-r` 选项** 让你无需文件即可直接执行 PHP code。例如，`php -r 'echo "Hello World";'` 可以在线运行该代码。这对于快速测试或 one-liners 非常方便。

**`-f` 选项** 明确指定要 parse 和执行的文件，虽然这不太常用，因为 `php filename.php` 也能实现同样的功能。

**`-d` 选项** 临时设置一个 PHP configuration directive。例如，`php -d display_errors=1 script.php` 仅为该次执行开启 error display。这在不修改 php.ini 的情况下进行 debugging 非常有用。

**`-v` 选项** 显示 PHP 版本，而 **`-i`** 显示你的 PHP configuration 信息（等同于运行 `phpinfo()`）。这些对于检查你的 setup 很有帮助。

**`-l` 选项** 在不执行文件的情况下检查 PHP syntax。运行 `php -l script.php` 可以验证你的代码是否存在任何 parse errors。

**`-a` 选项** 启动一个 interactive shell，你可以在其中输入 PHP code 并立即查看结果——适用于实验或快速计算。

**`-S` 选项** 启动一个用于 local development 的 built-in web server：`php -S localhost:8000` 在 8000 端口运行一个简单的 server。这对于在没有安装 Apache 或 Nginx 的情况进行测试非常棒。

这些是核心要点。PHP 还有更多针对特定用途的选项，例如定义 constants、处理大型文件或更改 working directories，但以上内容涵盖了大多数日常使用场景。
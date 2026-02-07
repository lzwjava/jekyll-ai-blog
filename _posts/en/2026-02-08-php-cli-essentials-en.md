---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: PHP Command Line Essentials Guide
translated: false
type: note
---

PHP has several useful command line options that let you run PHP scripts, execute code snippets, and configure how the interpreter behaves. Here are the main ones:

**Basic script execution** is the most common use. You can run a PHP file directly with `php filename.php`, and any command line arguments get passed to your script via the `$argv` array (where `$argv[0]` is the script name itself).

**The `-r` option** lets you execute PHP code directly without needing a file. For example, `php -r 'echo "Hello World";'` runs that code inline. This is handy for quick testing or one-liners.

**The `-f` option** explicitly specifies a file to parse and execute, though it's less common since `php filename.php` does the same thing.

**The `-d` option** temporarily sets a PHP configuration directive. For instance, `php -d display_errors=1 script.php` turns on error display just for that execution. This is useful for debugging without modifying php.ini.

**The `-v` option** shows the PHP version, and `-i` displays your PHP configuration info (equivalent to running `phpinfo()`). These are helpful for checking your setup.

**The `-l` option** checks PHP syntax without executing the file. Running `php -l script.php` validates whether your code has any parse errors.

**The `-a` option** starts an interactive shell where you can type PHP code and see results immediately—useful for experimenting or quick calculations.

**The `-S` option** starts a built-in web server for local development: `php -S localhost:8000` runs a simple server on port 8000. This is great for testing without needing Apache or Nginx installed.

These are the essentials. PHP has several more specialized options for things like defining constants, handling large files, or changing working directories, but these cover most everyday use cases.
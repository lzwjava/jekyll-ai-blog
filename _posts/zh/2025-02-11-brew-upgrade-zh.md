---
audio: false
generated: false
image: false
lang: zh
layout: post
title: Brew升级日志
translated: true
type: note
---

```bash
==> 收尾工作
ln -s ../../Cellar/azure-cli/2.68.0/etc/bash_completion.d/az az
ln -s ../Cellar/azure-cli/2.68.0/bin/az az
ln -s ../../../Cellar/azure-cli/2.68.0/share/fish/vendor_completions.d/az.fish az.fish
ln -s ../../../Cellar/azure-cli/2.68.0/share/zsh/site-functions/_az _az
==> 注意事项
zsh 补全功能已安装至：
  /opt/homebrew/share/zsh/site-functions
==> 总结
🍺  /opt/homebrew/Cellar/azure-cli/2.68.0: 24,507 个文件，580.4MB
==> 正在运行 `brew cleanup azure-cli`...
移除：/opt/homebrew/Cellar/azure-cli/2.67.0_1...（27,401 个文件，647.1MB）
移除：/Users/lzwjava/Library/Caches/Homebrew/azure-cli_bottle_manifest--2.67.0_1...（22.5KB）
移除：/Users/lzwjava/Library/Caches/Homebrew/azure-cli--2.67.0_1...（54MB）
==> 注意事项
==> openjdk
要让系统 Java 包装器找到此 JDK，请创建符号链接：
  sudo ln -sfn /opt/homebrew/opt/openjdk/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk.jdk

openjdk 是 keg-only 软件，这意味着它未被符号链接到 /opt/homebrew，
因为 macOS 已提供类似软件，并行安装此软件可能导致各种问题。

若需将 openjdk 置于 PATH 首位，请运行：
  echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc

要让编译器找到 openjdk，您可能需要设置：
  export CPPFLAGS="-I/opt/homebrew/opt/openjdk/include"
==> ruby
默认情况下，通过 gem 安装的二进制文件将置于：
  /opt/homebrew/lib/ruby/gems/3.4.0/bin

您可能需要将其添加到 PATH 环境变量中。

ruby 是 keg-only 软件，这意味着它未被符号链接到 /opt/homebrew，
因为 macOS 已提供此软件，并行安装另一个版本可能导致各种问题。

若需将 ruby 置于 PATH 首位，请运行：
  echo 'export PATH="/opt/homebrew/opt/ruby/bin:$PATH"' >> ~/.zshrc

要让编译器找到 ruby，您可能需要设置：
  export LDFLAGS="-L/opt/homebrew/opt/ruby/lib"
  export CPPFLAGS="-I/opt/homebrew/opt/ruby/include"
==> yt-dlp
zsh 补全功能已安装至：
  /opt/homebrew/share/zsh/site-functions
==> redis
升级后要重启 redis：
  brew services restart redis
或者，如果您不需要后台服务，可以直接运行：
  /opt/homebrew/opt/redis/bin/redis-server /opt/homebrew/etc/redis.conf
==> perl
默认情况下，非自制的 cpan 模块会安装到 Cellar。如果您希望
模块在更新后保留，建议使用 `local::lib`。

您可以这样设置：
  PERL_MM_OPT="INSTALL_BASE=$HOME/perl5" cpan local::lib
并将以下内容添加到 shell 配置文件中，例如 ~/.profile 或 ~/.zshrc
  eval "$(perl -I$HOME/perl5/lib/perl5 -Mlocal::lib=$HOME/perl5)"
==> awscli
"examples" 目录已安装到：
  /opt/homebrew/share/awscli/examples

zsh 补全功能和函数已安装至：
  /opt/homebrew/share/zsh/site-functions
==> php
要在 Apache 中启用 PHP，请将以下内容添加到 httpd.conf 并重启 Apache：
    LoadModule php_module /opt/homebrew/opt/php/lib/httpd/modules/libphp.so

    <FilesMatch \.php$>
        SetHandler application/x-httpd-php
    </FilesMatch>

最后，检查 DirectoryIndex 是否包含 index.php
    DirectoryIndex index.php index.html

php.ini 和 php-fpm.ini 文件位于：
    /opt/homebrew/etc/php/8.4/

要立即启动 php 并在登录时重启：
  brew services start php
或者，如果您不需要后台服务，可以直接运行：
  /opt/homebrew/opt/php/sbin/php-fpm --nodaemonize
==> nginx
文档根目录为：/opt/homebrew/var/www

默认端口已在 /opt/homebrew/etc/nginx/nginx.conf 中设置为 8080，
以便 nginx 无需 sudo 即可运行。

nginx 将加载 /opt/homebrew/etc/nginx/servers/ 中的所有文件。

升级后要重启 nginx：
  brew services restart nginx
或者，如果您不需要后台服务，可以直接运行：
  /opt/homebrew/opt/nginx/bin/nginx -g daemon\ off\;
==> git-lfs
更新 git 配置以完成安装：

  # 更新全局 git 配置
  $ git lfs install

  # 更新系统 git 配置
  $ git lfs install --system

zsh 补全功能已安装至：
  /opt/homebrew/share/zsh/site-functions
==> wireshark
此公式默认仅安装命令行工具。

使用 Homebrew Cask 安装 Wireshark.app：
  brew install --cask wireshark

如果可用捕获接口列表为空（默认 macOS 行为），请安装 ChmodBPF：
  brew install --cask wireshark-chmodbpf
==> doctl
zsh 补全功能已安装至：
  /opt/homebrew/share/zsh/site-functions
==> azure-cli
zsh 补全功能已安装至：
  /opt/homebrew/share/zsh/site-functions
```

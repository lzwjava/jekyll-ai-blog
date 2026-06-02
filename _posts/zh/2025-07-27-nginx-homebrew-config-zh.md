---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS Homebrew 环境下的 Nginx 配置
translated: true
type: note
---

对于通过 Homebrew 在 macOS 上安装的 Nginx（可通过二进制路径 `/opt/homebrew/bin/nginx` 确认），主配置文件通常位于：

```
/opt/homebrew/etc/nginx/nginx.conf
```

该目录还包含其他相关文件，例如位于 `servers/` 子目录中的服务器块配置（如 `/opt/homebrew/etc/nginx/servers/`）。

要确认当前 Nginx 实例使用的配置文件路径，请在终端中运行以下命令：

```
nginx -t
```

该命令将测试配置文件并输出正在使用的 `nginx.conf` 文件路径。或者使用 `nginx -V` 查看编译详情，包括配置路径前缀。

如果您使用的是安装路径为 `/usr/local` 的旧款 Intel 芯片 Mac，则路径应为 `/usr/local/etc/nginx/nginx.conf`，但您提供的二进制路径确认了当前为 `/opt/homebrew` 位置。

**参考链接**
[Locate the nginx.conf file my nginx is actually using - Stack Overflow](https://stackoverflow.com/questions/19910042/locate-the-nginx-conf-file-my-nginx-is-actually-using)
[Installing nginx in macOS using homebrew | by Ram - Medium](https://medium.com/@rprprasath05/installing-nginx-in-macos-ventura-using-homebrew-12b87a900a03)
[Simple Configuration of NGINX on Mac - DEV Community](https://dev.to/arjavdave/simple-configuration-of-nginx-on-mac-3cg3)

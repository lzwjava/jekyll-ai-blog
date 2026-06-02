---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 自定义电影路径的 Nginx 配置
translated: true
type: note
---

**Question:** 修改 Nginx 配置，将文件服务路径从 /var/www/movies/ 更改为 /home/lzw/qDownloads，同时保持 /movies/ URL 路径并启用 directory listing。

**Answer:**

这是使用新目录更新后的 Nginx 配置：

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /home/lzw/qDownloads/;
        autoindex on;
    }
}
```

### 替代版本（使用 `root` 代替 `alias` – 也非常常见）

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        root /home/lzw;
        # 或者: root /home/lzw/qDownloads/..;  ← 效果相同
        try_files $uri $uri/ =404;
        autoindex on;
    }
}
```

### 最推荐的版本（简洁 + 安全）

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /home/lzw/qDownloads/;
        autoindex on;

        # 可选但推荐的添加项：
        charset utf-8;
        autoindex_exact_size off;     # 显示人类可读的大小 (KB, MB…)
        autoindex_localtime on;       # 显示服务器时区的文件时间
    }
}
```

修改配置后：

1. 检查语法：
   `sudo nginx -t`

2. 重载 nginx：
   `sudo systemctl reload nginx`
   或
   `sudo nginx -s reload`

现在 <http://your-server-ip/movies/> 应该会显示 `/home/lzw/qDownloads/` 的内容。

**References:**

- 此类直接的配置更改无需参考资料。

---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Nginx跨域与HTTPS配置
translated: true
type: note
---

```nginx
# 定义映射以处理允许的源
map $http_origin $cors_origin {
    default "https://example.com";
    "http://localhost:3000" "http://localhost:3000";
    "https://example.com" "https://example.com";
    "https://www.example.com" "https://www.example.com";
}
```

### 功能说明
- 根据传入的`Origin`头（`$http_origin`）创建变量`$cors_origin`
- 当请求来自`http://localhost:3000`、`https://example.com`或`https://www.example.com`时，原样返回对应源
- 其他来源（或无来源）的请求默认使用`https://example.com`
- 后续用于动态设置`Access-Control-Allow-Origin`头，仅对受信任的前端域名启用CORS

---

```nginx
# HTTP重定向至HTTPS
server {
    listen 80;
    server_name example.com api.example.com;
    return 301 https://$host$request_uri;
}
```

### 功能说明
- 监听80端口（HTTP）
- 匹配发往`example.com`或`api.example.com`的请求
- 永久重定向（301）所有流量至相同URL的HTTPS版本
- 强制使用安全连接，禁止纯HTTP访问

---

```nginx
# example.com主站点配置
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    root /home/project/project-web;
    index index.html index.htm index.php default.html default.htm default.php;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)$ {
        expires 30d;
    }

    location ~ .*\.(js|css)?$ {
        expires 12h;
    }

    error_page 404 /index.html;
}
```

### 功能说明
- 为`example.com`启用**HTTPS服务**（443端口，SSL加密）
- 使用**Let's Encrypt**证书（可自动续期，免费）
- 强制使用现代TLS版本（`TLSv1.2`、`TLSv1.3`）和高强度加密套件
- 从`/home/project/project-web`目录提供静态文件服务
- 尝试按以下顺序响应：请求文件→目录→404错误
- 设置**缓存头**：
  - 图片：缓存30天
  - JS/CSS文件：缓存12小时
- 所有404错误均路由至`index.html`→支持**SPA（单页应用）**路由（如React、Vue）

---

```nginx
# api.example.com接口配置
server {
    listen 443 ssl;
    server_name api.example.com;

    ssl_certificate /etc/letsencrypt/live/example.com-0001/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com-0001/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;
    ssl_ciphers "EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH";

    location / {
        # 清除已存在的访问控制头
        more_clear_headers 'Access-Control-Allow-Origin';

        # 处理CORS预检请求
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' $cors_origin;
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
            add_header 'Access-Control-Allow-Headers' 'Origin, Content-Type, Accept, Authorization, X-Client-Info, X-Trace-Id, X-Requested-With, X-HTTP-Method-Override, DNT, Keep-Alive, User-Agent, If-Modified-Since, Cache-Control, Content-Range, Range';
            add_header 'Access-Control-Max-Age' 3600;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' $cors_origin always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' '...' always;

        proxy_pass http://127.0.0.1:5000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_connect_timeout 600s;
        proxy_send_timeout 600s;
        proxy_read_timeout 600s;
        send_timeout 600s;
    }
}
```

### 功能说明
- 为`api.example.com`启用**HTTPS反向代理**
- 使用**独立Let's Encrypt证书**（可能因多域名/SAN需求）
- 所有流量被代理至运行在`localhost:5000`的**本地后端服务**（如Flask、Node.js等）

#### CORS处理
- 使用`$cors_origin`映射**动态放行**已认证的源
- **清除现有**`Access-Control-Allow-Origin`头防止冲突
- 处理**OPTIONS预检请求**：
  - 立即返回`204 No Content`
  - 允许常见方法和头信息
  - 预检结果缓存1小时（`Max-Age: 3600`）
- 对实际请求添加带`always`参数的CORS头，确保错误响应也包含这些头信息

#### 代理设置
- 将真实客户端IP和协议信息传递至后端
- 设置高超时（10分钟）→ 适用于长时间运行的API操作（如文件上传、复杂计算）

---

### 架构总结

| 组件                | 功能说明 |
|---------------------|----------|
| `example.com`       | 提供静态SPA服务（React/Vue等） |
| `api.example.com`   | 安全API网关 → 5000端口后端服务 |
| HTTP转HTTPS         | 强制所有流量通过TLS传输 |
| CORS                | 仅限`example.com`、`www`及`localhost:3000` |
| 缓存优化            | 针对性能进行优化 |
| SSL证书             | Let's Encrypt，现代加密套件 |

### 安全说明
- 强TLS配置（SSL Labs评级可能为A+）
- CORS**非通配符**配置 → 阻止未授权站点调用API
- 高效处理预检请求
- 真实IP转发 → 便于后端进行日志记录/限流

如需图表或Docker化版本，欢迎告知！

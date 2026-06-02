---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 现代化过时的 Docker PHP 技术栈
translated: true
type: note
---

问：这个 Dockerfile 中这些库和 PHP 的最新技术/版本是什么？

答：

你的 Dockerfile **已经非常过时**（PHP 7.4 + Apache）。2026 年的现代技术栈需要升级 **PHP、基础镜像、扩展和架构**。

---

# 1. 你当前的技术栈（已过时）

* `php:7.4-apache` ❌（已结束生命周期）
* Apache prefork + mod_php（旧风格）
* 基于旧的 Debian 版本
* 单体容器

PHP 7.4 已于 **2022 年 11 月结束生命周期** —— 不再提供安全补丁。（[EOSL 日期][1]）

---

# 2. 最新的 PHP 版本（2026 年）

当前的现代选项：

* PHP **8.5** — 最新的稳定版本（推荐）
* PHP **8.4** — 稳定的生产版本
* PHP **8.3** — 仅提供安全修复

PHP 8.5 于 2025 年 11 月发布，支持到 2029 年。（[PHP.Watch][2]）

---

# 3. 现代的 Docker 基础镜像（推荐）

替代：

```dockerfile
FROM php:7.4-apache
```

使用以下选项之一：

### 选项 A — 现代的 Apache

```
FROM php:8.5-apache
```

### 选项 B — 现代生产环境（推荐）

```
FROM php:8.5-fpm
+ nginx 容器
```

现代架构：

```
nginx
  └── php-fpm (php:8.5-fpm)
        └── app
```

这是 **更快、可扩展且目前的标准做法**。

---

# 4. 更新的库（现代等效项）

你当前的列表大部分没问题，但需要更新：

| 旧版本                 | 新版本                  |
| --------------------- | --------------------- |
| libjpeg-dev           | libjpeg62-turbo-dev   |
| libpng-dev            | libpng-dev (ok)       |
| libfreetype6-dev      | libfreetype6-dev (ok) |
| libssl-dev            | 使用操作系统默认        |
| libcurl4-openssl-dev  | OK                    |
| libxml2-dev           | OK                    |
| ffmpeg                | OK（保留）             |

---

# 5. 现代的 PHP 扩展（推荐集合）

你当前安装：

```
mysqli
pdo
pdo_mysql
zip
opcache
curl
mbstring
json
xml
tokenizer
```

现代推荐：

```
pdo_mysql
mysqli
opcache
intl
bcmath
zip
gd
mbstring
curl
xml
exif
pcntl
```

添加这些新的扩展：

* intl（现在非常普遍）
* bcmath（货币处理 / APIs）
* exif（图像应用）
* pcntl（工作进程）

---

# 6. 现代的 Composer 安装（更好的做法）

替代：

```
composer install --no-dev
```

使用：

```
composer install \
  --no-dev \
  --prefer-dist \
  --optimize-autoloader \
  --no-interaction \
  --no-progress
```

---

# 7. 完全现代化的 Dockerfile（2026 年）

```
FROM php:8.5-apache

RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libzip-dev \
    libpng-dev \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    libcurl4-openssl-dev \
    libxml2-dev \
    libonig-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    mysqli \
    zip \
    opcache \
    curl \
    mbstring \
    xml \
    intl \
    bcmath \
    exif

COPY --from=composer:2 /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
COPY . .

RUN composer install \
    --no-dev \
    --prefer-dist \
    --optimize-autoloader \
    --no-interaction

RUN a2enmod rewrite headers

EXPOSE 80
CMD ["apache2-foreground"]
```

---

# 8. 更现代的方案（推荐架构）

当前的最佳实践：

```
docker-compose
  ├── nginx
  ├── php-fpm (php:8.5-fpm)
  ├── redis
  ├── mysql / postgres
```

这样可以获得：

* 更好的性能
* 水平扩展能力
* 异步工作进程
* 队列
* 缓存

---

# 9. 从 PHP 7.4 升级到 8.5 带来的重大改进

你将获得：

* JIT 编译器
* 2-3 倍的性能提升
* 类型化属性
* 枚举类型
* 只读类
* 纤程（异步）
* 更好的 opcache
* 更低的内存占用

仅此升级通常就能 **将延迟减半**。

---

# 10. 如果这是 CodeIgniter（看起来像）

最佳组合：

```
php:8.4-fpm
nginx
启用 opcache
redis 缓存
```

非常快。

---

如果你告诉我：

* CodeIgniter 3 还是 4
* Laravel / 旧版应用
* 需要 ffmpeg 视频处理

我可以提供 **生产级别的 Dockerfile**。

参考文献：

* [https://eosl.date/eol/product/php/](https://eosl.date/eol/product/php/)
* [https://php.watch/versions](https://php.watch/versions)
* [https://php.watch/versions/8.5/releases](https://php.watch/versions/8.5/releases)

[1]: https://eosl.date/eol/product/php/?utm_source=chatgpt.com "PHP End of Life (EOL), End of Support (EOS), EOSL Dates | 8.5.3 - February 2026 Release"
[2]: https://php.watch/versions/8.5/releases?utm_source=chatgpt.com "PHP 8.5 Releases • PHP.Watch"

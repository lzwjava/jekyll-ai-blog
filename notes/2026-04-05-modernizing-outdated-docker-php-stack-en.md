---
audio: false
generated: true
image: false
lang: en
layout: post
title: Modernizing Outdated Docker PHP Stack
translated: false
type: note
---

Question: What are the latest technologies/versions for these libraries and PHP in this Dockerfile?

Answer:

Your Dockerfile is **very outdated** (PHP 7.4 + Apache). The modern stack in 2026 should upgrade **PHP, base image, extensions, and architecture**.

---

# 1. Your current stack (outdated)

* `php:7.4-apache` ❌ (EOL)
* Apache prefork + mod_php (old style)
* Debian old base
* monolithic container

PHP 7.4 reached **end-of-life in Nov 2022** — no security fixes. ([EOSL Date][1])

---

# 2. Latest PHP versions (2026)

Current modern options:

* PHP **8.5** — latest stable (recommended)
* PHP **8.4** — stable production
* PHP **8.3** — security fixes only

PHP 8.5 released Nov 2025 and supported until 2029. ([PHP.Watch][2])

---

# 3. Modern Docker base images (recommended)

Instead of:

```dockerfile
FROM php:7.4-apache
```

Use one of these:

### Option A — Modern Apache

```
FROM php:8.5-apache
```

### Option B — Modern production (recommended)

```
FROM php:8.5-fpm
+ nginx container
```

Modern architecture:

```
nginx
  └── php-fpm (php:8.5-fpm)
        └── app
```

This is **faster + scalable + standard now**.

---

# 4. Updated libraries (modern equivalents)

Your current list is mostly OK, but update:

| Old                  | New                   |
| -------------------- | --------------------- |
| libjpeg-dev          | libjpeg62-turbo-dev   |
| libpng-dev           | libpng-dev (ok)       |
| libfreetype6-dev     | libfreetype6-dev (ok) |
| libssl-dev           | use OS default        |
| libcurl4-openssl-dev | OK                    |
| libxml2-dev          | OK                    |
| ffmpeg               | OK (keep)             |

---

# 5. Modern PHP extensions (recommended set)

You currently install:

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

Modern recommended:

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

Add these new ones:

* intl (very common now)
* bcmath (money / APIs)
* exif (image apps)
* pcntl (workers)

---

# 6. Modern Composer install (better)

Instead of:

```
composer install --no-dev
```

Use:

```
composer install \
  --no-dev \
  --prefer-dist \
  --optimize-autoloader \
  --no-interaction \
  --no-progress
```

---

# 7. Fully modernized Dockerfile (2026)

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

# 8. Even more modern (recommended architecture)

Best practice today:

```
docker-compose
  ├── nginx
  ├── php-fpm (php:8.5-fpm)
  ├── redis
  ├── mysql / postgres
```

This gives:

* better performance
* horizontal scaling
* async workers
* queues
* cache

---

# 9. Big improvements from PHP 7.4 → 8.5

You gain:

* JIT compiler
* 2-3x performance
* typed properties
* enums
* readonly classes
* fibers (async)
* better opcache
* lower memory

This upgrade alone often **halves latency**.

---

# 10. If this is CodeIgniter (looks like it)

Best combo:

```
php:8.4-fpm
nginx
opcache enabled
redis cache
```

Very fast.

---

If you tell me:

* CodeIgniter 3 or 4
* Laravel / legacy
* need ffmpeg video processing

I can give **production-grade Dockerfile**.

References:

* [https://eosl.date/eol/product/php/](https://eosl.date/eol/product/php/)
* [https://php.watch/versions](https://php.watch/versions)
* [https://php.watch/versions/8.5/releases](https://php.watch/versions/8.5/releases)

[1]: https://eosl.date/eol/product/php/?utm_source=chatgpt.com "PHP End of Life (EOL), End of Support (EOS), EOSL Dates | 8.5.3 - February 2026 Release"
[2]: https://php.watch/versions/8.5/releases?utm_source=chatgpt.com "PHP 8.5 Releases • PHP.Watch"

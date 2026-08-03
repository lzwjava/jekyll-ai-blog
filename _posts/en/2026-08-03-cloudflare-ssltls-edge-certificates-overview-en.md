---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare SSL/TLS Edge Certificates Overview
translated: false
type: note
---

## Question: Intro to Cloudflare SSL/TLS Edge Certificates

## Answer:

Cloudflare SSL/TLS has a simple idea:

```
Visitor Browser
      |
      | HTTPS (encrypted)
      |
Cloudflare Edge Server
      |
      | HTTP or HTTPS
      |
Your Origin Server
```

Cloudflare sits in the middle as a **reverse proxy**. The certificate your visitors see is usually **Cloudflare's Edge Certificate**, not your server's certificate.

---

## 1. What is SSL/TLS?

SSL is the old name. Today we mostly use **TLS (Transport Layer Security)**.

TLS provides:

### 1. Encryption

Nobody between user and Cloudflare can read:

```
GET /login
Cookie: session=xxxx
password=123
```

It becomes encrypted bytes:

```
9a 7f 3c a8 ...
```

---

### 2. Authentication

The browser verifies:

```
lzwjava.com
        |
        certificate
        |
        Cloudflare
        |
        trusted CA
```

Example:

```
Certificate:
  Subject:
      lzwjava.com

  Issuer:
      Google Trust Services CA

  Valid:
      2026-08-01 -> 2026-11-01
```

The browser asks:

"Can I trust this certificate?"

The answer comes from the CA chain.

---

### 3. Integrity

TLS prevents modification.

Without TLS:

```
User
 |
 |  hello
 |
Attacker changes:
"download app"
        |
        v
"download malware"
```

TLS detects this.

---

# 2. What is an Edge Certificate?

"Edge" means Cloudflare's edge network.

Example:

User in California:

```
Browser
   |
   |
Cloudflare Los Angeles Edge
   |
   |
Your server
```

The certificate installed on Cloudflare edge:

```
*.lzwjava.com
lzwjava.com
```

is called:

```
Edge Certificate
```

Your browser sees:

```
https://lzwjava.com
```

Certificate:

```
Issued to:
lzwjava.com

Issued by:
Cloudflare
```

not your VPS.

---

# 3. Your current certificates

You have:

```
*.lzwjava.com, lzwjava.com

Advanced
Expires:
2026-11-01

Universal
Expires:
2026-11-01

Backup
Expires:
2026-11-01
```

This is good.

It means:

```
lzwjava.com
```

works:

```
https://lzwjava.com
```

and wildcard:

```
https://blog.lzwjava.com
https://api.lzwjava.com
https://test.lzwjava.com
```

because:

```
*.lzwjava.com
```

covers subdomains.

---

# 4. Universal SSL vs Advanced Certificate Manager

## Universal SSL (free)

Cloudflare automatically gives:

```
lzwjava.com
*.lzwjava.com
```

You don't manage anything.

Good for:

* personal websites
* blogs
* small apps

Your current setup is enough.

---

## Advanced Certificate Manager (paid)

More control.

Example:

You have:

```
dev.api.internal.lzwjava.com
```

Normal wildcard:

```
*.lzwjava.com
```

does NOT cover:

```
dev.api.internal.lzwjava.com
```

because it only covers one level:

```
xxx.lzwjava.com
```

ACM can create:

```
*.api.internal.lzwjava.com
```

---

# 5. TLS versions

Your setting:

```
Minimum TLS Version
TLS 1.0 (default)
```

I would change this.

Modern setting:

```
TLS 1.2
```

or:

```
TLS 1.3
```

Reason:

TLS 1.0/1.1 are obsolete.

Modern browsers support:

```
TLS 1.2 2010
TLS 1.3 2018
```

Most websites use:

```
Minimum TLS: 1.2
TLS 1.3: ON
```

---

# 6. Always Use HTTPS

You have:

```
Always Use HTTPS
```

enabled.

Meaning:

User:

```
http://lzwjava.com
```

Cloudflare returns:

```
301 Redirect

https://lzwjava.com
```

Good.

---

# 7. HSTS

HTTP Strict Transport Security:

Without HSTS:

```
First visit:

http://lzwjava.com

redirect

https://lzwjava.com
```

With HSTS:

Browser remembers:

```
lzwjava.com always HTTPS
```

So:

```
http://lzwjava.com
```

is automatically upgraded.

Recommended:

```
Enable HSTS
```

but be careful:

If you enable:

```
includeSubDomains
```

then:

```
api.lzwjava.com
dev.lzwjava.com
```

must also support HTTPS.

---

# 8. TLS 1.3

Enable:

```
TLS 1.3: ON
```

Benefits:

TLS handshake:

TLS 1.2:

```
Client
 |
 | hello
 |
Server
 |
 | certificate
 |
Client
 |
 | key exchange
 |
Encrypted
```

TLS 1.3:

```
Client hello
+
key exchange

Encrypted
```

faster connection.

---

# 9. Automatic HTTPS Rewrites

Problem:

Your HTML:

```html
<img src="http://example.com/a.png">
```

Browser:

```
Mixed Content Warning
```

Cloudflare rewrites:

```html
<img src="https://example.com/a.png">
```

Useful for migrated sites.

---

# Recommended settings for lzwjava.com

For a personal AI blog / portfolio:

```
SSL/TLS mode:
    Full (strict)

Always Use HTTPS:
    ON

Minimum TLS:
    TLS 1.2

TLS 1.3:
    ON

Automatic HTTPS Rewrites:
    ON

HSTS:
    Enable after verifying everything works

Universal SSL:
    Keep enabled
```

Architecture:

```
Browser
   |
   | HTTPS
   |
Cloudflare Edge
   |
   | HTTPS (Full Strict)
   |
Your server/GitHub Pages
```

This is the normal production setup in 2026. Your current Cloudflare certificate status already looks healthy.

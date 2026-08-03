---
audio: false
generated: true
image: false
lang: en
layout: post
title: Enabling HTTPS on Cloudflare
translated: false
type: note
---

Question: How to enable HTTPS for `lzwjava.com` after moving DNS to Cloudflare?

Answer:

Since your domain is now active on Cloudflare, HTTPS is mostly automatic. Do these steps:

## 1. Enable Cloudflare SSL/TLS

Go to:

```
Cloudflare Dashboard
 → lzwjava.com
 → SSL/TLS
```

Set:

```
Encryption mode: Full
```

(or **Full (strict)** if your origin has a valid certificate)

For GitHub Pages, **Full** is usually fine.

---

## 2. Wait for Cloudflare certificate issuance

Go to:

```
SSL/TLS
 → Edge Certificates
```

You should see:

```
Universal SSL: Active
```

Cloudflare will automatically create a certificate:

```
lzwjava.com
www.lzwjava.com
```

Usually:

```
5 minutes - 24 hours
```

---

## 3. Enable HTTPS redirect

In:

```
SSL/TLS
 → Edge Certificates
```

Enable:

```
Always Use HTTPS: ON
```

Then:

```
Automatic HTTPS Rewrites: ON
```

Now:

```
http://lzwjava.com
```

redirects to:

```
https://lzwjava.com
```

---

## 4. Check DNS proxy status

Go to:

```
DNS → Records
```

For your website records, the cloud icon should be:

```
Orange cloud ☁️ Proxied
```

Example:

```
Type    Name       Target                  Proxy
CNAME   www        lzwjava.github.io       ☁️
A       @          185.199.xxx.xxx         ☁️
```

If it is:

```
Gray cloud ☁️ DNS only
```

Cloudflare HTTPS features won't apply.

---

## 5. Test

Run:

```bash
curl -I https://lzwjava.com
```

Expected:

```
HTTP/2 200
server: cloudflare
```

Check certificate:

```bash
openssl s_client -connect lzwjava.com:443 -servername lzwjava.com
```

You should see:

```
issuer=Cloudflare Inc ECC CA-3
```

---

For your case (Jekyll blog + GitHub Pages), the final architecture should be:

```
User
 |
 HTTPS
 |
Cloudflare Edge
 |
 HTTPS
 |
GitHub Pages
 |
 Jekyll static site
```

No need to buy SSL certificates. Cloudflare Universal SSL is free.

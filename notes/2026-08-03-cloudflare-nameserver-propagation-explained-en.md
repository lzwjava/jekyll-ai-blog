---
audio: false
generated: true
image: false
lang: en
layout: post
title: Cloudflare Nameserver Propagation Explained
translated: false
type: note
---

Question: What does “Waiting for your registrar to propagate your new nameservers” mean in Cloudflare?

Answer:

You are in the middle of **moving DNS management from Namecheap to Cloudflare**.

Your domain:

```
lzwjava.com
```

is still registered at **Namecheap**, but you told Cloudflare:

> "I want Cloudflare to manage my DNS."

Cloudflare gave you two nameservers:

```
barbara.ns.cloudflare.com
dion.ns.cloudflare.com
```

Now you need to tell Namecheap:

> "Use Cloudflare's nameservers instead of Namecheap's DNS."

Currently Namecheap still has:

```
dns1.registrar-servers.com
dns2.registrar-servers.com
```

So Cloudflare is waiting until the public DNS system sees:

```
lzwjava.com NS barbara.ns.cloudflare.com
lzwjava.com NS dion.ns.cloudflare.com
```

---

## What you should do now

Go to:

Namecheap → Domain List → lzwjava.com → Nameservers

Change:

```
dns1.registrar-servers.com
dns2.registrar-servers.com
```

to:

```
barbara.ns.cloudflare.com
dion.ns.cloudflare.com
```

Save.

---

## Then wait

Typical:

* Fast: 10 minutes
* Normal: 1–2 hours
* Worst case: 24–48 hours

Cloudflare will automatically detect the change.

You can check with:

```bash
dig NS lzwjava.com
```

Before:

```
lzwjava.com. NS dns1.registrar-servers.com
lzwjava.com. NS dns2.registrar-servers.com
```

After:

```
lzwjava.com. NS barbara.ns.cloudflare.com
lzwjava.com. NS dion.ns.cloudflare.com
```

---

## Important: check DNS records before switching

Cloudflare already imported your DNS records, but verify:

Cloudflare Dashboard:

```
lzwjava.com
  → DNS
```

You should see things like:

```
A     lzwjava.com       xxx.xxx.xxx.xxx
CNAME www               lzwjava.com
```

If you host your Jekyll blog on GitHub Pages, it should usually look like:

```
CNAME
www
lzwjava.github.io
```

and apex:

```
A
@
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

---

## SSL/TLS

After Cloudflare becomes active:

Go to:

```
Cloudflare
 → SSL/TLS
```

For GitHub Pages:

```
Encryption mode:
Full
```

Usually Cloudflare will issue:

```
https://lzwjava.com
https://www.lzwjava.com
```

certificate automatically.

---

## DNSSEC warning

The message says:

> Make sure DNSSEC is off

Because if Namecheap DNSSEC is enabled, changing nameservers can break DNS validation.

At Namecheap:

```
Domain
 → Advanced DNS
 → DNSSEC
```

Disable it first.

Later you can enable Cloudflare DNSSEC.

---

After this completes, your flow is:

```
Browser
   |
   v
Cloudflare DNS
   |
   v
GitHub Pages / Server
```

Benefits:

* Free SSL
* CDN
* DDoS protection
* Faster DNS
* Easier future deployment

For your Jekyll blog (`lzwjava.com` → GitHub Pages), this is the standard setup.

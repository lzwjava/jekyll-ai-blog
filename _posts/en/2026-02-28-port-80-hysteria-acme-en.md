---
audio: false
generated: true
image: false
lang: en
layout: post
title: Port 80 Required for Hysteria ACME Validation
translated: false
type: note
---

**Question:** Why does port 80 need to be open when Hysteria deals with Let's Encrypt, with UFW?

**Answer:**

Hysteria (especially **Hysteria 2**) has built-in **ACME client** support to automatically obtain and renew **TLS certificates** from **Let's Encrypt** (or ZeroSSL).

Let's Encrypt mainly uses two validation methods that Hysteria supports:

- **http-01** challenge → requires **TCP port 80** to be publicly reachable.
- **tls-alpn-01** challenge → requires **TCP port 443** to be publicly reachable.

By default, when you configure the `acme` section in Hysteria's config file (e.g., `listenHTTP: :80`), it uses the **http-01** challenge. Let's Encrypt servers connect to your domain on **<http://yourdomain.com/.well-known/acme-challenge/>...** (plain HTTP, port 80) to verify you control the domain.

If **port 80 is blocked** in your firewall (e.g., UFW), the validation fails with errors like:

- "Connection refused"
- "Timeout during connect (likely firewall problem)"
- "Fetching http://... : Connection refused"

That's why you must allow inbound **TCP/80** in UFW (at minimum during initial issuance and renewals):

```bash
sudo ufw allow 80/tcp
```

Hysteria's documentation explicitly warns:

> (Note: Changing to a port other than 80 requires port forwarding or HTTP reverse proxy, or the challenge will fail!)

**Alternatives to keep port 80 closed all the time:**

1. Use only **tls-alpn-01** challenge
   Set `disableHTTP: true` in the acme section → Hysteria will try **tls-alpn-01** (port 443 only).
   This works if port 443 is open (which it must be anyway for Hysteria).

2. Use **DNS-01** challenge
   This doesn't require any ports open on your server.
   You must use an ACME client that supports your DNS provider's API (e.g., acme.sh, certbot with DNS plugin, or manual setup), then point Hysteria to the obtained certificate files.

3. Use an **external tool** like certbot in `--standalone` or `--webroot` mode (temporarily open port 80 only during renewal via hooks/scripts).

Most simple Hysteria setups use the built-in ACME with **http-01** because it's automatic and convenient — but this is the main reason port 80 must be allowed in UFW.

**References:**

- <https://v2.hysteria.network/docs/advanced/Full-Server-Config>
- <https://letsencrypt.org/docs/allow-port-80>
- <https://letsencrypt.org/docs/challenge-types>
- <https://github.com/apernet/hysteria/issues/942>

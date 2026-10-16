---
audio: false
generated: true
image: false
lang: en
layout: post
title: Connect Namecheap Domain to Cloudflare Pages
translated: false
type: note
---

You can keep your domain registered at Namecheap and host the static website on Cloudflare Pages. You don't need to transfer the domain or change registrars.

There are two approaches:

- Recommended: Keep Namecheap as registrar, change nameservers to Cloudflare, and manage DNS through Cloudflare.
- Keep Namecheap DNS and point records to Cloudflare Pages. This is more limited: Pages custom domains generally require the domain to be a Cloudflare zone for an apex domain such as `example.com`. For a subdomain, such as `www.example.com`, you can use a CNAME to your Pages site.

## Step 1 — Add your domain to Cloudflare

1. Open the [Cloudflare Dashboard](https://dash.cloudflare.com/?utm_source=chatgpt.com).
2. Choose Add a domain (or Onboard a domain).
3. Enter your domain, e.g. `example.com`.
4. Select a plan; the Free plan is sufficient for most static sites.
5. Review the DNS records Cloudflare imports from Namecheap.

Important: Check your existing DNS records before changing nameservers, especially email records (MX, SPF, DKIM) and any existing subdomains. Missing records can interrupt those services.

## Step 2 — Change nameservers in Namecheap

After Cloudflare gives you two assigned nameservers:

1. Log in to [Namecheap Domain List](https://ap.www.namecheap.com/Domains/DomainList?utm_source=chatgpt.com).
2. Click Manage next to your domain.
3. Under Nameservers, select Custom DNS.
4. Enter the two nameservers Cloudflare assigned to your domain.
5. Save the changes.&#x20;

   [image](https://www.google.com/s2/favicons?domain=https://www.namecheap.com\&sz=32)

   Namecheap

   +1



Do not copy nameservers from another domain; use the exact pair Cloudflare assigned to yours.

## Step 3 — Attach the domain to Pages

Once Cloudflare shows your domain as Active:

1. Go to Workers & Pages in Cloudflare.
2. Open your Pages project.
3. Select Custom domains → Set up a domain.
4. Enter your domain, such as `example.com`, and follow the prompts.

Cloudflare will configure the necessary DNS record and provision HTTPS for the domain.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1



## Step 4 — Verify everything

Run these commands from your terminal, replacing the example domain:

```
dig NS example.com +short
dig example.com
curl -I https://example.com
```

Check that:

- The nameservers are the ones assigned by Cloudflare.
- The domain resolves correctly.
- HTTPS returns a successful response, typically `200` or a redirect such as `301`.

Nameserver changes can take time to propagate.

My recommendation: Keep Namecheap as your registrar, Cloudflare as your DNS/CDN, and Cloudflare Pages as your static hosting. This is a clean setup for a personal website, documentation site, or AI project landing page.

I can also help you set up a `www` → apex-domain redirect and configure caching rules so your static site has one canonical URL.

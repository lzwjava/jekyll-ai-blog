---
audio: false
generated: true
image: false
lang: en
layout: post
title: Configure Cloudflare Pages DNS Records
translated: false
type: note
---

For `zhiweisoft.site`, don't create an A record pointing to a guessed IP address if you're hosting on Cloudflare Pages. Pages uses a CNAME target, and for an apex domain Cloudflare can manage that record automatically once the domain is configured.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1



## Configure it based on where your DNS is hosted

### Case 1: You're using Cloudflare nameservers

In the [Cloudflare DNS dashboard](https://dash.cloudflare.com/?utm_source=chatgpt.com), select `zhiweisoft.site` → DNS → Records.

Once you add `zhiweisoft.site` under your Pages project's Custom domains, Cloudflare should create the required record automatically.

Expected setup:

| Field        | Value                                                      |
| ------------ | ---------------------------------------------------------- |
| Type         | `CNAME`                                                    |
| Name         | `@`                                                        |
| Target       | Your Pages project hostname, e.g. `your-project.pages.dev` |
| Proxy status | Proxied                                                    |

Don't manually add an A record if Cloudflare has already created the required record.

### Case 2: You're still using Namecheap DNS

If you want to keep Namecheap's nameservers, an A record won't directly connect the apex domain to Cloudflare Pages. You can instead use a subdomain such as `www.zhiweisoft.site` with a CNAME pointing to your Pages hostname, after adding that subdomain in the Pages dashboard.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developers.cloudflare.com\&sz=32)

Cloudflare Pages docs

+1



One question: In Namecheap, what does the Nameservers field currently show?

- `Namecheap BasicDNS`
- `Custom DNS` (Cloudflare nameservers)
- Something else

That determines exactly where you should configure the DNS record.

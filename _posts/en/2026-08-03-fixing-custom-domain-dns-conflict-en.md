---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Custom Domain DNS Conflict
translated: false
type: note
---

Question: Custom Domain binding for `lzwjava.com` on the Cloudflare Worker `jekyll-ai-blog` fails with "already has externally managed DNS records (A, CNAME, etc)."

Answer: Cloudflare Custom Domains need to own the DNS record for the hostname (it auto-creates a proxied CNAME/A pointing to the Worker). It refuses to touch a record it didn't create — since `lzwjava.com` already has a zone-apex A/CNAME (leftover from Namecheap parking, or whatever you pointed it at before moving nameservers), it blocks the bind rather than silently overwrite it.Custom Domains allow you to connect your Worker to a domain or subdomain, without having to make changes to your DNS settings or perform any certificate management. After you set up a Custom Domain for your Worker, Cloudflare will create DNS records and issue necessary certificates on your behalf.

Fix, dashboard path:

```
Cloudflare dashboard → lzwjava.com zone → DNS → Records
→ find A or CNAME on "@" (root) → Delete
→ Workers & Pages → jekyll-ai-blog → Settings → Domains & Routes → Custom Domains → Add lzwjava.com again
```

Fix, CLI path (faster, scriptable):

```bash
# find the zone id
export CF_API_TOKEN=<TOKEN>
ZONE_ID=$(curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones?name=lzwjava.com" | jq -r '.result[0].id')

# list root records
curl -s -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records?name=lzwjava.com" | jq '.result[] | {id,type,name,content}'

# delete the conflicting record (grab id from above)
curl -s -X DELETE -H "Authorization: Bearer $CF_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records/<RECORD_ID>"
```

Then rebind via wrangler.toml/jsonc (this is the actual recommended path since dashboard custom-domain UI and wrangler both hit the same 100117 check):

```jsonc
// wrangler.jsonc
{
  "name": "jekyll-ai-blog",
  "routes": [
    { "pattern": "lzwjava.com", "custom_domain": true },
    { "pattern": "www.lzwjava.com", "custom_domain": true }
  ]
}
```

```bash
npx wrangler deploy
```

Two gotchas people hit here:

1. `override_existing_dns_record` is referenced in the error message but **not actually implemented** in wrangler — it's dead in the CLI and dashboard. Don't waste time looking for that flag; deleting the record is the only working path right now.
2. If Namecheap still has DNS-only records synced in some way (unlikely once nameservers point to Cloudflare, but check), confirm at Namecheap that nameservers are fully `*.ns.cloudflare.com` — if Namecheap is still authoritative, Cloudflare's DNS panel is irrelevant and Custom Domains won't work at all since Cloudflare doesn't own the zone.

Quick check before retry:

```bash
dig NS lzwjava.com +short
```

Should return your two Cloudflare-assigned nameservers, not Namecheap's.

References:

- [Custom Domains — Cloudflare Docs](https://developers.cloudflare.com/workers/configuration/routing/custom-domains/)
- [override_existing_dns_record flag ignored in wrangler deploy · Issue #9878](https://github.com/cloudflare/workers-sdk/issues/9878)
- [Hostname already has externally managed DNS records — Cloudflare Community thread](https://community.cloudflare.com/t/hostname-already-has-externally-managed-dns-records/788820)

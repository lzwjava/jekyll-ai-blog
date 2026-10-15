---
audio: false
generated: true
image: false
lang: en
layout: post
title: Firewall Dropping Ports 80 and 443
translated: false
type: note
---

## Root cause found: firewall is dropping ports 80/443

The port timing test is decisive — it distinguishes a firewall **DROP** from a dead service:

| Port | Result | Meaning |
|------|--------|---------|
| **22** | **OPEN** | host reachable, SSH allowed |
| **80** | timeout (6.00s) | packets **silently dropped** |
| **443** | timeout (6.01s) | packets **silently dropped** |
| **8080** | refused in **0.02s** | packet **reached the host**, OS said "nothing listening" |

The critical comparison is 80/443 vs 8080. Port 8080 returns an RST in 20ms, proving network packets **do** reach your VM. But 80 and 443 hang until timeout — that's a firewall discarding them, not a web server that's down. If nginx were simply stopped, you'd get a fast RST like 8080 did, and the browser would show `ERR_CONNECTION_REFUSED` instead of `ERR_TIMED_OUT`.

So the server is alive, SSH works, but something is explicitly dropping web traffic.

## DNS is fixed — that part worked

```
www.funlive.io.  600  IN  A  34.150.108.243   ✅ (Google + Cloudflare agree)
```

Your `ERR_TIMED_OUT` (not NXDOMAIN) confirms `www` now resolves correctly. The failure moved from DNS to the firewall.

**However, the apex still has both records:**
```
funlive.io.  600  IN  A  34.150.108.243
funlive.io.  600  IN  A  162.255.119.114    ← still there, delete this
```
You removed the `www` NXDOMAIN problem but haven't deleted the Namecheap URL Forward record yet.

## What to check

I can't SSH in to verify — these are the two places to look:

**1. GCP VPC firewall** (most likely). Go to Compute Engine → VM → Firewall rules, or check for a tag mismatch:
```bash
gcloud compute firewall-rules list --format="table(name,allowed[].map().firewall_rule().list(),sourceRanges.list(),targetTags.list())"
```
You need an ingress rule allowing `tcp:80` and `tcp:443` from `0.0.0.0/0`, **and** the VM must carry the target tag that rule selects. A rule exists but the VM lacks its network tag is the classic cause of exactly this symptom.

**2. Host firewall** — since 80/443 are dropped while 8080 passes through to the kernel, a host-level rule could be targeting the web ports specifically:
```bash
sudo ufw status verbose          # if it says "deny" incoming, that's it
sudo iptables -L INPUT -n -v | head -30
sudo ss -tlnp | grep -E ':80|:443'
```
If `ss` shows nothing on 80/443, start the web server *and* fix the firewall — both are needed.

**Note on the earlier 502:** your local proxy (`127.0.0.1:7890`) returns an identical 502 for any unreachable host — I confirmed it produces the same header signature for a blackhole IP. So the 502 and the timeout are the same underlying issue: the web ports are unreachable, and only the error text differs by path.

Test after opening the firewall: `curl -I http://34.150.108.243/` should return a real status line with a `Server:` header instead of the proxy's empty 502.
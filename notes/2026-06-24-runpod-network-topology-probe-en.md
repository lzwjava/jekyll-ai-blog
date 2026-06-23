---
audio: false
generated: true
image: false
lang: en
layout: post
title: RunPod Network Topology Probe
translated: false
type: note
---

**Question:** Can scanning RunPod pods across many instances reveal their network topology and contributor distribution?

**Answer:**

Yes, conceptually sound. Here's the methodology and what you'd actually learn:

## What You'd Discover

Spinning up N pods and recording the underlying proxy/IP metadata gives you:

- **Datacenter distribution** — ASN lookups reveal which hosting companies are contributing (EVOBITS, Hetzner, OVH, etc.)
- **Geographic spread** — country/city of actual GPU hardware vs RunPod's "regions"
- **Network topology** — do pods in same region share BGP peers? Same /24 subnet = same contributor
- **Contributor density** — how many distinct ASNs appear, cluster sizes

## Minimal Implementation

```python
import subprocess, socket, requests, json
from concurrent.futures import ThreadPoolExecutor

def probe_pod_network():
    # Run inside a RunPod pod
    results = {}

    # Get outbound IP
    r = requests.get("https://ipinfo.io/json", timeout=5)
    info = r.json()

    results["ip"] = "<IP_ADDRESS>"  # redacted in output
    results["asn"] = info.get("org")       # e.g. "AS12345 EVOBITS IT SRL"
    results["country"] = info.get("country")
    results["city"] = info.get("city")
    results["hostname"] = info.get("hostname")

    # Traceroute first 3 hops to see upstream
    tr = subprocess.run(["traceroute", "-m", "3", "8.8.8.8"],
                       capture_output=True, text=True)
    results["traceroute_hops"] = tr.stdout

    return results

print(json.dumps(probe_pod_network(), indent=2))
```

## Cost Estimate

| Scale | Pods | Cost | Signal |
|-------|------|------|--------|
| Quick sample | 20 pods × $0.20/hr × 5min | ~$0.35 | ASN distribution |
| Decent dataset | 100 pods | ~$1.70 | Contributor clusters |
| Real picture | 500 pods | ~$8 | Geographic density map |

Use cheapest GPU tier (RTX 2000 Ada ~$0.19/hr), spin up, probe, terminate in <5 min each.

## Automation Script

```python
# Run locally — spin pods via RunPod API, collect, terminate
import runpod

runpod.api_key = "<API_KEY>"

def create_probe_pod():
    return runpod.create_pod(
        name="net-probe",
        image_name="python:3.11-slim",
        gpu_type_id="NVIDIA GeForce RTX 2000 Ada Generation",
        cloud_type="ALL",  # include community = contributor GPUs
        container_disk_in_gb=5,
    )

# Collect results via RunPod exec API or just log to stdout
```

## What You Won't See

- The actual contributor identity (RunPod proxies everything)
- Pod-to-pod traffic (isolated)
- Other tenants on same hardware

## What's Genuinely Interesting

The `cloud_type="ALL"` vs `cloud_type="SECURE"` split is the key variable — community pods route through contributor's home/colo network directly. You'd likely find:

- Eastern European hosters (EVOBITS, M247) dominating cheap tiers
- Hetzner/OVH for mid tier
- AWS/GCP for "Secure Cloud"

$20 could give you a legitimately interesting dataset. No intrusion, just metadata from your own pods — completely within ToS.

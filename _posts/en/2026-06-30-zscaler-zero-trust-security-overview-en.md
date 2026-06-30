---
audio: false
generated: true
image: false
lang: en
layout: post
title: Zscaler Zero Trust Security Overview
translated: false
type: note
---

Question: Give me an intro to Zscaler — what it is and how it works.

Answer:

Zscaler is a cloud-native security platform built on the **Zero Trust** model. Instead of routing traffic through on-prem firewalls/VPN concentrators, it inserts itself as a cloud proxy between users and whatever they're connecting to (internet, SaaS, internal apps). All traffic gets inspected inline in Zscaler's edge cloud before reaching its destination.

Core architecture — two main products:

**ZIA (Zscaler Internet Access)** — secure web gateway / forward proxy. Your device's traffic to the internet/SaaS is tunneled to the nearest Zscaler data center, where it's decrypted (TLS inspection via an installed root cert), inspected (DLP, malware sandbox, URL filtering, CASB), then forwarded. This is the piece that breaks things for engineers — it MITMs your TLS, so tools like `pip`, `npm`, `git`, `docker pull`, and curl hit cert verification errors unless you trust the Zscaler CA.

**ZPA (Zscaler Private Access)** — replaces VPN for internal apps. Instead of putting you "on the network," lightweight **App Connectors** sit next to internal apps and make *outbound* connections to the Zscaler cloud. When you request an app, Zscaler brokers a connection by stitching your tunnel to the connector's tunnel. The app is never network-reachable — no inbound ports, no exposed subnet. You only ever reach the specific app you're authorized for, not the whole LAN.

The data plane is the **Zscaler Client Connector** (agent on your laptop) → nearest ZEN/Service Edge (the inspection node) → destination. Auth/policy decisions are identity-based (SAML/SCIM with your IdP), so policy follows the user, not an IP.

Why it exists, in one line: the old model trusted anything inside the perimeter; Zero Trust assumes no implicit trust and authenticates + inspects every request regardless of location.

Practical note for your bank/dev setup — the TLS inspection is what bites. Typical fix is exporting the Zscaler root CA and pointing your toolchains at it:

```bash
# Extract the Zscaler root cert (macOS keychain)
security find-certificate -a -c "Zscaler" -p /Library/Keychains/System.keychain > zscaler.pem

# Point common tools at it
export REQUESTS_CA_BUNDLE=$PWD/zscaler.pem   # python requests
export NODE_EXTRA_CA_CERTS=$PWD/zscaler.pem  # node/npm
export CURL_CA_BUNDLE=$PWD/zscaler.pem        # curl
git config --global http.sslCAInfo $PWD/zscaler.pem
pip config set global.cert $PWD/zscaler.pem
```

For a deeper, current breakdown of the product line and architecture, worth checking their docs directly since the specifics evolve.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tailscale Relayed Connection Diagnostic Report
translated: false
type: note
---

Here's the complete network diagnostic report.

================================================================
TAILSCALE CONNECTION DIAGNOSTIC REPORT
================================================================

CONNECTION TYPE: RELAYED (DERP)
----------------------------------------------------------------

Route:       lzw-mac → DERP(SFO) → "to"
Path:        DERP relay via San Francisco (region 2)
NOT direct:  Both peers have Endpoints=[] — no P2P established

WHY NO DIRECT CONNECTION?
----------------------------------------------------------------

Your NAT:    Symmetric (MappingVariesByDestIP=true)
Peer NAT:    Also restrictive (Endpoints=[] = no public endpoints)
Result:      UDP hole punching impossible → forced to DERP relay

Your network context:

- Connected via iPhone Personal Hotspot (172.20.10.x subnet)
- Public IPv4: 69.63.219.52 (routed through DMIT proxy, LA)
- IPv6: 240e:47e:1490:dbb0:...
- Nearest DERP: San Francisco (~195ms ICMP)

PERFORMANCE METRICS (30 Tailscale pings)
----------------------------------------------------------------

  Latency min:   364 ms
  Latency avg:   466 ms
  Latency max:   821 ms (up to 2.1s in earlier burst)
  Packet loss:   10.7% (3/28 lost)
  Jitter:        142 ms (avg delta between consecutive pings)
  Stddev:        142 ms

DERP SERVER BENCHMARK (ICMP ping)
----------------------------------------------------------------

  SFO (current):   194ms avg, 20% loss on one burst
  Hong Kong:       320ms avg, 0% loss
  Tokyo:           372ms avg, 0% loss
  → SFO is already the best DERP for your location

LATENCY BREAKDOWN
----------------------------------------------------------------

  You → DERP(SFO):    ~195ms
  DERP(SFO) → Peer:   ~195ms (symmetric assumption)
  DERP relay overhead: ~75ms (encryption + queuing)
  Total:               ~465ms (matches measured avg)

  The 10.7% packet loss is happening on the relay path,
  likely between your iPhone hotspot and the DERP server.

ROOT CAUSE
----------------------------------------------------------------

1. Both machines are behind symmetric/restrictive NAT
2. Tailscale cannot establish direct WireGuard tunnel
3. All traffic relays through DERP(SFO) — 2x transpacific hop
4. iPhone hotspot adds instability (jitter, loss)

WHAT WOULD FIX THIS
----------------------------------------------------------------

Option A: Same LAN
  When both machines are on 192.168.1.x, Tailscale discovers
  direct LAN endpoints → P2P → latency drops to 1-10ms

Option B: Expose direct endpoints on "to"
  On the workstation, open UDP port 41641 in firewall:
    sudo ufw allow 41641/udp
  Then restart tailscale:
    sudo tailscale down && sudo tailscale up
  This gives "to" a stable public endpoint for hole punching.

Option C: Run a custom DERP relay closer to both machines
  Deploy a DERP on a VPS in Asia (e.g., Hong Kong/Tokyo)
  to reduce the round-trip distance.

Option D: Use subnet router
  If "to" is on a network you can reach directly,
  set up a Tailscale subnet router to expose the LAN.

================================================================

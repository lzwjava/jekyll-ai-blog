---
audio: false
generated: true
image: false
lang: en
layout: post
title: MTR Output Interpretation for Binance
translated: false
type: note
---

**Question:** How do I interpret this MTR output from my Mac to `api.binance.com`?

**Answer:**

## MTR Output Analysis: `192.168.1.46 → api.binance.com (103.200.31.172)`

### Column Reference

| Column | Meaning |
|--------|---------|
| **Loss%** | % of ICMP packets with no reply received |
| **Snt** | Total packets sent (~46) |
| **Last** | RTT of the most recent packet (ms) |
| **Avg** | Average RTT of all packets (ms) |
| **Best** | Best (lowest) RTT seen (ms) |
| **Wrst** | Worst (highest) RTT seen (ms) |
| **StDev** | Standard deviation — higher = more jitter/inconsistency |

---

### Hop-by-Hop Breakdown

**Hop 1 — `192.168.1.1` (Your Home Router)**
- Loss: 0.0% ✅
- Avg: 9.9ms, Best: 5.3ms, Wrst: 61.2ms, StDev: 10.0
- Your local router is healthy with no loss. The high Wrst (61ms) and StDev suggest occasional Wi-Fi or router CPU spikes, but not a real issue.

**Hop 2 — `100.69.0.1` (Your ISP's First Gateway)**
- Loss: 0.0% ✅
- Avg: 17.1ms, Best: 9.1ms, Wrst: 80.9ms, StDev: 16.0
- Still healthy. The latency increase (~7ms) is expected as packets leave your home network and enter the ISP backbone. The higher StDev indicates some jitter at the ISP edge.

**Hop 3 — `(waiting for reply)` ⚠️**
- This hop shows as `???` because it did not send a TTL time-exceeded message in response to the probe. This is not uncommon and is nothing to worry about if the missing hops are in the middle of the trace — the trace continued beyond this hop, so it is not a problem.

**Hop 4 — `14.147.135.205` — Loss: 64.4% 🚨**
- This is a major red flag on the surface, but context matters. If a network hop shows a loss percentage, check the subsequent hops. If any subsequent hop shows 0% loss, it is not actual packet loss — it is caused by the hop not generating ICMP Time Exceeded replies. However, since hop 5 also shows loss, this needs closer scrutiny.

**Hop 5 — `14.147.135.206` — Loss: 59.1% 🚨**
- Also high loss. When different amounts of loss appear across multiple hops, trust the reports from later hops. Always trace from both directions as some loss can be explained by problems in the return route.

**Hop 6 — `14.147.5.141` — Loss: 22.2% ⚠️**
- Loss drops significantly here. This is a positive sign. If the loss continues for more than one hop, it means there are some actual packet loss or routing problems. However, take the lowest percentage of loss in a sequence as the actual loss.

**Hop 7 — `(waiting for reply)`**
- If the report shows question marks but no packet loss at the destination, there is no network connection problem. Question marks are caused by a router discarding ICMP. The trace appears to still be in progress at this point (you only had 46 packets sent), and `api.binance.com` itself hasn't yet appeared as a final hop.

---

### Overall Diagnosis

**The critical question: Is the loss on hops 4–6 real?**

Packet loss or a high RTT that continues on all subsequent hops indicates an actual issue. However, some network providers configure routers not to generate ICMP Time Exceeded replies, and a router might also limit how many ICMP replies it emits — behaviors that can appear as packet loss or high latency without being real.

The pattern here — high loss at hops 4–5 (64%, 59%), dropping to 22% at hop 6 — suggests **two possible causes**:

1. **ICMP Rate Limiting (most likely):** The `14.147.x.x` ISP routers are deprioritizing ICMP probes. A single spike doesn't conclude any problem as long as subsequent hops show 0.0%. Most of the time, minimal packet loss is a result of ISP rate-limiting.

2. **Actual congestion or routing issue:** The fact that loss persists across multiple sequential hops (4, 5, 6) with no zero-loss hop in between makes this harder to dismiss as pure rate limiting.

---

### What to Do Next

1. **Run more cycles to confirm:**
   ```bash
   sudo mtr api.binance.com --report -c 200
   ```

2. **Try TCP mode on port 443** (bypasses ICMP rate limiting entirely):
   ```bash
   sudo mtr api.binance.com -T -P 443 --report -c 100
   ```

3. **Check if the final destination (hop ending at `103.200.31.172`) shows loss.** If you don't see any loss or concerning RTT on the final hop, you have a healthy network path despite intermittent hop statistics. Your output was cut off before reaching the final hop, so the verdict is still inconclusive.

4. **Run a reverse MTR** from Binance's side or use a looking glass tool to test the return path, since the path a packet takes from A to B is often not the same as B to A, meaning packet loss at a given hop is not necessarily caused by that hop.

**References:**

- [Diagnosing packet loss and latency with MTR – AWS re:Post](https://repost.aws/articles/ARYuHnu150R9ahMl-2hNNEVw/diagnosing-packet-loss-and-latency-with-mtr)
- [How to properly interpret a traceroute or MTR – APNIC Blog](https://blog.apnic.net/2022/03/28/how-to-properly-interpret-a-traceroute-or-mtr/)
- [MTR diagnose network issues – DataPacket](https://www.datapacket.com/blog/mtr-diagnose-network-issues)
- [Diagnosing Network Issues with MTR – Linode Docs](https://www.linode.com/docs/guides/diagnosing-network-issues-with-mtr/)

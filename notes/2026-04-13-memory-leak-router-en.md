---
audio: false
generated: true
image: false
lang: en
layout: post
title: Memory Leak in Router
translated: false
type: note
---

Question: After restarting my China Telecom home entrance router in Guangzhou and testing with both mobile phone and laptop through my TL-XDR3050 mesh router, I found weibo.com was slow even without VPN (DMIT.io LA server). A console restart didn't fix it, but physically unplugging the power did. Could this indicate a memory leak in the home entrance router?

Answer:

Yes, it's very possible that your home entrance router (the China Telecom broadband device) was experiencing a **memory leak** or similar resource exhaustion issue. Here's why the physical power cycle worked when a software restart didn't:

## Why Physical Power Cycle Was Necessary

**Software Restart vs. Hard Reset:**
- A **console/software restart** typically performs a graceful shutdown that may not fully clear all memory states, cached processes, or stuck network sessions
- A **physical power disconnect** (unplugging the battery/power) forces a complete hardware reset, clearing:
  - All RAM contents completely
  - Hardware buffers and caches
  - Stuck TCP connections and routing table entries
  - Any processes that failed to terminate during soft reboot

**Memory Leak Indicators:**
Your symptoms strongly suggest memory/resource exhaustion:
- Performance degradation over time (weibo.com slow)
- Issue affected both VPN and domestic connections (ruling out VPN-specific problems)
- Soft restart failed to resolve the issue
- Hard power cycle immediately restored normal function

## Common Causes in Home Routers

**Memory Leaks:**
- Consumer routers running 24/7 can accumulate memory leaks from:
  - NAT connection tracking tables filling up
  - DNS cache growing unbounded
  - Firmware bugs that don't properly release memory
  - ISP-provided routers often have less optimized firmware

**Connection Table Saturation:**
- Routers maintain tables for NAT translations, active connections, and ARP entries
- These can overflow with heavy usage, multiple devices, or long uptimes
- China Telecom routers often handle PPPoE sessions which can accumulate stale states

**Thermal Issues:**
- Prolonged operation without proper ventilation can cause:
  - CPU throttling affecting routing performance
  - Memory errors requiring full power cycle to clear

## Your Network Setup Specifics

**TL-XDR3050 as Middle Point:**
- Your TP-Link mesh router acts as a wireless access point/repeater between floors
- This adds another layer where issues could occur, but since the problem resolved after cycling the **entrance router**, that was the culprit
- The mesh router was likely functioning correctly but receiving degraded upstream performance

**Testing Methodology (Good Approach):**
- Testing both mobile and laptop confirmed device-independent issue
- Testing with/without VPN isolated the problem to domestic routing
- This systematic approach correctly identified the entrance router as the failure point

## Recommendations

**Short-term:**
- Schedule **weekly/monthly physical power cycles** of your China Telecom router (set a calendar reminder)
- Monitor if the issue recurs and note the time between power cycles

**Long-term Solutions:**
1. **Firmware Update:** Check if China Telecom has firmware updates for your router model
2. **Router Upgrade:** Consider requesting a newer model from China Telecom if your current one is older
3. **Custom Firmware:** If technically inclined and router is compatible, custom firmware like OpenWrt can resolve memory leak issues
4. **Separate Modem Mode:** If possible, put the China Telecom device in bridge/modem mode and use your TL-XDR3050 as the primary router (better firmware, more memory)

**Monitoring:**
- Keep track of router uptime and correlate with performance degradation
- If slowdowns consistently appear after X days of uptime, that confirms memory leak hypothesis

## Technical Explanation

When a router experiences memory exhaustion:
```
Normal Operation:
Available RAM → Routing processes → Release memory when done

Memory Leak:
Available RAM → Routing processes → Memory not released →
  → Gradual RAM depletion → Swap/slowdown → Packet processing delays
```

A hard power cycle breaks this chain by forcing complete memory deallocation, while a soft restart might preserve some system states or fail to properly terminate leaking processes.

Your diagnosis was correct—this is a classic symptom of embedded device resource exhaustion, common in consumer ISP-provided routers running continuously under load.

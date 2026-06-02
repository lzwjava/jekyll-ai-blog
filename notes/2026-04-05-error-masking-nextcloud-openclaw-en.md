---
audio: false
generated: true
image: false
lang: en
layout: post
title: Error Masking in Nextcloud OpenClaw Setup
translated: false
type: note
---

## Expanded: How the Errors Masked Each Other

### Error Timeline (What We Actually Saw)

```
Time (HKT)    Nextcloud Log                    OpenClaw Log
────────────────────────────────────────────────────────────────────────────────
02:04         401 Invalid backend               (nothing - requests rejected early)
               ↓
               (we fix baseUrl to http://localhost)
               ↓
02:38         401 Invalid signature            (webhook received, signature failed)
               ↓
               (we fix payload type "Activity")
               ↓
02:47         400 Invalid payload format        (schema validation failed)
               ↓
               (we patch OpenClaw for "Activity")
               ↓
02:55         400 Invalid payload format       (still failing!)
               ↓
               (we check more carefully...)
               ↓
02:55+        [no new Nextcloud errors]        room not found (token=eu42ecdy)
                                              ↑
                                              THIS was the real issue all along
```

---

### Problem #1: Signature Rejection (401) Hid Everything

**What happened:**

```
Nextcloud sends webhook → OpenClaw checks signature → REJECTED (401 Invalid backend)
                                                        ↑
                                              baseUrl didn't match
```

At this stage, OpenClaw **never even parsed the payload**, so we couldn't see:

- What payload format Nextcloud was sending
- That API calls would go to the wrong URL

**The 401 blocked ALL visibility into what came after.**

---

### Problem #2: Payload Format Error (400) Hid the API Issue

**What happened:**

```
Nextcloud sends webhook → OpenClaw parses payload → REJECTED (400 Invalid payload)
                                                        ↑
                                              "Activity" != "Create"
```

We fixed the `"Activity"` type, but then saw **new errors** — and thought the payload fix didn't work yet.

**But the real issue:** Even while Nextcloud was showing 400, OpenClaw was:

- Receiving webhooks ✅
- Attempting to send replies ❌ (going to wrong URL)
- Getting 404 on those reply attempts

The 400 from Nextcloud (reporting webhook delivery failures) made us think the whole flow was broken, when really:

- **Inbound was working** (after fixes)
- **Outbound was broken** (wrong URL for API calls)

---

### Why No Single Log Showed Everything

| Log | Shows | Missing |
|-----|-------|---------|
| **Nextcloud nextcloud.log** | Webhook delivery failures (401/400/404) | Why OpenClaw was rejecting |
| **OpenClaw gateway.log** | "room not found" on reply | That replies were going to nginx not Nextcloud |
| **OpenClaw audit log** | Blocked URL fetches | Which exact URL was being called |

**The smoking gun we missed:** When OpenClaw tried to send a reply, it called:

```
POST http://localhost/ocs/v2.php/apps/spreed/api/v1/bot/eu42ecdy/message
                         ↑
                         No port! → nginx (port 80) → 404
```

But OpenClaw's log just said "room not found (token=eu42ecdy)" — it didn't say **"I tried to call localhost without port and got 404 from nginx."**

---

### The "localhost" Ambiguity

```
┌─────────────────────────────────────────────────────────────────┐
│  "localhost" is ambiguous — different things on different hosts │
├─────────────────────────────────────────────────────────────────┤
│  From your LAPTOP:                                              │
│    localhost = your laptop (127.0.0.1)                          │
│                                                                 │
│  From NEXTLOUD DOCKER CONTAINER:                                │
│    localhost = the container itself                              │
│                                                                 │
│  From OPENCLAW (on host, Docker network):                       │
│    localhost = your laptop (127.0.0.1)                          │
│    172.17.0.1 = Docker bridge gateway                           │
│    localhost:8080 = Nextcloud (inside Docker)                   │
│    localhost:80 = nginx on host ❌ (not Nextcloud)              │
└─────────────────────────────────────────────────────────────────┘
```

**The bug:** When we set `baseUrl: "http://localhost"`, OpenClaw used it for both:

1. Verifying `X-Nextcloud-Talk-Backend` header ✅ (matched `http://localhost` from Nextcloud)
2. Making outbound API calls ❌ (called `http://localhost/ocs/...` which hit nginx, not Nextcloud)

---

### Summary: Sequential Debugging Blockers

```
Step 1: See 401 "Invalid backend"
   └─ Can't see payload format (rejected before parsing)
   └─ Can't see API URL issue (rejected before sending reply)

Step 2: Fix signature, see 400 "Invalid payload"
   └─ Focuses attention on payload schema
   └─ Miss the API URL problem (still masked by 400)

Step 3: Fix payload type, still see 400
   └─ Finally look at OpenClaw logs
   └─ See "room not found" but blame Nextcloud

Step 4: Realize replies go nowhere
   └─ Check what "localhost" actually resolves to
   └─ Find nginx vs Nextcloud port mismatch

Step 5: Fix with correct port (8080)
   └─ Finally everything works
```

The **layered failures** meant each fix revealed a new problem that was previously invisible behind the earlier error. 🦞

---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPU Droplet Limit Exceeded on DevCloud
translated: false
type: note
---

**Question:** Why does creating a GPU droplet on AMD DevCloud show "this will exceed your droplet limit" when trying to create an MI300X x8 instance?

**Answer:**

AMD DevCloud (powered by DigitalOcean's infrastructure) enforces **account-level resource limits** for new/unverified accounts. Here's why you're hitting it:

## Root Causes

### 1. Default Droplet Limit is Very Low for New Accounts

New AMD DevCloud accounts typically start with a **limit of 0 or 1 droplet**, or a very low **vCPU/RAM quota**. The MI300X x8 plan consumes:

- 160 vCPUs
- 1,920 GB RAM
- 2x NVMe disks

That alone blows past almost any default quota.

### 2. GPU Droplets Have Separate Quota Tiers

GPU resources are gated separately from regular compute. Even if your general droplet limit is fine, **GPU-specific limits** are often set to 0 by default until you request access or verify billing.

### 3. Billing/Verification Not Complete

At ~$1.99/GPU/hr × 8 GPUs = **$15.92/hr**, AMD DevCloud likely requires:

- Valid payment method confirmed
- Account identity/org verification
- Explicit quota increase request

---

## How to Fix It

### Option A: Request a Quota Increase

Go to your profile page you linked: `devcloud.amd.com/account/profile?i=cd3419`

Look for:

- **"Request Limit Increase"** or **"Quota"** section
- Submit a support ticket explaining your use case (model training, research, etc.)

### Option B: Contact AMD DevCloud Support Directly

AMD DevCloud has a support channel — mention:

- Your use case (LLM training, MI300X workload)
- Expected hours/duration
- That you've verified billing

### Option C: Check Current Limits via API (if DigitalOcean-backed)

```bash
# If they expose a DO-compatible API
curl -X GET "https://api.devcloud.amd.com/v2/account" \
  -H "Authorization: Bearer YOUR_API_TOKEN" | jq '.account.droplet_limit'
```

---

## Practical Note for Your Use Case

If you're training GPT-2 scale models or doing MI300X workloads, the MI300X x8 (1.5TB VRAM total) is massive — ROCm stack is solid for PyTorch now. But AMD DevCloud free-tier/trial accounts are intentionally capped. You likely need to either:

1. **Email them** with a use case to unlock GPU quota
2. **Upgrade to a paid/verified tier** if you haven't already
3. Start with **MI300X x1** (if available) to test that your quota allows any GPU droplets at all, then escalate

The limit message is a hard guardrail on their backend — no workaround except getting the quota raised by their team.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Create AMD GPU Droplets
translated: false
type: note
---

**Question:** I already created an AMD account — where exactly do I go to create a GPU Droplet on the AMD Developer Cloud?

**Answer:**

The AMD profile page you're looking at (`amd.com` profile) is **not** where you create GPU Droplets. The AMD Developer Cloud is a **separate website** powered by DigitalOcean. Here's the step-by-step guide:

---

## Step 1: Go to the Correct URL

The AMD Developer Cloud is accessible via **devcloud.amd.com** — it ultimately redirects to DigitalOcean, as the AMD Developer Cloud relies on DigitalOcean for the cloud environment and GPU Droplets.

👉 **Go to: [https://devcloud.amd.com](https://devcloud.amd.com)**

---

## Step 2: Sign In / Register for the AMD AI Developer Program

If you already have an AMD account, simply sign in and enroll in the AMD AI Developer Program. New users can select "Create an account" on the login page to set up an AMD account and enroll simultaneously.

Enrolling in the AMD AI Developer Program gives you **$100 in free GPU credits** (~50 hours on a single MI300X).

---

## Step 3: Add a Payment Method (Required)

Before you can create a GPU Droplet, the platform requires a valid payment method on file, **even if your credits will cover everything**. Without a card, the "Create GPU Droplet" button stays grayed out. Go to **Billing** in the left sidebar and add a card. Your credits will be consumed first; the card is a safety net for overage.

---

## Step 4: Apply for Free Credits (Optional but Recommended)

AMD is offering an initial **25 hours of complimentary cloud credit** to qualified developers who apply and are accepted. To apply, navigate to the **"GPU Droplet Page"** and fill out the credit request form. Once your credit is granted, you will see a "credits applicable" message on your droplet page.

---

## Step 5: Create a GPU Droplet

Once signed in, you will be directed to the **Create a GPU Droplet** page, where your credits should appear at the top. Then:
- **Select Hardware:** Choose a single MI300X instance
- **Select Image:** Choose the ROCm Software image (or vLLM Quick Start if you want a ready-to-use LLM stack)
- **Configure Access:** Add your SSH key

The droplet takes **2–4 minutes** to provision. You'll see it move from "Creating" to "Active" in the dashboard. Choose **ATL1 (Atlanta)** as the region, as it consistently has MI300X availability.

---

## Step 6: Connect to Your Droplet

Once active, you can connect via:

- **SSH** from your terminal: `ssh root@<your-droplet-ip>`
- **Web Console** button directly in the dashboard
- **JupyterLab** environment (if you chose that image — accessible in browser, no setup needed)

---

## Important Billing Warning

When you **power off** your GPU VM, you are **still billed** for it, because your disk space, CPU, RAM, and IP address are all reserved. Charges are made until you **destroy** the instance.

Always **Destroy** (not just power off) the droplet when you are done to stop charges.

---

## Pricing Reference

| Configuration | Price |
|---|---|
| 1x AMD Instinct MI300X (192 GB VRAM) | $1.99/hour |
| 8x AMD Instinct MI300X (1536 GB VRAM) | $15.92/hour |
| Free credits (AMD AI Developer Program) | ~$100 (~50 hours) |

---

**References:**

- [AMD Developer Cloud Official Page](https://www.amd.com/en/developer/resources/cloud-access/amd-developer-cloud.html)
- [How to Get Started on AMD Developer Cloud (AMD Blog)](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD Developer Cloud Tutorial – Lablab.ai](https://lablab.ai/ai-tutorials/amd-developer-cloud-host-llm-vllm)
- [Phoronix Review of AMD Developer Cloud](https://www.phoronix.com/review/amd-developer-cloud)
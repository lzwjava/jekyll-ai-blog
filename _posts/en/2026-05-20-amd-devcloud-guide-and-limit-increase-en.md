---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD DevCloud Guide and Limit Increase
translated: false
type: note
---

**Question:** How does AMD Developer Cloud (devcloud.amd.com) work, and how do you increase the Droplet limit?

---

## AMD Developer Cloud — How It Works

The key architectural fact: **devcloud.amd.com is DigitalOcean under the hood.** The AMD Developer Cloud relies on DigitalOcean for the cloud environment and ultimately deploys GPU Droplets. You can create either a single-GPU or 8x GPU AMD Instinct MI300X instance. AMD is essentially a reseller/partner skin on top of DO's GPU infrastructure.

### What You Get

It provides easy access to AMD GPUs via Docker containers preloaded with popular AI software, minimizing setup time, while giving developers flexibility to customize code. A Jupyter Notebook environment runs inside containers and is available upon VM launch — no local setup needed.

The hardware: MI300X has 192GB of HBM3 memory, making it practical for running 70B+ parameter models on a single instance without model parallelism.

### Access & Credits

To apply, visit devcloud.amd.com and create an account or log in to complete the "Request Credit" form. If approved, an initial 25 hours of cloud credit will be added to your account.

Credit allocation is determined by AMD based on the intended use case (inference, training, fine-tuning) and a detailed description of how you plan to use GPU credit. You may also add a payment option and pay-as-you-go, or switch to the production cloud anytime.

Key gotcha: If a GPU instance is powered off, you are still billed and credit hours still apply. Charges are incurred until the instance is destroyed.

### VM Configuration Options

Users can configure a VM from scratch with their preferred AI/ML software, choose a VM with pre-installed Docker images for major frameworks (PyTorch, vLLM, etc.), or launch directly into a ready-to-use JupyterLab environment available at VM creation.

---

## Increasing the Droplet Limit

Since AMD Developer Cloud is DigitalOcean, the Droplet limit (10 by default) is managed through the DO control panel.

**Steps:**

In the left menu of the DigitalOcean Control Panel, click **Resource Limits**. Then click **Request an increase** on the top right. In the dropdown, choose the resource (Droplets or GPU Droplets), enter the new limit, and describe your use case in the Reason field. Click Submit.

**What to write in the reason field** — be specific. Based on community reports: approval depends on explaining your use case and expected workload, and may depend on your current plan and usage history.

For GPU Droplets specifically: to create multi-node GPU Droplets, you need to contact support to enable that functionality for your team — the control panel alone isn't sufficient.

**Contact AMD directly** for credit/access issues: `devcloudrequests@amd.com`

---

## Practical Notes for Your Use Case

- The MI300X + ROCm stack is the main value prop — it's the only way to test ROCm-native code (HIP, rocBLAS, hipBLAS) without owning the hardware
- The 25 free hours is enough for a quick fine-tune run (LoRA on a 7B model fits comfortably in 192GB)
- **Destroy instances when done** — idle billing is a real trap
- If you're benchmarking PyTorch ROCm vs CUDA, this is the cheapest legit path without buying MI300X hardware

References:

- [AMD Developer Cloud — How to Get Started](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD Cloud Access & Credit Program](https://www.amd.com/en/developer/resources/cloud-access.html)
- [Phoronix Review — AMD Developer Cloud on DigitalOcean](https://www.phoronix.com/review/amd-developer-cloud)
- [DigitalOcean — View and Request Resource Limits](https://docs.digitalocean.com/platform/teams/how-to/view-resource-limits/)
- [DigitalOcean Droplet Limits Documentation](https://docs.digitalocean.com/products/droplets/details/limits/)
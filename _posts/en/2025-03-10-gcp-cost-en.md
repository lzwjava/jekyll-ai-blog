---
audio: false
generated: true
lang: en
layout: post
title: GCP Cost Estimation for VPN in Taipei
translated: false
type: note
---

To estimate the cost of using a Taipei server as a VPN with Google Cloud, considering you live in Guangzhou and expect 50 GB of network data per month using an E2 micro instance, we need to break down the costs into several components: the virtual machine (VM) instance, network egress traffic, and the persistent disk storage. Here’s a detailed calculation based on Google Cloud’s pricing for the asia-east1 region (Taipei), where your server will be hosted.

### 1. VM Instance Cost (E2 Micro in Taipei)
The E2 micro is a shared-core machine type with 0.25 vCPU and 1 GB of memory. According to Google Cloud’s pricing for Compute Engine in the asia-east1 region:
- **Hourly rate for E2 micro**: $0.0084 per hour.
- **Hours in a month**: Assuming a typical month has 730 hours (a standard approximation based on 365 days ÷ 12 months ≈ 30.42 days × 24 hours).
- **Monthly cost**:
  $0.0084/hour × 730 hours ≈ $6.132.

So, running the E2 micro instance continuously for a month costs approximately **$6.13**.

### 2. Network Egress Traffic Cost
Since you’re using the Taipei server as a VPN from Guangzhou, your setup involves running a VPN server (e.g., OpenVPN) on the E2 micro instance, not Google Cloud’s Cloud VPN service. Your 50 GB of monthly network data represents the total traffic processed through the VPN. Here’s how the traffic flows:
- **From your device in Guangzhou to the VPN server**: This is ingress traffic to Google Cloud (free).
- **From the VPN server to the internet**: This is egress traffic (charged).
- **From the internet back to the VPN server**: This is ingress traffic (free).
- **From the VPN server back to your device**: This is egress traffic (charged).

If your 50 GB refers to the total VPN tunnel traffic (data sent from your device plus data received back), the egress traffic billed by Google Cloud includes:
- Data sent from the VPN server to the internet.
- Data sent from the VPN server back to your device.

Assuming the 50 GB is the total data transferred (e.g., you send requests and receive responses, like browsing or streaming), the total egress traffic is approximately 50 GB. This simplifies the estimation, as the exact split between sent and received data depends on usage (e.g., streaming has more received data, while uploads have more sent data). For general internet usage, we’ll treat the 50 GB as the total egress.

Google Cloud charges for internet egress based on the source region (asia-east1 for Taipei):
- **Pricing tier**: For Asia (excluding China, India, Indonesia, and the Philippines), the rate is $0.12 per GiB for the first 1 TB of monthly egress.
- **Conversion**: Google Cloud uses GiB (1 GiB = 1024³ bytes), while you specified 50 GB (1 GB = 1000³ bytes). Precisely, 1 GB ≈ 0.931 GiB, so 50 GB ≈ 46.55 GiB. However, for simplicity and common practice in rough estimates, we’ll approximate 50 GB ≈ 50 GiB, as the difference is minor for small volumes.
- **Egress cost**:
  50 GiB × $0.12/GiB = $6.00.

Thus, the network egress cost is approximately **$6.00** per month.

### 3. Persistent Disk Cost
The E2 micro instance requires a boot disk. While Google Cloud’s free tier offers 30 GB of standard persistent disk storage in certain US regions, Taipei (asia-east1) is not included, so you’ll incur charges:
- **Disk size**: Assuming a typical 30 GB standard persistent disk (you could use less, like 10 GB, but 30 GB is common for a basic VM).
- **Pricing**: $0.040 per GB per month in asia-east1 for standard persistent disk.
- **Monthly cost**:
  30 GB × $0.040/GB = $1.20.

The persistent disk adds **$1.20** per month.

### 4. External IP Address
Your VPN server needs an external IP address to be accessible from Guangzhou. For Compute Engine VMs:
- If the IP is attached to a running VM, there’s no additional charge.
- If reserved but unused, there’s a small fee (not applicable here since the VM runs continuously).

Since your E2 micro will use the external IP, this cost is **included in the VM price**.

### Total Estimated Cost
Adding up all components:
- **VM instance**: $6.13
- **Egress traffic**: $6.00
- **Persistent disk**: $1.20
- **External IP**: $0.00 (included)

**Total**: $6.13 + $6.00 + $1.20 = **$13.33 per month**.

### Additional Notes
- **Ingress traffic**: Free, so data entering the VM (from you or the internet) incurs no cost.
- **No free tier**: The E2 micro free tier applies only to specific US regions (not Taipei), and the 1 GB free egress is from North America (not Asia), excluding China destinations, so it doesn’t apply here.
- **Usage assumptions**: The $13.33 assumes 50 GB is the total egress traffic. If it’s only data sent or received, adjust the egress cost proportionally (e.g., if 50 GB is data received, egress to you is $6.00, but egress to the internet might be less).
- **No Cloud VPN**: Since you’re running your own VPN software (e.g., OpenVPN), there are no additional Cloud VPN gateway or tunnel charges.

### Final Answer
The estimated cost of using a Taipei server (asia-east1) as a VPN on Google Cloud with an E2 micro instance, 50 GB of monthly network data, and a 30 GB disk is approximately **$13.33 per month**. This includes the VM instance ($6.13), egress traffic to the internet and your device ($6.00), and the persistent disk ($1.20).

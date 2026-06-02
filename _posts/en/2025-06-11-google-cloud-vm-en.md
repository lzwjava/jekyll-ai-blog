---
audio: false
generated: true
lang: en
layout: post
title: Cheapest Simple Google Cloud VM
translated: false
type: note
---

When looking for a cost-effective virtual machine (VM) on Google Cloud, there are a few options and considerations to keep in mind to meet your budget of around $5 per month. Here are some steps and tips to help you find the cheapest VM option:

1. **Shared-Core VMs**: Google Cloud offers shared-core VMs, which are the most budget-friendly options. These VMs share CPU power with other customers, which can result in less robust performance but are significantly cheaper. This might be a good starting point for a simple server with low resource requirements.

2. **Preemptible VMs**: Consider using preemptible VMs, which offer substantial discounts compared to regular VMs. These VMs can be terminated by Google Cloud if their resources are needed elsewhere, so they are best suited for fault-tolerant workloads. Preemptible VMs can provide discounts of up to 80% off regular prices.

3. **Tau VMs**: Google Cloud's Tau VMs are designed for scale-out workloads and offer up to 42% higher price performance compared to general-purpose VMs. These might be more cost-effective for certain types of workloads.

4. **Custom Machine Types**: You can create custom machine types tailored to your specific needs, which can help reduce costs by only paying for the resources you need. This flexibility allows you to fine-tune the CPU and memory to match your workload requirements.

5. **Sustained Use Discounts**: Google Cloud automatically applies sustained use discounts for VMs that run for a significant portion of the billing month. The discount increases with usage and can go up to 30% off the regular price.

6. **Free Tier**: Google Cloud offers a free tier that includes a small amount of compute resources each month. This might be sufficient for very lightweight applications and can help reduce costs further.

7. **Cost Calculator**: Use the Google Cloud Pricing Calculator to estimate the costs of different configurations and find the most cost-effective setup for your needs.

8. **Spot VMs**: Spot VMs offer dynamic pricing with discounts of 60-91% off the on-demand price for most machine types. These can be a very cost-effective option if your workload can tolerate interruptions.

For a simple server with low resource requirements, starting with a shared-core or preemptible VM might be the best approach. You can then monitor the performance and adjust the configuration as needed to balance cost and performance.

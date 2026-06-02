---
audio: false
generated: true
image: false
lang: en
layout: post
title: "DeepSeek-V2: A Masterclass in Efficiency"
translated: false
type: note
---

DeepSeek-V2 is famous in the AI world specifically because it cost significantly **less** than the $500 million figure you mentioned. While companies like OpenAI and Meta are spending billions on infrastructure, DeepSeek’s approach is a masterclass in efficiency.

Here is the breakdown of the costs, GPU hours, and hardware used for DeepSeek-V2:

### **1. Training Cost**
DeepSeek-V2 was remarkably cheap to train compared to its peers.
* **Estimated Cost:** Approximately **$2 million to $5 million USD** for the final training run.
* **Context:** For comparison, training a model of similar caliber (like Llama 3 70B or GPT-4) typically costs tens or even hundreds of millions of dollars. DeepSeek achieved this by using a **Mixture-of-Experts (MoE)** architecture, where only a fraction of the parameters (21B out of 236B) are active for any given task, drastically cutting down the math required.

### **2. GPU Hours & Compute**
The training efficiency is best seen in the total compute time:
* **Total GPU Hours:** DeepSeek reported using approximately **2.7 to 2.8 million GPU hours** for the V2/V3 training cycles.
* **Training Data:** They processed a massive corpus of **8.1 trillion tokens** during this time.
* **Inference Efficiency:** Because of their "Multi-head Latent Attention" (MLA) tech, they also reduced the KV cache (memory usage) by **93.3%**, making it one of the cheapest models to actually run (inference) once training is finished.

### **3. Hardware (The "Cards")**
DeepSeek’s hardware choice was strategic, partly due to US export restrictions on high-end chips to China.
* **GPU Model:** They primarily used **NVIDIA H800** GPUs.
    * The H800 is a "China-specific" version of the flagship H100. It has the same raw computing power but limited interconnect speeds (NVLink) to comply with trade regulations.
* **Cluster Size:** While they have access to a massive cluster of roughly **50,000 GPUs** for various tasks, the specific training runs for these models usually utilize a subset of around **2,000 to 10,000 GPUs** at a time.
* **Alternative Hardware:** They have also historically used **NVIDIA A100** clusters (specifically their "Fire-Flyer 2" cluster which had about 5,000 A100s).

### **Summary Table**

| Feature | DeepSeek-V2 Details |
| :--- | :--- |
| **Total Parameters** | 236 Billion |
| **Active Parameters** | 21 Billion (per token) |
| **Training Cost** | ~$5 Million (Final Run) |
| **Hardware** | NVIDIA H800 / A100 |
| **GPU Hours** | ~2.8 Million |
| **Main Innovation** | Multi-head Latent Attention (MLA) & MoE |

---
**References:**
* [DeepSeek-V2 Technical Report (arXiv)](https://arxiv.org/html/2405.04434v5)
* [Stratechery: DeepSeek FAQ](https://stratechery.com/2025/deepseek-faq/)
* [DeepSeek-V3 Training Cost Analysis](https://spreadsheets-are-all-you-need.ai/flops-demystified-ai-and-the-math-behind-deepseek-training-costs/)

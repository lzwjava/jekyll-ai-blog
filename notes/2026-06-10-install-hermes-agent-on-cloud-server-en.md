---
audio: false
generated: true
image: false
lang: en
layout: post
title: Install Hermes Agent on Cloud Server
translated: false
type: note
---

Question: Should I install Hermes Agent on my AMD Developer Cloud server for LLM experiments, or keep it on my laptop and use SSH?

Answer: For LLM training and inference experiments on an AMD Developer Cloud instance, you should **install Hermes Agent directly on the cloud server** (or configure your laptop's Hermes instance to use its native **SSH terminal backend**).

Here is why putting Hermes Agent on the cloud server or leveraging its native remote execution is the superior setup, compared to manually SSHing from your laptop every time:

### 1. Autonomous, Long-Running Experiments

LLM training and fine-tuning take time. If you run Hermes Agent on your laptop and force it to manually SSH for every action, your experiment will fail or halt the moment your laptop sleeps, loses Wi-Fi, or disconnects.

* Installing Hermes directly on the AMD server allows it to run 24/7.
* You can disconnect entirely, shut your laptop, and interact with the agent remotely through messaging platforms like Telegram, Discord, or Slack.

### 2. Native Multi-Backend Sandboxing

Hermes Agent natively supports **6 terminal backends**, including **Local** and **SSH**.

* **If you prefer the Hermes Desktop GUI on your laptop:** You don't need to manually SSH anymore. You can install Hermes on your laptop, configure its backend to **SSH**, and point it to your AMD Cloud instance. Hermes will autonomously manage the SSH connections, execute bash scripts, run Python code, and read files directly on the GPU cluster.
* **If you want complete independence:** Run the CLI version directly on the AMD server via Docker or a standard install, which gives Hermes ultra-fast local execution speed for handling datasets, logs, and model checkpoints.

### 3. Training Loop Integration & Tool Gateway

Hermes Agent features a continuous learning loop that saves successful code patterns, error resolutions, and commands as markdown "skills." If Hermes lives on the server (or manages it natively via the SSH backend), it can actively look at your AMD ROCm/PyTorch logs, catch CUDA out-of-memory errors, modify hyperparameters, and restart the training loop automatically without you playing middleman.

---

### Summary Recommendation

| Approach | Recommendation | Best For |
| --- | --- | --- |
| **Install on AMD Cloud (Local/Docker)** | **Highly Recommended** | Heavy automation, 24/7 training runs, and interacting with your server via CLI or mobile chat apps (Telegram/Slack). |
| **Install on Laptop using Hermes SSH Backend** | **Great alternative** | If you prefer using the **Hermes Desktop App** interface while allowing the agent to handle the SSH heavy lifting on the cloud GPU. |
| **Manual SSH from Laptop** | **Not Recommended** | Tethering yourself to a terminal defeats the purpose of an autonomous agent; any network drop kills your pipeline. |

To get started on your AMD cloud instance, you can simply run the server setup script:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes setup

```

References:

* [Hermes Agent Documentation](https://hermes-agent.nousresearch.com/docs/)
* [Hermes Agent Official NEW Desktop App Video](https://www.youtube.com/watch?v=nb5ALoAGAbE)

This video walks through the native Hermes Desktop application interface, showing how the agent manages persistent environments, file trees, and automation tasks.

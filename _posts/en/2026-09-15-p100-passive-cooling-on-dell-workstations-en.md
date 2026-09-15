---
audio: false
generated: true
image: false
lang: en
layout: post
title: P100 passive cooling on Dell workstations
translated: false
type: note
---

**Question:** What is a seller on Xianyu saying about using a P100 GPU card without buying an extra fan?

**Answer:**

The seller is sharing their experience using a **Dell workstation** with a **P100 GPU card**, and their advice is:

- They **did NOT buy an extra fan** — instead, they maxed out their Dell workstation's built-in fans to provide cooling.
- For **regular desktop PCs (普通主机)**, they recommend **buying an additional fan** since normal cases don't have strong enough airflow.
- However, if **your PC already has strong airflow/cooling**, you can try running the P100 without an extra fan first.

**Key takeaway:** The P100 is a **passive cooled** GPU (no built-in fan), so it relies entirely on case airflow. Dell workstations have powerful server-grade fans, which is why it works for the seller — but most regular PCs will need an aftermarket fan blowing directly on the card.

---

**References:**

- [NVIDIA Tesla P100 Overview](https://www.nvidia.com/en-us/data-center/tesla-p100/) — confirms passive cooling design
- [Xianyu (闲鱼)](https://www.goofish.com/) — Chinese second-hand marketplace where this listing appears

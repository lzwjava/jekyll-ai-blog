---
audio: false
generated: true
image: false
lang: en
layout: post
title: Quadro 410 No Native HDMI Port
translated: false
type: note
---

**Question:** Does the Quadro 410 have an HDMI port? What is it?

**Answer:**

The Quadro 410 does **not** have a native HDMI port. Quadro GPUs do not feature a native HDMI port.

However, you can still connect to an HDMI display using an adapter:

- **DVI → HDMI** cable/adapter — DVI and HDMI are pin compatible, so it is possible to run HDMI signaling over single link DVI cables, and even though the cable is single link in this mode you get the full HDMI 1.4 bandwidth.
- **DisplayPort → HDMI** dongle — a DisplayPort to HDMI cable can be used (resolution limited by the DisplayPort spec).

So the card's two physical ports are **DVI-I** and **DisplayPort** only — HDMI is only achievable via adapter, not a built-in connector.

---

**References:**

- [NVIDIA Support – Connecting Quadro to HDMI](https://nvidia.custhelp.com/app/answers/detail/a_id/3567/~/how-to-connect-a-stereo-display-to-the-quadro-card-hdmi-port)
- [PNY Quadro 410 Datasheet](https://www.azken.com/download/Nvidia_Quadro_410.pdf)

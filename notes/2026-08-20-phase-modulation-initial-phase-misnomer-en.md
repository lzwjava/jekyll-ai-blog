---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Phase Modulation: Initial Phase Misnomer"
translated: false
type: note
---

Question: Why is phase modulation (调相) described as "the initial phase of the carrier varying with the digital baseband signal"? Is this description accurate?

Answer:

This is actually a **subtle but important point** worth clarifying.

**What Phase Modulation (PSK) actually means:**

In digital phase modulation (Phase Shift Keying), the **instantaneous phase** of the carrier changes according to the baseband signal — not specifically the "initial phase" (初始相位).

The carrier signal is expressed as:

> s(t) = A · cos(2πf_c·t + **φ(t)**)

Where **φ(t)** is the phase that carries the information. For example:
- In BPSK: φ = 0° for bit "1", φ = 180° for bit "0"

**Why "initial phase" (初始相位) is a misleading term here:**

- "Initial phase" (初始相位) technically refers to the phase at t = 0, which is a fixed constant.
- In PSK, the phase shifts **continuously over time** as the data changes — so calling it "initial phase" is imprecise.
- The more accurate term is **instantaneous phase** (瞬时相位).

**Why option B is still marked correct in Chinese textbooks:**

In many Chinese telecommunications textbooks (e.g., 樊昌信《通信原理》), "初始相位随基带信号变化" is used as a **simplified pedagogical shorthand** to distinguish PSK from:
- 调幅 (AM): amplitude varies
- 调频 (FM): frequency varies
- 调相 (PM/PSK): **phase** varies

The intent is correct even if "初始相位" is not the most rigorous term. The key idea is that **the phase parameter** — not amplitude or frequency — is what encodes the information.

So B is the intended correct answer because it correctly identifies **which carrier parameter** is modulated, even though "初始相位" is a loose use of terminology.

References:
- [Phase-shift keying (PSK) – Wikipedia](https://en.wikipedia.org/wiki/Phase-shift_keying)
- [通信原理（第7版）樊昌信 – 相关章节](https://book.douban.com/subject/4749385/)

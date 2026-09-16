---
audio: false
generated: true
image: false
lang: en
layout: post
title: "USENIX: Systems Research Conferences"
translated: false
type: note
---

Question: What is USENIX, and what kind of conference is it?

Answer:

[USENIX](https://www.usenix.org?utm_source=chatgpt.com) is **not one conference**. It’s a nonprofit computing research organization that runs a family of highly technical systems conferences. Their focus is roughly:

> **“How do we build real computer systems that actually work?”**

It’s especially strong in **systems / infrastructure / security / networking / storage / OS / distributed systems**. USENIX describes its conferences as vendor-neutral venues for groundbreaking computing-systems research, with free/open access to proceedings and videos. ([USENIX][1])

The important conferences are:

| Conference          | Area                                   | Think                                      |
| ------------------- | -------------------------------------- | ------------------------------------------ |
| **OSDI**            | Operating systems, distributed systems | Linux / databases / runtimes / infra       |
| **NSDI**            | Networking + distributed systems       | datacenter networks, cloud, edge           |
| **USENIX Security** | Security                               | systems security, crypto, attacks/defenses |
| **FAST**            | Storage                                | SSDs, filesystems, storage systems         |
| **ATC**             | Broad systems                          | practical systems engineering              |
| **SREcon**          | Production/SRE                         | reliability, large-scale operations        |
| **SAIS**            | Secure agentic AI                      | newer AI-agent systems/security            |

USENIX currently lists **OSDI, NSDI, FAST, Security, SREcon**, and newer areas such as **SAIS (Secure Agentic-AI Systems)** among its conferences. ([USENIX][2])

### Why engineers care

The interesting thing about USENIX is that the papers tend to be **implementation-heavy**.

A typical systems paper isn't:

```text
We propose an exciting architecture.
```

It's more like:

```text
We built X
→ here's the architecture
→ here's the implementation
→ here's the workload
→ here's the baseline
→ here's the benchmark
→ here's where it breaks
→ here's why it is faster/cheaper/more reliable
```

For someone doing **LLM training/inference infrastructure, distributed systems, GPU clusters, storage, networking, or agents**, I'd pay particular attention to **OSDI + NSDI + FAST + SREcon**.

And there's a huge practical advantage: **USENIX makes its conference papers freely readable**, so you can basically treat the proceedings as a very high-quality open research feed. ([USENIX][1])

One useful mental model:

```text
ML conferences
  NeurIPS / ICML / ICLR
       ↓
  models + algorithms

Systems conferences
  OSDI / NSDI / FAST / ATC
       ↓
  machines + networks + storage + distributed software
```

For your kind of work, **OSDI/NSDI papers are probably much closer to the engineering problems underneath an LLM company than the average ML paper**.

I can also dig through the **last 2–3 years of OSDI/NSDI/FAST papers and pull out the ones most relevant to LLM inference/training infrastructure**.

[1]: https://www.usenix.org/ "USENIX Home | USENIX"
[2]: https://www.usenix.org/conferences/all?order=field_conference_date&sort=desc&utm_source=chatgpt.com "All Conferences | USENIX"

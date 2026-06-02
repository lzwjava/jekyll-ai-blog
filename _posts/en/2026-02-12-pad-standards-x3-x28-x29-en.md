---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: PAD Standards X.3 X.28 X.29
translated: false
type: note
---

Question: As an extension to the X.25 standard, CCITT proposed a set of three standards related to the Packet Assembler/Disassembler (PAD) facility. Which of the following are they?

Answer:

The correct answer is **C. X.3, X.28 and X.29**.

**Detailed explanation:**

The **Packet Assembler/Disassembler (PAD)** is a network device/function that allows non-packet-mode (character-mode) asynchronous terminals (such as dumb terminals or modems) to access packet-switched networks like those using X.25.

CCITT (now ITU-T) defined **three closely related recommendations** specifically for PAD operation:

- **X.3** — Packet Assembly/Disassembly facility (PAD) parameters
  Defines the **functions** and **configurable parameters** of the PAD (e.g., idle timer, line folding, character echoing, data forwarding conditions, editing functions, etc.). It specifies what the PAD actually does and how it can be parameterized.

- **X.28** — DTE/DCE interface for a start-stop mode DTE accessing the PAD in a public data network situated in the same country
  Defines the **user interface** between an asynchronous terminal (start-stop mode DTE) and the PAD. It covers:
  - How a terminal connects to the PAD
  - PAD command language (e.g., setting parameters with SET? READ? commands)
  - Profile selection
  - Call establishment/clearing procedures from the terminal side

- **X.29** — Procedures for the exchange of control information and user data between a PAD facility and a packet mode DTE or another PAD
  Defines the **protocol** between the PAD and the remote packet-mode host (or another PAD).
  It specifies how control information (e.g., parameter setting requests, break signals, reset) and user data are carried inside X.25 data packets using **Qualified Data (Q-bit = 1)** packets.

These three standards together form the complete PAD framework:

- X.3 = what the PAD does (functions & parameters)
- X.28 = how the terminal talks to the PAD
- X.29 = how the PAD talks to the network/host

**Why the other options are incorrect:**

- **A. X.3, X.25 and X.28** → X.25 is the base packet-layer protocol, not a PAD-specific standard.
- **B. X.3, X.25 and X.29** → Again includes X.25 instead of X.28, missing the terminal-to-PAD interface.
- **D. X.25, X.28 and X.29** → Includes X.25 (core protocol) but omits X.3, which is the actual definition of PAD parameters/functions.

**Memory tip (as provided):**
"三分包，28端，29网"
→ Three standards for PAD:
X.3 = PAD itself (包)
X.28 = terminal side (端)
X.29 = network/host side (网)

References:

- None (standard ITU-T/CCITT X-series recommendations for X.25-based packet networks and PAD operation)

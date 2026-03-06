---
audio: false
generated: true
image: false
lang: en
layout: post
title: Link Encryption Exposes Plaintext Nodes
translated: false
type: note
---

**Question:** When link encryption is used for information, how does information exist at each intermediate node in the network?

- A. Ciphertext at the sending node, plaintext at the receiving node
- B. Plaintext at the sending node, ciphertext at the receiving node
- C. Ciphertext
- D. Plaintext

**Correct Answer: D — Plaintext**

---

**Answer:**

## Understanding Link Encryption and Intermediate Nodes

### How Link Encryption Works

Link encryption (also called **online encryption**) operates at the **Data Link Layer** — it encrypts data only on the physical transmission links between adjacent nodes. The key characteristic is:

- Data is encrypted **before** leaving one node onto the wire
- Data is **decrypted** when it arrives at the next intermediate node
- Data is then **re-encrypted** before being forwarded to the next link

In link encryption, from source to destination, data passes through many intermediate nodes. At each intermediate node, the message is exposed in **plaintext** (except in node encryption). If any node on the link has weak security protection, then according to the "weakest link" principle, the overall link security is only as strong as the weakest node.

### Why the Answer is D (Plaintext), Not C (Ciphertext)

This is a subtle but critical distinction:

| Location | State of Data |
|---|---|
| On the wire (between nodes) | **Ciphertext** ✅ |
| **Inside an intermediate node** | **Plaintext** ✅ |

The question asks about how information **exists at the nodes** — not on the links. Since each node must decrypt to read routing information and then re-encrypt for the next hop, the receiving party for each link segment is the intermediate node machine itself, and information must be decrypted and re-encrypted at each node, thus appearing in plaintext inside each node.

### Why This Is a Security Weakness

This is the **biggest vulnerability of link encryption**: every intermediate node becomes a potential attack surface. An attacker who compromises any intermediate node gains full access to plaintext data.

This contrasts with:
- **Node encryption**: Uses a secure hardware module at each node so plaintext is never exposed in readable memory
- **End-to-end encryption**: Data stays encrypted all the way from sender to final recipient; intermediate nodes only see ciphertext

### Why Option C (Ciphertext) Is a Common Mistake

Many students confuse the **transmission links** (where data IS ciphertext) with the **nodes themselves** (where data must be plaintext for routing/processing). The question specifically asks about existence **at the nodes**, making **D (Plaintext)** the correct answer.

---

**References:**

- [链路加密、节点加密与端到端加密对比](https://www.grt-china.com/xinwenzixun/825.html)
- [What is Link Encryption – CyberGhost VPN](https://www.cyberghostvpn.com/glossary/link-encryption)
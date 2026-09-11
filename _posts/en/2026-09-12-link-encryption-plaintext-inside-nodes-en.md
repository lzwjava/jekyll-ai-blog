---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Link Encryption: Plaintext Inside Nodes"
translated: false
type: note
---

Question: In link encryption (链路加密), is the information at every node in plaintext (明文) or ciphertext (密文)?

Answer:

In **link encryption** (链路加密), information exists as **plaintext (明文) inside every intermediate node** and as **ciphertext (密文) on the transmission links** between the nodes.

When data travels across a network using link encryption, the process unfolds as follows:

1. **On the Transmission Link:** Data is encrypted before leaving a node and travels across the physical link as **ciphertext**.
2. **At an Intermediate Node (Switch/Router):**
* The node receives the ciphertext from the incoming link.
* It **decrypts** the data back into **plaintext** in its memory.
* It inspects the packet header/address information to determine the next destination.
* It **re-encrypts** the data into ciphertext using the key shared with the next link before sending it out.



### Summary Comparison

* **Link Encryption:** Data is ciphertext on the wire/link, but decrypted to **plaintext** at every intermediate node. (Requires nodes to be physically secure).
* **End-to-End Encryption (端到端加密):** Data remains **ciphertext** at all intermediate nodes and is only decrypted to plaintext at the final destination node.

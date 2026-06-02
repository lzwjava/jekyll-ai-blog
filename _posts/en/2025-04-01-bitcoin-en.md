---
audio: false
generated: true
lang: en
layout: post
title: How Bitcoin Works
translated: false
type: note
---

Technically, Bitcoin works through a combination of cryptography, a peer-to-peer network, and a consensus mechanism called Proof-of-Work (PoW). Here's a breakdown of the key components and processes:

**1. Cryptographic Foundations:**

* **Hashing (SHA-256):** Bitcoin heavily relies on the SHA-256 cryptographic hash function. This function takes any input data and produces a fixed-size 256-bit output (the hash). Key properties of SHA-256 used in Bitcoin include:
  * **Deterministic:** The same input always produces the same output.
  * **One-way:** It's computationally infeasible to reverse the process and find the input from the output.
  * **Collision-resistant:** It's extremely difficult to find two different inputs that produce the same output.
* **Digital Signatures (ECDSA):** Bitcoin uses the Elliptic Curve Digital Signature Algorithm (ECDSA) for securing transactions. Each Bitcoin user has a pair of cryptographic keys:
  * **Private Key:** A secret key that allows the user to authorize (sign) transactions.
  * **Public Key:** A key derived from the private key that can be shared with others. It's used to verify the authenticity of transactions signed by the corresponding private key.
* **Bitcoin Addresses:** These are derived from public keys using a series of hashing and encoding steps. They are the "addresses" that users share to receive Bitcoin.

**2. The Blockchain:**

* **Distributed Ledger:** Bitcoin maintains a public, decentralized ledger called the blockchain. This ledger records every Bitcoin transaction in a chronological and transparent manner.
* **Blocks:** Transactions are grouped into blocks. Each block contains:
  * A set of verified transactions.
  * A reference to the hash of the **previous block** in the chain. This creates the chain-like structure.
  * A **nonce**: A random number used in the mining process.
  * A **timestamp**.
  * The hash of the current block itself.
* **Immutability:** Once a block is added to the blockchain, it becomes extremely difficult to alter it because doing so would require recomputing the hashes of that block and all subsequent blocks, which would be computationally infeasible for an attacker controlling less than 51% of the network's computing power.

**3. Transactions:**

* **Structure:** A Bitcoin transaction typically includes:
  * **Inputs:** References to previous transactions where the sender received the Bitcoin they are now spending. These are essentially pointers to specific "unspent transaction outputs" (UTXOs).
  * **Outputs:** Specify the recipient's Bitcoin address(es) and the amount of Bitcoin being sent to each. A transaction can have multiple outputs.
  * **Signature:** A digital signature created using the sender's private key. This proves that the owner of the Bitcoin authorized the transaction.
* **Broadcasting:** Once a transaction is created and signed, it's broadcast to the Bitcoin peer-to-peer network.

**4. Mining and Proof-of-Work:**

* **Miners:** These are nodes in the Bitcoin network that perform the work of verifying and adding new transactions to the blockchain.
* **Transaction Verification:** Miners collect pending, unconfirmed transactions from the network and verify their validity (e.g., ensuring the sender has enough Bitcoin to spend and that the digital signatures are valid).
* **Creating a Block:** Miners bundle these verified transactions into a new block. They also include a special transaction called a "coinbase transaction" that awards them newly minted Bitcoin and any transaction fees paid by the senders in the transactions included in the block.
* **Proof-of-Work (PoW):** To add a new block to the blockchain, miners must solve a computationally difficult puzzle using the SHA-256 algorithm. This process is called "mining."
  * Miners repeatedly change the **nonce** (a random number) in the block header.
  * For each nonce, they calculate the SHA-256 hash of the entire block header.
  * The goal is to find a nonce that results in a hash that starts with a certain number of leading zeros. The number of leading zeros required is determined by the **difficulty** of the Bitcoin network.
  * Finding such a hash is a matter of trial and error and requires significant computational power.
* **Block Validation and Consensus:** Once a miner finds a valid hash (the "proof-of-work"), they broadcast the new block to the rest of the network. Other nodes on the network then verify:
  * The transactions in the block are valid.
  * The hash of the block is correct.
  * The hash meets the current difficulty target.
  * The previous block's hash reference is correct.
* **Adding to the Blockchain:** If the block is valid, other nodes accept it and add it to their copy of the blockchain, extending the chain. This process ensures that all nodes agree on the order and validity of transactions. The longest chain is considered the authoritative version.

**5. Incentives:**

* **Block Reward:** Miners who successfully mine a new block are rewarded with a certain amount of newly created Bitcoin (currently 3.125 BTC, which halves approximately every four years in an event called the "halving").
* **Transaction Fees:** Miners also collect the transaction fees that users voluntarily include when sending Bitcoin. These fees incentivize miners to prioritize certain transactions.

**6. Decentralization and Security:**

* **Peer-to-Peer Network:** Bitcoin operates on a decentralized peer-to-peer network, meaning there is no central authority controlling it. Transactions and blocks are propagated across many computers around the world.
* **Resistance to Censorship:** Because the blockchain is distributed and requires significant computational power to alter, it's very difficult for any single entity to censor transactions or control the network.
* **Security through Cryptography:** The use of strong cryptography ensures the security and integrity of transactions and the blockchain. Private keys allow users to control their Bitcoin, and digital signatures prevent tampering with transactions. The Proof-of-Work mechanism makes it computationally expensive for malicious actors to rewrite the transaction history.

**In summary, Bitcoin's technical operation relies on a sophisticated interplay of cryptographic techniques, a distributed and transparent ledger, and a computationally intensive consensus mechanism to ensure security, immutability, and decentralization.**

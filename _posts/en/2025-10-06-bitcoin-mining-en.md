---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Bitcoin Hash Calculation and Mining
translated: false
type: note
---

### How Bitcoin Calculates Hashes

Bitcoin uses a cryptographic hash function called **SHA-256** (Secure Hash Algorithm 256-bit) to calculate hashes. This is a one-way function that takes input data (like a block's header) and produces a fixed 256-bit (32-byte) output that's unique and unpredictable.

- **What gets hashed?** Primarily the block header, which includes:
  - Version number
  - Previous block's hash
  - Merkle root (a summary of all transactions in the block)
  - Timestamp
  - Difficulty target (bits)
  - Nonce (a number miners adjust)

- **The process:**
  1. The miner assembles the block header.
  2. Applies SHA-256 twice: `hash = SHA256(SHA256(header))`.
  3. Checks if the resulting hash is below the current target (e.g., starts with enough leading zeros, like 000000...).
  4. If not, increments the nonce and repeats. This is the "trial-and-error" part of Proof of Work (PoW).

Hashes are deterministic—same input always gives the same output—but tiny changes (like +1 to nonce) produce wildly different outputs. This makes it infeasible to reverse-engineer inputs from outputs.

### Why Mine Bitcoin? (And How It Ensures a 21 Million Supply Cap)

I think you meant "why mine" instead of "why mint"—mining is the process of validating transactions and adding blocks to the blockchain, rewarded with new bitcoins.

- **Why mine?**
  - **Security:** Miners secure the network by competing to solve PoW puzzles, preventing attacks like double-spending (spending the same BTC twice).
  - **Decentralization:** Anyone can mine, distributing control—no central authority.
  - **Incentive:** Miners earn **block rewards** (newly minted BTC) + transaction fees. This bootstraps the network and compensates for energy costs.

- **Ensuring the supply cap (it's actually 21 million, not 10 million):**
  Bitcoin's protocol hardcodes a total supply of **21 million BTC**, created through mining rewards that **halve** every 210,000 blocks (~4 years).
  - Started at 50 BTC per block in 2009.
  - Halved to 25 in 2012, 12.5 in 2016, 6.25 in 2020, 3.125 in 2024, and so on.
  - Last bitcoin will be mined around 2140; after that, only fees remain.
  - This is enforced by code: The reward formula is `reward = 50 * 0.5^(floor(block_height / 210000))`. No one can change it without 95% network consensus, making inflation predictable and capped.

This scarcity mimics gold, driving value.

### How Proof of Work (PoW) Works

PoW is Bitcoin's consensus mechanism—a computational puzzle that proves a miner invested "work" (CPU/GPU/ASIC power) to add a block.

- **Step-by-step:**
  1. **Collect transactions:** Miners gather pending transactions into a block (up to ~1-4 MB, depending on SegWit).
  2. **Build header:** Include Merkle root of transactions, link to previous block, etc.
  3. **Set target:** The network adjusts difficulty every 2016 blocks to keep average block time at 10 minutes. Target = a very small number (e.g., hash must be < 0x00000000FFFF...).
  4. **Find nonce:** Brute-force guess nonces (0 to 2^32-1). For each, hash the header. If hash < target, it's valid!
  5. **Broadcast block:** Other nodes verify (easy— just re-hash once). If valid, add to chain; miners start on next block.
  6. **Chain rule:** Longest valid chain wins (resolves forks).

PoW makes it cheap to verify blocks but expensive to create them, securing against 51% attacks (controlling >50% hash rate to rewrite history).

### Why So Many Computations for a Transaction?

Transactions don't directly require massive computation from users—just signing with your private key (elliptic curve crypto, quick). The heavy lifting is in **mining**:

- **Per block, not per transaction:** A block bundles ~2,000-3,000 transactions. Miners hash trillions of times per block to solve PoW.
- **Difficulty adjustment:** As more miners join (higher total hash rate), difficulty rises exponentially to maintain 10-min blocks. Current global hash rate is ~600 EH/s (exahashes/second)—that's 600 quintillion hashes per second!
- **Why the waste?**
  - **Security cost:** High computation makes attacks uneconomical. Rewriting a block costs re-doing all subsequent PoW.
  - **Sybil resistance:** Prevents flooding the network with fake identities.
  - **Trade-off:** Energy-intensive (Bitcoin uses ~150 TWh/year, like a mid-sized country), but proponents argue it's a feature for trustless money.

Users pay fees to prioritize transactions in blocks; low-fee ones wait.

If you meant something specific (like hardware for mining), let me know!

**References:**
[Bitcoin Whitepaper](https://bitcoin.org/bitcoin.pdf)
[Bitcoin Wiki: Proof of Work](https://en.bitcoin.it/wiki/Proof_of_work)
[Blockchain.com: Bitcoin Halving](https://www.blockchain.com/learning-crypto/bitcoin-halving)

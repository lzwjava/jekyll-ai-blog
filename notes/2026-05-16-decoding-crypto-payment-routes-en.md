---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding Crypto Payment Routes
translated: false
type: note
---

**Question:** I successfully topped up 10 USDC to OpenRouter, transferred from Binance — the route went through MetaMask → Coinbase → Stripe → OpenRouter. Isn't that quite a long route? Can you explain what happened in this on-chain transaction?

**Answer:**

Yes, that's quite a journey! And looking at the actual on-chain transaction, it's even more interesting than it seems. Here's a full breakdown of what happened:

---

## Transaction Summary

- **Status:** ✅ Success
- **Time:** May 16, 2026 at 02:46:17 AM UTC
- **Network:** Base (Layer 2 on Ethereum)
- **Amount Sent:** 10.5 USDC (~$10.50)
- **Amount Received by OpenRouter:** 10.395 USDC (after 1% fee)
- **Gas Fee:** ~$0.0044 (extremely cheap on Base L2)

---

## The Full On-Chain Route

Here's exactly what happened step by step, as recorded in the blockchain logs:

### 1. Entry Point (ERC-4337 Account Abstraction)
The transaction was initiated via **ERC-4337 Account Abstraction** (`Entry Point 0.6.0`). This is the standard that Coinbase's Smart Wallet uses — it means your wallet is a smart contract account, not a regular EOA. No need to hold ETH for gas yourself; a **Paymaster** sponsors the gas.

### 2. Your Coinbase Smart Wallet (the Sender)
Address `0x133243d4...be3C566Eb` — this is your Coinbase-managed smart wallet holding the USDC on Base. It authorized a transfer of **10.5 USDC**.

### 3. Coinbase Business: Payment Protocol
The 10.5 USDC first went to Coinbase's **Payment Protocol** contract (`0x0E3dF951...`). This is Coinbase's x402 payment infrastructure — an HTTP payment protocol built on Base that enables machine-to-machine crypto payments (used by OpenRouter's API billing system).

### 4. Fee Split (via x402 Router `0x47C5d3fc...`)
The payment router split the funds:
- **0.105 USDC (1%)** → Coinbase fee receiver (`0x6D8675A5...`) — this is Coinbase's cut for processing
- **10.395 USDC (99%)** → OpenRouter's receiving address (`0x4C3f2E39...`)

### 5. Gas Sponsored by Paymaster
The gas fee (~$0.004) was paid by a **Paymaster** (`0x2FAEB076...`), so you didn't need any ETH in your wallet at all. This is the magic of Account Abstraction.

---

## Why So Many Hops?

| Layer | Role |
|---|---|
| Binance | You withdrew USDC to Base network |
| MetaMask / Coinbase Wallet | Your wallet interface |
| Coinbase Smart Wallet (ERC-4337) | On-chain smart contract wallet |
| Coinbase x402 Payment Protocol | Machine-to-machine payment routing |
| Fee Router Contract | Splits 1% fee to Coinbase, 99% to OpenRouter |
| OpenRouter | Receives 10.395 USDC as API credit |

The route looks long but it's actually quite elegant:
- **Coinbase's x402 protocol** is designed for AI API billing — it lets services like OpenRouter charge per-request without traditional payment rails (no Stripe account needed on your end)
- **Account Abstraction** means zero gas friction for the user
- Everything settled on **Base L2** in seconds for less than half a cent in fees

---

## Fun Fact: What is x402?

The "x402" label you see in the transaction is a reference to **HTTP 402 "Payment Required"** status code — Coinbase's vision of a native web payment protocol. It's specifically designed so AI agents and APIs can pay each other autonomously on-chain, without human intervention. OpenRouter has integrated this so developers can fund API usage directly with on-chain USDC.

So yes — the route is long, but it's modern crypto payment infrastructure doing its job efficiently! 🎉

**References:**

- [BaseScan Transaction](https://basescan.org/tx/0x31f501491588da24e706aa199d1a6aa3ce15dea4159458efbeafea3a07ed0ec0)
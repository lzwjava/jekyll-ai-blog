---
audio: false
generated: true
image: false
lang: en
layout: post
title: ETH Not ERC-20 for Binance Transfers
translated: false
type: note
---

No, you cannot send ETH directly from Binance using the ERC-20 network to a MetaMask Ethereum mainnet address.

Here's why:

* **Ethereum (ETH)**: Ethereum (ETH) itself is transferred on the Ethereum main network. It is a native cryptocurrency of the Ethereum blockchain.
* **ERC-20**: ERC-20 is a token standard, not a specific blockchain. ERC-20 tokens (such as USDT, DAI, etc.) are tokens created on the Ethereum blockchain, but they are distinct from ETH, which is the main currency on the network.

To make it clearer:

* **ETH** transactions on the Ethereum network happen on the Ethereum mainnet, not as an ERC-20 token.
* If you withdraw ETH from Binance, it will be transferred via the **Ethereum mainnet**, not the ERC-20 token standard.
* **MetaMask ETH address** is on the Ethereum main network, which is compatible with ETH and ERC-20 tokens, but you need to make sure you select the **Ethereum main network** (not an ERC-20 token withdrawal) when withdrawing ETH from Binance to MetaMask.

### The correct steps would be:

1. **Withdraw ETH from Binance**: Choose the **Ethereum mainnet** (ETH) as the withdrawal method.
2. **Receive on MetaMask**: Your MetaMask ETH address is on the Ethereum main network, and you'll receive ETH directly.

### To summarize:

* **ETH is not an ERC-20 token**; it is the main currency of the Ethereum mainnet.
* When withdrawing ETH, use the **Ethereum mainnet** option for both Binance and MetaMask.

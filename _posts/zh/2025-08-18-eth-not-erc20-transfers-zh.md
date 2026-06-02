---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 币安转账应使用以太币而非ERC-20代币
translated: true
type: note
---

不，你不能直接通过 ERC-20 网络从币安向 MetaMask 的以太坊主网地址发送 ETH。

原因如下：

* **以太坊 (ETH)**：以太坊 (ETH) 本身是在以太坊主网络上传输的。它是以太坊区块链的原生加密货币。
* **ERC-20**：ERC-20 是一种代币标准，而非特定的区块链。ERC-20 代币（如 USDT、DAI 等）是在以太坊区块链上创建的代币，但它们与作为网络主货币的 ETH 是不同的。

更明确地说：

* **ETH** 在以太坊网络上的交易发生在以太坊主网，而不是作为 ERC-20 代币。
* 如果你从币安提取 ETH，它将通过**以太坊主网**进行转移，而不是通过 ERC-20 代币标准。
* **MetaMask 的 ETH 地址**位于以太坊主网络上，该地址兼容 ETH 和 ERC-20 代币，但在从币安向 MetaMask 提取 ETH 时，你需要确保选择**以太坊主网**（而不是 ERC-20 代币提取）。

### 正确的步骤应该是

1. **从币安提取 ETH**：选择**以太坊主网 (ETH)** 作为提取方式。
2. **在 MetaMask 上接收**：你的 MetaMask ETH 地址位于以太坊主网络上，你将直接收到 ETH。

### 总结

* **ETH 不是 ERC-20 代币**；它是以太坊主网的主货币。
* 提取 ETH 时，在币安和 MetaMask 上均使用**以太坊主网**选项。

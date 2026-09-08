---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Chainlink Labs：Chainlink背后的公司
translated: true
type: note
---

问题：**Chainlink Labs（`chainlinklabs.com`）是什么？**

答案：

![图片](https://images.openai.com/static-rsc-4/ykAE9_ouGsksgaVucT-UWXGuVB8B9vdy80-doKwTRTay3sFqS1DJCZYmGShdRiGV4eXMseejLgSt56D5du71daNxobnXxKL5gsUqa4sbMk_q935ryoSWPwk1EgYi4muqOCX9JGpEDpyhBv1CAwKmDyhpMaG3UIlLPGHiUUCl03kJ2Tw4XkJIqt-zRsSptBc9?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/Llsg2uGZkXkgvUvMJ-KZUv7F_RqKQrEFWCxHK1b1k_fJ-rCHaBKDk0kF1w_TtsAJAQg2nz-chvj1jKojDEwWZKu1o-juQOFHjApxarv_EF1D_EHbmJbWiTJ5THcGkpb-Ti_hLv8yE6_TdrLOLTkOBVJunUjxADm9-TIrVHcs3iRSxS-I7NsccEslaDe7NU2N?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/X2EDQaGChYBMSxVnRkjvdaymZMOpZ7qCkIu_w8VQnCNeB7CxxYaIcyC9Smro7KxhMguUKiHdVlR7x0pjMPYD7WN8_MOPNrxl3u5hdS6xCRYf2LLN4YTqNMbX2jARzhc4Kq62OC342qeTJHk_SnSIjsFGod3StZxuKeGdP4jZJEYwAcrNbHJc1fZ0jzvUdKN1?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/DteWZcFcQgNSKx0p0O0fjMEOzOEsG1BMiXxAW6h-s-aIxCkvg5j3KcgJz_iW_WrOmVMMxE55Wyy24Cn2HFLTmt_ZPk7Np9-cEszQYIURwU5YppD5iOcdH6z5FXYEwM9BX_9T6pR5GsliMJ4bZiCFxvOTW0sHhBfP8WcJTs4KjYYH03Ba0VeUS7JrvBgCMDUO?purpose=fullsize)

**Chainlink Labs 是构建 Chainlink 的公司**，后者是 Web3/区块链领域最重要的基础设施项目之一。

最简单的理解模型是：

> **Chainlink = 区块链与外部世界之间的中间件。**
> **Chainlink Labs = 开发该基础设施的公司。**

### 1. 核心问题

智能合约可以原生访问区块链状态：

```text
以太坊
   ↓
智能合约
   ↓
余额 / 交易 / 其他合约
```

但它无法安全地发起如下请求：

```python
price = requests.get("https://api.binance.com/...")
weather = requests.get(...)
stock = requests.get(...)
```

因为这会破坏区块链的共识机制：不同节点可能收到不同答案。

这就是**预言机问题**。

Chainlink 提供了去中心化的预言机网络：

```text
                    ┌── 节点 A ──┐
                    ├── 节点 B ──┤
真实世界数据 ────────┼── 节点 C ──┼──> 聚合
                    ├── 节点 D ──┤        ↓
                    └── 节点 E ──┘   区块链
                                          ↓
                                    智能合约
```

Chainlink 将预言机描述为一种为智能合约提供链外数据或将其连接到链外系统的系统。（[Chainlink][1]）

---

### 2. 为何变得如此重要

最初的关键应用是 **DeFi 价格数据源**。

例如，设想以下场景：

```solidity
function liquidate(address user) {
    uint256 ethPrice = chainlink.getPrice("ETH/USD");

    if (collateral[user] * ethPrice < debt[user]) {
        ...
    }
}
```

智能合约需要一个可信的 ETH/USD 价格。

Chainlink 的去中心化预言机网络从多个独立来源/节点获取价格，并生成一个区块链应用可以使用的数值。

这成为了借贷、衍生品、稳定币、保险、预测市场等领域的基础设施。

Chainlink 表示，其基础设施现已支持 DeFi、资本市场、代币化资产、跨链互操作性和链外计算。（[Chainlink][2]）

---

### 3. Chainlink 远不止“价格数据源”

这是 **2026 年** 的关键部分。

其演进过程大致如下：

```text
2017
  ↓
预言机
  ↓
价格数据源
  ↓
DeFi 基础设施
  ↓
跨链消息传递
  ↓
链外计算
  ↓
代币化现实世界资产
  ↓
机构金融基础设施
```

Chainlink 当前的定位越来越倾向于：

> **将传统金融引入链上的基础设施。**

其官网明确表示，正在与金融市场基础设施、资产管理公司和 DeFi 协议合作，围绕代币化资产开展工作。（[Chainlink Labs][3]）

例如，其生态系统包括与 **Swift、DTCC、Mastercard、UBS、Fidelity International、ANZ 和 Aave** 等组织的关系。（[Chainlink][2]）

因此，长期押注并非简单的：

> “加密货币上涨。”

而更接近于：

> **金融资产和金融工作流日益成为可编程的区块链资产。**

而 Chainlink 希望成为连接这些系统的基础设施层。

---

### 4. Chainlink 实际提供什么？

可以将其平台视为多个分布式系统产品的集合。

| 组件                     | 用途                             |
| ------------------------ | -------------------------------- |
| **数据源 (Data Feeds)**  | 将外部数据引入区块链             |
| **CCIP**                 | 跨链互操作协议                   |
| **自动化 (Automation)**  | 自动触发智能合约                 |
| **函数 (Functions)**     | 执行外部/API 计算                |
| **储备证明 (Proof of Reserve)** | 验证资产抵押情况                 |
| **VRF**                  | 可验证随机数                     |
| **数据流 (Data Streams)** | 低延迟市场数据                   |
| **机密计算 (Confidential Compute)** | 私有计算与数据工作流             |

因此，从架构上看，它正演变为类似以下结构：

```text
                Chainlink 网络
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     数据源         跨链          计算
     Data Feeds      CCIP        Functions
        │              │              │
        └──────────────┼──────────────┘
                       │
                 区块链应用
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       DeFi       代币化         金融
```

---

### 5. 创始人是谁？

Chainlink 由 **Sergey Nazarov 和 Steve Ellis** 创立。该公司最初以 SmartContract.com 的名义运营；Chainlink 白皮书于 2017 年发布，网络于 2019 年在以太坊上启动。

其技术顾问团队也异常强大。Chainlink Labs 列出的成员包括 **Ari Juels、Dan Boneh、Christian Cachin、Mike Reiter 和 Fan Zhang**。（[Chainlink Labs][4]）

这揭示了其技术导向：

```text
密码学
      +
分布式系统
      +
区块链
      +
金融基础设施
```

而非简单地“构建一个加密应用”。

---

### 6. LINK 是什么？

**LINK** 是 Chainlink 网络的原生代币。

它在 Chainlink 生态系统中用于支付服务费用，并根据服务/网络设计，可能涉及质押等经济安全机制。（[CloudFront][5]）

重要区别：

```text
Chainlink Labs       = 公司
Chainlink            = 去中心化基础设施/网络
LINK                 = 网络的原生加密资产
```

不要将三者等同。

---

### 7. 为何我认为这家公司值得你关注

鉴于你的工程背景，**Chainlink Labs 实际上是一家比普通加密初创公司有趣得多的 Web3 公司**。

其技术栈与你已关注的领域高度重叠：

```text
LLM 基础设施
GPU 系统
分布式系统
        │
        ├── 共识机制
        ├── 容错
        ├── 密码学
        ├── 网络
        ├── 分布式计算
        └── 金融系统
```

据报道，其当前团队拥有 **600 多名开发者、研究人员和资本市场专家**，并且该公司自称是远程优先的工作模式。（[Chainlink Labs][3]）

有趣的是，其薪酬模式目前包括 **基于 LINK 的长期激励机制，而非传统的公司股权**。（[Chainlink Labs][6]）

因此，我更倾向于将 Chainlink Labs 归类为：

> **一家分布式系统 + 密码学 + 金融基础设施公司，其产品恰好是区块链基础设施。**

[Chainlink Labs](https://chainlinklabs.com?utm_source=chatgpt.com)
[Chainlink 平台](https://chain.link/?utm_source=chatgpt.com)

如果你愿意，我接下来可以深入解析 **Chainlink 从节点/共识/RPC 层面的实际架构**，这可能是你最便于从技术角度理解的方式。

[1]: https://chain.link/faqs?utm_source=chatgpt.com "Chainlink 常见问题解答 | Chainlink"
[2]: https://chain.link/?utm_source=chatgpt.com "Chainlink：行业标准的预言机平台"
[3]: https://chainlinklabs.com/?utm_source=chatgpt.com "Chainlink Labs"
[4]: https://chainlinklabs.com/ "Chainlink Labs"
[5]: https://dnhj6igwtb6pj.cloudfront.net/1/cbd9b460-3b49-484f-9858-d21f08af8229?utm_source=chatgpt.com "GRAYSCALE CHAINLINK TRUST (LINK)"
[6]: https://chainlinklabs.com/careers?ashby_jid=dcaa141b-f6f2-4bd9-9beb-4da1d46e8708&utm_source=chatgpt.com "招聘 | Chainlink Labs"
---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TSY资本：香港量化公司简介
translated: true
type: note
---

问题：**香港公司 TSY Capital 是什么？**

回答：

TSY Capital 是一家**小型香港量化交易/资产管理公司**，法律名称为 **TSY Capital Limited（天市垣資本有限公司）**。

### 1. 他们实际做什么

TSY 本质上是一家**量化对冲基金/系统化交易机构**。

他们自己的描述是：

> 成立于 2022 年，利用机器学习设计算法交易系统，捕捉全球股票市场中的效率低下机会。（[TSY Capital][1]）

其技术栈异常工程化：

```text
市场数据
    ↓
Python / ML / 统计
    ↓
量化研究 + alpha 发现
    ↓
回测
    ↓
策略
    ↓
Rust 低延迟交易系统
    ↓
全球股票市场
```

他们的研究基础设施主要是 **Python + AWS**，而低延迟交易系统则主要使用 **Rust**。（[TSY Capital][1]）

因此，这本质上不是传统的投资银行类公司。可以理解为：

**ML + 统计 + 分布式系统 + 高性能计算 + 交易。**

---

### 2. 公司规模

TSY 相当小。

LinkedIn 目前显示其规模为 **11–50 名员工**，而其 LinkedIn 页面上仅可查找到约 15 名员工。（[LinkedIn][2]）

该公司于 **2022 年 6 月 13 日** 在香港注册成立，为私人股份有限公司。公司注册编号为 **3162135**，商业登记号码为 **74138601**。（[Bloomberg LEI][3]）

地址：

```text
Level 25
33 Des Voeux Road Central
Central, Hong Kong
```

（[TSY Capital][1]）

---

### 3. 实际上受 SFC 监管

这一点很重要。

TSY Capital Limited 是一家 **SFC 持牌法团**，中央编号 **BTI971**，获得 **第 9 类——资产管理** 授权。SFC 于 2023 年 7 月发布的出版物中已将 TSY Capital 列为新获牌照的第 9 类公司。（[SFC][4]）

因此，这并非一家不受监管、声称管理资金的“量化初创公司”。

其业务模式大致如下：

```text
投资者 / 资本
        ↓
TSY Capital
        ↓
系统化量化策略
        ↓
全球股票市场
        ↓
投资回报
```

其网站明确表示，其投资产品/基金面向符合适用法规的合格/专业投资者。（[TSY Capital][5]）

---

### 4. 有趣的部分：他们的工程文化

如果你从工程角度关注他们，这部分可能最相关。

他们目前的招聘材料明确要求：

* Rust / C / C++ / Go / Java
* 分布式中间件
* 高性能网络
* 数据库
* Linux 内核
* Python 科学计算栈
* PyTorch / JAX / CUDA
* AWS/GCP
* 智能编码工具
* 算法 / 系统 / 网络

他们还明确提到编程竞赛成就，如 **ICPC、CCPC 和 IOI** 作为加分项。（[TSY Capital][6]）

这很好地反映了他们的价值取向：

```text
                 TSY 工程师
                      │
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
    系统           ML/量化        基础设施
       │              │              │
    Rust/C++       PyTorch/JAX    AWS/Linux
       │              │              │
     网络           统计            分布式
       └──────────────┼──────────────┘
                      ↓
                 交易系统
```

这更接近于**量化/高频交易工程**，而非普通的金融科技后端开发。

---

### 5. 创始人的有趣背景

与 TSY 相关的知名人物之一是 **Tianyi Cui（崔添翼）**。SFC 记录显示，他从 2023 年 7 月至 2026 年 2 月担任 TSY 第 9 类资产管理活动的负责官员。（[Webb-site][7]）

也有证据表明，TSY 团队中曾有来自大型量化公司背景的人员。不过，我不认为整个公司拥有与 Jane Street / Citadel 等相同的规模或经济实力。

TSY 本身成立于 **2022 年**，因此是一家相对年轻的公司。（[TSY Capital][1]）

---

### 6. 对你而言

从工程要求来看，TSY 实际上**与你的技术背景相当匹配**，尤其是如果你正在尝试摆脱传统的 Java 企业级开发工作。

你的重叠领域大致如下：

| 你的背景                 | TSY 相关性                 |
| ----------------------- | ------------------------- |
| Java/后端               | 有用的系统基础             |
| Python                  | 直接相关                   |
| LLM/ML                  | 相关                       |
| CUDA/GPU                | 与 ML 基础设施相关         |
| 分布式系统               | 高度相关                   |
| Linux                   | 高度相关                   |
| 算法                     | 高度相关                   |
| AI 代理                  | TSY 明确提及               |
| Rust                     | **值得弥补的差距**         |
| 量化金融/统计            | **重大差距**               |
| 低延迟交易               | **重大差距**               |

最大的概念跳跃其实不在于 Rust。

而在于：

```text
软件工程
       ↓
系统工程
       ↓
量化研究
       ↓
市场微观结构
       ↓
alpha / 执行 / 风险
```

你在**系统/AI 工程**方面已有大量重叠。主要缺失的是**量化金融 + 统计 + 交易基础设施**。

而他们的招聘页面异常明确地表示，他们希望的是热爱编程和系统的人，而非仅仅金融领域的专家。（[TSY Capital][6]）

**结论：** TSY 看起来像一家小型、技术导向的香港量化公司，而非传统的金融服务公司。其 **ML + Rust + AWS + 分布式系统 + 低延迟交易** 的组合，尤其适合那些希望从企业软件/AI 工程向更硬核的系统/量化工程转型的人。

参考文献：

* [TSY Capital 官方网站](https://tsycapital.com/?utm_source=chatgpt.com)
* [TSY Capital 招聘页面](https://tsycapital.com/career.html?utm_source=chatgpt.com)
* [香港 SFC 记录/出版物](https://www.sfc.hk/-/media/EN/files/LIC/pr/addition_20230731_eng.pdf?hash=6807519F234ABE6372AA1B5A4590234D&rev=30beb7e2f23e41fcb3bcc0b4366e23ab&utm_source=chatgpt.com)
* [TSY Capital LinkedIn](https://hk.linkedin.com/company/tsycapital?utm_source=chatgpt.com)

[1]: https://tsycapital.com/?utm_source=chatgpt.com "TSY Capital"
[2]: https://hk.linkedin.com/company/tsycapital?utm_source=chatgpt.com "TSY Capital | LinkedIn"
[3]: https://lei.bloomberg.com/leis/view/98450036S10981O3FE10?utm_source=chatgpt.com "TSY CAPITAL LIMITED - LEI: 98450036S10981O3FE10"
[4]: https://www.sfc.hk/-/media/EN/files/LIC/pr/addition_20230731_eng.pdf?hash=6807519F234ABE6372AA1B5A4590234D&rev=30beb7e2f23e41fcb3bcc0b4366e23ab&utm_source=chatgpt.com "addition_eng"
[5]: https://tsycapital.com/disclaimer.html?utm_source=chatgpt.com "Disclaimer"
[6]: https://tsycapital.com/career.html?utm_source=chatgpt.com "TSY Capital"
[7]: https://webb-site.qizai.ai/personnel/30406212/sfc-licenses?utm_source=chatgpt.com "Cui, Tianyi (SFC:BTI974) 崔添翼 Hong Kong SFC License Details (ID 30406212)"

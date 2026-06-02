---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 强制执行源代码可用许可证的现实
translated: true
type: note
---

**问题：** open-core 公司如何对企业客户强制执行 source-available 许可？如果客户秘密复制和修改代码，会发生什么？

---

**回答：**

这是一个很好的问题，它涉及软件法律的现实以及实际的信任问题。诚实的答案是：**强制执行并不完美，但法律效力是真实的——而且还有超出法律的技术和商业机制。**

---

## 第一层：法律强制执行（Copyright Law）

最重要的是要理解：**source-available 许可不仅仅基于信任——它们在版权法下具有法律约束力。**

第一个重大判例是 *Jacobsen v. Katzer*（2008 年），联邦巡回法院裁定，被许可人违反 open-source 许可相当于**版权侵权**，而不仅仅是违反合同。法院认为，即使没有附加费用，披露要求等条件也享有充分的法律认可。

这一区别至关重要：

- **违反合同** → 起诉索赔，补救措施有限
- **版权侵权** → 禁令、法定损害赔偿、强制从市场移除产品

法院一贯支持 open-source 和 source-available 许可条款。2024 年对法国电信巨头 Orange 的 90 万欧元罚款树立了一个先例，即不合规可能代价极高。

因此，如果客户秘密复制并发布企业代码而没有许可，供应商可以起诉**版权侵权**——这是严重的。

---

## 第二层：违规实际如何被*检测到*

这是实际现实——供应商无法监视每个服务器。检测通过几个渠道发生：

**a) 竞争情报 / 公开发布**
如果客户基于盗用代码发布产品或 SaaS，它就会被检测到。竞争对手、前员工或研究人员可能注意到相似之处。

**b) Software Composition Analysis (SCA) 工具**
SCA 工具检查软件应用程序，以识别第三方和 open-source 组件及其相关的安全漏洞或法律许可限制。open-source 审计员为客户做出了许多“重大拯救”，捕捉到可能成为大问题的异常合规问题。这些工具可以指纹代码并检测跨产品的复制片段。

**c) 举报人 / 前员工**
在公司内部，处理代码的工程师可能离职并披露违规——尤其是如果他们自己对这种做法感到不舒服。

**d) License keys / telemetry in the binary**
许多企业产品会“打电话回家”、嵌入 license tokens，或在 binary 中内置**cryptographic license checks**。如果你剥离它们，你已经修改了代码——触发许可违规。

---

## 第三层：技术强制执行（超出法律）

公司不仅仅依赖法律救济。他们构建技术障碍：

| Mechanism | How it works |
|---|---|
| **License key servers** | 软件调用服务器验证 license key；离线篡改会破坏功能 |
| **Obfuscated / compiled binaries** | 企业功能作为编译工件发布——难以干净修改 |
| **Encrypted modules** | 代码在运行时使用与 license 绑定的密钥解密 |
| **Feature flags in SaaS** | 对于云托管的企业功能，服务器端切换——客户根本没有代码 |
| **Signed builds** | 篡改的 binary 会破坏签名验证 |

对于**纯 on-prem 部署并具有完整源代码访问**，这些技术控制较弱——这就是为什么法律框架更重要。

---

## 第四层：实际“灰色地带”——小规模违规往往未被检测到

老实说：**小规模内部使用复制/修改的企业代码且从未离开公司，非常难以检测或强制执行。** 公司通常：

- 接受某种程度的不可检测泄漏作为开展业务的成本
- 将强制执行精力集中在**商业竞争对手**重新分发其代码上
- 使用法律行动威胁作为威慑

强制执行趋势正在增长——从 OSS 倡导团体强制执行转向商业实体针对其他公司的强制执行。对于 AGPL 等许可，即使软件通过网络被第三方访问，也可能触发义务——即使未分发。

---

## 第五层：真正的威慑——商业风险

对于企业买家（大公司、受监管行业），被抓到的**声誉和运营风险**是巨大的：

- 供应商终止许可 → **系统一夜之间变黑**
- 供应商起诉 → **产品从市场移除**，高管责任
- 新闻泄露 → **与客户和监管机构的信任被摧毁**

如果你的业务以违反许可的方式使用 open-source 或 source-available 代码，请尽快补救，以免演变为真正的法律战斗。不合规可能导致积极诉讼、金钱损害、强制禁令——并且法院可能使你的软件不可用，并没收权利。

这种商业风险对于大型企业客户比技术控制更有效，因为下行风险是灾难性的。

---

## 总结

| Enforcement Layer | Strength | Notes |
|---|---|---|
| Copyright law | Strong | Infringement, not just breach of contract |
| SCA / code fingerprinting | Medium | Detects if code is shipped publicly |
| License key / telemetry | Medium | Technical barrier, bypassable but risky |
| Whistleblowers | Unpredictable | Often how large violations surface |
| Commercial deterrence | Very strong for large cos | Existential risk if caught |
| Small internal use detection | Weak | Practically hard to discover |

简而言之：**秘密复制企业源代码在法律上非常冒险、技术上比看起来更难，并且对严肃企业来说是商业自杀**——但公司在某个阴暗角落的小规模内部滥用？很可能未被检测到。该系统依赖法律恐惧、技术摩擦和商业自我利益的混合，而不是完美的强制执行。

---

**参考文献：**

- [Consequences of Violating Open Source Licenses - Berkeley Technology Law Journal](https://btlj.org/2015/11/consequences-violating-open-source-licenses/)
- [Open Source License Compliance Lessons from Court Cases (FOSSID)](https://fossid.com/articles/open-source-license-compliance-lessons-from-two-landmark-court-cases/)
- [Analyzing 5 Major OSS License Compliance Lawsuits (FOSSA)](https://fossa.com/blog/analyzing-5-major-oss-license-compliance-lawsuits/)
- [How to Enforce Open Source Licenses (TermsFeed)](https://www.termsfeed.com/blog/enforce-open-source-licenses/)
- [Open Source Software Policies: Business & Legal Risks (National Law Review)](https://natlawreview.com/article/open-source-software-policies-why-you-need-them-and-what-they-should-include)

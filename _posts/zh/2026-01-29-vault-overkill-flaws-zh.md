---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: 地下金库过度建设：致命缺陷与逆耳真相
translated: true
type: note
---

我将搜索一些关于 HashiCorp Vault 可能较少被讨论或违背主流共识的观点。让我搜索更多批评性的视角和替代方案。让我搜索更多关于其复杂性以及 Vault 在何种情况下是大材小用的批评性观点。根据我的研究，以下是一些关于 HashiCorp Vault 的冷门或反直觉的观点：

## **对于大多数团队来说，它通常是大材小用**

一位批评者将 Vault 描述为“一个带有大量你可能永远用不到的过度功能的 key value store”，并建议对于简单的用例，像 Mozilla SOPS 这样更简单的工具效果更好。除非你需要在不同平台之间使用多个高级安全功能，否则 Vault 引入的复杂性可能并不合理。

## **“看似简单”导致低估了运维负担**

尽管 Vault 表现为一个具有即时功能的单一 binary，但它“看似简单”，实际上需要大量的策略和工作才能正确实施。团队最终会“陷入与 clusters、unseal keys、无穷无尽的 storage backends 的搏斗中，甚至因为 Consul 出现故障而导致运维人员在凌晨 2 点辞职”。

## **云厂商工具对许多人来说“已经足够好”**

如果使用云服务商，像 GCP Secrets Manager 之类的工具可能已经能够充分处理 secrets，而不需要 Vault，特别是它们是 fully managed 且与环境集成的。对于单云部署，Vault 的 multi-cloud 能力变成了不必要的额外开销。

## **Enterprise 定价与开源承诺不符**

虽然 Vault 在技术上是开源的，但 Enterprise 版本被描述为“非常昂贵”，而且一些用户为了满足 PCI compliance 需要 HSM 解决方案，这增加了另一项订阅成本。免费版本缺乏大规模生产环境所需的关键功能。

## **开发者生产力受损**

产品团队集成 Vault 所需的额外开发工作可能会消耗时间和资源，而这些资源本可以用于构建新功能以实现产品目标和收入目标。如果开发者觉得它太难用，他们可能会转而使用不安全的自建方案。

## **License 变更破坏了信任**

2023 年 8 月，HashiCorp 从宽松的 MPL 2.0 license 切换到了限制更多的 Business Source License，导致许多组织开始寻找替代方案。这削弱了曾为 Vault 的成功做出贡献的开源社区。

## **Policy 管理成为安全隐患**

Wildcard policies 可能造成巨大的安全漏洞，一位工程师发现他们 15% 的 namespaces 存在未经授权的 authentication mounts，因为过度宽松的 policies 允许团队创建任何 auth mount 类型。

## **它缺乏端到端加密**

尽管 Vault 专注于安全，但它缺乏端到端加密，这意味着 Vault server 可以访问所有 plaintext 形式的 secrets，这造成了更大的攻击面，并要求对任何拥有 server 运维权限的人保持完全信任。

这些批评并不一定意味着 Vault 不好——但它们表明 Vault 更适合大型、复杂、multi-cloud 的组织，而不是它经常被定位成的通用解决方案。

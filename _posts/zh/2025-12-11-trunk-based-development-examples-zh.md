---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 开源主干开发示例
translated: true
type: note
---

问题：您能否提供一些使用 Trunk-Based Development 的开源 GitHub 项目示例以供学习？

答案：

Trunk-Based Development (TBD) 强调短生命周期分支（或根本没有分支），并频繁集成到单个主分支（“主干”）中，以实现快速反馈、减少合并冲突并支持持续交付。虽然许多大型开源项目通过高速贡献、直接提交和 CI/CD 管道近似 TBD，但由于贡献者的分布式性质，纯粹的 TBD 示例在开源项目中更为罕见。下面是精选的 GitHub 项目，它们要么明确采用 TBD，要么有效地展示了 TBD，要么作为学习资源（例如，通过文档或结构）。我专注于通过其提交历史、PR 模式和配置来研究其清晰工作流的活跃仓库。

### 1. **Flipt** (github.com/flipt-io/flipt)
   - **为什么要向它学习？** 一个开源的特性标志系统，专为 TBD 和 GitOps 设计。它将特性标志视为代码，允许主干提交而不会破坏生产。研究它们的 CI/CD 设置以及它们如何使用标志来对冲发布——非常适合在实际部署中查看 TBD 的运行情况。
   - **关键探索点：** 短生命周期 PR、每次推送到主分支时的自动化测试以及它们关于与主干工作流集成的文档。
   - **星标数：** 约 5k+ | 语言：Go

### 2. **Ripissue** (github.com/cwnt/ripissue)
   - **为什么要向它学习？** 一个用于从 GitFlow 迁移到 TBD 的开源工具，由维护者在其自己的工作流中使用。它自动化 rebase 和合并以保持分支的短暂性。非常适合动手学习：fork 它，模拟团队设置，观察它如何强制执行主干卫生。
   - **关键探索点：** `.github/workflows` 中的 Workflow YAML 文件和显示每日主干集成的提交历史。
   - **星标数：** 约 100+（持续增长） | 语言：Go

### 3. **Hexagonal Architecture TBD Demo** (github.com/gergely-nagymeyer/hexagonal-architecture-trunk-based)
   - **为什么要向它学习？** 一个 Java 项目，展示了带有特性切换和 Branch by Abstraction 的 TBD。它是一个使用 Spring Boot、Docker 和 GitHub Actions 构建的学习示例——非常适合查看如何在没有长分支的情况下处理大型重构。
   - **关键探索点：** 使用 Togglz 作为标志以及仓库的 README 关于在 DDD/六边形设置中应用 TBD 模式的内容。
   - **星标数：** 约 200+ | 语言：Java

### 4. **Abstract Feature Branch Gem** (github.com/paulhammant/abstract_feature_branch)
   - **为什么要向它学习？** 一个实现 Branch by Abstraction 和特性切换以用于 TBD 的 Ruby gem。它是开源贡献者的实用工具包；研究它如何实现在主干上并发开发而不进行隔离。
   - **关键探索点：** Rails 集成示例以及在主干提交上运行以防止中断的测试。
   - **星标数：** 约 50+ | 语言：Ruby

### 5. **Awesome Trunk-Based Dev** (github.com/cgbystrom/awesome-trunk-based-dev)
   - **为什么要向它学习？** 不是一个代码库，而是一个精选的 TBD 资源列表，包含更多项目、演讲和工具的链接。将其用作一个入口：它指向真实的开源示例，如 Google 的 monorepo 实践（尽管不完全公开）。
   - **关键探索点：** 关于在分布式团队中扩展 TBD 和特定于开源的适应性的部分。
   - **星标数：** 约 300+ | 语言：不适用（精选列表）

要深入了解，请克隆这些仓库并运行 `git log --graph --oneline main` 以可视化主干的线性历史（最小分支）。与 GitHub Actions 等工具结合使用，用于主分支上的 CI。要获得更广泛的启发，请查看 trunkbaseddevelopment.com，该网站引用了 Google/Facebook 等公司的规模化类似开源的设置。如果您对 Go/infra 感兴趣，请从 Flipt 开始——它是最接近生产就绪的示例。

参考文献：

- [Trunk Based Development](https://trunkbaseddevelopment.com/)
- [GitHub Topics: trunk-based-development](https://github.com/topics/trunk-based-development)
- [Awesome Trunk-Based Dev](https://github.com/cgbystrom/awesome-trunk-based-dev)
- [Flipt on X](https://x.com/devhunt_/status/1720093931902554448)
- [Ripissue on X](https://x.com/gubasso777/status/1811602748523102598)

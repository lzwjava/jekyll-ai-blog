---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 关于集成测试的争议性观点
translated: true
type: note
---

问题：关于集成测试不受欢迎的观点有哪些？

答案：

集成测试用于验证多个组件或模块如何协同工作（通常涉及数据库或外部服务等真实依赖），是软件开发中的标准实践。然而，一些与主流观点相悖或不受欢迎的意见挑战了其相对于单元测试或其他方法的价值、有效性或必要性。这些观点通常源于对维护开销、设计影响和投资回报的经验。

### 主要不受欢迎的观点
- **集成测试是“骗局”或本质上有问题**：一个突出的观点认为，过度依赖集成测试会导致脆弱、缓慢和重复的测试套件。它们存在组合爆炸（太多的交互路径无法完全覆盖）、故障隔离差（难以查明问题）以及未能有效批判代码设计的问题。相反，应提倡使用窄范围的单元测试（带 mock）或契约/协作测试来强制实现更好的模块化。
- **集成测试表明软件设计不佳**：大量使用集成测试表明代码紧密耦合或过度依赖框架，使得真正的隔离变得不可能。设计良好的代码应尽量减少对集成测试的需求，因为它们是弥补不良抽象的“权宜之计”。
- **优先选择集成测试而不是单元测试（或完全跳过单元测试）**：在某些情况下（例如，简单的 CRUD 应用程序、带有 TypeScript 的 React 组件，或交互导致大部分错误的现代系统），单元测试的投资回报率较低，因为 mock 开销和脆弱性。集成测试被认为更真实，能更快地捕获实际问题，并足以提供信心。
- **在某些场景中，集成测试被高估或不必要**：对于小型服务、具有纯逻辑的库，或者当端到端测试覆盖整个系统时，集成测试会增加不必要的缓慢和复杂性，而没有带来相应的益处。一些人认为经典的“测试金字塔”模式（大量单元测试，较少集成测试）在分布式或容器化环境中不再适用。
- **过多的集成测试会增加维护负担**：累积的集成测试会“扼杀”代码库，导致更新成本高昂和虚假的信心，尤其是在它们重复覆盖或变得不稳定时。

这些观点具有争议性，因为主流建议（例如，测试金字字塔）强调平衡的集成测试。批评者通常主张解耦代码以实现快速单元测试，而支持者则强调实际世界的 bug 源于集成，而非孤立的单元。

这场辩论凸显了没有一刀切的方法——测试策略取决于项目规模、复杂性、团队和架构。

参考文献：
- [Integrated Tests Are A Scam by J.B. Rainsberger](https://blog.thecodewhisperer.com/permalink/integrated-tests-are-a-scam)
- [Sign of Bad Software Design: Integration Tests (Medium)](https://medium.com/@rayepps/the-most-missed-sign-of-bad-software-design-integration-tests-56093d001fee)
- [Reddit: Integrated Tests Are A Scam](https://www.reddit.com/r/SoftwareEngineering/comments/xnr83u/integrated_tests_are_a_scam/)
- [Reddit: Should you skip unit tests and do only integration tests?](https://www.reddit.com/r/reactjs/comments/10panfs/should_you_skip_unit_tests_and_do_only/)
- [Why Your Product's Probably Mostly Just Integration Tests (And That's Okay)](https://www.reddit.com/r/programming/comments/1ke9sh2/why_your_products_probably_mostly_just/)
- [Unit Testing is Overrated](https://tyrrrz.me/blog/unit-testing-is-overrated)

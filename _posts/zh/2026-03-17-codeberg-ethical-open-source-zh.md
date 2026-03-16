---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Codeberg 道德开源托管
translated: true
type: note
---

**Codeberg** 是一个 **非营利**、**社区驱动**的平台，用于托管和协作开发 **free and open-source software** (FOSS) 项目。它是 **GitHub** 等商业服务的流行伦理和注重隐私的替代方案。

### Core Facts (as of early 2026)

- **Official website**: https://codeberg.org
- **Operator**: Codeberg e.V. — 一个注册的非营利协会（eingetragener Verein），位于 **Berlin, Germany**
- **Founded**: September 2018（公开启动于 2019 年 1 月）
- **Software stack**: 基于 **Forgejo**（Gitea 的免费社区维护软分叉）
- **Philosophy**: 优先考虑公共利益和自由软件 — 无盈利动机、无投资者、无广告、无默认对公共代码进行 AI 训练

### Main Services

- **Git hosting** with issues, pull/merge requests, project boards, wikis, releases, packages
- **Codeberg Pages** — 免费静态网站托管（`username.codeberg.page` 或自定义域名）
- **CI/CD runners** (Woodpecker CI) — 开源项目免费分钟数
- **Translation platform** (Weblate instance at translate.codeberg.org)
- **Mirroring** 支持和联合实验（ActivityPub/ForgeFed 相关工作）

### Key Characteristics Compared to GitHub

| Aspect               | Codeberg                              | GitHub (Microsoft)                     |
|----------------------|---------------------------------------|----------------------------------------|
| 法律结构             | 德国非营利 e.V.                       | 营利性公司                             |
| 托管位置             | 欧盟（主要德国）                      | 主要美国                               |
| 私有仓库             | 允许但 **非主要焦点**（资源有限）     | 完全支持且为核心业务                   |
| 盈利模式             | 捐款 + 会员费                         | 企业计划、Copilot 等                   |
| 数据与隐私           | 强大的欧盟 GDPR 基础，无跟踪/广告     | 更多数据收集与商业化                   |
| 社区治理             | e.V. 成员可投票                       | 由 Microsoft 控制                      |
| 规模（仓库数）       | ~ 数十万                              | > 10 亿                                |
| 网络效应             | 较小的发现性 / 较少集成               | 主导生态系统                           |

Codeberg 故意保持较小且更专注。它优先考虑独立性、长期可持续性和与自由软件价值观的一致性，而不是在原始规模或企业功能上竞争。

### Who Uses Codeberg?

- 希望 **离开或避免** 大科技平台的自由软件项目
- 关注美国司法管辖权的欧洲项目（例如 DMCA 下架风险）
- 偏好 **非营利管理** 的个人/组织
- 重视 **Forgejo/woodpecker** 生态且不喜欢 GitHub 日益商业化的项目

### How to Get Started

1. 访问 https://codeberg.org
2. 注册账户（免费，无需信用卡）
3. 创建或导入仓库
4. 可选：加入 Codeberg e.V. 作为支持或活跃成员 → 获得投票权并在财务上帮助平台

会员资格 **并非** 使用服务所必需 — 只要遵守使用条款，个人和开源项目即可免费使用 Codeberg。

### Strengths

- 真正的非营利结构
- 基于欧盟（更强的隐私法）
- 非常接近原生 Forgejo → 轻量且快速
- 活跃的社区，关心软件自由
- 无企业路线图劫持

### Limitations (realistic view in 2026)

- 较小的生态 → 较少的现成集成与 actions
- 搜索与可发现性弱于 GitHub
- CI 分钟数和存储更有限（依赖捐款）
- 私有仓库被容忍但不鼓励（公共优先理念）
- 新项目“社交”可见性较低

简而言之：如果您想要 **类似 GitHub 的功能但没有 GitHub 公司**，Codeberg 目前（2026 年）是 FOSS 友好代码锻造景观中最成熟、稳定且理念纯净的选择之一。

References:  

- [Codeberg 官网](https://codeberg.org/)
- [What is Codeberg? - Documentation](https://docs.codeberg.org/getting-started/what-is-codeberg)
- [Codeberg on Wikipedia](https://en.wikipedia.org/wiki/Codeberg)
- [Codeberg vs GitHub comparisons (various 2025–2026 sources)](https://shyft.ai/tools/compare/codeberg-vs-github)
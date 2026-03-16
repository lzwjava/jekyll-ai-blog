---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 2026 年 Codeberg 顶级项目
translated: true
type: note
---

**问题：** Codeberg 上目前有哪些热门 / 流行 / 趋势项目？

**回答：**

截至 2026 年 3 月，Codeberg **没有** 官方的“Trending”部分（类似于 GitHub 的每日趋势）。社区长期以来有此请求（问题自 2020 年起开放），但仍未实现，因为大多数仓库的 star 数量相对较低，使得短期“热门”排名意义不大。

相反，流行度通常通过以下方式判断：

- 总 **stars**（终身收藏）
- Forks
- 最近活动（commits、issues、PRs）
- 社区提及 & 已知旗舰项目

### Codeberg 上最受欢迎 / 旗舰项目（2026 年初）

这些项目在讨论、博客草稿和社区列表中始终是最多 star 或被提及最多的：

- **Freeyourgadget / Gadgetbridge**  
  Codeberg 上明确的第一受欢迎仓库（star 和 forks 数量遥遥领先）。  
  开源 Android 应用，用于管理和使用智能手表 / 健身手环（Pebble、Mi Band、Amazfit、Garmin 等），无需厂商云锁定。

- **forgejo / forgejo**  
  驱动 Codeberg 的实际软件（Gitea 的软分叉）。  
  开发非常活跃，贡献者众多，是整个平台的核心。

- **Codeberg / Community** & **Codeberg / org** 仓库  
  讨论、治理、功能请求、基础设施主题。活动量天然较高。

- **woodpecker-ci / woodpecker**  
  Codeberg 上使用的主要 CI 系统（Woodpecker CI）。  
  频繁更新，并被托管在那里的项目广泛使用。

其他经常被提及或高可见度的类别/项目：

- **注重隐私 & 自由的移动 / 桌面应用**（许多类似 Gadgetbridge 的项目）
- **ForgeFed / 联邦实验**（早期的 ActivityPub-for-git 工作）
- **欧洲 / GDPR 专注的软件**（为主权原因从 GitHub 迁移的项目）
- **Gentoo** 镜像 → https://codeberg.org/gentoo/gentoo（2026 年 2 月正式宣布，作为 GitHub 退出策略的一部分）
- 托管在 translate.codeberg.org 的各种 Weblate 翻译项目
- 来自避开大科技平台的 FOSS 爱好者的静态站点生成器、CLI 工具、小型实用工具

### 如何自己查找当前活跃 / “热门”项目

1. 访问 https://codeberg.org/explore/repos  
   - 按 **Most stars** 排序 → 显示历史最受欢迎的项目（Gadgetbridge 通常排名第一）  
   - 按 **Recently updated** 排序 → 显示当前活跃开发的项目  
   - 按 **Recently created** 排序 → 显示全新项目

2. 查看 https://codeberg.org/explore/organizations → 大型组织通常有多个活跃仓库

3. 检查主要组织的最近 commits / 活动：  
   - https://codeberg.org/forgejo  
   - https://codeberg.org/woodpecker-ci  
   - https://codeberg.org/Freeyourgadget

4. 关注 Codeberg 公告 / 博客，或加入 https://codeberg.org/Codeberg/Community issue tracker 以获取焦点讨论。

总之：Codeberg 更注重长期可持续的 FOSS，而不是病毒式每日趋势。**Gadgetbridge** 仍是杰出的“star 王者”。要查看当前动态，按最近更新排序 explore 页面，或关注 Forgejo/Woodpecker 组织。

**参考资料：**

- [Trending repositories 讨论（自 2020 年起开放）](https://codeberg.org/Codeberg/Community/issues/213)
- [社区焦点 / 最受欢迎仓库提及（Gadgetbridge）](https://codeberg.org/Codeberg/Community/issues/200)
- [Codeberg 上的 Gentoo 镜像公告（2026 年 2 月）](https://www.gentoo.org/news/2026/02/16/codeberg.html)
- [Awesome Codeberg 列表（社区策展）](https://codeberg.org/kate/Awesome_Codeberg)
- [Codeberg Explore Repositories](https://codeberg.org/explore/repos)
---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过GitHub API对工程师进行画像
translated: true
type: note
---

这是一个很好的问题。以下是一个通过公开API对工程师进行画像的系统框架：

```
=== 如何通过 GitHub 了解一位工程师 ===

1.  PROFILE API  --  /users/{name}
    curl -s 'https://api.github.com/users/{name}'

    可获取的信息：
    - bio: 自我介绍（通常是一句话的身份描述）
    - location: 所在地
    - company: 当前雇主
    - blog: 个人网站（需深入查看）
    - created_at: 加入 GitHub 的时长
    - public_repos / followers / following:
      比例可看出是生产者还是消费者
      （仓库多、关注者少 = 创造者，而非推广者）

2.  REPOS API  --  /users/{name}/repos?sort=stars&per_page=100
    curl -s 'https://api.github.com/users/{name}/repos?sort=stars&direction=desc'

    可获取的信息：
    - Languages: 实际使用的编程语言（而非自称的语言）
    - Stars: 社区对其作品的认可度
    - Descriptions: 他们如何理解自己的工作
    - Topics: 自我标注的领域标签
    - pushed_at: 是否仍活跃？还是自2020年起就停滞了？
    - Forks vs originals: 是贡献者还是原创者？
   
    值得关注的模式：
    - Dotfiles/config 仓库 = 工具控
    - 大量教程/速查表仓库 = 学习者/分享者
    - 一个大型项目 vs 多个小型项目 = 深度 vs 广度
    - 热门项目的 fork = 向上游贡献

3.  STARS API  --  /users/{name}/starred?per_page=30
    curl -s 'https://api.github.com/users/{name}/starred?per_page=30'

    这是「宝藏」。Star 信息揭示：
    - 他们渴望构建什么（愿景兴趣）
    - 正在投资哪个技术生态
    - 对工具和框架的品味
    - 新兴兴趣点（最近加星的项目）
   
    通常比仓库更真实——仓库展示的是已完成的作品，
    Star 展示的是真正在意的东西。

4.  EVENTS API  --  /users/{name}/events?per_page=30
    curl -s 'https://api.github.com/users/{name}/events?per_page=30'

    可获取的信息：
    - Recent activity: 现在正在做什么
    - Push events: 正在积极开发的仓库
    - Issue/PR activity: 团队协作还是单打独斗？
    - Watch events: 关注了哪些社区
   
5.  ORGS API  --  /users/{name}/orgs
    curl -s 'https://api.github.com/users/{name}/orgs'

    可获取的信息：
    - 公司/团队归属
    - 所属的开源社区
    - 职业社交网络

6.  FOLLOWERS/FOLLOWING  --  /users/{name}/followers
    展示其职业社交网络图谱。
    关注TA的人 = 认可TA工作的人。
    TA关注的人 = TA学习模仿的对象。

7.  个人网站  --  个人资料中的 {blog}
   
    如果有博客/笔记（如 .github.io）：
    - 文字能体现思考深度
    - 主题能展示真正愿意写的内容
    - 技术文章 > "学习心得"类文章，更能体现技能水平
    - 发文频率体现持续性

8.  语言分布
   
    不要只看仓库总数——要看最近的仓库。
    一个开发者有20个Java仓库但最近3个是Rust，
    那他现在就是Rust开发者，而非Java开发者。

    语言时间线 = 数据中可见的职业发展轨迹。

9.  仓库命名与描述
   
    - 专业描述 = 大厂背景
    - 表情符号/俏皮描述 = 创业/开源文化
    - 中文描述 = 可能base中国，双语背景
    - 学术术语 = 科研背景
    - 无描述 = 只管交付，不善营销

10. 贡献图（不在API中，但可见）
    
    github.com/{name} 显示绿色方块：
    - 连续不断 = 自律的日常编码者
    - 突增突减 = 项目驱动、截止日期驱动
    - 空白期 = 换工作、倦怠期或做副业
    - 周末活动 = 热情项目时间

=== 各信息源揭示的内容 ===

  数据源          | 揭示内容
  ----------------+----------------------------------
  Profile bio     | 自我身份认同（一句话）
  Repos           | 搭建了什么
  Stars           | 欣赏/向往什么
  Events          | 现在在做什么
  Orgs            | 与谁共事
  Followers       | 谁认可他们
  Blog            | 如何思考
  Languages       | 实际使用什么
  Topics          | 关心哪些领域
  Forks           | 向什么贡献
  Stars（近期）   | 正在学习什么
  Created_at      | 资历（平台使用年限）

=== 共同兴趣检测 ===

  比较两位工程师：
  1. 语言重叠 --> 共享技术栈
  2. Star 重叠 --> 共同兴趣（最强信号）
  3. 主题重叠 --> 相同领域
  4. 共同组织 --> 相同社区
  5. 共同关注者 --> 职业圈重叠
  
  Star 重叠是最真实的信号，因为：
  - 人们只给自己真正感兴趣的项目加星
  - 没有社交压力（Star 相对私密）
  - 展示的是愿景，而非过去的工作成果
```

核心洞察：**Stars > Repos** 更能了解一个人的兴趣。Repos 展示的是他们在各种限制（工作、时间、机会）下完成的作品。Stars 展示的是他们真正在意的东西——发自内心的好奇心。当我分析 nocmk2 时，他加星的项目（hermes-agent, openclaw, langfuse, opencode）比他的55个仓库（许多是空仓库或 fork）更清晰地描绘了他对 AI 代理的痴迷。

想要我把这个变成一个可重复使用的脚本或技能，能自动为任何 GitHub 用户画像吗？
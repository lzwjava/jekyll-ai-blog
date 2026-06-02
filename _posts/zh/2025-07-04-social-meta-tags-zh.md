---
audio: false
generated: true
lang: zh
layout: post
title: SSI社交元标签
translated: true
type: note
---

您提供的代码包含 **Open Graph (OG)** 和 **Twitter Card** 元标签，用于控制在社交媒体平台（如 Facebook、Twitter（现为 X）以及其他支持这些协议的平台）上分享内容时的显示方式。这些标签是网站 HTML `<head>` 部分的一部分，为社交媒体信息流中的页面展示提供元数据，以增强其呈现效果。

在本例中，这些元标签用于 **Safe Superintelligence Inc. (SSI)** 的网站，可通过 `https://ssi.inc` 访问。下面，我将解释这些标签是什么、它们如何工作，并根据提供的信息提供关于 Safe Superintelligence Inc. 的背景说明。

---

### 这些元标签是什么？

**Open Graph (OG) 元标签**：
- 由 Facebook 开发，Open Graph 标签允许网站在支持 Open Graph 协议的平台（如 Facebook、LinkedIn 等）上定义其内容被分享时的显示方式。
- 这些标签指定了页面的关键细节，如标题、描述、图片和 URL，确保链接被分享时能呈现一致且视觉上吸引人的预览。

**Twitter Card 元标签**：
- Twitter Cards 是 Twitter（现为 X）使用的类似概念，用于丰富推文或帖子中的链接预览。
- 它们提供元数据，以便在平台上分享 URL 时显示摘要、图片或其他媒体内容。

这两组标签通过确保共享的链接看起来专业并提供相关信息（如标题、描述和图片）来帮助优化用户体验。

---

### 元标签详解

以下是您提供的代码中每个标签的作用：

#### Open Graph 标签
1. `<meta property="og:url" content="https://ssi.inc">`
   - 指定要分享页面的规范 URL。这确保显示和跟踪的是正确的 URL，避免重复（例如 `ssi.inc` 与 `www.ssi.inc`）。
   - **值**: `https://ssi.inc`

2. `<meta property="og:type" content="website">`
   - 定义内容类型。在本例中，`website` 表示一个通用网页（其他类型包括 `article`、`video` 等）。
   - **值**: `website`

3. `<meta property="og:title" content="Safe Superintelligence Inc.">`
   - 设置在社交媒体预览中显示的标题。这通常是页面或组织的名称。
   - **值**: `Safe Superintelligence Inc.`

4. `<meta property="og:description" content="The world's first straight-shot SSI lab, with one goal and one product: a safe superintelligence.">`
   - 提供页面内容的简要描述，显示在预览中。这概括了 Safe Superintelligence Inc. 的使命。
   - **值**: `The world's first straight-shot SSI lab, with one goal and one product: a safe superintelligence.`

5. `<meta property="og:image" content="https://ssi.inc/public/og-preview.jpg">`
   - 指定在预览中显示的图片。这通常是徽标、横幅或相关图形。
   - **值**: `https://ssi.inc/public/og-preview.jpg`

#### Twitter Card 标签
1. `<meta name="twitter:card" content="summary_large_image">`
   - 定义 Twitter Card 的类型。`summary_large_image` 创建一个带有大图片、标题和描述的预览。
   - **值**: `summary_large_image`

2. `<meta name="twitter:site" content="@ssi">`
   - 指定与网站关联的 Twitter (X) 账号，链接到该组织的官方账户。
   - **值**: `@ssi`

3. `<meta property="twitter:domain" content="ssi.inc">`
   - 指示被分享网站的域名。
   - **值**: `ssi.inc`

4. `<meta property="twitter:url" content="https://ssi.inc">`
   - 指定被分享页面的 URL，类似于 `og:url`。
   - **值**: `https://ssi.inc`

5. `<meta name="twitter:title" content="Safe Superintelligence Inc.">`
   - 设置 Twitter Card 的标题，与 Open Graph 标题一致。
   - **值**: `Safe Superintelligence Inc.`

6. `<meta name="twitter:description" content="The world's first straight-shot SSI lab, with one goal and one product: a safe superintelligence.">`
   - 提供 Twitter Card 的描述，与 Open Graph 描述一致。
   - **值**: `The world's first straight-shot SSI lab, with one goal and one product: a safe superintelligence.`

7. `<meta name="twitter:image" content="https://ssi.inc/public/og-preview.jpg">`
   - 指定 Twitter Card 的图片，与 Open Graph 图片一致。
   - **值**: `https://ssi.inc/public/og-preview.jpg`

---

### 这些元标签如何工作？

1. **目的**：
   - 当有人在 Facebook 或 Twitter (X) 等平台上分享 URL `https://ssi.inc` 时，该平台的网络爬虫（例如 Facebook 的爬虫或 Twitter 的机器人）会从页面的 HTML 中读取这些元标签。
   - 爬虫提取标题、描述、图片和其他元数据以生成丰富的预览卡片。例如：
     - 在 **Facebook** 上，共享的链接将显示一张卡片，标题为 "Safe Superintelligence Inc."，描述为 "The world's first straight-shot SSI lab…"，并显示位于 `https://ssi.inc/public/og-preview.jpg` 的图片。
     - 在 **Twitter (X)** 上，会出现一张类似的卡片，带有大图片、相同的标题和描述，以及用于归属的 `@ssi` 账号。

2. **机制**：
   - **爬取**：当 URL 被分享时，社交媒体平台会向网站的服务器发送请求以获取 HTML 并解析元标签。
   - **渲染**：平台使用标签值创建预览卡片。例如，Twitter 上的 `summary_large_image` 确保显示一个带有下方文字的突出图片。
   - **缓存**：平台可能会缓存元数据以减少服务器负载。如果标签已更新，像 Facebook 这样的平台提供工具（例如 Sharing Debugger）来刷新缓存。
   - **验证**：平台可能会验证图片（例如，确保其可访问且符合尺寸要求），并在标签缺失或无效时回退到默认文本或图片。

3. **影响**：
   - 这些标签通过使共享的链接在视觉上更具吸引力且信息丰富，从而提高了用户参与度。
   - 它们通过允许网站所有者控制标题、描述和图片来确保品牌一致性。
   - 它们可以通过提供引人入胜的预览来为网站带来流量。

---

### 关于 Safe Superintelligence Inc. (SSI)

根据元标签以及所提供搜索结果中的额外背景信息，以下是关于 Safe Superintelligence Inc. 的已知信息：

- **概述**：
  - Safe Superintelligence Inc. (SSI) 是一家美国人工智能公司，由 Ilya Sutskever（OpenAI 前首席科学家）、Daniel Gross（Apple AI 前负责人）和 Daniel Levy（AI 研究员和投资者）于 2024 年 6 月创立。
  - 其使命是开发 **安全超智能**，定义为超越人类智能同时优先考虑安全性以防止伤害的 AI 系统。

- **使命与方法**：
  - SSI 的唯一重点是创建一个安全的超智能系统，这既是其使命，也是其唯一产品。与其他 AI 公司不同，SSI 避免商业产品周期，专注于长期安全性和技术突破。
  - 该公司将安全性和 AI 能力视为相互交织的技术挑战，旨在快速提升能力，同时确保安全至关重要。
  - SSI 强调一种使其免受短期商业压力影响的商业模式，从而能够专注于安全、保障和进步。

- **运营**：
  - SSI 在 **加利福尼亚州帕洛阿尔托** 和 **以色列特拉维夫** 设有办事处，以招募顶尖技术人才。
  - 截至 2024 年 9 月，SSI 拥有约 20 名员工，但正在积极招聘研究员和工程师，重点关注"良好品格"和非凡能力，而不仅仅是资历。

- **融资与估值**：
  - 2024 年 9 月，SSI 以 **50 亿美元估值** 筹集了 **10 亿美元**，投资者包括 Andreessen Horowitz、Sequoia Capital、DST Global 和 SV Angel。
  - 到 2025 年 3 月，SSI 在由 Greenoaks Capital 领投的一轮融资中达到 **300 亿美元估值**，随后在 2025 年 4 月又筹集了 **20 亿美元**，使其总融资额达到 **30 亿美元**，估值为 **320 亿美元**。
  - 资金正用于获取计算能力（例如通过与 Google Cloud 合作获取 TPU）和招聘顶尖人才。

- **背景与领导层**：
  - Ilya Sutskever 是 OpenAI 的联合创始人，也是 ChatGPT 和 AlexNet 背后的关键人物，他于 2024 年 5 月离开 OpenAI，原因涉及安全担忧以及 Sam Altman 被罢免的事件。SSI 反映了他认为 OpenAI 已将重点转向商业化而非安全的信念。
  - SSI 对 **存在性安全**（例如，防止 AI 造成灾难性损害）的关注使其区别于"信任与安全"方面的努力（如内容审核）。
  - 该公司因其高知名度的团队和使命而备受关注，Meta 曾试图收购 SSI，并在 2025 年聘请了其 CEO Daniel Gross。

- **现状**：
  - SSI 处于 **隐匿模式**，截至 2025 年 7 月，尚无公开产品或收入。其网站极为精简，仅包含一个带有使命声明和联系信息的页面。
  - 该公司正专注于研发数年，然后才会发布其第一个产品，即安全的超智能。

---

### Safe Superintelligence Inc. 如何运作？

尽管 SSI 的技术细节因其隐匿模式而未公开，但可以从现有信息推断其运营模式：

1. **研究与开发**：
   - SSI 在 AI 安全、伦理、安全和治理方面进行基础研究，以识别风险并开发可验证的保障措施。
   - 该公司旨在创建一个与人类价值观保持一致并保持受控的超智能 AI 系统，类似于确保极端条件下核反应堆的安全。

2. **安全优先方法**：
   - 与 OpenAI 等开发 ChatGPT 等商业产品的公司不同，SSI 专门专注于构建单一的安全超智能系统，避免产品周期的"竞争激烈竞赛"。
   - 安全性被整合到能力开发中，通过创新工程将两者都作为技术问题来解决。

3. **团队与人才**：
   - SSI 正在帕洛阿尔托和特拉维夫建立一个精干、高技能的工程师和研究员团队，优先考虑那些致力于其安全使命的人员。
   - 公司花费大量时间审查候选人，以确保其与公司文化和使命保持一致。

4. **基础设施**：
   - SSI 与 Google Cloud 等云提供商合作，以获取 TPU（张量处理单元）来支持其 AI 训练的计算需求。
   - 该公司计划与芯片公司合作以获取额外的计算资源。

5. **教育与协作**：
   - 除了开发，SSI 还旨在教育研究员、开发者、政策制定者和公众关于安全 AI 实践，培养一种优先考虑安全而非商业化的全球思维模式。
   - 它寻求建立一个协作生态系统，为安全 AI 开发制定全球规范和最佳实践。

---

### 这些元标签对 SSI 的重要性

这些元标签反映了 SSI 的品牌和使命：
- 一致的标题和描述（"Safe Superintelligence Inc." 和 "The world's first straight-shot SSI lab…"）强调了其对安全超智能的单一关注，与其公开信息保持一致。
- Twitter 账号 `@ssi` 将网站与其官方 X 账户连接起来，公司成立公告等更新曾在该账户发布。
- 图片 (`og-preview.jpg`) 很可能是一个品牌图形或徽标，尽管其内容未公开描述。它确保了网站在被分享时的视觉一致性。

这些标签对于处于隐匿模式、公众形象极少的初创公司 SSI 至关重要，因为它们有助于控制其在社交媒体上的叙事，特别是考虑到其高知名度的创始人和重大的投资者兴趣。

---

### 局限性与说明
- **缺乏公开细节**：SSI 的网站和公开信息非常稀少，反映了其早期阶段和隐匿状态。元标签提供了对其品牌的一瞥，但未涉及其技术方法。
- **推测性质**：关于 SSI 估值和融资的说法基于报道，但具体细节（例如产品路线图）仍未披露。
- **X 推文作为情绪指标**：X 上的推文暗示了对 SSI 潜力的兴奋，但这并非事实证据，可能包含推测。

如果您希望我根据现有数据更深入地研究 SSI 的技术方法、分析相关的 X 推文以了解情绪，或进一步解释元标签，请告诉我！

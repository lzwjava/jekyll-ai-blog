---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Llama 4s热潮遭遇开发现实
translated: true
type: note
---

### 理解Llama 4发展轨迹与扎克伯格评论

马克·扎克伯格最初将Llama 4宣传为Meta开源AI事业的重要飞跃，计划在2025年内通过多次发布推动多模态能力发展（如原生处理文本与图像）。在2024年12月的更新中，他将其称为Llama 3之后的“下一站”。到2025年4月，Meta推出了“Llama 4系列”的首批模型——包括针对单GPU速度优化的Llama 4 Scout和擅长处理长文本的Llama 4 Maverick等较小模型。扎克伯格通过视频庆祝时称“发展轨迹非常清晰”，并预告更多版本即将推出。

然而完整版Llama 4系列（尤其是旗舰级“Behemoth”模型——拥有2万亿参数的庞然大物）的进展并未如此顺利。截至2025年5月，有报道称Meta因内部担忧推迟Behemoth发布：工程师难以实现相较前代版本的显著性能提升，且质疑改进幅度是否足以支撑公开推广。这使得项目脱离了扎克伯格早前制定的激进时间表——他在2025年初曾强力推动团队在48周内达成关键里程碑。

时间推进到2025年7月，事态进一步升级——据报道Meta在完成训练后考虑彻底放弃Behemoth，理由是其“内部表现欠佳”。他们停止进一步测试，将重心转向新的闭源模型而非坚持开源路线。这一转变与扎克伯格2025年9月的表态相呼应，他承认Llama 4“未处于正确轨道”，并促使Meta大举招聘组建“超智能实验室”以重整旗鼓，在没有僵化自上而下 deadline 的情况下加速进展。

截至2025年10月，Llama 4核心版本（Scout与Maverick）已上线并可通过AWS等平台获取，但Behemoth仍未见发布且实质上已被搁置。核心问题在于开发期间未达预期效果——尽管投入巨大算力资源，仍未能达到与OpenAI或谷歌等竞争对手抗衡的性能基准。扎克伯格早期的乐观主义与这些现实产生碰撞，最终导致延期、资源重新分配以及向更可控（闭源）开发策略的转变。

简而言之，这是AI热潮与规模化挑战碰撞的典型范例：虽怀揣雄心壮志，但在从日益庞大的模型中榨取最后一点能力时遭遇技术壁垒。

### 参考资料
- [马克·扎克伯格谈Llama 4训练进展](https://www.reddit.com/r/LocalLLaMA/comments/1id6gcj/mark_zuckerberg_on_llama_4_training_progress/)
- [Llama 4正式发布 | 马克·扎克伯格](https://www.facebook.com/zuck/videos/llama-4-is-here-/1334337587862376/)
- [AI的未来：基于Llama构建](https://ai.meta.com/blog/future-of-ai-built-with-llama/)
- [扎克伯格称其AI实验室采用‘扁平化管理’且不设硬性截止期限](https://www.businessinsider.com/mark-zuckerberg-superintelligence-lab-jobs-limited-deadlines-2025-9)
- [据华尔街日报报道：Meta推迟发布‘Behemoth’AI模型](https://www.reuters.com/business/meta-is-delaying-release-its-behemoth-ai-model-wsj-reports-2025-05-15/)
- [Meta计划放弃Llama 4 Behemoth，原因为何？](https://analyticsindiamag.com/global-tech/meta-plans-to-abandon-llama-4-behemoth-but-why/)
- [Llama 4系列：新时代的开端](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)

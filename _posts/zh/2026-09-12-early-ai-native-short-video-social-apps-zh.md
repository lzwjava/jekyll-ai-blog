---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 早期的AI原生短视频社交应用
translated: true
type: note
---

问题：是否存在**AI原生的短视频社交平台**，其内容由AI生成，具有无限滚动信息流，并配有原生iOS/Android应用？

答案：**是的——但这个类别仍处于极早期阶段。** 我找到了一些更接近你描述的案例，而非“AI视频生成器+导出到TikTok”的模式。

### 1. AICines —— 最接近你的构想

AICines可能是最清晰的例子。

[AICines在App Store上](https://apps.apple.com/us/app/aicines-ai-social-media/id6769682599?utm_source=chatgpt.com)

它的定位本质上是：

> **TikTok，但每个视频都由AI生成。**

它具备：

* 无限个性化信息流
* AI生成的短片/短视频/微型场景
* 关注/点赞/评论/收藏
* AI文本转视频+图像转视频
* 混音/重新创作他人的视频
* 创作者排行榜
* 创作者在作品被混音时获得积分
* 原生iPhone/iPad应用

有趣的是，**生成和消费处于同一个产品循环中**。([App Store][1])

这比Runway/Veo/Kling这类产品有趣得多。

---

### 2. Clip AI —— AI原生短视频信息流

Clip AI是另一个相当直接的例子。

它自称是一款**AI驱动的短视频应用**，具备：

* 无尽的短视频信息流
* AI生成的视频
* 个性化娱乐
* AI角色/聊天
* Android应用
* Google Play上100万+次下载

[Clip AI在Google Play上](https://play.google.com/store/apps/details?id=joinclip.ai&utm_source=chatgpt.com)

这更偏向娱乐/社交，而非“AI电影”。([Google Play][2])

---

### 3. Havira —— 更偏向AI原生创作+社交发现

[Havira](https://havira.app/?utm_source=chatgpt.com)

这个产品很有意思，因为它从以下步骤开始：

> 选择主题 → 描述想法 → 添加照片 → AI制作视频

并且明确具备：

* 展示区
* 精选视频
* 好友视频
* 社交信息流
* iOS + Android
* 多种底层视频模型

它还抽象了模型层——目前提及Veo、Kling和fal.ai——因此用户无需关心是哪个模型生成的片段。([Havira][3])

---

### 重要的区分

实际上，正在涌现**三个不同的类别**：

| 产品       | 生成 | 消费信息流 | 社交图谱 | 仅AI内容 |
| ---------- | ---: | ---------: | -------: | -------: |
| TikTok     |    ❌ |          ✅ |        ✅ |        ❌ |
| Sora       |    ✅ |          ✅ |     部分 |   mostly AI |
| Kling      |    ✅ |       有限 |        ❌ |        ❌ |
| VIBE       |    ✅ |          ❌ |        ❌ |        ❌ |
| **AICines** |    ✅ |        **✅** |      **✅** |      **✅** |
| **Clip AI** |    ✅ |        **✅** |      **✅** | **mostly** |
| **Havira**  |    ✅ |        **✅** |     部分 |    mostly |

所以，**如果你在思考的是产品类别，而非仅仅寻找一个AI视频生成器，那么AICines是我会首先研究的产品。**

真正有趣的产品论点是：

```text
             传统TikTok
                    │
             人类创作
                    ↓
             视频上传
                    ↓
             推荐算法
                    ↓
             观众


             AI原生视频
                    │
             用户有想法
                    ↓
             AI生成视频
                    ↓
             即时发布
                    ↓
             推荐算法
                    ↓
             观众
                    │
                    ↓
             混音/变异
                    │
                    ↓
             AI再次生成
```

最后一个循环是关键。

不再是：

**观看 → 观看 → 观看**

而是：

**观看 → 混音 → 生成 → 发布 → 观看 → 混音**

这有可能使**内容图谱具有生成性**，而不仅仅是UGC。

另外值得注意的是：现在已经有像VIBE这样的移动端AI视频生成器，但它们主要是**创作工具**，而非社交网络。VIBE支持iOS/Android和多种视频模型，但产品循环仍然是生成→导出/分享，而非生成→发布→推荐→混音。([VIBE: AI视频生成器][4])

如果你正在将这一领域作为产品机会进行探索，**我可以绘制当前的AI视频社交版图，并识别最大的未解决产品缺口**——包括AICines、Clip AI、Sora、TikTok、Instagram以及底层的生成经济学。

[1]: https://apps.apple.com/us/app/aicines-ai-social-media/id6769682599?utm_source=chatgpt.com "‎AICines: AI社交媒体应用 - App Store"
[2]: https://play.google.com/store/apps/details?hl=en-US&id=joinclip.ai&utm_source=chatgpt.com "Clip AI - 短视频与聊天 - Google Play应用"
[3]: https://havira.app/?utm_source=chatgpt.com "Havira | 面向所有人的AI视频生成器"
[4]: https://www.myvideoai.app/?utm_source=chatgpt.com "VIBE: iPhone和Android上的AI视频生成器应用"

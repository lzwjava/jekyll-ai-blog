---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 播客音频设置指南与专业麦克风
translated: true
type: note
---

**问题：** 根据当前 Newmine（MUSIC-BOOST）、USB、48 kHz、1 通道的配置，如何为播客录音选择最佳音频设置——Lex Fridman、Joe Rogan 等人使用什么设备？

---

**回答：**

## ⚠️ 当前配置存在的问题

你的 `Newmine MUSIC-BOOST` EQ 配置文件是为**音乐聆听**设计的，而非人声录音。它会人为增强低音和高音，这会让你的播客人声听起来**浑浊且不自然**。录音前应切换到**平坦/中性**或**语音/人声**配置文件。

你的其他设置实际上是正确的：

- **48 kHz** ✅ — 这是广播标准（BBC Radio 等使用），非常适合播客制作。推荐使用 48kHz 标准：所有音频制作和分发都应采用 48kHz，不仅是为了可听的音质，也是为了与广播工作流程兼容。
- **1 通道（单声道）** ✅ — 对于以语音为主的播客（如访谈、单人叙述或对话类节目），单声道录音通常是最佳选择。

---

## 🎙️ Lex Fridman 和 Joe Rogan 使用的设备

两人使用同一款传奇麦克风：

**Shure SM7B（XLR 动圈）**

- Lex Fridman 使用 Shure SM7B 动圈麦克风，以其温暖清晰的声音著称，是播客圈的热门选择。
- Joe Rogan 广为人知的播客麦克风正是流行的 Shure SM7B 动圈麦克风。
- Joe Rogan 选择的音频接口是 Universal Audio Apollo（当今等效产品为 Universal Apollo x6 Thunderbolt）。他的耳机是 Sennheiser HD280PRO，剪辑软件使用 Adobe Audition。

> **重要提示：** SM7B 是**纯 XLR 接口**，这意味着它需要音频接口（如 Focusrite Scarlett 2i2）才能连接到电脑。它**不是** USB 麦克风。

---

## 📊 按级别划分的最佳麦克风选择

| 级别 | 麦克风 | 连接方式 | 推荐理由 |
| --- | --- | --- | --- |
| **入门 USB** | Audio-Technica AT2040USB | USB | 最佳预算选择，适合噪声可控的环境 |
| **中端 USB** | Rode NT-USB+ | USB-C | 24-bit 位深、48kHz 采样率、USB-C——无需调音台 |
| **最佳 USB/XLR 混合** | Shure MV7+ | USB + XLR | 最适合 Twitch、YouTube 和播客，人声表现稳定一致 |
| **专业级（同 Lex/Rogan）** | Shure SM7B | 仅 XLR | 需要音频接口（Focusrite Scarlett 2i2 是热门搭配） |
| **高端** | Electro-Voice RE20 | 仅 XLR | 温暖清晰的人声，听起来质感高级——经典广播麦克风 |

---

## ✅ 对你当前配置的推荐操作

1. **立即执行：** 在系统音频设置中，将配置文件从 `MUSIC-BOOST` 切换为平坦/中性/人声配置文件
2. **保持：** 48 kHz 采样率、1 通道（单声道）
3. **如果升级麦克风：** 从 **Shure MV7+** 开始（USB/XLR 混合——兼具两者优势，音质接近 SM7B）
4. **如果走专业路线：** **Shure SM7B** + **Focusrite Scarlett 2i2** 音频接口（约 $400 美元），与 Lex 和 Rogan 相同的配置路径

---

**参考来源：**

- [Lex Fridman 的播客设备 – SwipeFile](https://swipefile.com/lex-fridmans-podcast-setup)
- [Joe Rogan 的设备清单 – LowerStreet](https://lowerstreet.co/equipment/joe-rogan)
- [2025 年最佳播客麦克风 – PodcastVideos](https://www.podcastvideos.com/best-podcast-microphones-2025/)
- [播客立体声与单声道对比 – PodcastVideos](https://www.podcastvideos.com/one-ear-or-two-stereo-vs-mono-techniques/)
- [48kHz 播客工作流程 – Earth.org.uk](https://www.earth.org.uk/metacast-2.html)

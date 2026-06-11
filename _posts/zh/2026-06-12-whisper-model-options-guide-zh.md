---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper 模型选项指南
translated: true
type: note
---

以下是 Whisper 选项的完整说明：

== 模型 ==

  tiny    39M 参数   ~1 GB VRAM   最快，质量最低
  base    74M 参数   ~1 GB VRAM   适合原型开发
  small  244M 参数   ~2 GB VRAM   均衡表现
  medium 769M 参数   ~5 GB VRAM   高质量
  large 1550M 参数  ~10 GB VRAM   最佳质量，仅支持多语言
  turbo  809M 参数   ~6 GB VRAM   速度/质量最佳平衡

建议：一般使用 turbo，快速测试用 base。

== 语言（共 99 种）==

  顶级（WER < 10%）：
    en  英语          zh  中文          ja  日语
    es  西班牙语      ko  韩语          fr  法语
    de  德语          it  意大利语      pt  葡萄牙语
    nl  荷兰语        pl  波兰语        ru  俄语

  良好（WER 10-20%）：
    ar  阿拉伯语      tr  土耳其语      vi  越南语
    sv  瑞典语        fi  芬兰语        cs  捷克语
    ro  罗马尼亚语    hu  匈牙利语      da  丹麦语
    no  挪威语        th  泰语          he  希伯来语
    el  希腊语        id  印尼语        ms  马来语

  还支持：南非荷兰语、阿尔巴尼亚语、阿姆哈拉语、亚美尼亚语、孟加拉语、
  波斯尼亚语、保加利亚语、缅甸语、粤语、加泰罗尼亚语、克罗地亚语、
  爱沙尼亚语、芬兰语、格鲁吉亚语、古吉拉特语、海地克里奥尔语、印地语、
  冰岛语、爪哇语、卡纳达语、哈萨克语、高棉语、老挝语、拉丁语、
  拉脱维亚语、立陶宛语、马其顿语、蒙古语、尼泊尔语、波斯语、
  旁遮普语、梵语、塞尔维亚语、斯洛伐克语、斯洛文尼亚语、索马里语、
  巽他语、斯瓦希里语、他加禄语、泰米尔语、泰卢固语、藏语、土耳其语、
  乌克兰语、乌尔都语、乌兹别克语、威尔士语、意第绪语、约鲁巴语等。

  语言代码为 ISO 639-1（2字母）。

== 关键选项 ==

  language="zh"           # 指定语言（比自动检测更快）
  task="transcribe"       # 以原语言转录（默认）
  task="translate"        # 将任何语言翻译成英语
  initial_prompt="..."    # 上下文提示（提高技术术语准确度）
  word_timestamps=True    # 词级时间戳
  temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)  # 后备温度
  device="cuda"           # 强制使用 GPU（未设置时自动检测）
  output_format="srt"     # 可选 txt、srt、vtt、json

== CLI 用法 ==

  whisper audio.mp3 --model turbo --language Chinese
  whisper audio.mp3 --task translate --output_format srt

== 中文特定提示 ==

  - 使用 medium 或 large 模型（small 的 WER 约 15%，large 降至约 5%）
  - 明确指定 language="zh"
  - 添加 initial_prompt 提供上下文：
      initial_prompt="这是一段关于技术的讨论"
  - 粤语有单独的代码：language="yue"
---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Pixel Recorder转录iPhone通话
translated: true
type: note
---

**问题：** 在 iPhone 上进行微信语音通话或电话通话时，使用 Pixel（第二部手机）上的 Google Recorder 录制音频并获取文字记录，再通过 AI 进行总结或重新整理，这是一个好主意吗？

**回答：**

是的，这是一种非常实用的工作流程。以下是其工作原理及优化方法：

## 为何有效

Google Recorder 在 Pixel 上确实是最优秀的免费转录工具之一——设备端实时处理、无需上传，且对中英文混说场景支持良好，这正好符合你的需求。

双手机设置解决了一个现实问题：iOS 和微信都让通话录音变得困难（iPhone 不支持原生通话录音，微信不开放音频流）。将 Pixel 靠近扬声器或放在通话双方中间，可以清晰捕捉环境音频以确保转录质量。

## 优化工作流

```
iPhone（微信/电话通话）
        ↓ 音频
Pixel（Google Recorder）→ 实时文字记录
        ↓ 导出 .txt
AI 处理流程（Claude/GPT）→ 清晰总结、待办事项、结构化笔记
```

**实用技巧：**
- 将 Pixel 放在扬声器附近，或使用小型支架固定
- Google Recorder 可直接导出 `.txt` 格式的文字记录——分享至你选择的 AI 工具即可
- 对于长通话，可将文字记录通过 API 直接输入 Claude，并附带提示词如："从这段通话记录中提取待办事项、决策和关键点"

## 快速 AI 优化脚本

```python
import anthropic

def refine_transcript(transcript_path: str) -> str:
    with open(transcript_path) as f:
        transcript = f.read()

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": f"""整理这段通话记录并提取：
1. 做出的关键决策
2. 待办事项（如提及负责人请标注）
3. 总结（3-5句话）

通话记录：
{transcript}"""
        }]
    )
    return msg.content[0].text

print(refine_transcript("call_transcript.txt"))
```

## 需注意的局限性

- 若未开启扬声器，耳塞音频难以清晰捕捉，录音质量会下降
- 存在背景噪音或口音较重时，Google Recorder 的准确率会降低
- 中文转录效果尚可但不完美；中英文混合的通话需要后期人工修正

总体而言：是的，这是一个实用且低门槛的设置，完全适合你的使用场景。
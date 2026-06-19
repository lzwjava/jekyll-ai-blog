---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transcribe iPhone Calls with Pixel Recorder
translated: false
type: note
---

**Question:** When doing a WeChat voice call or phone call on iPhone, is it a good idea to use Google Recorder on a Pixel (second phone) to capture audio and get a transcript, then use AI to summarize or reformat it?

**Answer:**

Yes, this is a solid practical workflow. Here's why it works and how to optimize it:

## Why It Works

Google Recorder on Pixel is genuinely one of the best free transcription tools available — on-device, real-time, no upload needed. It handles Mandarin + English code-switching reasonably well too, which matters for your context.

The two-phone setup solves a real problem: iOS and WeChat both make call recording difficult (no native call recording on iPhone, WeChat doesn't expose audio streams). A Pixel held near the speaker, or placed between both parties, captures ambient audio cleanly enough for transcription.

## Optimized Workflow

```
iPhone (WeChat/Phone call)
        ↓ audio
Pixel (Google Recorder) → real-time transcript
        ↓ export .txt
AI pipeline (Claude/GPT) → clean summary, action items, structured notes
```

**Practical tips:**
- Put Pixel on speakerphone-adjacent position, or use a small stand
- Google Recorder exports transcript as `.txt` directly — share to your AI tool of choice
- For long calls, the transcript can be piped straight into Claude via API with a prompt like `"Extract action items, decisions, and key points from this call transcript"`

## Quick AI Refinement Script

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
            "content": f"""Clean up this call transcript and extract:
1. Key decisions made
2. Action items (with owner if mentioned)
3. Summary (3-5 sentences)

Transcript:
{transcript}"""
        }]
    )
    return msg.content[0].text

print(refine_transcript("call_transcript.txt"))
```

## Limitations to Know

- Audio quality degrades if you're not on speaker — earpiece audio is hard to capture
- Google Recorder accuracy drops with background noise or strong accents
- Mandarin transcription is decent but not perfect; mixed-language calls need post-correction

Overall: yes, this is a practical, low-friction setup that works well for your use case.

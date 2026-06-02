---
audio: false
generated: true
image: false
lang: en
layout: post
title: Refine Chinese Meeting Transcription Prompt
translated: false
type: note
---

Question: Improve the prompt for refining a Whisper meeting transcription into a Chinese article/post

Answer:

Read `@meeting_01_2.txt`, which is a raw Whisper transcription of a meeting conversation in Chinese.

Generate a new file named `meeting_01_2_refined.md`.

Requirements:

* Rewrite and organize the content into a clean, readable Chinese article, meeting summary, or post.
* Preserve the original meaning, tone, speaking style, and emotional nuance as much as possible.
* The original transcription involved two speakers, but speaker labels were lost. Do not attempt to reconstruct exact identities or use “Speaker A/B”.
* Instead, describe the discussion naturally from a third-person perspective using words such as “他们”, “双方”, or contextual narration.
* Remove obvious transcription noise, repeated filler words, broken sentences, and recognition artifacts from Whisper.
* Reorganize fragmented dialogue into coherent paragraphs and logical sections.
* Keep the original language as Chinese throughout the output.
* Do not overly formalize the content; retain the conversational and authentic feel of the original meeting.
* If some sentences are unclear due to transcription quality, infer conservatively and keep ambiguity rather than inventing details.
* Add:

  * A suitable Chinese title
  * Section headings where appropriate
  * A short summary at the beginning
* Output only valid Markdown content into `meeting_01_2_refined.md`.

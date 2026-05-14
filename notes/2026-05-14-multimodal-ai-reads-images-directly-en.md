---
audio: false
generated: true
image: false
lang: en
layout: post
title: Multimodal AI Reads Images Directly
translated: false
type: note
---

Earlier today I asked Claude (inside Claude Code) to look at a screenshot on my Mac, `~/Downloads/s1.jpg`, and pull the exam scores out of it. It did. Then I asked: *how did you actually read the JPG?* This post is the longer version of the answer, plus a side note on whether ChatGPT does the same thing.

## What happened

Claude Code has a built-in `Read` tool. When the path you give it points to a text file, it returns the lines. When the path points to an image — PNG, JPG, screenshot, photo, anything Claude can decode — the tool does something different: it loads the bytes and **hands the image directly to the model as part of the conversation**, the same way you would attach an image to a chat in the Claude web app.

There is no OCR step. There is no external vision API call. The model itself looks at the pixels.

So when the screenshot showed:

```
计算机网络技术    23
大学语文          57
计算机高级程序设计  74
习近平新时代...    56
```

Claude is not running Tesseract behind the scenes and feeding the extracted text back to itself. It is *seeing* the rendered Chinese characters and the numbers next to them, in the same pass where it decides what to do with the file you edited five minutes ago. The text and the image are both tokens in the same context window.

## What "multimodal" actually means

A model is **multimodal** when its weights were trained to accept more than one kind of input — typically text and images, sometimes audio, sometimes video. Inside the model, an image gets chopped into patches, each patch gets turned into a vector (a "visual token"), and those vectors sit alongside the text tokens in the same sequence the transformer processes.

This is different from the older pipeline approach:

- **Old pipeline (not multimodal):** image → OCR service → text → language model
- **Multimodal model:** image → patch embeddings → same transformer that handles text

The pipeline version loses everything that isn't text: layout, colors, handwriting style, whether a checkbox is checked, the fact that a number is highlighted in red. A native multimodal model keeps all of that, because the pixels are right there in context.

## Is Claude multimodal? Is ChatGPT?

Yes to both, with caveats worth knowing.

**Claude** (the Anthropic model family — Opus, Sonnet, Haiku in the Claude 4 series, currently 4.6) accepts text and images as input. It does **not** accept audio or video directly, and it does **not** generate images — output is text only. Claude Code's `Read` tool taking a JPG works because the underlying model supports image input.

**ChatGPT** (OpenAI's product) is a wrapper around several models. GPT-4o and later are natively multimodal: they accept text, images, and audio, and can produce text, images (via tool-use to the image model), and audio. The voice mode you've probably heard about works because audio is a first-class input, not a transcript routed through Whisper.

**Gemini** (Google) goes further on paper: text, images, audio, *and* video as native inputs, with very long context windows.

So "is X multimodal?" is rarely a yes/no. It is more useful to ask: *which modalities go in, and which come out?* For my screenshot task I only needed image-in, text-out, which is the most widely supported combination and is exactly what Claude offers.

## Why this matters for everyday work

Once you internalize that the model genuinely sees the image, a class of tasks gets very easy:

- Paste a screenshot of an error dialog instead of retyping it.
- Drop in a photo of a whiteboard and ask for the equations in LaTeX.
- Show a UI mockup and ask for the HTML/CSS.
- Hand over a chart and ask what the trend is — no need to export the underlying data.

The thing I did this afternoon — reading four scores off a Chinese exam-result screenshot and updating a Markdown file — is just the boring version of this. The interesting part is that the boring version now works reliably enough that I stopped thinking of it as a separate step. The file path went in, the right scores came out.

## The small footnote

There is one place the abstraction can leak: images cost tokens. A high-resolution screenshot can eat a few thousand tokens of context, more than the surrounding code in a typical session. If you are paying per token or running close to a context limit, prefer cropped or downscaled images over full-screen dumps. But for occasional use — a screenshot here, a photo there — it is genuinely the most natural way to hand information to the model.
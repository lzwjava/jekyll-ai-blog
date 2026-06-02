---
audio: false
generated: true
image: false
lang: en
layout: post
title: macOS Live Text OCR Feature
translated: false
type: note
---

Question: In macOS Preview, you can select text from an image. Is this using OCR technology?

Answer:

Yes, what you are seeing is indeed based on OCR (Optical Character Recognition) technology, but Apple calls it **Live Text**. Starting from **macOS Monterey (12)**, Apple integrated a system-wide feature that can recognize text in images, screenshots, and even in the camera view on iOS devices. When you open an image in Preview (or Photos, Safari, etc.), macOS analyzes the image in real time, detects any text, and makes it selectable and copyable.

Key points:

* This is **native OCR**, fully built into the system, not a separate app.
* It works on images, screenshots, and even PDFs where the text is part of the image, not embedded as text.
* Apple uses machine learning models on-device for this, which means no internet connection is required for text recognition.
* Beyond copying, you can also **look up words, translate, or call phone numbers** detected in images.

In short, it’s essentially magic from a user perspective, but behind the scenes, it’s sophisticated **on-device OCR powered by ML models**.

References:

* [Apple: Use Live Text on your Mac](https://support.apple.com/guide/mac-help/use-live-text-mchl3f2f7b0a/mac)
* [Apple introduces Live Text in macOS Monterey](https://www.apple.com/newsroom/2021/10/macos-monterey-introduces-powerful-new-features/)

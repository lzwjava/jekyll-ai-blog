---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Purpose of HTML5 Meta Charset Tag
translated: false
type: note
---

Question: What is the primary purpose of the <meta charset="utf-8"> tag in HTML5?

A) To set the page background color
B) To specify the character encoding for the document
C) To define the page title
D) To link an external CSS file

Answer:

The correct answer is **B) To specify the character encoding for the document**.

In HTML5, the `<meta charset="utf-8">` tag (a simplified form of the more verbose meta element) is placed in the `<head>` section and declares the character encoding used in the document. The most common and recommended value is "utf-8", which supports a wide range of characters and symbols from virtually all languages. This declaration helps browsers correctly interpret and render special characters, preventing issues like garbled text (e.g., "mojibake").

- Option A is incorrect because background color is handled by CSS (e.g., `body { background-color: ... }`).
- Option C is incorrect because the page title is defined using the `<title>` tag.
- Option D is incorrect because external CSS files are linked using the `<link rel="stylesheet" href="styles.css">` tag.

This tag should be one of the first elements in the `<head>` to ensure proper encoding detection before any content is parsed.

Your selection of B is correct.

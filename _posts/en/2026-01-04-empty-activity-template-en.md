---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Choosing the Empty Activity Template
translated: false
type: note
---

Question: When creating a new Android project in Android Studio, which template is typically chosen for a basic empty app?

Answer:

The correct answer is **A) Empty Activity**.

In recent versions of Android Studio (including those up to 2025–2026), when creating a new project and selecting the "Phone & Tablet" category, the default and most commonly recommended template for a basic empty app is **Empty Activity**. This template provides a minimal setup with a single blank activity (usually `MainActivity.kt` or `.java`) and its corresponding layout file (`activity_main.xml`), containing only a "Hello World!" TextView by default. It is ideal for starting from scratch without any pre-added UI components like toolbars, floating action buttons, or navigation elements.

- **Basic Activity**: Includes additional UI elements such as an app bar, a floating action button, and often a menu—more than a truly basic empty app.
- **Navigation Drawer Activity**: Adds a sliding navigation drawer with a menu, intended for apps with multiple sections.
- **Blank Fragment**: Focuses on creating a project with fragment-based architecture, not a simple single-activity app.

The "Empty Activity" (or sometimes labeled "Empty Views Activity" in newer templates) remains the standard choice for the simplest starting point.

References:

- [Android Developers - Create a project](https://developer.android.com/studio/projects/create-project)

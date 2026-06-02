---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Storage Location for Android Drawable Resources
translated: false
type: note
---

Question: In which folder should drawable resources like images be placed?
A) res/values
B) res/layout
C) res/drawable
D) res/menu

Answer:

The correct answer is **C) res/drawable**.

In an Android project, drawable resources such as images (PNG, JPEG, SVG), vector drawables, and other graphical assets that can be drawn on the screen should be placed in the `res/drawable` folder (or its density-specific variants like `drawable-hdpi`, `drawable-mdpi`, etc.).

### Brief explanation of each option

- **A) res/values**: This folder is for XML files defining simple values like strings, dimensions, colors, styles, and arrays — not images or drawables.
- **B) res/layout**: This folder contains XML layout files that define the UI structure of activities, fragments, etc.
- **C) res/drawable**: Correct folder for bitmap files, vector drawables, shapes, selectors, and other drawable resources.
- **D) res/menu**: This folder is for XML files defining menus (e.g., options menus, context menus).

Placing images in the correct `res/drawable` folder ensures they can be properly referenced in code or XML (e.g., `@drawable/my_image`) and supports automatic density handling.

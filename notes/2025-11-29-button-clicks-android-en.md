---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Handling Button Clicks in Android
translated: false
type: note
---

**Correct answer: B. OnClickListener**

In Android development, the most common and recommended way to handle click events on a `Button` (or any `View`) is by implementing or setting a **`View.OnClickListener`**.

### Why B is correct:
- `View.OnClickListener` has a single method: `onClick(View v)`
- It's specifically designed for handling standard tap/click events
- Example usage:
  ```java
  button.setOnClickListener(new View.OnClickListener() {
      @Override
      public void onClick(View v) {
          // Handle click
      }
  });
  ```
  or with lambda (Kotlin/Java 8+):
  ```java
  button.setOnClickListener(v -> { /* Handle click */ });
  ```

### Why the others are not the best choice:
- **A. OnTouchListener** – Lower-level touch events (ACTION_DOWN, ACTION_UP, etc.). Overkill for simple clicks and can interfere with gesture detection.
- **C. OnLongClickListener** – Only for long-press events, not regular clicks.
- **D. OnKeyListener** – For hardware/software keyboard key events, not view clicks.

**Best practice**: Always use `OnClickListener` for standard button clicks (you can also define the click handler directly in XML with `android:onClick="methodName"`).

So, **B** is definitely the correct answer.

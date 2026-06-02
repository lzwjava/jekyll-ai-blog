---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding CSS Flex Shorthand Explained
translated: false
type: note
---

Question: What does `flex: 0 1 20%` mean in CSS?

Answer: The `flex` property is a shorthand for three specific flexbox properties. When you write `flex: 0 1 20%`, you are defining how a flex item should grow, shrink, and its initial size.

### Breakdown of the Values

1.  **`0` (flex-grow):**
    This defines the ability of a flex item to grow if there is extra space in the container. A value of `0` means the item **will not grow** to fill up remaining space. It will only stay as wide as its content or its `flex-basis`.

2.  **`1` (flex-shrink):**
    This defines the ability of a flex item to shrink if the container is too small. A value of `1` (the default) means the item **will shrink** proportionally with other items to prevent overflowing the container.

3.  **`20%` (flex-basis):**
    This defines the default size of the element before the remaining space is distributed. Setting it to `20%` means the item starts with an initial width (or height, depending on `flex-direction`) of **20% of the parent container**.

---

### Summary Table

| Property | Value | Description |
| :--- | :--- | :--- |
| **flex-grow** | `0` | Does not expand to fill extra space. |
| **flex-shrink** | `1` | Shrinks if the container gets too small. |
| **flex-basis** | `20%` | Starts at 20% width/height of the container. |



### Practical Behavior
If you have a row with five items all set to `flex: 0 1 20%`, they will perfectly fill the row. However, if you only have two items with this setting, they will each take up 20% of the width and leave 60% of the container empty because `flex-grow` is set to `0`.

Would you like me to show you a code example of how this behaves compared to `flex: 1 1 20%`?

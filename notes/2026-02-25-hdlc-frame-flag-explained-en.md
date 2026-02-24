---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDLC Frame Flag Explained
translated: false
type: note
---

Question: In the HDLC frame format, what is the flag field F?

Answer:

## HDLC Flag Field

The correct answer is **D: 01111110**

### Explanation

HDLC (High-Level Data Link Control) uses a special bit pattern as a **flag** to mark the boundaries of a frame.

The flag field value is:

```
01111110
```

This pattern serves dual purposes:
- It marks the **end** of the previous frame
- It marks the **beginning** of the next frame

### Why 01111110?

The flag `01111110` contains **six consecutive 1s** surrounded by 0s. To prevent this pattern from appearing accidentally within the data payload, HDLC uses a technique called **bit stuffing**:

- **Sender side**: After every five consecutive 1s in the data, a `0` is automatically inserted
- **Receiver side**: After receiving five consecutive 1s, if the next bit is `0`, it is automatically removed (destuffed)

This ensures the `01111110` pattern can **only** appear as an actual frame delimiter, never as part of the data content.

### Why the other options are wrong?

| Option | Value | Reason |
|--------|-------|--------|
| A | 11111111 | All ones — not the HDLC standard flag |
| B | 10000001 | Not the defined flag pattern |
| C | 01111101 | Close but incorrect — only five 1s, missing one |
| D | 01111110 | ✅ Correct — standard HDLC flag |

Option C (`01111101`) is a common trap because it looks similar, but it has the wrong bit arrangement and does not match the HDLC specification.
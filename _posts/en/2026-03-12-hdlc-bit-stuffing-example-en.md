---
audio: false
generated: true
image: false
lang: en
layout: post
title: HDLC Bit Stuffing Example Process
translated: false
type: note
---

Question: In HDLC framing, if the data field contains the bit string "01011111001", what is the output after bit stuffing?

Answer:

## HDLC Bit Stuffing Explanation

### Rule

In HDLC, the flag byte is `01111110`. To prevent this pattern from appearing inside data, **bit stuffing** is applied:

- **Sender:** After every **5 consecutive 1s**, automatically insert a `0`
- **Receiver:** After every **5 consecutive 1s**, automatically remove the following `0`

---

### Step-by-Step Processing

Original bit string: `0 1 0 1 1 1 1 1 0 0 1`

Let's scan for 5 consecutive 1s:

```
Position:  0  1  0  1  1  1  1  1  0  0  1
                      ^  ^  ^  ^  ^
                      1  2  3  4  5  ← 5 consecutive 1s found!
```

After the 5th consecutive `1` (at position index 7), insert a `0`:

```
Original:  0  1  0  1  1  1  1  1     0  0  1
                               ↓ insert 0 here
Result:    0  1  0  1  1  1  1  1  0  0  0  1
```

### Result

| Stage | Bit String |
|---|---|
| Before stuffing | `0 1 0 1 1 1 1 1 0 0 1` |
| After stuffing | `0 1 0 1 1 1 1 1 0 0 0 1` |

→ **`010111110001`** ✅

---

### Why Not Option B?

Option B = `010111110010` — This would mean the inserted `0` went to the **end**, which is **incorrect**. The `0` must be inserted **immediately after** the 5th consecutive `1`, not shifted elsewhere.

### Answer: **D) 010111110001**

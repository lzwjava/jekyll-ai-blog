---
audio: false
generated: true
image: false
lang: en
layout: post
title: Finding and Connecting GA-H81M-DS2 Speaker
translated: false
type: note
---

**Question:** How do you find and connect the SPEAKER header on the GA-H81M-DS2 motherboard?

---

**Answer:**

---

### 1. 📍 Where is the SPEAKER Header on the Board?

It is located in the **front panel header group** — a cluster of pins near the **bottom-right edge** of the motherboard, labeled **F_PANEL**.---

**Question:** How do you find and connect the SPEAKER header on the GA-H81M-DS2?

**Answer:**

---

### Step 1 — Find It on the Board

The SPEAKER header sits inside the **F_PANEL header group**, at the **bottom-right corner** of the motherboard (as shown in the diagram above). The entire F_PANEL area is a cluster of small pin headers all grouped together.

Look for the label **"SPEAKER"** silkscreened on the PCB in white text — it is a **4-pin block** (2×2 arrangement).

---

### Step 2 — Pin Layout

```
Pin 1 (+)  | Pin 2 (NC)
Pin 3 (NC) | Pin 4 (–)
```

- **Pin 1** = positive (+5V signal)
- **Pin 4** = negative (GND)
- Pins 2 & 3 are not connected (NC)

---

### Step 3 — The Speaker Cable / Speaker Itself

You have two options:

**Option A — Case has a built-in speaker wire**
Most ATX cases include a small 4-pin plug from the case that says `SPEAKER` or `SPK`. Just plug it into the header matching Pin 1 (+) direction.

**Option B — Your case has NO speaker**
Buy a **PC case speaker / piezo buzzer** — costs less than $2 on Amazon or any electronics shop. It looks like a small black cylinder with a 4-pin connector or bare wires.

> ⚠️ This is **different from your audio jack** — it is a tiny mechanical buzzer for diagnostic beep codes only, not for music or sound.

---

### Step 4 — Confirm It Works

After connecting, boot the PC. If RAM is missing or there's a POST error, you will hear beep codes. If it boots normally, you hear **one short beep** — that confirms the speaker is working.

---

**References:**
- [GA-H81M-DS2 User's Manual — F_PANEL header pin assignments (Gigabyte PDF)](https://download.gigabyte.com/FileList/Manual/mb_manual_ga-h81m-ds2_4001_e.pdf)

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Case Speaker and POST Beeps
translated: false
type: note
---

**Question:** What exactly is a "case speaker" and how does it connect to the SPEAKER header?

---

**Answer:**

A **case speaker** (also called a **PC speaker** or **piezo buzzer**) is a tiny, cheap buzzer built specifically to make the **beep codes** you hear during POST. It is **completely separate** from your normal audio system.---

### What It Looks Like

It's a **tiny black cylinder** (about the size of a thumbnail) attached to a small 4-pin plug. The cylinder is the buzzer, and the plug slots directly onto the SPEAKER header on the motherboard.

---

### It Is NOT Your Audio Speaker

| | Case Speaker (Piezo Buzzer) | Normal PC Speaker |
|---|---|---|
| Purpose | POST beep codes only | Music, audio, sound |
| Sound quality | Harsh single-tone beep | Full audio |
| Connected to | Motherboard SPEAKER header | Front panel audio / rear jack |
| Cost | ~$1–$2 | $10–$100+ |
| Required for diagnostics? | ✅ Yes | ❌ No |

---

### Does Your Case Already Have One?

**Check inside your case** — many older ATX cases include one already, usually:
- A small black buzzer **glued or screwed** to the inside of the case frame
- With a wire running to a **4-pin connector** labeled `SPK` or `SPEAKER`

If yours does, just plug it into the F_PANEL SPEAKER pins on the board.

---

### If Your Case Doesn't Have One — What to Buy

Search for any of these terms:
- **"PC internal speaker buzzer"**
- **"motherboard piezo speaker"**
- **"PC POST speaker"**

They are sold on Amazon, AliExpress, Shopee, or any local computer parts shop for under **$2 USD**. The connector is always the same standard 4-pin plug — it fits the GA-H81M-DS2 SPEAKER header directly.

---

### How to Connect ItHere's a clear diagram of how everything connects:---

### Quick Tips

**Polarity** — the red wire or the side marked with a triangle/arrow on the plug goes to Pin 1 (+). If you plug it in backwards you get no beeps, but nothing breaks. Just flip it around.

**No plug, just bare wires?** Some cheap buzzers come with loose wires instead of a plug. In that case, just push the red wire into Pin 1 and black wire into Pin 4 of the header manually — or use a small jumper clip.

**Already have one inside the case?** Look along the inside walls of the PC case, usually near the front panel wires. It may already be there with a labeled connector — just find it and plug it in.

---

**References:**
- [GA-H81M-DS2 User's Manual — F_PANEL pin assignments](https://download.gigabyte.com/FileList/Manual/mb_manual_ga-h81m-ds2_4001_e.pdf)
- [Gikfun PC Motherboard Internal Piezo Speaker on Amazon](https://www.amazon.com/s?k=pc+internal+speaker+buzzer+motherboard)

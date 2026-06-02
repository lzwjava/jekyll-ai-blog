---
audio: false
generated: true
image: false
lang: en
layout: post
title: Camera Screen Privacy Risks
translated: false
type: note
---

**Question:** When working in a coffee shop, can nearby cameras (2–3 meters away, at angles) leak information from my screen, given modern high-resolution cameras? Is this a real concern, or not a big issue for tools like Teams, Jira, or Confluence?

**Answer:**

You’re right to think about this—**visual data leakage (shoulder surfing + camera capture)** is a real, but often *overestimated*, risk. The truth sits in the middle: **possible, but usually low probability unless conditions are favorable**.

---

## 🎯 How realistic is camera-based screen leakage?

### ✔️ Technically possible

Modern cameras (CCTV or phones) can:

* Capture **4K or higher resolution**
* Zoom digitally
* Enhance contrast / sharpen text

From **2–3 meters away**, under good conditions, they *can* capture:

* Large text (titles, headings)
* UI structure (which app you're using, e.g. Jira or Confluence)
* Possibly short words if:

  * font is large
  * screen brightness is high
  * viewing angle is direct

---

### ❌ But in most real scenarios, it’s limited

For typical work like:

* Microsoft Teams chats
* Jira tickets
* Confluence pages

At **2–3 meters distance + 45° angle**:

* Small text (normal UI font ~10–14pt):

  * becomes **blurred or unreadable**
* Motion (scrolling, typing):

  * reduces clarity further
* Lighting + reflections:

  * degrade capture quality
* Compression (CCTV systems):

  * often lowers actual usable resolution

👉 So your intuition is mostly correct:

> After a short time / normal usage, **fine-grained content is hard to extract reliably**

---

## ⚠️ When it *does* become a real risk

You should be more cautious if:

### 1. **High-value / sensitive data**

* Credentials, tokens, API keys
* Customer data, financial info
* Internal documents not meant for exposure

---

### 2. **Favorable capture conditions**

* Camera directly facing your screen
* You sitting still for long periods
* Large external monitor
* High brightness + high contrast (dark text on white background)

---

### 3. **Targeted attack scenario (rare but possible)**

* Someone intentionally recording you (not random CCTV)
* Insider threat in shared workspace

---

## 🧠 Practical reality (important perspective)

For most people working in a coffee shop:

> The **biggest risks are NOT cameras**, but:

* Public Wi-Fi attacks (already mitigated by VPN 👍)
* Phishing / credential theft
* Malware on device

Camera-based leakage is:

* **Low probability**
* **Low bandwidth** (can’t easily capture large amounts of detailed data)

---

## 🔒 Simple, high-impact protections

You don’t need paranoia—just smart habits:

### ✔️ Reduce visual exposure

* Sit with your **back to a wall**
* Avoid facing cameras or open space
* Slightly tilt screen downward

---

### ✔️ Control screen readability

* Lower brightness slightly
* Use dark mode when possible
* Avoid zooming sensitive text too large

---

### ✔️ Use a privacy screen filter (very effective)

* Narrows viewing angle to ~30°
* Makes side-angle viewing almost impossible

---

### ✔️ Be mindful during sensitive actions

* Logging into systems
* Viewing credentials
* Accessing confidential documents

---

## 🧾 Bottom line

* **Yes**, modern cameras *can* capture screen info in theory
* **But in typical coffee shop conditions**, readable data leakage from 2–3 meters at an angle is **limited and unreliable**
* For tools like Teams, Jira, Confluence → **generally not a major concern**

> The risk exists—but it’s not where most real-world compromises happen.

---

If you want, I can break this down quantitatively (pixel density vs distance vs font size) to show exactly when text becomes readable or not.

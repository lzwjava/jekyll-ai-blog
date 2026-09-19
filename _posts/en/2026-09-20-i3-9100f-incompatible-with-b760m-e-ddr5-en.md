---
audio: false
generated: true
image: false
lang: en
layout: post
title: i3-9100F Incompatible with B760M-E DDR5
translated: false
type: note
---

**Question:** Is the Intel Core i3-9100F compatible with the MSI PRO B760M-E DDR5 motherboard?

**Answer:**

❌ **No, the i3-9100F is NOT compatible** with this motherboard.

### ❌ Compatibility Check

| Feature | Detail |
|---|---|
| **Socket** | LGA1151 ❌ (board needs LGA1700) |
| **Generation** | 9th Gen (Coffee Lake) ❌ |
| **Chipset Support** | Requires Z390/B365/H310 ❌ |
| **Memory Type** | DDR4 only ❌ |

### 🔴 Why It Won't Work

- The i3-9100F uses an **LGA1151 socket**, which is physically **different and incompatible** with the LGA1700 socket on the B760M-E DDR5
- It is a **9th Gen** CPU — the B760 chipset only supports **12th, 13th, and 14th Gen** Intel processors
- It only supports **DDR4**, while this board is DDR5-only
- You **cannot force it to fit** — the pin layouts are completely different

### 💡 What You Should Get Instead

Stick with **12th, 13th, or 14th Gen LGA1700 CPUs**, such as:

| Budget | Recommended CPU |
|---|---|
| Low | i3-12100F |
| Mid | i5-12400F / i5-13400F |
| High | i5-13600K / i7-13700F |

---

**References:**
- [Intel Core i3-9100F Specifications](https://ark.intel.com/content/www/us/en/ark/products/190886/intel-core-i3-9100f-processor-6m-cache-up-to-4-20-ghz.html)
- [MSI PRO B760M-E DDR5 Specification](https://www.msi.com/Motherboard/PRO-B760M-E-DDR5/Specification)
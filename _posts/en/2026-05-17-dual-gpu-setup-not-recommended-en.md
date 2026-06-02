---
audio: false
generated: true
image: false
lang: en
layout: post
title: Dual GPU Setup Not Recommended
translated: false
type: note
---

**Question:** Can I add an AMD GPU to my JD.com PC build that already has an MSI RTX 4070 GPU?

**Answer:**

## Short Answer: Technically Yes, But It's Not Recommended for Gaming

AMD GPUs are fully compatible with Intel CPUs. Both AMD and Intel comply with universal industry standards like PCIe, so there are no cross-brand restrictions at the hardware level. However, your specific situation involves adding a *second* GPU to a system that already has an RTX 4070, which is a different matter entirely.

---

## 1. CPU × AMD GPU Compatibility — Not an Issue

Compatibility between an AMD GPU and an Intel CPU is generally straightforward, as the GPU and CPU operate largely independently within the system architecture. The critical factor is the motherboard's chipset and the available PCIe slots, which facilitate communication between the GPU and CPU.

So pairing an Intel i9-13900KF with an AMD GPU is perfectly fine.

---

## 2. Can Your Motherboard (MSI MAG B760M Mortar WiFi) Support a Second GPU?

This is where the real limitation lies. The MSI MAG B760M Mortar WiFi is a **Micro-ATX (mATX)** board. It features a PCIe 5.0 slot, but mATX boards typically only have **one full-length PCIe x16 slot**. A second GPU would need to fit into a smaller PCIe x1 or x4 slot, which would severely limit bandwidth and is not physically suitable for a full-size discrete GPU.

In short: **your motherboard physically cannot host two full-size GPUs side by side in a meaningful way.**

---

## 3. Dual GPU with Mixed Brands (RTX 4070 + AMD) — Not Supported for Gaming

Even if you had the physical slots, mixing GPU brands doesn't work for combined gaming performance. Where you run into issues is using a multi-GPU setup with different cards. Unless you're running a Dual Graphics setup with compatible APUs and AMD GPUs, you have to use identical cards for a multi-GPU setup.

Modern games and rendering engines don't support cross-brand GPU collaboration. NVIDIA's NVLink/SLI and AMD's CrossFire only work within the same brand and often the same GPU model series — and even those technologies are largely **deprecated** in modern gaming.

---

## 4. What About AMD Smart Access Memory (SAM)?

If you were to replace the RTX 4070 with an AMD GPU, note that AMD Smart Access Memory only works if you have an AMD CPU and an AMD GPU. Since you have an Intel CPU, you would not benefit from SAM. This is a minor loss (~5–15% in some games), but not a dealbreaker.

---

## 5. Power Supply Concern

Your build uses a **Corsair CX650F 750W PSU**. The RTX 4070 alone draws around 200W under load, and the i9-13900KF can draw up to 250W. Adding a second GPU (even a mid-range AMD card at 150–200W) would push total system draw well above 600W, approaching or exceeding your PSU's safe operating range. **This would be risky.**

---

## Summary Table

| Consideration | Verdict |
|---|---|
| Intel CPU + AMD GPU compatibility | ✅ Fully compatible |
| B760M Mortar WiFi supports 2 full GPUs | ❌ Only 1 PCIe x16 slot |
| RTX 4070 + AMD GPU for gaming | ❌ Not supported (different brands) |
| AMD SAM benefit with Intel CPU | ❌ Not available |
| 750W PSU for dual GPU | ⚠️ Likely insufficient |
| Case (Aigo Mini) fits two GPUs | ❌ Mini cases rarely support 2 GPUs |

---

## Recommendation

Your build with the **RTX 4070 alone is excellent** for gaming at 1440p and even 4K. Adding an AMD GPU to this specific build is not practical due to motherboard, case, power, and software limitations. If you want more GPU power in the future, the best path is to **replace** the RTX 4070 with a higher-tier GPU rather than adding a second card.

**References:**

- [Can You Use A AMD GPU With An Intel CPU – techygpu.com](https://www.techygpu.com/2024/09/26/can-you-use-a-amd-gpu-with-an-intel-cpu/)
- [Can You Use An AMD GPU With An Intel CPU? – cgdirector.com](https://www.cgdirector.com/use-amd-gpu-with-intel-cpu/)
- [AMD GPU with Intel CPU Compatibility – computerknown.com](https://computerknown.com/can-you-use-a-amd-gpu-with-an-intel-cpu/)
- [MSI MAG B760M MORTAR WIFI – us.msi.com](https://us.msi.com/Motherboard/MAG-B760M-MORTAR-WIFI/)
- [PCPartPicker: Intel CPU with AMD GPU discussion](https://pcpartpicker.com/forums/topic/98670-i-can-use-a-intel-cpu-with-a-amd-gpu)

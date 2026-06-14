---
audio: false
generated: true
image: false
lang: en
layout: post
title: SoSIM Carrier Label for MMS
translated: false
type: note
---

**Question:** On a Google Pixel with eSIM, when using SoSIM, what does "SoSIM" mean in the context of MMS messages?**Answer:**

**SoSIM** is a Hong Kong-based eSIM provider/MVNO (Mobile Virtual Network Operator). SoSIM offers eSIM plans that activate in about 3 minutes by scanning a QR code, providing connectivity that's easy to switch without a physical card. Their contact domain is `sosimhk.com`, so it's a Hong Kong carrier product.

When you see **"SoSIM"** in the context of MMS on your Google Pixel, it means:

**Your active eSIM profile is from SoSIM (the carrier), and MMS is being routed through that line.**

On a dual-SIM Pixel (physical SIM + eSIM), the phone labels MMS/SMS by which SIM/carrier is handling it. If SoSIM is your active eSIM profile, the messaging app will display "SoSIM" as the line identifier for that MMS — similar to how it might show "T-Mobile" or "Verizon" for a US carrier.

### Practical things to check if MMS isn't working on SoSIM eSIM:

1. **APN settings** — SoSIM may require specific APN config for MMS. Check their website or contact support for the correct APN.
2. **Mobile data must be on** — MMS does not work over Wi-Fi; it needs cellular data active on the SoSIM line specifically.
3. **Default SIM for data** — Go to `Settings → Network & Internet → SIMs` and make sure SoSIM is set as the data SIM (or at least has data enabled) when sending MMS.
4. **Carrier Services app** — Keep it updated; it handles a lot of the SIM/MMS plumbing on Pixel.

In short: SoSIM = the carrier name for your eSIM profile, appearing as a label in MMS to tell you which line is being used.

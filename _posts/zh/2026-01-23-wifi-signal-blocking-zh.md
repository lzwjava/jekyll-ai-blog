---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 为什么 WiFi 信号会被阻挡
translated: true
type: note
---

Question: Why do WiFi signals (radio waves) get significantly weakened or blocked by physical obstacles?

Answer:

WiFi signals are **radio waves** (electromagnetic waves) primarily at **2.4 GHz** or **5 GHz**. When these waves encounter physical obstacles, their strength is reduced through several key physical mechanisms. Here's why this happens:

### Main Reasons for Weakening / Blocking

1. **Absorption** (Dielectric loss / energy dissipation)
   材料吸收 electromagnetic energy 并将其转化为热能。
   - 含有极性分子的材料（尤其是含水材料，如 concrete、brick、wood、plaster 以及人体）吸收能量非常有效——特别是在 2.4 GHz 频率下，该频率接近水分子的共振频率。
   - 高密度 dielectrics 会导致电场使分子/电子产生振荡，从而以热振动的形式损失能量。

2. **Reflection**
   波的大部分在表面反射，而不是穿透。
   - **Metals** 是效果最明显的：它们是极佳的 conductors → 几乎反射所有能量（就像 radio waves 的镜子一样）。
   - 这就是为什么金属门、箔纸隔热层、文件柜或 reinforced concrete（带有钢筋）几乎会完全阻挡 WiFi。

3. **Scattering**
   波击中微小的凹凸不平、颗粒或粗糙表面，并被重新定向到多个方向。
   - 常见于多孔材料、纹理墙面、家具或植物叶片。
   - 这会减少到达接收器的直接（有效）信号。

4. **Refraction & Diffraction** (less dominant indoors)
   - 当波从空气进入不同材料时会发生折射（速度改变）。
   - Diffraction 允许波在边缘处产生一定的弯曲，但这种效应在 WiFi 频率下较弱，无法通过绕射来补偿厚重障碍物带来的损失。

### Why Different Materials Behave Differently

| Material | Typical Attenuation (at ~5 GHz) | Main Reason | WiFi Impact |
| :--- | :--- | :--- | :--- |
| Drywall / Wood | Low (~3–10 dB) | Mild absorption | Minor weakening |
| Brick | Medium (~15–30 dB) | Absorption + some scattering | Noticeable drop |
| Concrete (plain) | High (~20–50 dB) | Strong absorption | Serious weakening |
| Reinforced concrete | Very high (~40–60+ dB) | Absorption + strong reflection (rebar) | Often blocks almost completely |
| Metal (door, foil) | Extreme (~50–100+ dB) | Almost total reflection | Effectively blocked |
| Glass (normal) | Low | Low absorption | Minor |
| Water / human body | High | Strong absorption (water) | Significant loss |

- 每减少 ~3 dB = 信号功率减半。
- 减少 10 dB = 信号功率降至 1/10。
- 减少 20 dB = 信号功率降至 1/100 → 通常会降至可用水平以下。

### Summary – Why obstacles matter so much for WiFi

与较旧的 radio 技术（如 FM 约为 3 m）相比，WiFi 使用相对较高的频率（short wavelengths：2.4 GHz 约 12 cm，5 GHz 约 6 cm）。更短的波长与日常物品的相互作用更强 → 产生更多的 absorption、reflection 和 scattering。较低频率的信号（如某些 cellular 频段或 AM radio）穿透力更好，因为它们较长的波长使材料看起来不那么致密。

这纯粹是 electromagnetic wave propagation 的物理特性——在当前的 WiFi 频率下，无法绕过这些基础物理效应。

References:

- [Which Building Materials Can Block Wi-Fi Signals?](https://eyenetworks.no/en/wifi-signal-loss-by-material)
- [Materials that Block WiFi Signal](https://www.signalboosters.com/blog/materials-that-block-wifi-signals)
- [Wi-Fi signal attenuation coefficients when passing through different materials](https://help.keenetic.com/hc/en-us/articles/213968869-Wi-Fi-signal-attenuation-coefficients-when-passing-through-different-materials)
- [RF effects in Real World – Absorption, Reflection, Scattering](https://www.networkacademy.io/ccna/wireless/radio-signals-in-real-world-environments)

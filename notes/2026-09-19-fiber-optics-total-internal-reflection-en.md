---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Fiber Optics: Total Internal Reflection"
translated: false
type: note
---

Question: How does optical fiber work? What property of light does it use?

Answer: Optical fiber mainly exploits **total internal reflection** to guide light through a very thin glass/plastic fiber.

![Image](https://images.openai.com/static-rsc-4/f51fuex8FuD4qyclLZ_BnLQU2c6OFdKZGk92OfafDXeOtAnP7zkhm5penu23805uXwk2HbSLfRUXQhbtdE0NW2HvmkwuXM70IZ-rlB4piOMzR5N9oVF2WblcW6QmU52XNiDH0vjNvYxh5dZ2EXO8oar84E8YTC-Av5qvVuujjUEbikbcq2CZj-IJjpcfPz62?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/0S3l63Q-gF9DnsDBxB2bw7LrhzrgiZZGb5yjx6wQsDcl1mlAIn--0heyFbozXMMGyh-IOBPnNLwoAgiCYyeHaedK9PxoAx6XW_bnS3rOeKANaHA2wlTnOHerqFpAFdiSY9M3d-um-8VTw9s5wqFsvEuLxcgwc3dyCRpHnzKr2s7Ul3jVN_TEwnuYwRJY-Ncm?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/J5a13Mv4V2mIqTcshqZpFGPlhNoy7--IGhIrm1B4GlKr6fvUvIo-qehLK7LKWvyiGrv18TRxkYfGuXkmkepCYBAhXy-2TvJwsfoM8ZOjstptUCCpkUMMERFCyF-e7p1G5iixSMxIwRsre7QyK4i9XIC7pwfpaTOPWn2uCen1ZX5oxzv8tFn72RyNvNetT2G7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Hj8_y7IVtNtjOSvjR7obHq4wBzL1gF8Iqbp_v6fpnj5IIeeVnUx020vSz0lxEt7SlXVEKXOG5DNiudEZ00oDcqeuCCX8OD7h_Ohfz_SEBq82wdrzVKScAenmHzaih-BK5f1-rd9oLKtSMB41-wcGxNsbU7OZXHyJmX_sF9Ld0TSjFvHGVxUNLOAQzBVjHi5V?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/FVUq0zZExp6kYTu2oTkVDZAyeJWn_M0PtBxdVseTp-twA0SHh7qJlZJmODz1j1iCq_dsN9jAu_C1SV4k5JAeb_p4iYcS4PlgGEnWKgP5HPD-GmczW5D2shC3UuOX14R8rwdvJ7GUYV1M5q1TtS7-mJjnHdcn3k_1T6WBxbXdNxSct2kwRDy6Th5QUsv93Lsh?purpose=fullsize)

The key idea is:

```text
        cladding (lower refractive index)
   ┌─────────────────────────────────────┐
   │  ↘       ↗       ↘       ↗         │
   │    ↘   ↗           ↘   ↗           │
   │      ↘               ↘             │
   │        ↘             ↗             │
   │          ↘         ↗               │
   └─────────────────────────────────────┘
             ↑
           core
       higher refractive index
```

### 1. It uses the **electric field of light** to carry information

A transmitter converts electrical data:

```text
10110010...
    ↓
laser / LED
    ↓
light pulses
```

For example:

```text
1 → light ON
0 → light OFF
```

More sophisticated systems encode information using several properties of the optical wave, including:

* **Intensity/amplitude**
* **Phase**
* **Frequency / wavelength**
* **Polarization**

Modern coherent fiber communication can encode multiple bits per symbol using combinations of amplitude and phase.

### 2. Why doesn't the light escape?

The fiber has two layers:

```text
        Cladding
   ┌─────────────────┐
   │    ┌───────┐    │
   │    │ CORE  │    │
   │    │       │    │
   │    └───────┘    │
   └─────────────────┘
```

The **core has a higher refractive index** than the cladding:

```text
n_core > n_cladding
```

When light inside the core hits the core/cladding boundary at a sufficiently large angle, it undergoes **total internal reflection**.

The critical angle is

$$
\theta_c = \sin^{-1}\left(\frac{n_{cladding}}{n_{core}}\right)
$$

so the light stays confined to the core.

### 3. The really interesting part: fiber is basically a waveguide

It is tempting to imagine:

```text
laser → bouncing photon → bouncing photon → receiver
```

but physically, the electromagnetic field propagates as **guided optical modes**.

So a better mental model is:

```text
electrical bits
      ↓
electro-optical modulation
      ↓
electromagnetic wave
      ↓
fiber waveguide
      ↓
photodetector
      ↓
electrical bits
```

At the receiving end, a photodiode converts the optical signal back into an electrical signal.

### 4. Why fiber can carry enormous bandwidth

Visible light has frequencies around hundreds of **THz**.

Telecommunications commonly uses wavelengths around:

```text
850 nm
1310 nm
1550 nm
```

1550 nm corresponds to roughly

$$
f = \frac{c}{\lambda}
  \approx \frac{3\times10^8}{1.55\times10^{-6}}
  \approx 193\text{ THz}
$$

That's an enormous electromagnetic bandwidth compared with ordinary electrical cables.

And modern systems don't simply use ON/OFF. They can use **WDM (wavelength-division multiplexing)**:

```text
1550.1 nm ──┐
1550.3 nm ──┤
1550.5 nm ──┤──→ same fiber
1550.7 nm ──┤
1550.9 nm ──┘
```

Each wavelength can carry an independent high-speed data stream.

So the shortest answer is:

> **Optical fiber uses electromagnetic light waves, and the fiber's refractive-index structure guides those waves through the core. Information is encoded by modulating properties such as intensity, phase, frequency, and polarization.**

I can next walk through **one Ethernet packet going from a CPU → NIC → optical transceiver → fiber → receiving NIC**, including exactly where the electrical signal becomes photons and back.

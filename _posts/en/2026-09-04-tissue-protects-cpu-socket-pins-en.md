---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tissue Protects CPU Socket Pins
translated: false
type: note
---

Question: Why do Xianyu motherboard sellers often put tissue/paper over the CPU socket?

Answer: Usually it is **to protect the LGA CPU socket pins during storage and shipping**.

On Intel LGA motherboards, the socket contains hundreds/thousands of extremely thin spring contacts. They are very easy to bend if something touches them.

Sellers may put tissue/paper over the socket because:

* **Protects the pins from physical contact** — especially if the CPU is removed.
* **Prevents dust and debris** from getting into the socket.
* **Prevents the socket from being scratched/damaged by packaging.**
* When shipping a used motherboard, the seller may not have the original **plastic LGA socket cover**, so tissue is a cheap substitute.

However, **tissue is not ideal**. The correct protection is the original **CPU socket protective cap**:

![Image](https://images.openai.com/static-rsc-4/UfyIQmzD0MrhKGDWjt5OpEjf7qeu2mX030i0RdIGf2YlWJIVGn6fVYo-zqOfWoSbroFQMTOVQOno9wdWUtHbU3yHIKnp-km9OAnqwZVn_LyL25bPw_xc5a6M2T3cfmST6fu4_tY8XReRjf2KW5-BoRpkP43EZP2LIcDn1XCA2ASQAE4uyhzNt9QMgh7cZTGc?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Q8YOXKzGmFMgq5I2mk-_XN6_ZZZIDIddb2W7os31y4DmF9pVUXpngdSdzfU9t2qcRBvEnETKwgVb66yURIW9--oM6lTR4Prn1EdPrX02boumIQ5yzeGQpZrSEYZd0goDKSN_giECxMh7405ulZiLfEd55G4eV12Xf91ILaYaIuKCxkOPlmZR7ec0B59CU_En?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/Ok_eSX9mbsb0s3Teu9arMNXFG5LYRT0CzfrTkVdsJcgX9ZhbcK2JoYQ1sMEZ4ssV_tuXv_TDB2sJajoW4S3_nO6kO4s05W7VrOFlGi4zyKSoUm5TwLyLxE5EJQVENE9KPrxkE5j8LsNNkS_gfpQM4156Chgvuo021blcuWgAccvZlMV3lwO_d_1YOwbErZuZ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/jUAyVZ8eO8WCTniIci4UL6h83wKgQV8i6kURC7TmzcC5ZwP4G_ImjVCXz0RHGrS5M1wzDW_3Ux3b2TCu4VJxyJ0oFKYv9EP4fJ7SKNjVenQpcn40tmNf7UgcquYO7XhNeNIcEDD6e_od68m0n2bsmca_H6_5HXanweF_zAno1nuXOlJGW8mi57EKh39syZwJ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/WnI3xZZs-PPnL-3Q7X8aIpPfqfHkY8XRXduwQG6XF1pOpEWQQHVaXrcNbjUQP83VDDbI3E-rGzpJMV_zZk7_ct7XTPQP3dlpvsKcCo1SqWMZ0DeXJjhdfvIUMucgtapO_H9H53CclZ2pkJJBNYpEOWqalWuNv6Zg4ffkR0_Q8tSrP7VIuZX5Yalnfg_ai01_?purpose=fullsize)

### Why this matters when buying a used motherboard

If you receive a motherboard with tissue over the socket, **don't immediately pull the tissue sideways**.

The dangerous part is the pins:

```text
        CPU socket
   ┌─────────────────┐
   │  \ \ \ \ \ \ \  │
   │   \ \ \ \ \ \   │  ← extremely fragile pins
   │  \ \ \ \ \ \ \  │
   └─────────────────┘
          ↑
       tissue
```

If the tissue has fibers caught in the pins, pulling it can bend them.

Instead:

1. Remove the motherboard from the packaging.
2. Hold it horizontally.
3. Inspect the socket under strong light/magnification.
4. If tissue is sitting loosely on top, lift it **straight up** very gently.
5. Check whether any socket pins are bent.

And importantly, **a motherboard with the CPU installed doesn't need tissue over the socket**—the CPU itself protects the contacts. The tissue is mainly seen when the seller ships a board **without a CPU and without the original socket cover**.

If you're buying these cheap Xianyu boards specifically for your GPU-testing setup, I'd pay particular attention to **bent LGA pins, missing socket cover, corrosion, and whether the board actually POSTs**, rather than treating the tissue itself as suspicious.

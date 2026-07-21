---
audio: false
generated: true
image: false
lang: en
layout: post
title: Disable Secure Boot for NVIDIA
translated: false
type: note
---

Question: Which should I choose: sign the NVIDIA kernel module or disable Secure Boot?

Answer:

I would choose **B: disable Secure Boot**, unless you specifically need Secure Boot for your security model or enterprise policy.

Here's the tradeoff:

| Option                        | Pros                                                                               | Cons                                                                                                 |
| ----------------------------- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **A. Sign the NVIDIA module** | Keep Secure Boot enabled, officially supported                                     | More setup (MOK key generation, enrollment, module signing), may need repeating after driver changes |
| **B. Disable Secure Boot**    | Takes 1–2 minutes, no future signing headaches, what most Linux ML workstations do | Lose Secure Boot verification during boot                                                            |

For an AI workstation running CUDA, PyTorch, vLLM, etc., **disabling Secure Boot is the common path**.

The boot chain becomes:

```
BIOS
   ↓
UEFI
   ↓
Secure Boot?
   ├── ON
   │      ↓
   │ verify kernel
   │ verify NVIDIA module signature
   │        ↓
   │ unsigned module → rejected
   │
   └── OFF
          ↓
      load nvidia.ko
          ↓
      /dev/nvidia*
          ↓
      nvidia-smi works
```

Your diagnosis already tells the story:

```
Driver installed ✔
DKMS built ✔
Kernel module exists ✔
nvidia-smi ✘
Secure Boot enabled
```

That almost always means the module is present but the kernel refuses to load it because it isn't signed.

### Disable Secure Boot

1. Reboot.
2. Enter UEFI/BIOS (usually `Del`, `F2`, `F10`, or `Esc`).
3. Find **Secure Boot**.
4. Set it to **Disabled**.
5. Save and reboot.

Then verify:

```bash
mokutil --sb-state
```

Expected:

```
SecureBoot disabled
```

Load/check the module:

```bash
sudo modprobe nvidia
nvidia-smi
```

or simply reboot once and run:

```bash
nvidia-smi
```

You should see something like:

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 580.167.08 |
| GPU 0: GeForce RTX 4070 |
+-----------------------------------------------------------------------------+
```

### When should you keep Secure Boot enabled?

Choose **module signing** if:

* your organization requires Secure Boot,
* you're dual-booting under strict security policies,
* you're building a production appliance,
* or you simply want the additional boot-chain integrity.

For a personal Linux machine dedicated to AI development, most people disable Secure Boot because it avoids recurring maintenance after driver updates.

So, for your RTX 4070 development machine, I'd pick **Option B (disable Secure Boot)**.
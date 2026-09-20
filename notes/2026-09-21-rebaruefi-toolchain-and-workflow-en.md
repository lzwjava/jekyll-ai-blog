---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReBarUEFI Toolchain and Workflow
translated: false
type: note
---

We now have both pieces of the toolchain built:

```
Build/ReBarUEFI/RELEASE_GCC/X64/ReBarDxe.ffs   ← the DXE driver to inject into the BIOS
ReBarUEFI/ReBarState/build/ReBarState           ← the config tool (writes the NVRAM variable)
```

## What ReBarUEFI actually does (per the README)

`ReBarDxe.ffs` is a **UEFI DXE driver**. When placed in the firmware's DXE volume it runs on every boot and:

1. Hooks `PreprocessController` of `PciHostBridgeResourceAllocationProtocol`
2. Checks if the GPU advertises Resizable BAR capability
3. Sets the BAR size from an NVRAM variable called `ReBarState` (GUID `A3C5B77A-C88F-4A93-BF1C-4A92A32C65CE`)
4. Then `PciBus` enumerates PCI later and allocates the new (larger) BAR accordingly

So the full path is: **inject the driver → flash modified BIOS → enable 4G decoding + disable CSM → set the BAR size via ReBarState → reboot**.

## Step-by-step workflow (from README + wiki)

**1. Get your motherboard's BIOS image** — latest from the manufacturer site (`.cap`/`.rom`/`.bin`).

**2. Insert `ReBarDxe.ffs` into the DXE volume** using [UEFITool 0.28 (non-NE)](https://github.com/LongSoft/UEFITool/releases/tag/0.28.0):

- Open the BIOS, `File → Search`, header-only GUID search for `3C1DE39F-D207-408A-AACC-731CFB7F1DD7` (the **PciBus** module) to locate the correct volume
- Scroll to the last module in that volume → right-click → **Insert after** → pick `ReBarDxe.ffs`
- Save the image
- (MMTool is the fallback if UEFITool doesn't work)

**3. Apply UEFIPatch patches** — most consumer boards have 64-bit BAR bugs that need fixing:

- Download [UEFIPatch](https://github.com/LongSoft/UEFITool/releases/tag/0.28.0)
- Put `UEFIPatch/patches.txt` (from the repo) + your BIOS in one folder and run `UEFIPatch <biosfile>`
- This removes the `<4GB/<16GB/<64GB` BAR limits, expands MMIO space, prevents 64-bit BARs being downgraded, etc. Output is `<biosfile>.patched`
- Extra platform-specific patches to append if needed: `HswAbove4G.txt` (Haswell/Broadwell 4G decoding, *required* there), `IvyUSB3.txt`/`HswUSB3.txt`/`BdwUSB3.txt` (USB3-in-BIOS fixes), and the X79 fix (uncomment in `patches.txt`)
- **Watch for the pad-file corruption bug** (mostly ASUS) — compare pad files in UEFITool before flashing

**4. Flash the modified BIOS** with your board's flash tool / programmer. ⚠️ This is the risky part — a bad flash can brick the board.

**5. In BIOS setup:** enable **Above 4G Decoding**, disable **CSM**.

**6. Boot the OS and run ReBarState as root:**

```bash
sudo ./ReBarUEFI/ReBarState/build/ReBarState
# then type: 32   (unlimited — works in most cases)
```

`32` = unlimited; smaller values set `2^x` MB (e.g. `10` = 1 GB, `11` = 2 GB). It's recommended to try a small value above 256 MB first if you're unsure the BIOS handles large BARs. Then **reboot**.

**7. Verify** with GPU-Z (Windows) / `nvidia-smi` / amdgpu (`dmesg | grep -i bar`).

## Important notes

- **Secure Boot can usually stay on** — most firmwares accept unsigned/patched modules.
- If the system won't POST after setting a bad BAR size: **clear CMOS** (pull the battery in some cases) — ReBAR gets disabled.
- If you don't want to mod the BIOS at all: on **Linux** with 4G decoding on, recent kernels + `pci=realloc` will resize GPU BARs automatically — but **Windows requires the BIOS mod**.
- NVIDIA Turing (16/20 series) needs [NvStrapsReBar](https://github.com/terminatorul/NvStrapsReBar) instead of `ReBarDxe.ffs`.

Want me to also fetch the DSDT-patching wiki page, or help you inspect a specific motherboard BIOS image if you have one?

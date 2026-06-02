---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5.2
title: Preinstall Disk Partitioning Guide
translated: false
type: note
---

Question: How can I create or modify disk partitions on an Ubuntu system **before** running the installer?

Answer:

Since you are already running **Ubuntu**, you can fully prepare the disk **before launching the installer**. This is actually the cleanest and most reliable approach. Below are **three correct methods**, from simplest to most controlled.

---

## Method 1: Use **GParted** (Recommended, Visual & Safe)

### Step 1: Install GParted (if not already installed)

```bash
sudo apt update
sudo apt install gparted
```

### Step 2: Launch GParted

```bash
sudo gparted
```

### Step 3: Select the correct disk

* Top-right dropdown → choose your main disk (usually `/dev/nvme0n1`)
* **Be very careful** not to pick the USB installer

### Step 4: Create a clean GPT layout (UEFI systems)

1. **Device → Create Partition Table**
2. Select:

   * Partition table type: **GPT**
3. Apply

### Step 5: Create partitions for Windows (example)

Create these in order:

| Partition            | Size       | File system | Purpose          |
| -------------------- | ---------- | ----------- | ---------------- |
| EFI System Partition | 300–500 MB | FAT32       | UEFI boot        |
| Microsoft Reserved   | 16 MB      | unformatted | Windows internal |
| Windows (C:)         | Remaining  | NTFS        | Windows install  |

**Important**

* Set **EFI partition flags**: `esp`, `boot`

### Step 6: Apply changes and close GParted

Now start the Windows installer — it will **reuse** these partitions.

---

## Method 2: Use `parted` / `diskpart-style` CLI (Precise)

Best if you want full control and no GUI.

### Step 1: Identify disk

```bash
lsblk
```

Look for something like:

```text
nvme0n1   476G
```

### Step 2: Enter parted

```bash
sudo parted /dev/nvme0n1
```

### Step 3: Create GPT

```text
mklabel gpt
```

### Step 4: Create EFI partition

```text
mkpart EFI fat32 1MiB 501MiB
set 1 esp on
```

### Step 5: Create Windows partition

```text
mkpart Windows ntfs 501MiB 100%
```

### Step 6: Exit

```text
quit
```

### Step 7: Format partitions

```bash
sudo mkfs.fat -F32 /dev/nvme0n1p1
sudo mkfs.ntfs -f /dev/nvme0n1p2
```

---

## Method 3: Let Ubuntu Installer Prepare the Disk (Fastest)

If you don’t care about fine control:

1. Start Ubuntu installer
2. Choose **Something else**
3. Select the disk
4. Create:

   * EFI partition (FAT32, mount `/boot/efi`)
   * Root `/` (ext4) or leave free space for Windows
5. Apply

Then later Windows installer can take remaining free space.

---

## Important Notes for Dual-Boot / Windows Install

* **Always use GPT + UEFI**
* **Disable Fast Boot** in BIOS
* **Secure Boot** can stay ON for Ubuntu + Windows
* Windows prefers:

  * EFI at the **start of disk**
  * Unallocated space (best)

If your goal is **Windows-only**, the cleanest is:

```bash
sudo parted /dev/nvme0n1 mklabel gpt
```

…and leave the disk **empty**. Windows installer will create everything.

---

## Recommendation for Your Case (Lenovo + Windows)

Since your BIOS is already **AHCI**:

**Best option**

1. From Ubuntu:

   ```bash
   sudo parted /dev/nvme0n1 mklabel gpt
   ```

2. Shut down
3. Boot Windows USB
4. Select **Unallocated Space**
5. Install

Zero drivers. Zero issues.

---

If you want, tell me:

* Windows only or dual-boot?
* NVMe disk size
* Ubuntu version

I can give you an **exact partition layout** tailored to your setup.

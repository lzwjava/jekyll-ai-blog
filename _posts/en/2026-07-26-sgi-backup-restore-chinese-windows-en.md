---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGI Backup Restore Chinese Windows
translated: false
type: note
---

Question: **What is the "SGI" backup/restore software used in some Chinese Windows installations?**

Answer:

You are probably referring to **SGI Image / SGI Backup and Restore** software that appears in some Chinese Windows installation or recovery environments. In practice, people often mean one of these OEM/PE tools:

### 1. SGI (系统备份还原) in Chinese WinPE

Many Chinese Windows PE systems bundle a tool named **SGI备份还原**. It is usually a **Ghost-like disk imaging tool**:

* Backup Windows partition → create image file
* Restore image → deploy Windows quickly
* Usually works with:

  * `.gho` (Ghost image)
  * `.wim`
  * `.sg` / proprietary formats depending on version

Typical workflow:

```
Boot WinPE USB
    |
    v
SGI Backup Restore
    |
    +--> Backup C: -> image file on D:/external disk
    |
    +--> Restore image -> C:
```

It is popular in China because technicians can clone Windows installations quickly.

---

### 2. It is not related to Silicon Graphics (SGI)

The name is confusing. It is **not**:

* Silicon Graphics workstation software
* SGI IRIX
* NVIDIA/graphics related

It is just a Chinese Windows deployment utility.

---

### 3. Similar tools you may see in Chinese Windows installers

| Tool                  | Usage                                |
| --------------------- | ------------------------------------ |
| **Ghost32 / Ghost64** | Classic Norton Ghost cloning         |
| **SGI备份还原**           | Modern WinPE imaging tool            |
| **CGI备份还原**           | Another common Chinese PE clone tool |
| **DISM++**            | WIM image management                 |
| **微PE工具箱**            | WinPE environment                    |
| **老毛桃 / 大白菜**         | PE boot systems                      |

---

### 4. For modern Windows 11 (UEFI + GPT + NVMe)

I would avoid old Ghost-style restore if possible.

Better:

```bash
# Capture
dism /capture-image \
 /imagefile:D:\install.wim \
 /capturedir:C:\ \
 /name:"Windows11"

# Restore
dism /apply-image \
 /imagefile:D:\install.wim \
 /index:1 \
 /applydir:C:\
```

or use:

* Microsoft `DISM`
* `wbAdmin`
* Clonezilla
* Macrium Reflect

because Windows 11 systems often have:

```
EFI System Partition
MSR partition
Windows partition
Recovery partition
```

Ghost/old SGI restores sometimes break boot entries:

```
BCD missing
EFI boot failed
0xc000000e
```

---

For your **Lenovo Xiaoxin 14 Windows 11 installation case**, if you are seeing SGI in a Chinese PE USB, it is likely just the PE technician tool. It can restore a prepared Windows image, but it does not solve the original install problem (VMD/RST, partition mode, drivers, etc.).

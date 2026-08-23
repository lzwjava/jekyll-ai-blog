---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVFlash指南：备份、列出、刷写VBIOS
translated: true
type: note
---

**问题：** 如何使用 NVFlash 对 RTX 显卡进行 ROM 备份、列出 GPU 以及刷写新的 VBIOS？

**回答：**

---

## ⚠️ 警告 — 请先阅读

刷写错误的 VBIOS **可能永久损坏你的 GPU**。务必先进行备份。刷写过程中切勿中断电源。在操作前请确认兼容性。

---

## 1. 下载 NVFlash

最新稳定版本为 **v5.867**（2025 年 2 月发布），支持 RTX 5000（Blackwell）至 GTX 1000 系列。仅从 **TechPowerUp.com**（可信官方镜像）下载——存在带恶意软件的伪造文件。无需安装，只需解压 `.exe` 文件并在命令提示符中运行即可。

压缩包包含 `nvflash.exe`（32 位）和 `nvflash64.exe`（64 位）。现代系统请使用 64 位版本。

解压至 `C:\nvflash\` 以便快速访问。

---

## 2. 设置

1. 以 **管理员身份打开命令提示符**（搜索 `cmd` → 右键 → *以管理员身份运行*）
2. 导航至文件夹：

   ```
   cd C:\nvflash
   ```

---

## 3. 关键命令

### 列出所有 GPU

```
nvflash --list
```

列出系统中所有 NVIDIA GPU，显示其索引号、设备 ID、子系统厂商 ID 和 BIOS 版本。

### 显示 GPU 信息 / BIOS 版本（无修改）

```
nvflash --version
nvflash -v
```

### 显示指定适配器的详细信息

```
nvflash -i 0
```

*（将 `0` 替换为 `--list` 显示的索引号）*

---

## 4. 备份当前 VBIOS（请先执行此步骤！）

```
nvflash --save backup.rom
```

保存特定 GPU（例如索引 0）的 ROM：

```
nvflash -i0 --save gpu0.rom
```

请清晰命名文件——例如 `RTX3070-GamingX-original.rom`——包含显卡型号。将副本保存在本地、USB 驱动器和云存储中。同时将与 ROM 文件一同使用的 NVFlash 版本也保存一份。

通过 **GPU-Z** 打开备份文件进行验证（点击 *保存 BIOS* → 对比保存的文件与 GPU-Z 从显卡读取的内容）。

---

## 5. 刷写新 VBIOS

### 标准刷写（同型号/同厂商）

```
nvflash -6 newbios.rom
```

`-6` 标志允许覆盖 PCI 子系统 ID 不匹配的情况。若存在差异，NVFlash 会要求确认——按 `Y`（非美式键盘则按 `Z`）。

### 强制刷写（跳过确认）

```
nvflash -f -6 newbios.rom
```

### 按索引刷写指定 GPU（多 GPU 系统）

```
nvflash --index=0 bios.rom
```

请先使用 `--list` 找到多 GPU 设备中每张显卡的正确索引。

### 若写保护阻止刷写

```
nvflash --protectoff newbios.rom
```

此命令在当前会话中临时禁用写保护。冷重启后保护将重新启用。

---

## 6. 恢复原始 VBIOS

使用与刷写相同的命令，配合备份文件：

```
nvflash -6 original.rom
```

在将显卡送修前，这是标准恢复流程。

---

## 7. 刷写后验证

重启后，GPU-Z 应显示新的 BIOS 版本字符串，系统应正常自检（POST），GPU 驱动应无错误加载。若版本字符串未变，则刷写未生效——请重试。若无显示输出，请遵循恢复流程。

---

## 8. 关于 RTX 20+ 签名 BIOS 的重要说明

自 Turing（RTX 20）系列起，每款 NVIDIA VBIOS 均经过**加密签名**——显卡仅接受签名镜像。将某厂商的原始 BIOS 刷写到具有相同板卡设计的另一厂商显卡上通常可行，`-6` 可用于处理子系统 ID 不匹配。

修改过的 BIOS（如编辑功耗表、更改设备 ID）在 Blackwell（RTX 50）系列上会被签名验证阻止。

---

## 快速命令速查表

| 任务 | 命令 |
| --- | --- |
| 列出所有 GPU | `nvflash --list` |
| 显示版本/信息 | `nvflash -v` |
| 备份 VBIOS | `nvflash --save backup.rom` |
| 备份指定 GPU | `nvflash -i0 --save gpu0.rom` |
| 刷写 VBIOS | `nvflash -6 newbios.rom` |
| 强制刷写 | `nvflash -f -6 newbios.rom` |
| 刷写指定 GPU | `nvflash --index=0 newbios.rom` |
| 禁用写保护 | `nvflash --protectoff newbios.rom` |
| 恢复备份 | `nvflash -6 original.rom` |

---

**参考：**

- [GPU BIOS Flash Guide 2026 (nvflash, commands, recovery)](https://www.mvktech.net/gpu-bios-flash-guide/)
- [nvflash Command Reference 2026](https://www.mvktech.net/nvflash-guide/)
- [NVflash: How to Flash a GPU BIOS (myminingrig.com)](https://myminingrig.com/how-to-flash-a-gpu-bios-with-nvflash/)
- [NVIDIA nvFlash v5.867 Overview](https://pcgamingtools.com/nvidia-nvflash-download/)
- [TechPowerUp NVFlash Download (official mirror)](https://www.techpowerup.com/download/nvidia-nvflash/)
- [Minerstat: NVIDIA VBIOS Flashing Guide](https://minerstat.com/help/nvidia-vbios-flashing)

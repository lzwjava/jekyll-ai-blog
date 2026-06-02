---
audio: false
generated: true
lang: zh
layout: post
title: 使用UF2文件刷写Pico
translated: true
type: note
---

要将 `RPI_PICO-20250415-v1.25.0.uf2` 文件刷入挂载在 `/media/lzw/RPI-RP2` 的树莓派 Pico，请使用以下命令：

```bash
cp ~/Downloads/RPI_PICO-20250415-v1.25.0.uf2 /media/lzw/RPI-RP2/
```

### 说明

- `cp`：复制文件命令
- `~/Downloads/RPI_PICO-20250415-v1.25.0.uf2`：Downloads 目录中 `.uf2` 文件的路径
- `/media/lzw/RPI-RP2/`：Pico 设备 `RPI-RP2` 驱动器的挂载点，如输出所示

### 执行命令后

- `.uf2` 文件将被复制到 Pico，设备将自动刷入固件
- 刷写完成后 `RPI-RP2` 驱动器会自动卸载（消失），表示操作成功
- 若驱动器重新出现，则刷写可能失败。请验证 `.uf2` 文件有效性或更换 USB 数据线/接口

如遇问题或需要进一步协助，请随时告知！

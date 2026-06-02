---
audio: false
generated: true
lang: en
layout: post
title: Flash Pico with UF2 File
translated: false
type: note
---

To flash the `RPI_PICO-20250415-v1.25.0.uf2` file to your Raspberry Pi Pico, which is mounted at `/media/lzw/RPI-RP2`, use the following command:

```bash
cp ~/Downloads/RPI_PICO-20250415-v1.25.0.uf2 /media/lzw/RPI-RP2/
```

### Explanation
- `cp`: Copies the file.
- `~/Downloads/RPI_PICO-20250415-v1.25.0.uf2`: The path to your `.uf2` file in the Downloads directory.
- `/media/lzw/RPI-RP2/`: The mount point of the Pico’s `RPI-RP2` drive, as shown in your output.

### After Running the Command
- The `.uf2` file will be copied to the Pico, and the device will automatically flash the firmware.
- The `RPI-RP2` drive will unmount (disappear) once the flashing is complete, indicating success.
- If the drive reappears, the flash may have failed. Verify the `.uf2` file is valid or try a different USB cable/port.

If you encounter issues or need further assistance, let me know!

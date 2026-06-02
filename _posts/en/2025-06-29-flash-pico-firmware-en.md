---
audio: false
generated: true
lang: en
layout: post
title: Flash Pico Firmware via UF2
translated: false
type: note
---

To flash firmware onto your Raspberry Pi Pico (or RP2040-based board) in BOOTSEL mode by copying a `.uf2` file to the `RPI-RP2` drive, follow these steps:

### Step-by-Step Guide

1. **Confirm the Device is in BOOTSEL Mode**:
   - Your device should appear as a USB drive named `RPI-RP2` when connected to your computer. This confirms it’s in BOOTSEL mode (as indicated by `Bus 001 Device 009: ID 2e8a:0003 Raspberry Pi RP2 Boot`).
   - If it’s not in BOOTSEL mode, unplug the device, hold the BOOTSEL button on the Pico, and plug it into your computer’s USB port while holding the button. Release the button after a few seconds.

2. **Obtain a Valid `.uf2` File**:
   - **MicroPython**: Download the latest MicroPython firmware for the Raspberry Pi Pico from the [official MicroPython website](https://micropython.org/download/rp2-pico/). Choose the `.uf2` file for the Pico or Pico W (e.g., `rp2-pico-latest.uf2`).
   - **CircuitPython**: Download the CircuitPython firmware from the [CircuitPython website](https://circuitpython.org/board/raspberry_pi_pico/) for the Pico or Pico W.
   - **Custom Program**: If you’ve written a program (e.g., in C/C++ using the Pico SDK), compile it to generate a `.uf2` file. For example, use the Pico SDK or Arduino IDE to build your project.
   - Save the `.uf2` file to an easily accessible location on your computer (e.g., Desktop or Downloads folder).

3. **Locate the RPI-RP2 Drive**:
   - On your computer, open the file explorer:
     - **Windows**: Look for `RPI-RP2` under “This PC” as a removable drive.
     - **macOS**: The drive should appear on the Desktop or in Finder under “Devices.”
     - **Linux**: Check under `/media` or `/mnt`, or use `lsblk` to list connected drives.
   - If the drive doesn’t appear, ensure the USB cable is data-capable (not power-only) and try a different USB port or cable.

4. **Copy the `.uf2` File to the RPI-RP2 Drive**:
   - Drag and drop the `.uf2` file onto the `RPI-RP2` drive, or copy and paste it using your file explorer.
   - Alternatively, use a terminal command (on Linux/macOS):

     ```bash
     cp /path/to/your/file.uf2 /media/your_username/RPI-RP2/
     ```

     Replace `/path/to/your/file.uf2` with the path to your `.uf2` file and adjust the mount point as needed.

5. **Wait for the Flash Process**:
   - Once the `.uf2` file is copied, the Raspberry Pi Pico automatically flashes the firmware. The `RPI-RP2` drive will disappear (unmount) as the device restarts, indicating the process is complete.
   - This typically takes a few seconds. Do not unplug the device during this time.

6. **Verify the Device**:
   - After flashing, the Pico should exit BOOTSEL mode and run the new firmware.
   - For MicroPython or CircuitPython, connect to the device using a terminal (e.g., PuTTY, screen, or Thonny IDE) via the USB serial port (e.g., `COM3` on Windows or `/dev/ttyACM0` on Linux/macOS). You should see a Python REPL prompt.
   - For custom programs, check the expected behavior (e.g., LED blinking, serial output, etc.).
   - If the `RPI-RP2` drive reappears, the flash may have failed. Try a different `.uf2` file or check for hardware issues (e.g., USB cable, flash chip).

### Troubleshooting

- **Drive Not Showing**: Ensure the Pico is in BOOTSEL mode and the USB cable supports data transfer. Try pressing BOOTSEL, then briefly pressing the RESET button (if available) while connected.
- **Copy Fails or Drive Reappears**: The `.uf2` file may be corrupted, or the flash memory might be faulty. Download a fresh `.uf2` file or test with a minimal one, like MicroPython’s. If it persists, use `picotool` to diagnose:

  ```bash
  picotool info
  ```

  Install `picotool` from the [Raspberry Pi Pico SDK](https://github.com/raspberrypi/picotool).
- **No Response After Flashing**: If using MicroPython/CircuitPython, ensure your IDE (e.g., Thonny) is set to the correct serial port. For custom programs, verify the code was compiled correctly.

### Example: Flashing MicroPython

1. Download the MicroPython `.uf2` file from [micropython.org](https://micropython.org/download/rp2-pico/).
2. Hold BOOTSEL, plug in the Pico, and release BOOTSEL.
3. Open your file explorer, find the `RPI-RP2` drive, and copy the `.uf2` file to it.
4. Wait for the drive to disappear.
5. Open Thonny IDE, select the Pico’s serial port, and start coding in MicroPython.

If you need help with a specific `.uf2` file, tool, or setup (e.g., installing `picotool` or using Thonny), let me know!

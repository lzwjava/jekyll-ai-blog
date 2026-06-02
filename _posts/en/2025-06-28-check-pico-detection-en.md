---
audio: false
generated: true
lang: en
layout: post
title: Checking Raspberry Pi Pico Detection on Ubuntu
translated: false
type: note
---

To check if your Raspberry Pi Pico is detected by Ubuntu after plugging it in, follow these steps:

1. **Check USB Devices**:
   - Open a terminal and run:
     ```bash
     lsusb
     ```
   - Look for an entry like `Raspberry Pi Pico` or a device with a vendor ID of `2E8A` (Raspberry Pi's vendor ID). For example:
     ```
     Bus XXX Device XXX: ID 2e8a:0003 Raspberry Pi Pico
     ```

2. **Check Serial Ports**:
   - If the Pico is in BOOTSEL mode (for flashing firmware) or running a MicroPython/Arduino program with serial output, check for a serial port:
     ```bash
     ls /dev/tty*
     ```
   - Look for a device like `/dev/ttyACM0` or `/dev/ttyUSB0`. The Pico typically appears as `/dev/ttyACM0` when running MicroPython.

3. **Check Disk Devices (BOOTSEL Mode)**:
   - If the Pico is in BOOTSEL mode (holding the BOOTSEL button while plugging in), it should appear as a mass storage device. Run:
     ```bash
     lsblk
     ```
   - Look for a device like `/dev/sdb` (or similar) with a mount point, often labeled `RPI-RP2`.

4. **Use `dmesg` for Kernel Logs**:
   - Run:
     ```bash
     dmesg | tail -n 20
     ```
   - Check for messages indicating the Pico was detected, such as:
     ```
     [1234.567890] usb 1-1: New USB device found, idVendor=2e8a, idProduct=0003
     [1234.567891] usb 1-1: Product: Pico
     [1234.567892] cdc_acm 1-1:1.0: ttyACM0: USB ACM device
     ```
   - This confirms the Pico is recognized and assigned a port (e.g., `ttyACM0`).

5. **Test with MicroPython (if installed)**:
   - If you’re using MicroPython, install a tool like `picocom` or `minicom`:
     ```bash
     sudo apt install picocom
     ```
   - Connect to the Pico’s serial port:
     ```bash
     picocom /dev/ttyACM0
     ```
   - If detected, you should see the MicroPython REPL prompt (>>>). Press `Ctrl+C` to exit.

**Notes**:
- Ensure the Pico is properly connected via a good USB cable (data, not just power).
- If in BOOTSEL mode, the Pico appears as a storage device, not a serial device.
- If not detected, try a different USB port, cable, or check if drivers (like `cdc_acm` for serial) are loaded:
  ```bash
  lsmod | grep cdc_acm
  ```

If you don’t see the Pico in any of these checks, let me know more details (e.g., mode of the Pico, what you’re trying to do), and I can help troubleshoot further!

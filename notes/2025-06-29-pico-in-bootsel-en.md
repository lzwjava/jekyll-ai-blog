---
audio: false
generated: true
lang: en
layout: post
title: Raspberry Pi Pico in BOOTSEL Mode
translated: false
type: note
---

The device listed as `Bus 001 Device 009: ID 2e8a:0003 Raspberry Pi RP2 Boot` is a Raspberry Pi Pico (or a similar RP2040-based board) in BOOTSEL mode. Here's a breakdown:

- **ID 2e8a:0003**: This is the USB Vendor ID (2e8a) and Product ID (0003) assigned to Raspberry Pi for the RP2040 microcontroller when it is in BOOTSEL mode.
- **Raspberry Pi RP2 Boot**: Indicates the device is a Raspberry Pi Pico (or another RP2040-based board, like the Pico W or a custom board) that has entered its bootloader mode. In this mode, the device appears as a USB mass storage device, allowing you to upload firmware (e.g., .uf2 files) by copying them to the drive.

### What is BOOTSEL Mode?
BOOTSEL mode is activated by holding the BOOTSEL button on the Raspberry Pi Pico while plugging it into a USB port or by resetting it while holding the button. This mode is used to flash new firmware or programs onto the RP2040 microcontroller. When in this mode, the Pico appears as a removable drive (named `RPI-RP2`) on your computer.

### Why is it showing up like this?
Your device is likely in BOOTSEL mode because:
1. You intentionally pressed the BOOTSEL button to update or flash firmware.
2. The device is not running a program and defaults to bootloader mode (e.g., after a failed flash or reset).
3. There might be an issue with the firmware or connections, causing it to stay in bootloader mode. For example, issues with the flash memory or improper flashing can cause the device to revert to this mode.[](https://forums.raspberrypi.com/viewtopic.php?p=2078375)

### What to do next?
- **If you want to flash firmware**: Copy a valid `.uf2` file (e.g., a MicroPython or CircuitPython firmware, or a compiled program) to the `RPI-RP2` drive. The device will automatically flash the firmware and restart, exiting BOOTSEL mode.[](https://forum.arduino.cc/t/solved-nano-rp2040-connect-does-not-accept-uf2/888152)
- **If it's stuck in BOOTSEL mode**: This could indicate a problem with the flash memory or firmware. Try:
  1. Re-flashing with a known working `.uf2` file, such as the MicroPython firmware from the official Raspberry Pi website.
  2. Checking the USB cable and port, as a faulty cable can cause issues.[](https://raspberrypi.stackexchange.com/questions/139506/raspberry-pi-pico-doesnt-create-tty-file)
  3. Using tools like `picotool` to verify the device status or reset it. For example, run `picotool info` to check the device’s state.[](https://forums.raspberrypi.com/viewtopic.php?p=2078375)
  4. If using a custom RP2040 board, ensure the flash chip is properly connected and configured, as issues with QSPI signals or flash ICs can prevent successful flashing.[](https://forums.raspberrypi.com/viewtopic.php?p=2078375)
- **If you want to exit BOOTSEL mode**: If valid firmware is already flashed, unplug the device, ensure the BOOTSEL button is not pressed, and plug it back in. The device should boot into its programmed mode (e.g., running a MicroPython script or C program).

### Additional Notes
- The RP2040 is the microcontroller used in the Raspberry Pi Pico, Pico W, and other boards. The `RP2 Boot` designation specifically refers to the bootloader mode of the RP2040 chip.[](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
- If you’re using a Raspberry Pi Pico W, note that it includes wireless capabilities, but these are not active in BOOTSEL mode.[](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html)
- If you encounter errors (e.g., `picotool` failing to verify or load), it could be due to a hardware issue (like a faulty flash chip or soldering problem on a custom board) or a corrupted firmware file.[](https://forums.raspberrypi.com/viewtopic.php?p=2078375)

If you need specific help (e.g., flashing firmware, troubleshooting, or identifying the exact board), let me know more details about your setup or what you’re trying to achieve!

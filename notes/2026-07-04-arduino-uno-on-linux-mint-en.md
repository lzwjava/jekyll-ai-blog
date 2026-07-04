---
audio: false
generated: true
image: false
lang: en
layout: post
title: Arduino Uno on Linux Mint
translated: false
type: note
---

**Question:** Can I develop for the Arduino Uno on Linux Mint?

**Answer:**

Yes, fully supported. Linux Mint (Ubuntu-based) works out of the box with the Uno — the board itself runs its own firmware on the ATmega328P; your Mint machine is just the host for compiling and flashing over USB.

Two ways to set it up:

**Option 1 — Arduino IDE 2.x (quickest):**

```bash
# Download the AppImage from arduino.cc, then:
chmod +x arduino-ide_*.AppImage
./arduino-ide_*.AppImage

# Critical: add yourself to the dialout group for serial port access
sudo usermod -aG dialout $USER
# Log out and back in for it to take effect
```

**Option 2 — arduino-cli (terminal-first, fits your workflow better):**

```bash
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
export PATH=$PATH:~/bin

arduino-cli core update-index
arduino-cli core install arduino:avr

# Compile and flash a sketch
arduino-cli compile --fqbn arduino:avr:uno blink/
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno blink/

# Serial monitor
arduino-cli monitor -p /dev/ttyACM0 -c baudrate=9600
```

The Uno enumerates as `/dev/ttyACM0` (genuine board, ATmega16U2 USB chip) or `/dev/ttyUSB0` (clones with CH340 — driver is already in the mainline kernel, no install needed). Check with `ls /dev/tty{ACM,USB}*` after plugging in.

The only common gotcha on Mint: `brltty` (braille display daemon) sometimes grabs CH340 clone boards. If your port vanishes right after plugging in:

```bash
sudo apt remove brltty
```

Since you're terminal-first, `arduino-cli` + a Makefile (or just shell aliases) is the clean path — no GUI needed at all, and it scripts nicely into agent workflows.

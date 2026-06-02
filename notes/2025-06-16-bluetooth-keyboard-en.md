---
audio: false
generated: true
lang: en
layout: post
title: Fix Bluetooth Keyboard Connection Issues
translated: false
type: note
---

Based on the `bluetoothctl` output showing `[DEL] Device` when attempting to connect, here's a precise solution:

### Immediate Fix for Connection Deletion Issue

1. **Remove existing device records** (critical for stale configurations):

   ```bash
   bluetoothctl
   remove F4:73:35:78:28:4E  # Remove keyboard
   remove 24:27:30:24:C8:31   # Remove potential interfering device
   exit
   ```

2. **Reset Bluetooth stack**:

   ```bash
   sudo systemctl stop bluetooth
   sudo rm -rf /var/lib/bluetooth/*
   sudo systemctl start bluetooth
   ```

3. **Repair using correct sequence**:

   ```bash
   bluetoothctl
   power on
   discoverable on
   pairable on
   agent on  # Enable passkey agent
   scan on
   ```

   - **Put K380 in pairing mode** (LED blinking rapidly)
   - When keyboard appears:

     ```bash
     pair F4:73:35:78:28:4E
     ```

   - **Immediately type the 6-digit passcode** shown on-screen (e.g., `123456`) **on the keyboard** and press Enter

4. **Connect only after successful pairing**:

   ```bash
   connect F4:73:35:78:28:4E
   trust F4:73:35:78:28:4E
   scan off
   quit
   ```

### Why This Happens

- The `[DEL] Device` occurs because:
  - Bluetooth stack detects connection failure and purges the device record
  - **Missing pairing step** before connection attempt
  - Possible RF interference from other devices (like the `midea` device)

### Additional Critical Checks

1. **Verify antenna connection**:
   - Ensure Bluetooth antennas are screwed into your MSI motherboard's rear I/O panel

2. **Check kernel drivers**:

   ```bash
   dmesg | grep -i bluetooth
   ```

   Look for errors like `hci0: command timeout` or `Firmware failed to start`

3. **Update firmware** (if timeout errors appear):

   ```bash
   sudo apt install linux-firmware
   ```

4. **Test with minimal environment**:

   ```bash
   sudo rfkill unblock all
   sudo systemctl stop NetworkManager  # Temporary stop
   sudo systemctl restart bluetooth
   ```

### If Still Failing

1. **Alternative pairing method** (bypass agent):

   ```bash
   echo -e 'remove F4:73:35:78:28:4E\npair F4:73:35:78:28:4E\nconnect F4:73:35:78:28:4E\ntrust F4:73:35:78:28:4E' | bluetoothctl
   ```

2. **Check keyboard battery** (critical for Bluetooth):
   - Replace battery if voltage is low (K380 uses CR2032 x 2)

3. **USB Bluetooth adapter test**:
   - If internal Bluetooth is problematic, try a $10 CSR4.0 USB adapter

**Expected success indicators**:

- `Pairing successful` message
- `Connection successful` in bluetoothctl
- `dmesg` showing `HIDP: Bluetooth HID device driver`

After pairing, your K380 should survive reboots. If disconnections recur, check `journalctl -u bluetooth -f` for real-time errors.

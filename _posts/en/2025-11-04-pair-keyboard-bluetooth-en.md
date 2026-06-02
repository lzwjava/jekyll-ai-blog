---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Pair Logitech Keyboard via Bluetooth CLI
translated: false
type: note
---

### Prerequisites

- Ensure your Bluetooth 5.3 emitter (dongle) is plugged into the USB 3.0 port and recognized by Ubuntu. Run `lsusb` in the terminal to check if it shows up (look for something like "Bluetooth" or the vendor ID). If not, try a different USB port or reboot.
- Install Bluetooth tools if not already present:

  ```
  sudo apt update
  sudo apt install bluez bluetooth bluez-tools
  ```

- Unblock Bluetooth if needed:

  ```
  rfkill unblock bluetooth
  ```

- Restart the Bluetooth service:

  ```
  sudo systemctl restart bluetooth
  ```

### Pairing Steps Using bluetoothctl (Recommended for CLI)

The `bluetoothctl` tool is the standard way to manage Bluetooth in Linux/Ubuntu. Logitech keyboards (like MX Keys, K380, or similar) often require entering a pairing PIN on the keyboard itself.

1. **Open the Bluetooth console**:

   ```
   bluetoothctl
   ```

   This enters an interactive shell (prompt changes to `[bluetooth]#`).

2. **Enable the adapter**:

   ```
   power on
   ```

   (If it says "No default controller available," run `list` to see your adapter and `select <adapter_MAC>` if multiple.)

3. **Set up the pairing agent**:

   ```
   agent on
   default-agent
   ```

   This enables PIN handling and makes your session the default for pairing.

4. **Start scanning for devices**:

   ```
   scan on
   ```

   Keep this running. Your Logitech keyboard should appear after ~10-20 seconds (e.g., as "Logitech K380" or similar, with a MAC address like `XX:XX:XX:XX:XX:XX`).

5. **Put your Logitech keyboard in pairing mode**:
   - Turn it on (if it has a power switch).
   - Press and hold the Bluetooth pairing button (usually on the side or top—check your model; for multi-device models like MX Keys, hold the channel button 1/2/3 for 3-5 seconds until the LED blinks rapidly).
   - If it's a single-device model, hold the main pairing button.

6. **Pair the device**:
   Once it shows in the scan (press Enter to refresh), run:

   ```
   pair <MAC_ADDRESS>
   ```

   - Example: `pair 12:34:56:78:9A:BC`
   - Ubuntu will prompt for a PIN (often 0000 or 1234 for Logitech—try defaults first).
   - **Key step for Logitech**: Type the PIN directly on the *physical keyboard* and press Enter. (If no GUI notifications appear, this is crucial—some users report needing to enable system notifications via `gnome-control-center` > Notifications, but CLI often bypasses this.)

7. **Trust and connect**:

   ```
   trust <MAC_ADDRESS>
   connect <MAC_ADDRESS>
   ```

   - This auto-connects on future use.

8. **Exit the console**:

   ```
   exit
   ```

### Troubleshooting

- **Device not scanning**: Ensure the keyboard is in pairing mode (blinking LED). Run `scan off` then `scan on` again. Wait up to 30 seconds.
- **Pairing fails (e.g., "AuthenticationCanceled")**: Remove the device first (`remove <MAC>`), then retry. For stubborn Logitech models, try holding the pairing button longer or toggling channels.
- **No PIN prompt**: Some keyboards pair without one—proceed to connect. If stuck, check logs: `sudo journalctl -u bluetooth -f` while pairing.
- **Adapter issues**: If using a USB Bluetooth 5.3 dongle, confirm kernel support (Ubuntu 22.04+ handles BT 5.3 well). Update kernel if on older Ubuntu: `sudo apt install linux-generic-hwe-22.04`.
- **GUI alternative**: Open Settings > Bluetooth, toggle on, and pair from there—but CLI is more reliable for Logitech quirks.
- Test: After pairing, type in a terminal. If it works, add to startup auto-connect via `bluetoothctl` or crontab.

If your specific Logitech model (e.g., MX Keys Mini) has unique issues, provide the exact model for tailored steps.

### References

- [Pairing LOGITECH K380 in Ubuntu 20.04](https://unix.stackexchange.com/questions/590221/pairing-logitech-k380-in-ubuntu-20-04)
- [Logitech MX Keys won't pair with Bluetooth](https://askubuntu.com/questions/1270419/20-04-logitech-mx-keys-wont-pair-with-bluetooth)
- [Pair Logitech MX Keys with Xubuntu via Bluetooth](https://zroupas.github.io/linux/2021/08/25/pair_mxkeys_xubuntu_bt.html)
- [Ubuntu 20.04 cannot pair Bluetooth Keyboard](https://askubuntu.com/questions/1398096/ubuntu-20-04-cannot-pair-bluetooth-keyboard)

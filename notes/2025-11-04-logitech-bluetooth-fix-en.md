---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Fixing Logitech Bluetooth Pairing Issues
translated: false
type: note
---

### Troubleshooting the AuthenticationCanceled Error

This error commonly occurs with Logitech Bluetooth keyboards (your MAC `F4:73:35:78:28:4E` matches Logitech's OUI prefix) during pairing in Ubuntu due to authentication timeouts, missing PIN prompts, or agent mishandling in BlueZ. The brief connect/disconnect in your log suggests the keyboard is responding but the process times out before completion. Other devices (like `54:2B:FC:F1:1C:D8`) appearing may cause interference—clear them first.

#### Quick Prep Steps
1. **Remove all paired devices** to avoid conflicts:
   In `bluetoothctl`, run `devices` to list them, then `remove <MAC>` for each (e.g., `remove 54:2B:FC:F1:1C:D8`). Exit with `exit`.

2. **Restart Bluetooth service**:
   ```
   sudo systemctl restart bluetooth
   sudo systemctl status bluetooth  # Verify it's active
   ```

3. **Put keyboard in pairing mode**: Press and hold the pairing button (e.g., Easy-Switch channel or Bluetooth button) until the LED blinks rapidly. Do this fresh each attempt.

#### Enhanced Pairing Steps in bluetoothctl
Reopen `bluetoothctl` and follow these **exactly**—the agent setup is crucial, and trusting first often bypasses some timeouts. For Logitech models (e.g., K380, K480, MX Keys), enter any PIN **blindly** on the physical keyboard (no on-screen echo) immediately after the `pair` command.

1. **Enter bluetoothctl**:
   ```
   bluetoothctl
   ```

2. **Power on and set agent**:
   ```
   power on
   agent on
   default-agent
   ```

3. **Scan and confirm device**:
   ```
   scan on
   ```
   Wait for `F4:73:35:78:28:4E` to appear (refresh with Enter if needed). Then:
   ```
   scan off  # Stop scanning to focus
   ```

4. **Trust the device** (helps with auto-accept on reconnects):
   ```
   trust F4:73:35:78:28:4E
   ```

5. **Pair**:
   ```
   pair F4:73:35:78:28:4E
   ```
   - If a PIN/passkey appears (e.g., `[agent] PIN code: 390412` or `[agent] Passkey: 299595`), **immediately type it on the physical keyboard** and press Enter. Do this blindly—even if no prompt seems active.
   - If no PIN shows (common with some Logitechs), try typing `0000` or `1234` on the keyboard and Enter anyway.
   - Watch for `[CHG] Paired: yes`. If it connects briefly then drops, re-run `connect F4:73:35:78:28:4E` right after.

6. **Connect and trust**:
   ```
   connect F4:73:35:78:28:4E
   trust F4:73:35:78:28:4E  # If not done earlier
   ```

7. **Exit and test**:
   ```
   exit
   ```
   Open a text editor or terminal—type to verify input. If it works, it should auto-reconnect on wake.

#### If It Still Fails
- **GUI fallback**: Use Ubuntu Settings > Bluetooth (toggle on, select the device). This often shows a visible PIN prompt. If CLI agent fails, GUI's pinentry handles it better.
- **Blind PIN retry**: Even without a displayed code, some users succeed by typing `0000` + Enter right after `pair`—the keyboard authenticates silently.
- **Logs for clues**: Run `sudo journalctl -u bluetooth -f` in another terminal during pairing. Look for "PIN code" or timeout messages.
- **BlueZ update**: Ensure latest (Ubuntu 24.04+ has BlueZ 5.72+ with better Logitech support):
  ```
  sudo apt update && sudo apt upgrade bluez
  ```
- **USB dongle quirk**: Your BT 5.3 emitter on USB 3.0 is fine, but test on USB 2.0 port—rare interference reported.
- **Model-specific**: If it's a K480/MX Keys, hold the pairing button 5+ seconds. For multi-device, cycle to an unused channel first.

This should resolve it—most Logitech cases stem from the blind PIN step. If you share your exact model or full logs, I can refine further.

[Bluetooth Pairing - AuthenticationCanceled (AskUbuntu)](https://askubuntu.com/questions/1373574/bluetooth-pairing-authenticationcanceled)
[[SOLVED] Bluetooth keyboard: Unable to pair (Arch Linux Forums)](https://bbs.archlinux.org/viewtopic.php?id=174239)
[Barely able to pair Logitech K480 on bluez 5.72 (GitHub)](https://github.com/bluez/bluez/issues/654)

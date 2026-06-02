---
audio: false
generated: true
image: false
lang: en
layout: post
title: Run Mihomo Persistently on macOS
translated: false
type: note
---

Question: How to add a service in macOS to keep mihomo-darwin-amd64-v1-alpha-3035ae8 running always?

Answer:

To make **mihomo** (Clash Meta core) run automatically as a background service on macOS and keep restarting if it crashes, use **launchd** (macOS's built-in service manager).

The recommended way is to create a **LaunchDaemon** (system-wide service that runs as root — usually needed for TUN mode / enhanced-mode / system proxy features).

### Step-by-step guide

1. **Prepare the binary and config**
   - Rename your binary to `mihomo` for simplicity (optional but cleaner):

     ```
     mv mihomo-darwin-amd64-v1-alpha-3035ae8 mihomo
     chmod +x mihomo
     ```

   - Move it to a standard location:

     ```
     sudo mkdir -p /usr/local/bin
     sudo mv mihomo /usr/local/bin/mihomo
     ```

   - Put your config file in a good place, for example:

     ```
     mkdir -p ~/.config/mihomo
     mv config.yaml ~/.config/mihomo/config.yaml
     ```

     (You can also use `/etc/mihomo/config.yaml` or `/usr/local/etc/mihomo/config.yaml`)

2. **Create the plist file**

   Create this file with sudo (because LaunchDaemons must be in a system directory):

   ```bash
   sudo nano /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   Paste the following content (adjust paths if needed):

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.metacubex.mihomo</string>

       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/mihomo</string>
           <string>-d</string>
           <string>/Users/yourusername/.config/mihomo</string>
           <!-- Optional: add more flags if needed, e.g. -->
           <!-- <string>--log-level</string> -->
           <!-- <string>info</string> -->
       </array>

       <key>RunAtLoad</key>
       <true/>

       <key>KeepAlive</key>
       <true/>

       <key>StandardOutPath</key>
       <string>/var/log/mihomo.log</string>

       <key>StandardErrorPath</key>
       <string>/var/log/mihomo.log</string>

       <!-- Optional: lower priority if you want -->
       <!-- <key>Nice</key> -->
       <!-- <integer>10</integer> -->

       <!-- Optional: only start after network is up -->
       <!-- <key>WatchPaths</key> -->
       <!-- <array> -->
       <!--     <string>/Library/Preferences/SystemConfiguration</string> -->
       <!-- </array> -->
   </dict>
   </plist>
   ```

   Important notes:
   - Replace `/Users/yourusername/.config/mihomo` with your actual config directory
   - `-d` tells mihomo where the config folder is (it looks for `config.yaml` inside)
   - `KeepAlive` makes launchd restart mihomo automatically if it dies

3. **Check syntax**

   ```bash
   sudo plutil -lint /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   Should say: `/Library/LaunchDaemons/com.metacubex.mihomo.plist: OK`

4. **Load and start the service**

   ```bash
   sudo launchctl load -w /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   The `-w` makes it start automatically on every boot.

5. **Check status**

   ```bash
   sudo launchctl list | grep mihomo
   ```

   Or see logs:

   ```bash
   tail -f /var/log/mihomo.log
   ```

6. **Stop / unload (if needed)**

   ```bash
   sudo launchctl unload /Library/LaunchDaemons/com.metacubex.mihomo.plist
   ```

   Or temporarily stop without unloading:

   ```bash
   sudo launchctl stop com.metacubex.mihomo
   ```

### Alternative: simpler user-level service (LaunchAgent)

If you **don't** need TUN mode or root privileges:

- Put the plist in `~/Library/LaunchAgents/com.metacubex.mihomo.plist` (no sudo)
- Remove `sudo` from launchctl commands
- It only runs after you log in

But for most mihomo use cases (especially TUN / full system proxy), use LaunchDaemon + root.

### Tips

- If mihomo crashes immediately → check logs (`/var/log/mihomo.log`)
- Common issues: wrong config path, permission denied, or mihomo requires root for TUN
- You can also use Homebrew's `mihomo` formula (`brew install mihomo`) — it installs the binary but still needs manual plist for daemon

This setup will keep mihomo running always, even after reboot or crash.

References:

- [https://wiki.metacubex.one/en/startup/service](https://wiki.metacubex.one/en/startup/service) (Linux example but useful concepts)
- [https://note.okhk.net/use-launchctl-to-start-clash-meta-kernel-on-macos](https://note.okhk.net/use-launchctl-to-start-clash-meta-kernel-on-macos)
- [https://github.com/MetaCubeX/mihomo/discussions/614](https://github.com/MetaCubeX/mihomo/discussions/614) (macOS launchd plist discussion)

---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: macOS Default Daemon Processes
translated: false
type: note
---

### Default Daemon Processes in macOS

In macOS, daemon processes are background services that run without a user interface, typically starting at boot or on demand. They are managed by **launchd**, the system's init and service management framework (PID 1). Daemons differ from agents: daemons run as root/system-wide (before login), while agents run per-user (after login).

Default system daemons are defined in property list (.plist) files located in `/System/Library/LaunchDaemons/`. There are typically around 300–350 of these on a standard install (e.g., 339 on macOS 10.14 Mojave), covering everything from networking and security to hardware management. User-installed or third-party daemons go in `/Library/LaunchDaemons/`.

#### How to View Default Daemons
To list all loaded daemons (and agents) in Terminal:
- `sudo launchctl list` (shows system-wide daemons and agents).
- `launchctl list` (shows user-specific agents only).

For a full directory listing: `ls /System/Library/LaunchDaemons/` (requires no sudo, but the files are read-only).

These commands output columns like PID, status, and label (e.g., `com.apple.timed`).

#### The "timed" Daemon
You specifically mentioned "timed," which refers to **com.apple.timed** (the Time Sync Daemon). This is a core system daemon introduced in macOS High Sierra (10.13) to replace the older `ntpd` process.

- **Purpose**: It automatically synchronizes the Mac's system clock with NTP (Network Time Protocol) servers for accuracy, querying them every 15 minutes. This ensures precise timekeeping for logs, certificates, and network operations.
- **How it works**: Launched by launchd from `/System/Library/LaunchDaemons/com.apple.timed.plist`, it runs as the `_timed` user (in the `_timed` and `_sntpd` groups). It uses the `settimeofday` syscall to adjust the clock based on server responses. Configuration is in `/etc/ntpd.conf` (NTP servers) and state is cached in `/var/db/timed/com.apple.timed.plist`.
- **Related**: Ties into System Settings > General > Date & Time > "Set time and date automatically." If disabled, timed won't sync. For advanced setups (e.g., high-precision needs), tools like Chrony can replace it but disable timed.

If your clock drifts, check for network issues or firewall blocks on NTP (UDP port 123).

#### Other Common Default Daemons ("etc.")
Here's a table of some frequently running default system daemons, grouped by function. This isn't exhaustive (there are hundreds), but covers essentials. Labels are from the .plist filenames.

| Category       | Daemon Label                  | Description |
|----------------|-------------------------------|-------------|
| **Core System** | `com.apple.launchd`          | The launchd process itself; starts all others. |
| **Time & Sync** | `com.apple.timed`             | NTP time synchronization (as above). |
| **User Management** | `com.apple.opendirectoryd`   | Handles user/group accounts and directory services. |
| **User Management** | `com.apple.accounts`         | Manages user accounts and authentication. |
| **Networking** | `com.apple.mDNSResponder`    | Bonjour/mDNS for local network discovery (e.g., AirDrop). |
| **Networking** | `com.apple.nesessionmanager` | Network extension and VPN management. |
| **Bluetooth/Wireless** | `com.apple.bluetoothd`      | Bluetooth device handling. |
| **iCloud/Sync** | `com.apple.cloudd`            | iCloud data syncing and services. |
| **Security**   | `com.apple.securityd`        | Keychain and credential management (often as an agent too). |
| **Updates**    | `com.apple.softwareupdated`  | Handles software updates and catalog downloads. |
| **Hardware**   | `com.apple.kextd`             | Kernel extension loading and management. |
| **Logging**    | `com.apple.systemnotificationd` | System notifications and logging. |
| **MDM (if enabled)** | `com.apple.mdmclient`     | Mobile Device Management client for enterprise setups. |

These run continuously or on triggers to keep macOS stable. If one misbehaves (e.g., high CPU), you can unload it temporarily with `sudo launchctl unload /System/Library/LaunchDaemons/com.apple.example.plist`, but avoid modifying system files.

For a full, current list on your Mac (as of October 2025, likely macOS 15 Sequoia or later), run the commands above—versions evolve slightly with updates.

#### References
- [The macOS Process Journey — “timed” (Time Sync Daemon)](https://medium.com/@boutnaru/the-macos-process-journey-timed-time-sync-daemon-4898c8185b4b)
- [Daemons and Agents could be slowing down your Mac](https://appleinsider.com/inside/macos/tips/daemons-and-agents-could-be-slowing-down-your-mac)
- [What files are included in the /System/Library/LaunchAgents and /System/Library/LaunchDaemons](https://apple.stackexchange.com/questions/361029/what-files-are-included-in-the-system-library-launchagents-and-system-library)
- [Script management with launchd in Terminal on Mac](https://support.apple.com/guide/terminal/script-management-with-launchd-apdc6c1077b-5d5d-4d35-9c19-60f2397b2369/mac)
- [How to show all running launchctl daemons/agents?](https://apple.stackexchange.com/questions/134817/how-to-show-all-running-launchctl-daemons-agents)

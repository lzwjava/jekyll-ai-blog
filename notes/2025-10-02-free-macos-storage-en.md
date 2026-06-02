---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Free Up macOS System Storage
translated: false
type: note
---

### Overview of Cleaning macOS System Storage Space

Based on Apple's official guidance and expert recommendations, freeing up space on macOS (version 15.6.1 like yours) involves built-in tools for optimizing storage, safely clearing removable caches, and deleting unnecessary files. System Data often includes caches, temp files, and logs—much of which can be cleared manually or automatically without harming your Mac. Avoid deleting critical system files, as this could cause instability. Your system shows about 13 GiB available out of 460 GiB total, with 45% used, so focus on caches, downloads, and attachments for quick gains.[1][2][3]

### Using macOS Built-in Storage Management Tools
Apple provides integrated ways to analyze and free space without third-party apps.
1. **Check Storage Usage**: Go to Apple menu > System Settings > General > Storage. This shows a color-coded breakdown (e.g., Apps, Documents, System Data). Click any category for recommendations.[1]
2. **Optimize Storage Automatically**: In Storage settings, enable "Optimize Storage" to offload unused app data and manage attachments. Also, toggle "Empty Trash Automatically" after 30 days.[1]
3. **Empty Trash and Bin Downloads**: System Data includes Trash contents—manually empty it from Finder. Check ~/Downloads for old files and delete them.[1][2]
4. **Manage Large Attachments**: Go to Storage settings > Applications > Manage > Mail > "Optimize Storage" to download large email attachments on-demand.[1]

For a deeper clean, use the "Previous Items" tab in Storage to review recent backups (like Time Machine backups) and remove if unnecessary.[2]

### Identifying and Clearing Removable Cache Files
Caches are temporary files that speed up apps but can accumulate gigabytes. Safely clear user-level caches via Finder; avoid system-level caches unless guided by Apple support to prevent issues. Your Mac's caches are in library folders—check sizes with Finder's Get Info.

1. **User Cache Directory (Safest to Clear)**:
   - Navigate to Finder > Go > Go to Folder, type `~/Library/Caches`, and press Enter.
   - This folder contains app caches (e.g., for browsers, Office apps). Select all folders inside and delete them. These are mostly safe and regenerate.
   - Tip: Check subfolders like `com.apple.*` for Apple app caches, but skip if unsure. Empty Trash afterward.[4][2]

2. **Application-Specific Caches**:
   - Browsers: In Safari, clear history/caches via Safari menu > Clear History. For Chrome/Google apps: Go to Chrome > Settings > Privacy > Clear Browsing Data.
   - Xcode/Developer: If you code, clear derived data in Xcode > Preferences > Locations > Derived Data.
   - Other apps: Check app preferences for cache-clearing options or use Finder to view `~/Library/Caches` subfolders.[2][3]

3. **System and Library Caches (Proceed with Caution)**:
   - `/Library/Caches` may have system caches—only delete specific folders like outdated app caches here, not core system ones (e.g., avoid `com.apple.coreservices`).
   - To analyze sizes safely, use Terminal to list large caches: Open Terminal and run `du -sh /Library/Caches/* | sort -h`.
   - Last resort for deep system caches: Restart in Recovery Mode (Command+R at startup) and run Disk Utility > First Aid, then boot back and use Storage tools.[2]

### Additional Tips for Manual and Safe Cleaning
- **Remove Temporary and Log Files**: System Data includes logs in `/private/var/log`. Use Terminal commands like `sudo rm -rf /private/var/log/asl/*.asl` for older Apple logs (log out and back in first). For temp files, delete from `/tmp` via `sudo rm -rf /tmp/*` after checking.[2]
- **Offload to External Storage**: Move photos/videos to iCloud or an external drive via Storage settings > "Store in iCloud".[1]
- **Apps for Safe Analysis**: Third-party tools like CleanMyMac (from MacPaw) or OmniDiskSweeper scan for large caches/files—use these for guidance, but always back up first (e.g., via Time Machine).[3]
- **Monitor Post-Clean**: Reboot after major deletions to refresh. Recheck Storage usage; regenerable cache deletion shouldn't affect performance.[2]

If System Data remains high (e.g., 218 GB as in some reports), it might be hidden backups or corrupted files—Apple Support suggests running `tmutil thinlocalsnapshots / 10000000000 4` in Terminal for Time Machine cleanup.[5] Ensure you have backups before proceeding. These methods should reclaim significant space without risks on Apple Silicon Macs like your M2.[1][2][4]

Citations:
[1] https://support.apple.com/en-us/102624
[2] https://macpaw.com/how-to/clear-system-storage-mac
[3] https://nektony.com/how-to/clean-up-system-storage-on-mac?srsltid=AfmBOorJjQPPX59Jw3MM47n0NZ8DQlerYQAbkZdymj0rUZM0rtLZlw1s
[4] https://www.reddit.com/r/MacOS/comments/154rp99/how_to_do_i_clear_system_data_on_mac_os/
[5] https://discussions.apple.com/thread/255084458

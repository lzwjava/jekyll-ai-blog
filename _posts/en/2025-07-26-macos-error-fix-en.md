---
audio: false
generated: true
lang: en
layout: post
title: Fixing macOS File Permission Errors
translated: false
type: note
---

### Understanding the Error
This error message typically appears on macOS when you're trying to move, copy, delete, or manipulate files/folders (e.g., emptying the Trash or dragging items), but the system encounters permission issues, locked files, or read-only restrictions. The message itself provides the core fix, but sometimes additional steps are needed if the problem persists, such as using Terminal commands, repairing disk permissions, or handling stubborn files.

### Step-by-Step Fixes
Follow these in order, starting with the simplest. These assume you're on macOS (e.g., Ventura, Sonoma, or later). Make sure you're logged in as an admin user.

1. **Unlock Files and Adjust Permissions (As Suggested in the Error)**:
   - Select the problematic file or folder in Finder.
   - Right-click (or Control-click) and choose **Get Info** (or press Command + I).
   - In the Get Info window:
     - Under the **General** section, uncheck the **Locked** box if it's selected.
     - Scroll to the **Sharing & Permissions** section at the bottom.
     - Click the lock icon in the bottom-right corner and enter your admin password to unlock changes.
     - For your username (or "everyone" if needed), set the Privilege to **Read & Write**.
   - If multiple items are affected, you can select them all, Get Info, and apply changes (hold Command to select multiples).
   - Close the window and retry the operation (e.g., delete or move the files).

2. **If the Issue is with Trash (Common Scenario)**:
   - This error often pops up when emptying the Trash if files are locked or have permission issues.
   - First, open the Trash, select the items, and apply the above Get Info steps to unlock/adjust permissions.
   - If that doesn't work, force-empty the Trash:
     - Hold the Option key while right-clicking the Trash icon in the Dock and select **Empty Trash**.
   - Alternative via Terminal (if GUI fails):
     - Open Terminal (from Applications > Utilities or Spotlight search).
     - Type: `sudo rm -rf ~/.Trash/*` and press Enter.
     - Enter your admin password (it won't show as you type).
     - Warning: This permanently deletes everything in Trash—use cautiously, as there's no undo.

3. **Repair Disk Permissions Using Disk Utility**:
   - Open **Disk Utility** (from Applications > Utilities or Spotlight).
   - Select your main drive (e.g., Macintosh HD) in the sidebar.
   - Click **First Aid** > **Run** (or **Repair Disk Permissions** in older macOS versions).
   - Let it complete, then restart your Mac and try again.

4. **Check for External Drives or Network Volumes**:
   - If the files are on an external drive, USB, or network share:
     - Eject and reconnect the drive.
     - In Get Info, ensure the **Ignore ownership on this volume** box is checked (under Sharing & Permissions).
   - For read-only formats (e.g., NTFS drives), you may need third-party tools like Paragon NTFS for write access.

5. **Advanced Terminal Fixes (If Permissions Are Stubborn)**:
   - To reset permissions on a specific folder/file:
     - In Terminal: `sudo chmod -R 777 /path/to/folder` (replace `/path/to/folder` with the actual path; drag the folder into Terminal to auto-fill).
     - This sets full read/write/execute for everyone—use sparingly.
   - To unlock all files in a directory: `sudo chflags -R nouchg /path/to/folder`.
   - Restart in Safe Mode (hold Shift during boot) to clear caches, then try again.

6. **Other Troubleshooting**:
   - **Restart Your Mac**: Simple but often resolves temporary glitches.
   - **Update macOS**: Go to System Settings > General > Software Update.
   - **Check for Malware/Antivirus Interference**: Run a scan with Malwarebytes or similar.
   - If files are from downloads or apps, ensure they're not quarantined: In Terminal, `xattr -d com.apple.quarantine /path/to/file`.
   - If nothing works, boot into Recovery Mode (Command + R on startup), run First Aid on the disk, or consider resetting permissions via Terminal in Recovery.

If the error persists after these steps, provide more details like your macOS version, what operation you're trying (e.g., deleting specific files), and if it's in Trash or elsewhere.

### References
[Apple Support: Change permissions for files, folders, or disks on Mac](https://support.apple.com/guide/mac-help/change-permissions-for-files-folders-or-disks-mchlp1203/mac)
[How to Fix "Operation Can't Be Completed" Error on Mac](https://www.macrumors.com/how-to/fix-operation-cant-be-completed-error-mac/)
[Empty Trash When It Says Files Are In Use](https://apple.stackexchange.com/questions/52257/empty-trash-when-it-says-files-are-in-use)

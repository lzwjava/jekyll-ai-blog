---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Transferring Media to External Disk
translated: false
type: note
---

### Moving Photos and Videos to a Portable Disk on macOS

Based on your system information, you have a macOS 15.6.1 system with a portable disk mounted at `/Volumes/Untitled` (2.0 TB total capacity, 1.5 TB available). Moving photos and videos involves transferring files from your Mac's storage (e.g., in `~/Pictures` for photos or `~/Movies` for videos) to the external disk. This can be done via the graphical interface (Finder) or command-line tools like Terminal, depending on your preference. I'll cover both methods below, assuming you're moving files rather than the entire Photos app library (if that's needed, export them first from the Photos app).

**Important Notes:**

- **Backup First:** Ensure you have backups of your files to avoid data loss in case of errors.
- **Permissions:** You may need administrative permissions for certain actions. Run Terminal commands as an admin if prompted.
- **Space Check:** Verify the files' size doesn't exceed the portable disk's available space (1.5 TB in your case).
- **File Locations:** Default paths are `~/Pictures` for photos and `~/Movies` for videos. If they're in other directories (e.g., Downloads), adjust accordingly.
- **Unmount Safely:** After moving, unmount the disk via Finder > Eject or `diskutil unmount /Volumes/Untitled` to prevent corruption.

#### 1. Using Finder (Graphical Method - Beginner-Friendly)

This is the simplest way for most users. It involves drag-and-drop via macOS's file manager.

1. **Locate the Portable Disk and Files:**
   - Open Finder (click the smiley face icon in the Dock).
   - In the sidebar, under "Locations," you'll see "Untitled" (your portable disk). Click it to browse its contents.
   - Open a separate Finder window (Command + N) and navigate to where your photos/videos are stored (e.g., your Pictures or Movies folder).

2. **Move the Files:**
   - Select the photos/videos you want to move (hold Command to multi-select).
   - Drag them from their current location into the portable disk's window (e.g., create a folder like "PhotosBackup" on the disk first for organization).
   - To move (relocate permanently, freeing space on your Mac), hold Option while dragging. To copy (duplicate), just drag normally.
     - Alternatively, right-click the selected files > "Move to Trash" after copying to effectively "move" them by deleting originals post-copy.
   - If organizing, create folders on the disk (right-click > New Folder) like "Photos" and "Videos."

3. **Verify and Eject:**
   - Open the portable disk in Finder and confirm the files are there.
   - Drag the disk icon to the Trash (or right-click > Eject) to safely unmount before disconnecting.

This method preserves metadata (e.g., creation dates) and handles large files efficiently.

#### 2. Using Terminal (Command-Line Method - Efficient for Bulk Operations)

If you prefer scripting or handling via commands (as shown in your Python scripts), use Terminal for precision. This is useful for automated or recursive moves.

1. **Navigate to Your Files and Disk:**
   - Open Terminal (Applications > Utilities > Terminal).
   - Check your current directory: Run `pwd` and navigate as needed (e.g., `cd ~/Pictures` to access photos).
   - Confirm the disk is mounted: Run `ls /Volumes` to see "Untitled." Your disk is already mounted based on the provided output.

2. **Move the Files:**
   - To **move** files (relocate permanently, deleting from original location):
     - For individual files: `mv /path/to/photo.jpg /Volumes/Untitled/Photos/
`
     - For directories (e.g., entire Photos folder): `mv ~/Pictures/PhotosLibrary /Volumes/Untitled/`
     - Example full move: `mv ~/Pictures/* /Volumes/Untitled/Photos/` (moves all contents from Pictures to a new folder on the disk; add options like `-v` for verbose output).
   - To **copy** instead (duplicate without deleting originals): Use `cp` with `-r` for recursive directories.
     - Example: `cp -r ~/Pictures/PhotosLibrary /Volumes/Untitled/Photos/` (copies recursively; great for backups where you want to keep originals).
   - For videos in Movies: `cp -r ~/Movies/Videos/ /Volumes/Untitled/Videos/`
   - To handle hidden files or permissions: Add `sudo` if needed (e.g., `sudo mv ~/Pictures/photo.jpg /Volumes/Untitled/`).
   - For safety, preview what you'll move: `ls -la ~/Pictures` to list files.

3. **Verify and Unmount:**
   - Check the disk: `ls /Volumes/Untitled` to confirm transfers.
   - Unmount safely: `diskutil unmount /Volumes/Untitled` and then physically disconnect the disk.

**Advanced Tips:**

- **Use Rsync for Syncing:** For incremental backups (only new/changed files), `rsync -av ~/Pictures /Volumes/Untitled/Photos` (install rsync if not present, but it's built-in on macOS).
- **Automation:** Adapt this into your Python scripts (e.g., using `subprocess` to run `cp` or `mv` commands based on `list_portable_disks.py` output).
- **MacBook Specific:** On your M2 MacBook Air (Model Mac14,2), transfers should be fast via USB-C. Monitor battery/Temp (e.g., via Activity Monitor) if needed.

If you encounter issues (e.g., permissions errors), provide more details like exact file paths or error messages for tailored advice. This process should work reliably on your setup.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix macOS Disk Ejection Issues
translated: false
type: note
---

## Quick Solutions

### 1. **Using Activity Monitor (GUI)**
- Open **Activity Monitor** (Applications > Utilities)
- Click the **Disk** tab
- Look for processes using your external drive
- Select the process and click the stop button (⊘)
- Then try ejecting again

### 2. **Using Terminal (Command Line)**

#### Find what's using the disk:
```bash
# Replace DISKNAME with your actual disk name (e.g., MyDrive, Untitled, etc.)
lsof | grep DISKNAME

# Or use this to see all open files on mounted volumes
lsof +D /Volumes
```

#### Identify the disk mount point:
```bash
# List all mounted volumes and their paths
mount | grep -E "Volumes|media"

# Or use diskutil
diskutil list
```

#### Find processes accessing your drive:
```bash
# Replace /Volumes/DISKNAME with your actual path
lsof | grep "/Volumes/DISKNAME"

# Shows process name and PID (Process ID)
```

#### Kill the process:
```bash
# Replace PID with the actual process ID (e.g., 1234)
kill -9 PID

# Or kill by name (less precise, affects all instances)
killall -9 processname
```

---

## Step-by-Step Instructions

### **Method 1: Activity Monitor (Easiest)**

1. Open **Spotlight Search** (⌘ + Space)
2. Type "Activity Monitor" and press Enter
3. In the window that opens, click the **Disk** tab
4. Look for your disk name in the list (right side shows "I/O Read Bytes" and "I/O Write Bytes")
5. Identify which process is accessing it
6. Click the process → Click the **Stop** button (red circle with ⊘)
7. Confirm the force quit
8. Try ejecting your disk again

### **Method 2: Terminal (More Control)**

1. Open **Terminal** (Applications > Utilities)

2. **Find your disk's mount point:**
   ```bash
   diskutil list
   ```
   Look for your external drive's name. Note the mount point (e.g., `/Volumes/MyDrive`)

3. **Find processes using that disk:**
   ```bash
   lsof | grep "/Volumes/MyDrive"
   ```
   Replace "MyDrive" with your actual disk name

4. **Check the output** - You'll see:
   ```
   COMMAND   PID    USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
   Finder    123   user   cwd    DIR    1,2        4096 1234 /Volumes/MyDrive
   ```
   - **COMMAND**: Process name
   - **PID**: Process ID (the number you'll need to kill)

5. **Kill the process:**
   ```bash
   kill -9 123
   ```
   Replace 123 with the actual PID

6. **Try ejecting again** from Finder or via Terminal:
   ```bash
   diskutil eject /Volumes/MyDrive
   ```

---

## Common Processes That Lock Disks

| Process | Cause | Solution |
|---------|-------|----------|
| `Finder` | Browsing the disk | Close Finder windows for that disk |
| `Spotlight` | Indexing the drive | Disable Spotlight for external drives (System Settings > Siri & Spotlight) |
| `Backup` or `Time Machine` | Automatic backup running | Wait for backup to complete or disable |
| `Google Drive`, `Dropbox`, `OneDrive` | Cloud sync in progress | Quit the app or wait for sync to complete |
| `Terminal` | Current working directory on disk | Change directory: `cd ~` then try eject |
| `Preview`, `Word`, `Excel` | File is open | Close the application |

---

## Advanced: Safe Eject via Terminal

```bash
# First, find the disk identifier (shows as /dev/diskX)
diskutil list

# Eject using the identifier (preferred method)
diskutil eject /dev/disk2

# Or eject by mount point
diskutil eject /Volumes/MyDrive

# Force eject (last resort, unmounts immediately)
diskutil secureEject /Volumes/MyDrive
```

---

## Prevention Tips

1. **Add external drives to Spotlight exclusion:**
   - System Settings > Siri & Spotlight
   - Click "Exclude" next to your external drive

2. **Use proper eject method:**
   - Don't just unplug—always eject first
   - Right-click disk in Finder → Eject

3. **Close applications before ejecting:**
   - Save and close any files open from the drive
   - Quit cloud sync apps before ejecting

4. **Avoid background operations:**
   - Don't start backups or syncs right before ejecting
   - Wait for Spotlight indexing to finish (if re-enabling)

---

## If Nothing Works

```bash
# List all mounted volumes
mount

# Force unmount (use with caution - data loss risk if writes pending)
sudo umount -f /Volumes/MyDrive

# Or use diskutil
sudo diskutil unmountDisk force /Volumes/MyDrive
```

⚠️ **Warning:** Using `sudo` and force unmount should be a last resort as it can cause data loss if files are being written.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Mount and Extract ISO Files
translated: false
type: note
---

Yes, absolutely! There are several ways to extract or inspect the contents of an ISO file.

**On Linux/macOS (using terminal):**

The most common method is to **mount** it:

```bash
# Create a mount point
mkdir /mnt/iso

# Mount the ISO (Linux)
sudo mount -o loop yourfile.iso /mnt/iso

# Then browse it
ls /mnt/iso
```

Or **extract without mounting** using `7zip`:

```bash
# Install 7zip
sudo apt install p7zip-full   # Ubuntu/Debian

# Extract
7z x yourfile.iso -o./output_folder
```

**On macOS:**

```bash
# Simply double-click the .iso in Finder, or:
hdiutil mount yourfile.iso
```

**On Windows:**

- **Double-click** the ISO in File Explorer (Windows 10/11 mounts it automatically)
- Or right-click → **"Mount"**
- Use **7-Zip** → right-click → Extract Here

**Using Python (for scripting/automation):**

```python
import subprocess

# Mount (Linux)
subprocess.run(["sudo", "mount", "-o", "loop", "file.iso", "/mnt/iso"])
```

---

**What you'll typically find inside an ISO:**

| ISO Type | Contents |
| --- | --- |
| OS installer (e.g., Ubuntu) | `boot/`, `casper/`, `.vmlinuz`, `initrd` |
| Game disc | Game files, `autorun.inf` |
| Software installer | `setup.exe`, config files |
| Blu-ray/DVD | `BDMV/`, `VIDEO_TS/` |

Would you like help with a specific ISO file or use case?

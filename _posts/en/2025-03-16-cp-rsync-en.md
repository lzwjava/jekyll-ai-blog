---
audio: false
generated: true
lang: en
layout: post
title: Copying Files with Directory Structure
translated: false
type: note
---

Given your `find` command output, you want to copy all the `.log` files to `/Users/lzwjava/projects/logs` while preserving their directory structure. For example, a file like `./CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log` should end up as `/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log`. I’ll show you how to achieve this using `find` combined with `cp` or `rsync`, ensuring the directory hierarchy is maintained.

---

### **Solution 1: Using `find` with `cp`**
You can use `find` to locate the `.log` files and `cp` with the `--parents` option to copy them while preserving their directory structure.

#### **Command**
```bash
find . -name "*.log" -exec cp --parents {} /Users/lzwjava/projects/logs \;
```

#### **Explanation**
- **`find . -name "*.log"`**: Locates all `.log` files in the current directory and subdirectories (as in your example).
- **`-exec cp --parents {} /Users/lzwjava/projects/logs \;`**:
  - `cp --parents`: Copies the file and recreates its directory path relative to the source (`.`).
  - `{}`: Placeholder for each file found by `find`.
  - `/Users/lzwjava/projects/logs`: Destination directory.
  - `\;`: Terminates the `-exec` command.

#### **Result**
- `./CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log` → `/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/system.log`
- Directory structure under `CoreSimulator` is preserved.

#### **Before Running**
- Ensure `/Users/lzwjava/projects/logs` exists:
  ```bash
  mkdir -p /Users/lzwjava/projects/logs
  ```

---

### **Solution 2: Using `rsync`**
`rsync` is another powerful tool that can copy files while preserving directory structure, and it’s often more efficient for bulk operations.

#### **Command**
```bash
find . -name "*.log" -exec rsync -R -a {} /Users/lzwjava/projects/logs \;
```

#### **Explanation**
- **`-R`**: Uses relative paths, preserving the directory structure from the source (`.`).
- **`-a`**: Archive mode (preserves timestamps, permissions, etc.).
- `{}`: Each `.log` file found.
- `/Users/lzwjava/projects/logs`: Target directory.

#### **Result**
Same as above—files are copied with their full relative paths intact.

#### **Before Running**
- Create the destination directory if it doesn’t exist:
  ```bash
  mkdir -p /Users/lzwjava/projects/logs
  ```

---

### **Verifying the Copy**
After running either command, check the destination:
```bash
ls -R /Users/lzwjava/projects/logs
```
You should see:
```
/Users/lzwjava/projects/logs:
CoreSimulator

/Users/lzwjava/projects/logs/CoreSimulator:
CoreSimulator.log  FC275C39-59CC-4483-A64E-5D459D7A1D57  Simulator.log

/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57:
com.apple.itunesstored  system.log

/Users/lzwjava/projects/logs/CoreSimulator/FC275C39-59CC-4483-A64E-5D459D7A1D57/com.apple.itunesstored:
itunesstored.log
```

---

### **Key Notes**
- **Permissions:** Ensure you have write access to `/Users/lzwjava/projects/logs`. If not, use `sudo` (e.g., `sudo cp ...`) or adjust permissions:
  ```bash
  chmod -R u+w /Users/lzwjava/projects/logs
  ```
- **Overwriting:** If files already exist at the destination:
  - `cp` will overwrite without warning.
  - `rsync -a` will overwrite too, but you can add `--ignore-existing` to skip existing files:
    ```bash
    find . -name "*.log" -exec rsync -R -a --ignore-existing {} /Users/lzwjava/projects/logs \;
    ```
- **Dry Run (Test First):**
  - For `cp`, add `echo` to preview:
    ```bash
    find . -name "*.log" -exec echo cp --parents {} /Users/lzwjava/projects/logs \;
    ```
  - For `rsync`, use `--dry-run`:
    ```bash
    find . -name "*.log" -exec rsync -R -a --dry-run {} /Users/lzwjava/projects/logs \;
    ```

---

### **Which to Choose?**
- **`cp`**: Simpler, no extra tools needed (available on all Unix-like systems).
- **`rsync`**: More flexible (e.g., for syncing, skipping duplicates), but requires `rsync` to be installed (standard on most systems).

Both will work for your case. I recommend starting with `cp --parents` for simplicity.

---

### **Final Command (Recommended)**
```bash
mkdir -p /Users/lzwjava/projects/logs
find . -name "*.log" -exec cp --parents {} /Users/lzwjava/projects/logs \;
```

Run this from your `Logs` directory (`lzwjava@anonymous Logs %`), and you’re set! Let me know if you hit any snags or want to adjust the behavior (e.g., flatten the structure instead).

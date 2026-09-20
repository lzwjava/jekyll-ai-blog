---
audio: false
generated: true
image: false
lang: en
layout: post
title: EDK2 Build System Missing
translated: false
type: note
---

The `buildffs.py` script failed because it relies on the **EDK2 build system**, which isn't installed on this machine. As stated in the [README](https://github.com/xCuri0/ReBarUEFI#build):

> *"Use the provided buildffs.py script after cloning inside an [edk2](https://github.com/tianocore/edk2) tree to build the DXE driver."*

Here's what the script expects:

1. **ReBarUEFI must be cloned *inside* an EDK2 tree** — e.g. `edk2/ReBarUEFI/ReBarDxe/`
2. **EDK2 environment must be set up** — source `edksetup.sh` (sets `$WORKSPACE`, `$EDK_TOOLS_PATH`, etc.) and have `BaseTools` built
3. **Dependencies installed** — `nasm`, `iasl`, `uuid-dev`, `python3-pefile`
4. Then from `edk2/ReBarUEFI/ReBarDxe/`:

   ```bash
   source ../edksetup.sh   # from edk2 root
   python buildffs.py
   ```

5. The script `chdir`'s to `../../` (the EDK2 root) and runs the `build` command

**Issues encountered:**

- ❌ `ModuleNotFoundError: No module named 'pefile'` → fixed (installed in venv)
- ❌ `FileNotFoundError: [Errno 2] No such file or directory: 'build'` → `build` is EDK2's build tool, requires the full EDK2 environment

**What you need to do to build locally:**

```bash
# Clone EDK2
git clone --recursive https://github.com/tianocore/edk2.git
cd edk2

# Clone ReBarUEFI inside EDK2
git clone https://github.com/xCuri0/ReBarUEFI.git

# Install deps (macOS)
brew install nasm acpica
pip install pefile

# Build BaseTools
make -C BaseTools

# Source environment & build
source edksetup.sh
cd ReBarUEFI/ReBarDxe
python3 buildffs.py
```

**Alternatively**, if you just want the pre-built `.ffs` file, grab it from the [Releases page](https://github.com/xCuri0/ReBarUEFI/releases) — no local build needed.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: ReBarUEFI build successful
translated: false
type: note
---

Done. `python3 buildffs.py` now works and produced the `.ffs` file.

## Result

```
Build/ReBarUEFI/RELEASE_GCC/X64/ReBarDxe.ffs   (12,338 bytes)
Build/ReBarUEFI/RELEASE_GCC/X64/ReBarDxe.efi   (12,288 bytes)
```

The FFS header contains the expected GUID (`a8ee1777-...`) and the NX_COMPAT flag was set on the PE (`DllCharacteristics=0x0100`).

## What I fixed / did

1. **Installed dependencies** (nasm, iasl via acpica-tools, pefile for the system Python):

   ```bash
   sudo apt-get install -y nasm acpica-tools python3-pefile
   ```

   (`uuid-dev` was already present.)

2. **Built BaseTools** using the system Python 3.12 (not Homebrew's 3.14, which is first in `PATH` and lacks `pefile`):

   ```bash
   cd /home/lzw/projects/edk2
   export PYTHON_COMMAND=/usr/bin/python3
   make -C BaseTools
   ```

3. **Generated the Conf files and configured them**:

   ```bash
   source edksetup.sh --reconfig
   ```

   Then edited `Conf/target.txt`:
   - `ACTIVE_PLATFORM = ReBarUEFI/ReBarDxe/ReBar.dsc`
   - `TARGET = RELEASE`
   - `TARGET_ARCH = X64`
   - `TOOL_CHAIN_TAG = GCC`  ← **important**: this EDK2 tree removed `GCC5` (`tools_def.txt` v3.06 removed GCC48/GCC49/GCC5), so the original `GCC5` produced `Tool chain [GCC5] is not defined`.

4. **Ran the build**:

   ```bash
   cd /home/lzw/projects/edk2
   export PYTHON_COMMAND=/usr/bin/python3
   source edksetup.sh >/dev/null
   cd ReBarUEFI/ReBarDxe
   /usr/bin/python3 buildffs.py
   ```

The one line in the log that looks scary — `cp: cannot stat '.../*.pdb': No such file or directory` — is harmless and explicitly ignored by the build (`Error 1 (ignored)`); PDB files simply don't exist on GCC builds.

## One-liner to reproduce the build later

```bash
cd /home/lzw/projects/edk2 && export PYTHON_COMMAND=/usr/bin/python3 && source edksetup.sh >/dev/null && cd ReBarUEFI/ReBarDxe && /usr/bin/python3 buildffs.py
```

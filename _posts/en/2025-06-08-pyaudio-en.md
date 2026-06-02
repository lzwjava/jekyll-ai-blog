---
audio: false
generated: true
lang: en
layout: post
title: PortAudio and pyaudio
translated: false
type: note
---

The error occurs because **pyaudio** requires the PortAudio development headers to compile, which are missing on your system. Here's how to fix it:

### Step-by-Step Solution:

1. **Install PortAudio Development Headers** (required for pyaudio):
```bash
sudo apt update && sudo apt install portaudio19-dev
```

2. **Install Python Development Tools** (if not already installed):
```bash
sudo apt install python3-dev
```

3. **Retry the Installation**:
```bash
pip install -r requirements.local.txt
```

### If You Still Encounter pycrypto Issues:
The pycrypto package is deprecated and may have compatibility issues. Replace it with **pycryptodome** by modifying your `requirements.local.txt`:

1. Open the requirements file:
```bash
nano requirements.local.txt
```

2. Replace `pycrypto` with:
```
pycryptodome
```

3. Save and re-run the installation:
```bash
pip install -r requirements.local.txt
```

### Why This Works:
- `portaudio19-dev` provides the missing PortAudio headers needed to compile pyaudio
- `python3-dev` includes necessary Python development headers
- `pycryptodome` is a maintained drop-in replacement for the deprecated pycrypto

### Alternative for pycrypto (if you must keep it):
If you specifically need pycrypto, install build dependencies first:
```bash
sudo apt install build-essential libgmp-dev
pip install pycrypto
```
But note pycrypto has compatibility issues with newer Python versions.

After these steps, all packages should install correctly. The DEPRECATION warnings about legacy builds are informational and won't prevent installation - they indicate the packages will need migration to PEP 517 builds in the future.

---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Configuring ibm_db on Red Hat Linux
translated: false
type: note
---

Question: How to configure the `ibm_db` Python package on Red Hat Linux to successfully import it without shared library errors?

Answer:

On Red Hat Linux (RHEL, including versions 7–9+), the `ibm_db` Python package (the official IBM driver for DB2) is straightforward to install and configure, especially since pip wheels now include a bundled clidriver (DB2 client libraries). This avoids the need for a separate DB2 client installation in most cases. The equivalent of Windows' "DLL load failed" error on Linux is typically `ImportError: libdb2.so: cannot open shared object file` or similar, which occurs if the shared libraries aren't found. Below are the steps to install and configure it properly.

### Prerequisites
- Python 3.9+ (wheels are available up to Python 3.14; earlier versions may require source builds).
- Ensure you have a C++ compiler (GCC) and Make installed for source builds:
  ```bash
  sudo yum install gcc make  # or dnf on RHEL 8+
  ```
- Install Python development headers if you encounter build errors (e.g., missing `python.h`):
  ```bash
  sudo yum install python3-devel  # Adjust for your Python version, e.g., python39-devel
  ```
- For Docker or minimal environments, also install:
  ```bash
  sudo yum install libxml2 pam wget
  ```
  Then install pip if needed:
  ```bash
  wget https://bootstrap.pypa.io/get-pip.py
  python3 get-pip.py
  ```

### Installation (Recommended: Use Bundled clidriver)
The simplest method installs a prebuilt wheel with the clidriver (v11.5.9 by default, which includes `libdb2.so` and dependencies). No environment variables are needed.

```bash
pip install ibm_db
```

This also installs `ibm_db_dbi` (DB-API 2.0 wrapper). After installation, test the import:
```python
import ibm_db  # Should work without errors
```

The clidriver is extracted to `<your-python-site-packages>/clidriver` (e.g., `/usr/local/lib/python3.11/site-packages/clidriver`), and `ibm_db` automatically handles the library loading.

### Alternative: Use Existing DB2 Client or Custom clidriver
If you have a separate DB2 Runtime Client (e.g., from IBM's RPM packages) or prefer a different clidriver version:

1. Install the DB2 client (if needed):
   Download `v11.5.x` or `v12.1.x` RPM from IBM (e.g., `clicli_v11.5.9_linuxx64_server_r1.tar.gz`). Extract and install:
   ```bash
   tar -xzf clicli_v11.5.9_linuxx64_server_r1.tar.gz
   cd clicli
   sudo ./db2setup  # Follow the installer
   ```
   Typical install path: `/opt/ibm/db2/V11.5` or `/opt/ibm/clidriver`.

2. Set environment variables:
   ```bash
   export IBM_DB_HOME=/opt/ibm/clidriver  # Path to your clidriver install
   export LD_LIBRARY_PATH=$IBM_DB_HOME/lib:$LD_LIBRARY_PATH  # For library loading
   ```
   Add these to `~/.bashrc` for persistence:
   ```bash
   echo 'export IBM_DB_HOME=/opt/ibm/clidriver' >> ~/.bashrc
   echo 'export LD_LIBRARY_PATH=$IBM_DB_HOME/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
   source ~/.bashrc
   ```

3. Install from source (to use your custom setup):
   ```bash
   pip install ibm_db --no-binary :all: --no-cache-dir
   ```
   - For clidriver v12.1 (if needed):
     ```bash
     export CLIDRIVER_VERSION=v12.1.0
     pip install ibm_db --no-binary :all: --no-cache-dir
     ```
   - For a custom clidriver tarball:
     ```bash
     export IBM_DB_INSTALLER_URL=/path/to/your/clidriver.tar.gz
     pip install ibm_db --no-binary :all: --no-cache-dir
     ```

### Troubleshooting Import Errors
- **Shared library not found (e.g., `libdb2.so` error)**:
  Verify `LD_LIBRARY_PATH` includes the clidriver lib dir (see above). Test with:
  ```bash
  ldd $(python -c "import ibm_db; print(ibm_db.__file__.replace('ibm_db.so', ''))")  # Check dependencies
  ```
  If using bundled clidriver, it should self-resolve; otherwise, run `ldconfig` after setting paths.

- **Build failures (e.g., missing headers)**:
  Install `python3-devel` and retry.

- **License issues (for z/OS or iSeries connections)**:
  Place `db2con*.lic` (matching your clidriver version) in `$IBM_DB_HOME/license/` as a regular file (not symlink). Validate:
  ```bash
  cd $IBM_DB_HOME/bin
  ./db2cli validate -connstring "DATABASE=mydb;HOSTNAME=server;PORT=50000;UID=user;PWD=pass;" -displaylic
  ```

- **Version mismatches**:
  Check clidriver version:
  ```bash
  $IBM_DB_HOME/bin/db2level
  ```
  Ensure it matches your DB2 server.

### Pros of Bundled clidriver vs. Separate Client

| Approach                  | Needs Separate Install? | Needs LD_LIBRARY_PATH? | Works in Virtual Env? | Size Added      |
|---------------------------|-------------------------|------------------------|-----------------------|-----------------|
| Bundled clidriver (pip)  | No                      | No                     | Yes                   | ~120 MB        |
| Separate DB2 Client      | Yes                     | Yes                    | If paths set globally | ~300–500 MB    |

Use the bundled approach unless you need a specific clidriver version or have existing DB2 tools.

After setup, connect like this:
```python
conn = ibm_db.connect("DATABASE=mydb;HOSTNAME=server;PORT=50000;UID=user;PWD=pass;", "", "")
```

[ibm_db GitHub - Linux Installation](https://github.com/ibmdb/python-ibmdb#linux)
[ibm_db PyPI Page](https://pypi.org/project/ibm-db/)

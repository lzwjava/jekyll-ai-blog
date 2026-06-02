---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Using ibm_db with bundled clidriver on Windows
translated: false
type: note
---

Question: Can we use the IBM-provided `clidriver` (the private DB2 client bundled with the `ibm_db` package) on Windows to avoid the "DLL can't be loaded" error?

Answer:

Yes – this is actually the **easiest and most recommended way** on Windows today.

IBM maintains a special package called **ibm_db_clidriver** (or simply installed via `ibm_db[clidriver]`) that contains a complete, private copy of the 64-bit DB2 runtime client (including `db2cli64.dll` and all dependencies).
After installing this package, `import ibm_db` works immediately with no PATH changes, no `os.add_dll_directory()`, and no separate DB2 client installation required.

### How to use it (2025, current method)

```bash
# Option 1 – recommended (one line)
pip install "ibm_db[clidriver]"

# Option 2 – explicit (same result)
pip install ibm_db
pip install ibm_db_clidriver
```

That’s it. Now this works everywhere:
```python
import ibm_db          # ← no DLL error anymore
conn = ibm_db.connect("DATABASE=mydb;HOSTNAME=server;PORT=50000;UID=user;PWD=pass;", "", "")
```

### What happens under the hood
- The `clidriver is extracted into `<your-python-site-packages>/clidriver`
- Example path:
  `C:\Python312\Lib\site-packages\clidriver\bin\amd64.VC12`
- `ibm_db` automatically adds this private `clidriver\bin` directory to the DLL search path at import time, so Windows always finds `db2cli64.dll` even if nothing is in the system PATH.

### Pros vs separate DB2 client installation

| Approach                        | Needs system PATH change? | Needs os.add_dll_directory()? | Works in virtual environments? | Works after pip install only? | Size       |
|--------------------------------|---------------------------|-------------------------------|--------------------------------|-------------------------------|------------|
| Separate IBM Data Server Client | Yes                       | Sometimes                     | Only if PATH is set globally   | No                            | ~300–800 MB |
| ibm_db[clidriver]              | No                        | No                            | Yes                            | Yes                           | ~120 MB    |

### When you might still prefer a full separate client
- You already have applications (outside Python) that need the DB2 client.
- You need very recent fixes or features not yet in the bundled clidriver.
- Corporate policy forbids bundling runtime libraries inside Python packages.

Otherwise, just use the bundled clidriver – it’s what most people on Windows do now.

References:
- [python-ibmdb – Using ibm_db_clidriver package](https://github.com/ibmdb/python-ibmdb#using-ibm_db_clidriver-package)
- [ibm_db PyPI page – clidriver extra](https://pypi.org/project/ibm-db/)

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Run Oracle XE on Ubuntu 24.04
translated: false
type: note
---

This laptop is running **Ubuntu 24.04.4 LTS (x86_64)**, so none of the official packages are a perfect match — but here's the breakdown:

| Option | Verdict |
| --- | --- |
| **Windows 64-bit** (`.zip`) | ❌ You're on Linux, not Windows. |
| **Oracle Linux 8** (`.rpm`) | ✅ **Best choice** — the RPM is the one you'd want to attempt on Ubuntu. |
| **Pre-install RPM for RHEL 8** | ❌ Supplementary package only. |

---

## Recommended approach

**Install the OL8 RPM on Ubuntu** — it's not officially supported, but it's the most common approach. On this system:

1. **Install `alien`** to convert the `.rpm` to `.deb`:

   ```bash
   sudo apt update && sudo apt install alien
   ```

2. **Convert and install**:

   ```bash
   alien --scripts -d oracle-database-xe-21c-1.0-1.ol8.x86_64.rpm
   sudo dpkg -i oracle-database-xe-21c-1.0-1.ol8.x86_64.deb
   ```

3. **Run the configuration script**:

   ```bash
   sudo /etc/init.d/oracle-xe-21c configure
   ```

> ⚠️ **Caveats**: This is a community workaround, not officially supported. Expect to manually resolve dependency issues (e.g., `libaio1`, `bc`). Some users report better luck with `rpm --nodeps` + manual link fixes instead of `alien`.

---

## Alternative (recommended as a simpler approach)

**Run Oracle XE in Docker** — avoids OS compatibility headaches entirely:

```bash
docker run -d --name oracle21c \
  -p 1521:1521 -p 5500:5500 \
  -e ORACLE_PDB=XE \
  -e ORACLE_PWD=your_password \
  container-registry.oracle.com/database/express:21.3.0-xe
```

This works cleanly on Ubuntu 24.04 and is much easier to maintain.

---

**Bottom line**: If you must install natively, go with the **OL8 `.rpm`** and use `alien`. But I'd recommend **Docker** instead — it's the path of least resistance on this system.

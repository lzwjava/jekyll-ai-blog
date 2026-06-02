---
audio: false
generated: true
lang: en
layout: post
title: Fixing typing-extensions Package Issue
translated: false
type: note
---

### How to Fix the "Cannot uninstall typing-extensions None" Error

When you encountered the error during your package installation with pip, it was due to an issue with uninstalling the `typing-extensions` package. The error message states:

```
error: uninstall-no-record-file
× Cannot uninstall typing-extensions None
╰─> The package's contents are unknown: no RECORD file was found for typing-extensions.
```

This error occurs because pip is trying to uninstall an existing installation of `typing-extensions` (likely to replace it with a version required by the packages you're installing), but it can't proceed because the RECORD file is missing. The RECORD file is a metadata file that pip uses to track the files installed by a package, so without it, pip doesn't know how to properly uninstall `typing-extensions`. The installation log also provides a helpful hint:

```
hint: You might be able to recover from this via: pip install --force-reinstall --no-deps typing-extensions==4.14.0
```

Below is a step-by-step solution to resolve this issue and successfully complete your package installation.

---

### Step 1: Understand the Problem
The log shows that pip is installing the following packages:
- `pyperclip`
- `typing-extensions`
- `packaging`
- `jmespath`

During this process, pip attempts to uninstall the existing `typing-extensions` installation because one of the packages you're installing (or an existing dependency) likely requires a specific version of `typing-extensions`. However, the uninstallation fails because the RECORD file for the current `typing-extensions` installation is missing or corrupted. This could happen if the package was installed improperly, the RECORD file was deleted, or the installation was interrupted in the past.

The "typing-extensions None" in the error message suggests that pip cannot determine the version of the existing installation, further indicating a problem with its metadata.

---

### Step 2: Fix the `typing-extensions` Installation
To resolve this, you need to repair the broken `typing-extensions` installation. The suggested command from the hint is the best approach:

```bash
pip install --force-reinstall --no-deps typing-extensions==4.14.0
```

#### What This Command Does:
- **`pip install`**: Installs the specified package.
- **`--force-reinstall`**: Forces pip to reinstall `typing-extensions`, even if it’s already present, overwriting the existing installation.
- **`--no-deps`**: Prevents pip from installing any dependencies of `typing-extensions`. Since `typing-extensions` is a standalone pure Python package with no dependencies, this flag ensures a clean reinstall without affecting other packages.
- **`typing-extensions==4.14.0`**: Specifies version 4.14.0, which is likely the version pip was trying to install when the error occurred.

Running this command will:
- Reinstall `typing-extensions` version 4.14.0.
- Create a proper RECORD file in the package’s directory (typically in `site-packages`).
- Fix the corrupted or incomplete installation.

#### Run the Command:
Open your terminal and execute:

```bash
pip install --force-reinstall --no-deps typing-extensions==4.14.0
```

After this command completes successfully, the `typing-extensions` package should be correctly installed with all necessary metadata.

---

### Step 3: Retry the Original Installation
Once `typing-extensions` is fixed, you can proceed with installing the packages you originally intended to install. Based on the log, it seems you were running a command like:

```bash
pip install pyperclip
```

This command likely triggered the installation of `pyperclip`, `typing-extensions`, `packaging`, and `jmespath` because `pyperclip` or another package has dependencies on them. Now that `typing-extensions` is properly installed, the uninstallation issue should no longer occur.

#### Run the Original Command:
Retry the installation by running:

```bash
pip install pyperclip
```

This should now complete without errors, installing all collected packages successfully.

---

### Why This Works
- The missing RECORD file prevented pip from uninstalling the old `typing-extensions` installation, causing the process to fail.
- Force-reinstalling `typing-extensions` with the specified version ensures that pip can manage the package correctly moving forward.
- The `--no-deps` flag keeps the fix isolated to `typing-extensions`, avoiding unnecessary changes to other packages.

---

### Additional Notes
- **Safety**: Since `typing-extensions` is a pure Python package and not a system-level dependency, force-reinstalling it is safe and won’t disrupt your Python environment.
- **Version Confirmation**: The hint specifies version 4.14.0, which is likely the version required by one of the packages you’re installing. If you need a different version, you can check the requirements of `pyperclip`, `packaging`, or `jmespath` (e.g., via their documentation or `pip show <package>` after installation).
- **Manual Cleanup (Not Recommended)**: You could manually delete the `typing-extensions` folder from `site-packages`, but this is riskier and unnecessary since `pip --force-reinstall` handles it cleanly.

---

### Final Steps
1. Fix `typing-extensions`:
   ```bash
   pip install --force-reinstall --no-deps typing-extensions==4.14.0
   ```
2. Install your packages:
   ```bash
   pip install pyperclip
   ```

After following these steps, the error should be resolved, and your package installation will complete successfully. If you encounter any further issues, feel free to share the updated log for additional assistance!

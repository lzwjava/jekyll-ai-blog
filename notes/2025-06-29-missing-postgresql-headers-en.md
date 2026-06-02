---
audio: false
generated: true
lang: en
layout: post
title: Missing libpq-fe.h for psycopg2
translated: false
type: note
---

When trying to install the Python package `psycopg2`, you encountered an error indicating that the wheel could not be built successfully. The key part of the error message is:

```
In file included from psycopg/adapter_asis.c:28:
./psycopg/psycopg.h:36:10: fatal error: libpq-fe.h: No such file or directory
   36 | #include <libpq-fe.h>
      |          ^~~~~~~~~~~~
compilation terminated.
```

This error occurs because the file `libpq-fe.h`, a header file from the PostgreSQL client library, is missing on your system. The `psycopg2` package requires this file to build from source, as it provides the interface to connect Python to PostgreSQL databases. Below, I’ll explain why this happens and provide a step-by-step solution to fix it.

---

### Why This Error Occurs

The `psycopg2` package is a PostgreSQL adapter for Python, and when you install it using `pip`, it attempts to compile its C extensions. These extensions depend on the PostgreSQL client library, specifically the development headers like `libpq-fe.h`. The error message confirms this:

```
It appears you are missing some prerequisite to build the package from source.
```

Your system, which appears to be a Debian-based Linux distribution (based on the use of `x86_64-linux-gnu-gcc`), lacks the necessary PostgreSQL development files. Without these, the compilation fails, preventing the wheel for `psycopg2` from being built.

The error also suggests two options:

1. Install the pre-built binary package `psycopg2-binary` via PyPI.
2. Install the missing prerequisites and build `psycopg2` from source.

Since your project specifies `psycopg2` (not `psycopg2-binary`) in the requirements file, and building from source may be necessary for compatibility or customization, we’ll focus on fixing the build process. However, I’ll also mention the binary option later for completeness.

---

### How to Fix the Error

To resolve this, you need to install the PostgreSQL client development package, which provides `libpq-fe.h` and other necessary files. Here’s how to do it:

#### Step 1: Identify Your System

Your build output includes `x86_64-linux-gnu-gcc`, indicating you’re likely using a Debian-based system like Ubuntu. The solution will be tailored to this, but I’ll note alternatives for other distributions later.

#### Step 2: Install the PostgreSQL Development Package

On Debian-based systems (e.g., Ubuntu), the package `libpq-dev` contains the PostgreSQL client library headers, including `libpq-fe.h`. Install it with the following command:

```bash
sudo apt-get update
sudo apt-get install libpq-dev
```

- **`sudo apt-get update`**: Ensures your package list is current.
- **`sudo apt-get install libpq-dev`**: Installs the development files for the PostgreSQL client library.

This package places `libpq-fe.h` in a standard location (typically `/usr/include/postgresql`), which the build process searches (as seen in your include path: `-I/usr/include/post每月

#### Step 3: Retry the Installation

Once `libpq-dev` is installed, retry installing your requirements:

```bash
pip install -r scripts/requirements/requirements.local.txt
```

This should now succeed, as the missing `libpq-fe.h` file will be available, allowing `psycopg2` to build its wheel.

---

### Verifying the Fix

If the installation still fails, check that the PostgreSQL headers are correctly installed:

- Run `pg_config --includedir` to see where the headers are located (e.g., `/usr/include/postgresql`).
- Ensure this matches the include path in the build command (`-I/usr/include/postgresql`).

Your build output shows `-DPG_VERSION_NUM=140018`, indicating it’s targeting PostgreSQL 14. The `libpq-dev` package is version-agnostic and should work with PostgreSQL 14 headers.

---

### Alternative: Use the Binary Package

If you don’t need to build `psycopg2` from source (e.g., for specific optimizations or compatibility), you can install the pre-built `psycopg2-binary` instead:

```bash
pip install psycopg2-binary
```

To use this in your project, update `scripts/requirements/requirements.local.txt` to replace `psycopg2` with `psycopg2-binary`. However, note that `psycopg2-binary` may have limitations (e.g., potential compatibility issues with certain PostgreSQL versions), so building from source is preferred if your project requires it.

---

### For Other Distributions

If you’re not on a Debian-based system, install the equivalent package:

- **Red Hat/CentOS/Fedora**: `sudo yum install postgresql-devel` or `sudo dnf install postgresql-devel`
- **Arch Linux**: `sudo pacman -S postgresql-libs`
- **macOS (with Homebrew)**: `brew install libpq`

Then, retry the `pip install` command.

---

### Summary

The error occurs because `libpq-fe.h` is missing, which is part of the PostgreSQL client development files. For your Debian-based system, installing `libpq-dev` with `sudo apt-get install libpq-dev` should resolve the issue. After that, re-run your `pip install` command, and `psycopg2` should build successfully. If you prefer a quicker fix and don’t need source compilation, use `psycopg2-binary` instead.

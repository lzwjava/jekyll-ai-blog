---
audio: false
generated: true
lang: en
layout: post
title: Fix psycopg2 by installing PostgreSQL
translated: false
type: note
---

The error you're encountering indicates that the `psycopg2` package requires the PostgreSQL `pg_config` executable to build from source, but it’s not found on your system. This means you need to install PostgreSQL on your macOS system to provide the necessary dependencies. Below are the steps to install PostgreSQL on macOS and resolve the issue.

### Steps to Install PostgreSQL on macOS

#### 1. **Install PostgreSQL Using Homebrew (Recommended)**

Homebrew is the easiest way to install and manage PostgreSQL on macOS.

1. **Install Homebrew (if not already installed)**:
   - Open the Terminal and run:

     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

   - Follow the on-screen instructions to complete the Homebrew installation.

2. **Install PostgreSQL**:
   - In the Terminal, run:

     ```bash
     brew install postgresql
     ```

   - This command installs PostgreSQL and its dependencies, including the `pg_config` executable needed for `psycopg2`.

3. **Start PostgreSQL**:
   - To start the PostgreSQL service, run:

     ```bash
     brew services start postgresql
     ```

   - Alternatively, to start it manually for a single session:

     ```bash
     pg_ctl -D /opt/homebrew/var/postgres start
     ```

4. **Verify Installation**:
   - Check if PostgreSQL is installed and running:

     ```bash
     psql --version
     ```

   - You should see the PostgreSQL version (e.g., `psql (PostgreSQL) 17.0`).
   - You can also log in to the PostgreSQL shell to confirm:

     ```bash
     psql -U $(whoami)
     ```

#### 2. **Install `psycopg2` After PostgreSQL**

Once PostgreSQL is installed, retry installing `psycopg2`. The `pg_config` executable should now be available in your PATH.

1. **Install `psycopg2`**:
   - Run:

     ```bash
     pip install psycopg2
     ```

   - If you’re using a requirements file, run:

     ```bash
     pip install -r scripts/requirements/requirements.local.txt
     ```

2. **Alternative: Install `psycopg2-binary` (Easier Option)**:
   - If you want to avoid building `psycopg2` from source (which requires PostgreSQL dependencies), you can install the precompiled `psycopg2-binary` package:

     ```bash
     pip install psycopg2-binary
     ```

   - Note: `psycopg2-binary` is not recommended for production environments due to potential compatibility issues, but it’s fine for development or testing.

#### 3. **Optional: Add `pg_config` to PATH (if needed)**

If the `pg_config` executable is still not found after installing PostgreSQL, you may need to add it to your PATH manually.

1. Locate `pg_config`:
   - Homebrew typically installs PostgreSQL in `/opt/homebrew/bin` (for Apple Silicon) or `/usr/local/bin` (for Intel Macs).
   - Verify the location:

     ```bash
     find /opt/homebrew -name pg_config
     ```

     or

     ```bash
     find /usr/local -name pg_config
     ```

2. Add to PATH:
   - If `pg_config` is found (e.g., in `/opt/homebrew/bin`), add it to your PATH by editing your shell configuration file (e.g., `~/.zshrc` or `~/.bash_profile`):

     ```bash
     echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
     ```

   - Apply the changes:

     ```bash
     source ~/.zshrc
     ```

3. Verify `pg_config`:
   - Run:

     ```bash
     pg_config --version
     ```

   - If it returns a version, the PATH is set correctly.

#### 4. **Troubleshooting**

- **Error Persists**: If `pip install psycopg2` still fails, ensure you have the necessary build tools:
  - Install Xcode Command Line Tools:

    ```bash
    xcode-select --install
    ```

  - Install `libpq` (PostgreSQL client library) explicitly if needed:

    ```bash
    brew install libpq
    ```

- **Python Version Compatibility**: Ensure your Python version (3.13 in your case) is compatible with `psycopg2`. If issues persist, consider using a virtual environment with a slightly older Python version (e.g., 3.11 or 3.12):

  ```bash
  python3.11 -m venv venv
  source venv/bin/activate
  pip install psycopg2
  ```

- **Check Homebrew**: Ensure Homebrew is up to date:

  ```bash
  brew update
  brew upgrade
  ```

#### 5. **Alternative Installation Methods (Optional)**

If you prefer not to use Homebrew, you can install PostgreSQL via:

- **Postgres.app**:
  - Download from [postgresapp.com](https://postgresapp.com/).
  - Follow the setup instructions to install and start PostgreSQL.
  - Add the `bin` directory (e.g., `/Applications/Postgres.app/Contents/Versions/latest/bin`) to your PATH as described above.
- **Official PostgreSQL Installer**:
  - Download the macOS installer from [postgresql.org](https://www.postgresql.org/download/macosx/).
  - Follow the installation wizard.

#### 6. **Retry Your Project**

After installing PostgreSQL and `psycopg2` (or `psycopg2-binary`), retry running your project or reinstalling the requirements:

```bash
pip install -r scripts/requirements/requirements.local.txt
```

### Additional Notes

- **Why the Error Happened**: The `psycopg2` package requires PostgreSQL development libraries (specifically `libpq`) to build from source. Installing PostgreSQL via Homebrew provides these libraries.
- **Production Considerations**: For production, use `psycopg2` (not `psycopg2-binary`) and ensure your PostgreSQL version matches the target environment.
- **Documentation**: For more details, refer to the `psycopg2` installation guide at [psycopg.org/docs/install.html](https://www.psycopg.org/docs/install.html).

If you encounter further issues, please share the specific error message, and I can help troubleshoot further!

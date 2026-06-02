---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Secure Database Configuration Strategies
translated: false
type: note
---

### Handling Sensitive Database Configuration in Python Projects

Managing sensitive information like database passwords and ports in configuration files is a common challenge in Python projects. The goal is to avoid committing secrets to version control (e.g., Git) while keeping deployment straightforward. Below, I'll compare the two approaches you mentioned: (1) using a template `config_example.ini` with `.gitignore` for the real file, and manual setup on servers like UAT; and (2) using GPG encryption to store encrypted values in `config.ini` and decrypt them at runtime. Both are secure if implemented correctly, but they trade off simplicity for automation.

#### Approach 1: Template Config + `.gitignore` + Manual Server Setup

This is a straightforward, low-tech method. You create a sample config file for developers and CI/CD pipelines, ignore the real one in Git, and handle the actual config manually on production-like environments (e.g., UAT servers).

**Steps to Implement:**

1. Create `config_example.ini` with placeholders:

   ```
   [database]
   host = localhost
   port = 5432  # Example port; replace with real one
   user = dbuser
   password = example_password  # Replace with real password
   database = mydb
   ```

2. Add the real `config.ini` to `.gitignore`:

   ```
   config.ini
   ```

3. In your Python code, load from `config.ini` (fall back to example if missing for dev):

   ```python
   import configparser
   import os

   config = configparser.ConfigParser()
   config_file = 'config.ini' if os.path.exists('config.ini') else 'config_example.ini'
   config.read(config_file)

   db_host = config['database']['host']
   db_port = config['database']['port']
   db_user = config['database']['user']
   db_password = config['database']['password']
   db_name = config['database']['database']
   ```

4. For UAT servers: Manually copy `config.ini` with real values (e.g., via SCP or Ansible) during deployment. Developers can copy `config_example.ini` to `config.ini` and fill in locally.

**Pros:**

- Simple—no extra libraries or keys to manage.
- No runtime overhead (decryption).
- Easy for small teams; works well with manual deploys.

**Cons:**

- Manual setup on each server increases error risk (e.g., forgetting to update password).
- Not ideal for automated CI/CD; requires secure secret injection (e.g., via environment variables in pipelines).
- If someone commits `config.ini` by mistake, secrets are exposed.

This approach is great for early-stage projects or when encryption feels overkill.

#### Approach 2: GPG Encryption for Config Values

Here, you encrypt sensitive fields (e.g., password) using GPG, store the encrypted blob in `config.ini`, and decrypt it in your code at runtime. The encrypted file can be committed to Git safely, as long as your private key is never shared.

**Steps to Implement:**

1. Install GPG on your system (it's standard on Linux/Mac; use Gpg4win on Windows). Generate a key pair if needed:

   ```
   gpg --gen-key  # Follow prompts for your key
   ```

2. Encrypt the sensitive value (e.g., password) into a file:

   ```
   echo "real_password_here" | gpg --encrypt --recipient your-email@example.com -o encrypted_password.gpg
   ```

   - This creates `encrypted_password.gpg`. You can base64-encode it for easy storage in INI:

     ```bash
     base64 encrypted_password.gpg > encrypted_password.b64
     ```

3. Update `config.ini` to include the encrypted (and base64-encoded) value. Commit this—it's safe:

   ```
   [database]
   host = localhost
   port = 5432
   user = dbuser
   password_encrypted = <base64-encoded-encrypted-blob-here>  # From encrypted_password.b64
   database = mydb
   ```

4. In your Python code, decrypt using the `gnupg` library (install via `pip install python-gnupg` for dev, but assume it's available):

   ```python
   import configparser
   import gnupg
   import base64
   import tempfile
   import os

   config = configparser.ConfigParser()
   config.read('config.ini')  # Can commit this safely

   # Decrypt password
   gpg = gnupg.GPG()  # Assumes GPG is installed and key is available
   encrypted_b64 = config['database']['password_encrypted']
   encrypted_data = base64.b64decode(encrypted_b64)

   with tempfile.NamedTemporaryFile(delete=False) as tmp:
       tmp.write(encrypted_data)
       tmp.flush()
       decrypted = gpg.decrypt_file(None, passphrase=None, extra_args=['--batch', '--yes'], output=tmp.name)
       if decrypted.ok:
           db_password = decrypted.data.decode('utf-8').strip()
       else:
           raise ValueError("Decryption failed")

   os.unlink(tmp.name)  # Clean up

   db_host = config['database']['host']
   db_port = config['database']['port']
   db_user = config['database']['user']
   db_name = config['database']['database']

   # Now use db_password...
   ```

5. For UAT servers: Deploy `config.ini` as-is (via Git or copy). Ensure the GPG private key is securely placed on the server (e.g., via Ansible vault or manual secure copy). The code will decrypt on startup.

**Pros:**

- Encrypted config can be version-controlled—no `.gitignore` needed for secrets.
- Automates deployment; works with CI/CD (just sync the key securely).
- Auditable: Changes to encrypted values are tracked.

**Cons:**

- Requires GPG setup and key management (e.g., rotate keys periodically; never commit private keys).
- Runtime dependency on GPG and `python-gnupg`; decryption fails if key is missing.
- Slightly more complex for beginners; potential perf hit on decrypt (negligible for passwords).

Use this for teams with automated deploys or when sharing configs across environments.

#### Comparison Table

| Aspect              | Template + .gitignore + Manual | GPG Encryption + Runtime Decrypt |
|---------------------|--------------------------------|----------------------------------|
| **Security**       | High if manual steps are careful; risk of human error. | High; secrets never in plain text. |
| **Ease of Setup**  | Very easy (no tools needed).  | Moderate (GPG + library).       |
| **Version Control**| Template committed; real file ignored. | Full config committed (encrypted). |
| **Deployment**     | Manual per server (e.g., SCP).| Automated (key sync needed).    |
| **Overhead**       | None.                         | Minor (decrypt on load).        |
| **Best For**       | Small/manual projects.        | Automated/CI/CD pipelines.      |

#### Recommendations

- Start with **Approach 1** if your project is simple or team is small—it's battle-tested.
- Switch to **Approach 2** (or evolve to env vars/secrets managers like AWS SSM/HashiCorp Vault) for scaling.
- Always combine with env vars for overrides (e.g., `os.getenv('DB_PASSWORD', db_password)`).
- Test decryption in a staging env before UAT.

If you share more details (e.g., your deployment tool or full config), I can refine the code!

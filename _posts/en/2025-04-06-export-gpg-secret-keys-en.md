---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Exporting GPG Secret Keys Securely
translated: false
type: note
---

### Exporting Secret Keys with GPG in Armored Format

GPG (GNU Privacy Guard) allows exporting secret (private) keys in an armored ASCII format, which saves them as a human-readable `.asc` file (not binary). This is useful for backups, transfers, or importing on another machine.

**Important Warning:** Secret keys contain sensitive information. Export them only when necessary, encrypt the output file if storing or transmitting, and delete the export after use to avoid unintentional leaks. Never share secret keys publicly.

#### Basic Command Structure
To export a secret key for a specific user ID (email or name associated with the key), use:

```
gpg --export-secret-keys --armor [KEY_ID] > filename.asc
```

- `KEY_ID`: The key fingerprint, short ID, email, or name. You can list your keys with `gpg --list-secret-keys`.
- `--armor`: Outputs in armored (ASCII) format instead of binary.
- `> filename.asc`: Redirects output to a file (e.g., `my_secret_key.asc`). Omit this to print to the terminal.

#### Step-by-Step Usage Example
1. **List your secret keys** to find the KEY_ID:
   ```
   gpg --list-secret-keys
   ```
   Example output:
   ```
   sec   rsa3072/ABC12345 2023-01-01 [SC] [expires: 2025-01-01]
         Key fingerprint = 1234 5678 ABCD EF01 2345 6789 ABCD EF01 2345 6789
   uid                 [ultimate] Your Name <your@email.com>
   ```

   Here, `ABC12345` is the short key ID, or use the full fingerprint `ABCDEF0123456789ABCDEF0123456789` for precision.

2. **Export the secret key**:
   ```
   gpg --export-secret-keys --armor ABC12345 > my_secret_key.asc
   ```

3. **Verify the export** (optional):
   ```
   cat my_secret_key.asc
   ```
   The file should start with `-----BEGIN PGP PRIVATE KEY BLOCK-----` and end with `-----END PGP PRIVATE KEY BLOCK-----`.

#### Additional Options
- **Export all secret keys**: Omit the KEY_ID to export all:
  ```
  gpg --export-secret-keys --armor > all_secret_keys.asc
  ```
- **With passphrase protection**: GPG will prompt for your passphrase if the key is encrypted (default).
- **If you need public keys instead**: Use `--export` (for public keys only).

For full documentation, refer to the GPG man page: `man gpg`. If you're new to GPG, generate a key first with `gpg --gen-key`.

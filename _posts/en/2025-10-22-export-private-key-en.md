---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Exporting a GPG Private Key
translated: false
type: note
---

### Exporting a GPG Private Key from the Server

To export your private key, you'll need access to the server via SSH or a terminal. GPG private keys are sensitive—handle them securely and delete the exported file after transfer.

1. **List your secret keys** (to identify the key by email or key ID):

   ```
   gpg --list-secret-keys
   ```

   Look for the entry like `sec   rsa4096/ABC123DEF456 2023-01-01 [SC]`. Note the email or key ID (e.g., `user@example.com` or `ABC123DEF456`).

2. **Export the private key** (use `--armor` for ASCII format, easier to transfer):

   ```
   gpg --export-secret-keys --armor user@example.com > private-key.asc
   ```

   - Replace `user@example.com` with your actual email or key ID.
   - This creates `private-key.asc` in your current directory.
   - If you have multiple keys, specify the key ID for precision: `gpg --export-secret-keys --armor ABC123DEF456 > private-key.asc`.
   - **Security note**: This exports the key *without* its passphrase. You'll need to enter the passphrase on import if prompted.

3. **Securely transfer the file** to your local laptop:
   - Use `scp` (from your local machine):

     ```
     scp user@server-ip:/path/to/private-key.asc ./
     ```

     Replace `user@server-ip` with your server details and `/path/to/` with the actual path.
   - Alternatives: `rsync` for larger files or SFTP for a GUI option. Avoid email or unsecured channels.

4. **Clean up on the server**:

   ```
   rm private-key.asc
   ```

   Verify it's gone with `ls`.

### Importing the GPG Private Key on Your Local Laptop

Assuming you have GPG installed (e.g., via `apt install gnupg` on Linux, `brew install gnupg` on macOS, or Chocolatey on Windows).

1. **Import the key**:

   ```
   gpg --import private-key.asc
   ```

   - You'll see output like "gpg: key ABC123DEF456: secret key imported".
   - If prompted for a passphrase during import, enter the original one.

2. **Verify the import**:

   ```
   gpg --list-secret-keys
   ```

   Your key should now appear under "sec".

3. **Optional: Set trust level** (if using for signing/email):

   ```
   gpg --edit-key user@example.com
   ```

   - In the prompt, type `trust`, select "ultimate" (option 5), then `save` and `quit`.
   - This marks the key as fully trusted on your local machine.

### Tips and Warnings

- **Passphrase**: Always use a strong one. If you forget it, the key becomes unusable.
- **Subkeys**: If your key has subkeys (e.g., for encryption), export them too with `--export-secret-subkeys`.
- **Backup**: Store exports in a secure vault (e.g., encrypted drive).
- **Versions**: Tested on GPG 2.x; works similarly on 1.x.
- For more details, see the official GPG docs: [GnuPG Manual](https://www.gnupg.org/documentation/manuals/gnupg/).

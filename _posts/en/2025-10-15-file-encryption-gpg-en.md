---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Encrypting Files with GPG
translated: false
type: note
---

### Encrypting a File with Your GPG Key

Your GPG key listing shows a public key (pub) with the fingerprint `982740390B5D33E90B6B6133892BC5A4789B71CD` associated with your email `lzwjava@gmail.com`. To encrypt a file using this key (so only you can decrypt it with your private key), follow these steps in your terminal:

1. **Navigate to the directory** containing the file you want to encrypt (e.g., if your file is `secret.txt`):
   ```
   cd ~/path/to/your/file
   ```

2. **Encrypt the file** using the `--encrypt` option and specify the recipient (your email or key ID). This creates an encrypted `.gpg` file.

   - Using your email (simpler):
     ```
     gpg --encrypt --recipient lzwjava@gmail.com secret.txt
     ```

   - Using the key ID (full fingerprint):
     ```
     gpg --encrypt --recipient 982740390B5D33E90B6B6133892BC5A4789B71CD secret.txt
     ```

   This outputs `secret.txt.gpg`, which is the encrypted version. The original `secret.txt` remains unchanged.

3. **Verify the encryption** (optional):
   ```
   gpg --list-packets secret.txt.gpg
   ```
   This shows details about the encrypted packet.

### Decrypting the File (For Later Reference)

To decrypt it back (only possible with your private key and passphrase):
```
gpg --decrypt secret.txt.gpg > secret.txt.decrypted
```
Enter your passphrase when prompted.

### Tips
- **Symmetric encryption** (if you don't need a recipient key, just a passphrase): Use `gpg -c secret.txt` instead.
- **Encrypt and sign** (to prove it's from you): Add `--sign` to the encrypt command, e.g., `gpg --encrypt --sign --recipient lzwjava@gmail.com secret.txt`.
- If you encounter errors (e.g., key not trusted), run `gpg --edit-key lzwjava@gmail.com` and use `trust` to set it to ultimate.
- Always back up your `~/.gnupg` directory for key safety.

For more details, check the GPG manual: [GPG Documentation](https://www.gnupg.org/documentation/manpage.html).

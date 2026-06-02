---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Verifying GPG Digital Signatures
translated: false
type: note
---

### Verifying Signatures in GPG

GnuPG (GPG) allows you to verify digital signatures to ensure a file or message hasn't been tampered with and comes from the claimed sender. Verification requires the signer's public key in your keyring. Below are the steps and commands for common scenarios.

#### Prerequisites
1. **Install GPG**: Ensure GnuPG is installed on your system (e.g., via `apt install gnupg` on Debian-based systems or `brew install gnupg` on macOS).
2. **Import the signer's public key**: You need the public key of the person or entity that signed the file. Download it from a keyserver or file, then import it:
   ```
   gpg --import public-key.asc
   ```
   (Replace `public-key.asc` with the actual key file. If it's from a keyserver, use `gpg --keyserver keyserver.ubuntu.com --recv-keys KEYID` where `KEYID` is the key's fingerprint or ID.)

#### Verification Steps
The exact command depends on how the signature was created (e.g., inline in the file or detached).

1. **Verify a detached signature** (common for files like software releases; signature is in a separate `.sig` file):
   ```
   gpg --verify signature.sig original-file
   ```
   - Example output for a good signature:
     ```
     gpg: Signature made [date] using [key type] key ID [KEYID]
     gpg: Good signature from "[Name] <email@example.com>"
     ```
   - If the key isn't trusted, you may see a warning like "This key is not certified with a trusted signature!" You can adjust trust levels with `gpg --edit-key KEYID` and then `trust`.

2. **Verify an inline-signed file** (the signature is embedded in the file, often binary):
   - To check the signature only:
     ```
     gpg --verify signed-file
     ```
   - To verify and extract the original content:
     ```
     gpg --output original-file --decrypt signed-file
     ```
     This will prompt for any passphrase if encrypted, but for signatures alone, it just verifies.

3. **Verify a clearsigned message** (human-readable text with ASCII-armored signature, common in emails or READMEs):
   ```
   gpg --verify clearsigned-file.txt
   ```
   The output will show the signature status without altering the file.

#### Troubleshooting
- **"No public key" error**: Import the key as shown above.
- **Bad signature**: The file may have been altered—redownload it.
- **Key validity**: Check key details with `gpg --list-keys` or verify fingerprints match the official source.
- For batch verification or scripting, add `--batch --exit-on-status-write-error`.

For more details on signing or advanced options, see the official manual.

[Making and verifying signatures - GnuPG Manual](https://www.gnupg.org/gph/en/manual/x135.html)

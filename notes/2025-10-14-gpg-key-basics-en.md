---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: GPG Key Management Basics
translated: false
type: note
---

## Introduction to GPG Key Management

GPG (GNU Privacy Guard) is a free implementation of the OpenPGP standard for secure communication, used for encrypting, signing, and verifying data. At its core is **public-key cryptography**, where each user has a **public key** (shared openly for encryption and verification) and a **private key** (kept secret for decryption and signing). Key management involves creating, distributing, maintaining, and securing these keys to prevent tampering, compromise, or misuse. Poor management can lead to attacks like key substitution, where an attacker replaces your key with theirs to intercept communications.

The "web of trust" model in GPG allows users to certify each other's keys, building a network of verified identities. Keys are stored in **keyrings** (public and private files, e.g., `pubring.kbx` and `secring.gpg` in older versions, or unified in newer ones). Always back up your private keys and use strong passphrases.

## Key Structure

A GPG keypair isn't just one key—it's a bundle:

- **Primary key**: A master signing key (e.g., RSA or DSA) used for certifying (signing) other keys and self-signing your key's components.
- **Subkeys**: Optional subordinate keys for specific tasks:
  - Signing subkey: For signing messages.
  - Encryption subkey: For encrypting data (often rotated periodically).
  - Authentication subkey: For SSH or similar.
- **User IDs (UIDs)**: Strings like "Alice (Comment) <alice@example.com>" linking the key to a real identity. Multiple UIDs can exist for different roles.
- **Self-signatures**: The primary key signs its own components to prevent tampering.

View a key's structure interactively:

```
gpg --edit-key <key-id-or-email>
```

Inside the menu, use `check` to verify self-signatures or `toggle` to see private parts (if available).

## Generating Keys

Start with a primary keypair. Use the interactive method for beginners:

1. Run `gpg --full-gen-key` (or `--gen-key` for defaults).
2. Choose key type (default: RSA for both signing and encryption).
3. Select key size (e.g., 4096 bits for stronger security; minimum 2048 recommended).
4. Set expiration (e.g., 1y for one year; "0" for never—avoid indefinite if possible).
5. Enter user ID (name, email).
6. Set a strong passphrase (20+ characters, mixed case/symbols).

For quick generation (non-interactive):

```
gpg --quick-generate-key "Alice <alice@example.com>" rsa default 1y
```

After generation, create a **revocation certificate** (a file to invalidate your key if compromised):

```
gpg --output revoke.asc --gen-revoke <your-key-id>
```

Store this safely (e.g., printed in a vault)—don't share it until needed.

To add subkeys or UIDs later:

- Enter `gpg --edit-key <key-id>`, then `addkey` (for subkey) or `adduid` (for UID). These are self-signed automatically.

## Listing and Viewing Keys

- List public keys: `gpg --list-keys` (or `--list-public-keys`).
- List private keys: `gpg --list-secret-keys`.
- Detailed view: `gpg --list-keys --with-subkey-fingerprint <key-id>` (shows fingerprints for subkeys).

Output shows key ID (short/long), creation/expiration dates, capabilities (e.g., `[SC]` for sign/certify), and UIDs.

## Exporting and Importing Keys

**Exporting** shares your public key or backs up private ones:

- Public key: `gpg --armor --export <key-id> > mykey.asc` (ASCII-armored for email).
- Private key (backup only): `gpg --armor --export-secret-keys <key-id> > private.asc`.
- To a keyserver: `gpg --keyserver hkps://keys.openpgp.org --send-keys <key-id>`.

**Importing** adds others' keys to your public keyring:

- `gpg --import <file.asc>` (merges with existing; adds new signatures/subkeys).
- From keyserver: `gpg --keyserver hkps://keys.openpgp.org --recv-keys <key-id>`.

After importing, verify with `gpg --edit-key <key-id>` and `check` for self-signatures.

## Signing and Certifying Keys

To build trust:

- Sign a key (certify it's valid): `gpg --sign-key <other-key-id>` (or `lsign-key` for local-only).
- Quick sign: `gpg --quick-sign-key <fingerprint> "User ID"`.
- Set trust level: In `--edit-key`, use `trust` (e.g., "5" for ultimate trust).

This creates signatures on the key, visible in listings. The web of trust calculates validity based on your trust in signers.

## Revoking Keys

Revocation invalidates a key or component without deleting it, ensuring others see it's no longer valid:

- Full key: Import your revocation cert: `gpg --import revoke.asc`, then export/send the updated key.
- Subkey/UID: In `--edit-key`, select with `key 1` or `uid 1`, then `revkey` or `revuid`.
- Quick revoke UID: `gpg --quick-revoke-uid <key-id> <uid-to-revoke>`.

Reasons for revocation: compromised, no longer used, superseded. Always publish revoked keys.

## Best Practices

- **Security**: Use hardware tokens (e.g., YubiKey) for private keys. Rotate encryption subkeys yearly (`gpg --quick-add-key <fingerprint> rsa encr 1y`). Change passphrases regularly (`gpg --change-passphrase <key-id>`).
- **Expiration**: Set reasonable expirations (1-2 years) to force updates and detect compromises.
- **Distribution**: Share public keys via keyservers or directly; verify fingerprints in person or via trusted channels to avoid man-in-the-middle attacks.
- **Backup**: Export private keys to encrypted storage. Generate revocation certs immediately.
- **Cleanup**: Use `gpg --edit-key` with `clean` to remove invalid signatures.
- **Updates**: As of 2025, GnuPG 2.5+ supports quantum-resistant algorithms (e.g., `--quick-generate-key ... pqc`); consider migrating for future-proofing.
- **Common Pitfalls**: Never share private keys. Avoid indefinite expirations. Test revocations in a sandbox.

For hands-on, experiment in a test directory with `gpg --homedir ./test-gpg`.

[GnuPG Handbook: Key Management](https://www.gnupg.org/gph/en/manual/c235.html)
[GNU Privacy Guard Manual: OpenPGP Key Management](https://www.gnupg.org/documentation/manuals/gnupg/OpenPGP-Key-Management.html)
[GnuPG Getting Started](https://www.gnupg.org/gph/en/manual/c14.html)

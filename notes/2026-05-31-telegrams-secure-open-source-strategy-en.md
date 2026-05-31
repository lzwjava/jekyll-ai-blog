---
audio: false
generated: true
image: false
lang: en
layout: post
title: Telegram's Secure Open-Source Strategy
translated: false
type: note
---

Here's the full breakdown of how Telegram safely open-sources their code:

---

## 1. API Keys — Committed to the Repo (By Design)

The Telegram API ID and hash are **intentionally public**. They're committed right in the repo:

```json
// build-system/appstore-configuration.json
{
    "bundle_id": "ph.telegra.Telegraph",
    "api_id": "8",
    "api_hash": "7245de8e747a0d6fbe11f7cc14fcc0bb",
    "team_id": "C67CF9S4VU",
    "appstore_id": "686449807"
}
```

And also in the example Bazel config:

```python
// build-system/example-configuration/variables.bzl
telegram_api_id = "8"
telegram_api_hash = "7245de8e747a0d6fbe11f7cc14fcc0bb"
```

**Why this is safe:** Telegram's API uses a challenge-response protocol (MTProto). The `api_id` and `api_hash` are public identifiers — they identify your app to Telegram's servers, like a client ID. They don't authenticate you. Authentication happens via phone number + SMS code + MTProto key exchange. Every third-party Telegram client (Pyrogram, Telethon, etc.) uses these same values. There's even a [public list](https://github.com/nicegram/nicegram-ios/blob/main/Nicegram/Nicegram-API-Keys.plist) of API keys for other clients.

The template for third-party developers uses placeholders:

```json
// build-system/template_minimal_development_configuration.json
{
    "api_id": "{! get one at https://my.telegram.org/apps !}",
    "api_hash": "{! get one at https://my.telegram.org/apps !}",
    "team_id": "{! check README.md !}"
}
```

---

## 2. Code Signing — Encrypted Git Repo + Environment Password

This is the real secret management. Provisioning profiles and certificates are stored in a **separate private git repo** (the "fastlane match" repo), encrypted with AES-256.

The build system fetches and decrypts them at build time:

```python
# build-system/Make/Make.py line 422
password = os.getenv('TELEGRAM_CODESIGNING_GIT_PASSWORD')
if password is None:
    print('TELEGRAM_CODESIGNING_GIT_PASSWORD environment variable is not set')
    sys.exit(1)

private_key = os.getenv('TELEGRAM_CODESIGNING_PRIVATE_KEY')

profile_source = GitCodesigningSource(
    repo_url=arguments.gitCodesigningRepository,  # e.g. git@gitlab.com:peter-iakovlev/fastlanematch.git
    private_key=private_key,
    team_id=build_configuration.team_id,
    bundle_id=build_configuration.bundle_id,
    codesigning_type=arguments.gitCodesigningType,  # development, adhoc, appstore, enterprise
    password=password,
    always_fetch=not arguments.gitCodesigningUseCurrent
)
```

The encrypted repo is cloned, then each `.mobileprovision`, `.cer`, and `.p12` file is decrypted:

```python
# build-system/Make/BuildConfiguration.py
def decrypt_codesigning_directory_recursively(source_base_path, destination_base_path, password):
    for file_name in os.listdir(source_base_path):
        source_path = source_base_path + '/' + file_name
        destination_path = destination_base_path + '/' + file_name
        allowed_file_extensions = ['.mobileprovision', '.cer', '.p12']
        if os.path.isfile(source_path) and any(source_path.endswith(ext) for ext in allowed_file_extensions):
            decrypt_match_data(source_path, destination_path, password)
        elif os.path.isdir(source_path):
            os.makedirs(destination_path, exist_ok=True)
            decrypt_codesigning_directory_recursively(source_path, destination_path, password)
```

---

## 3. Custom AES-256-GCM Decryption (No OpenSSL Dependency)

They wrote their own AES-256 implementation in pure Python to decrypt the codesigning data — supports both V1 (AES-CBC, OpenSSL legacy) and V2 (AES-GCM, fastlane match modern format):

```python
# build-system/Make/DecryptMatch.py
_V1_PREFIX = b"Salted__"
_V2_PREFIX = b"match_encrypted_v2__"

def _decrypt_stored(stored_data, password):
    if stored_data.startswith(_V2_PREFIX):
        salt = stored_data[20:28]
        auth_tag = stored_data[28:44]
        ciphertext = stored_data[44:]
        material = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            10_000,                    # 10k PBKDF2 iterations
            dklen=32 + 12 + 24,       # 256-bit key + 96-bit IV + 192-bit AAD
        )
        key = material[0:32]
        iv = material[32:44]
        aad = material[44:68]
        return _aes_gcm_decrypt(ciphertext, key, iv, aad, auth_tag)

    if stored_data.startswith(_V1_PREFIX):
        salt = stored_data[8:16]
        ciphertext = stored_data[16:]
        key, iv = _evp_bytes_to_key(password, salt, 'md5', 32, 16)
        return _aes_cbc_decrypt(ciphertext, key, iv)
```

V2 uses PBKDF2-HMAC-SHA256 with 10,000 iterations for key derivation, then AES-256-GCM for authenticated encryption. The GCM auth tag prevents tampering.

---

## 4. Build Variable Injection — Bazel `variables.bzl` Generated at Build Time

The configuration JSON is parsed by `BuildConfiguration.py` and written to a Bazel `.bzl` file that's **generated at build time, not committed**:

```python
# build-system/Make/BuildConfiguration.py
def write_to_variables_file(self, bazel_path, use_xcode_managed_codesigning, aps_environment, path):
    string = ''
    string += 'telegram_api_id = "{}"\n'.format(self.api_id)
    string += 'telegram_api_hash = "{}"\n'.format(self.api_hash)
    string += 'telegram_team_id = "{}"\n'.format(self.team_id)
    string += 'telegram_is_internal_build = "{}"\n'.format(self.is_internal_build)
    # ... writes to a file that Bazel imports
```

The BUILD file then injects these as **compiler flags** (not runtime values):

```python
# submodules/BuildConfig/BUILD
load("@build_configuration//:variables.bzl", "telegram_api_id", "telegram_api_hash", ...)

objc_library(
    name = "BuildConfig",
    copts = [
        "-DAPP_CONFIG_API_ID={}".format(telegram_api_id),
        "-DAPP_CONFIG_API_HASH=\\\"{}\\\"".format(telegram_api_hash),
        "-DAPP_CONFIG_IS_INTERNAL_BUILD={}".format(telegram_is_internal_build),
        "-DAPP_CONFIG_IS_APPSTORE_BUILD={}".format(telegram_is_appstore_build),
    ],
)
```

The API hash becomes a C string literal baked into the binary at compile time — it's not read from a file at runtime.

---

## 5. Three Codesigning Sources — Pick Your Path

The build system supports three ways to provide signing identities:

```python
# build-system/Make/Make.py
if arguments.gitCodesigningRepository is not None:
    # Path A: Encrypted git repo (Telegram's internal CI)
    profile_source = GitCodesigningSource(...)
elif arguments.codesigningInformationPath is not None:
    # Path B: Local directory (developer's own certs)
    profile_source = DirectoryCodesigningSource(...)
elif arguments.xcodeManagedCodesigning:
    # Path C: Xcode automatic signing (simplest, for simulator/dev)
    profile_source = XcodeManagedCodesigningSource()
```

Path A is what Telegram uses internally — the encrypted `fastlanematch` repo. Path B is for developers who have their own Apple Developer certs. Path C is for simulator-only builds (no signing needed).

For simulator-only builds, you can skip codesigning entirely:

```sh
python3 build-system/Make/Make.py --overrideXcodeVersion \
    generateProject \
    --configurationPath=build-system/template_minimal_development_configuration.json \
    --disableProvisioningProfiles    # <-- this flag
```

---

## 6. Environment Variables — The Actual Secrets

The only real secrets are:

| Secret | Where it lives | What it protects |
|--------|---------------|-----------------|
| `TELEGRAM_CODESIGNING_GIT_PASSWORD` | `~/.zshrc` (developer machine) | Decrypts the codesigning repo |
| `TELEGRAM_CODESIGNING_PRIVATE_KEY` | Environment (CI) | SSH key for the codesigning repo |
| Apple Developer certs (`.p12`) | Encrypted in the codesigning repo | Code signing identity |
| Provisioning profiles (`.mobileprovision`) | Encrypted in the codesigning repo | App distribution entitlements |

None of these are in the open-source repo. The `.gitignore` doesn't even need to list them because they live in a completely separate repository.

---

## 7. The `build-input/` Directory — Generated, Not Committed

The `build-input/` directory is in `.gitignore`:

```
build-input/*
```

This is where the build system writes:
- `build-input/data/variables.bzl` — generated from the configuration JSON
- `build-input/configuration-repository-workdir/` — cloned + decrypted codesigning repo

This directory is ephemeral — generated fresh each build, never committed.

---

## Summary: The Security Model

```
┌─────────────────────────────────────────────────────────┐
│  OPEN SOURCE REPO (Telegram-iOS)                        │
│                                                         │
│  ✅ api_id, api_hash — public, by design                │
│  ✅ All source code — open source                       │
│  ✅ Build system (Bazel, Make.py) — open source         │
│  ✅ AES decryption code — open source                   │
│  ✅ Template config with placeholders                   │
│  ❌ No signing certs, no provisioning profiles          │
│  ❌ No passwords, no SSH keys                           │
│  ❌ No build-input/ directory                           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  PRIVATE REPO (fastlanematch)                           │
│                                                         │
│  🔒 Encrypted .mobileprovision files (AES-256-GCM)     │
│  🔒 Encrypted .p12 certificates                        │
│  🔒 Encrypted .cer files                               │
│  🔒 Decrypted only with TELEGRAM_CODESIGNING_GIT_PWD   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  DEVELOPER MACHINE / CI                                 │
│                                                         │
│  🔑 TELEGRAM_CODESIGNING_GIT_PASSWORD in ~/.zshrc       │
│  🔑 TELEGRAM_CODESIGNING_PRIVATE_KEY (SSH key)          │
│  🔑 Apple Developer account                             │
└─────────────────────────────────────────────────────────┘
```

The key insight: **the code is safe to open-source because the secrets aren't in the code**. The API keys are public by protocol design. The signing certs are in a separate encrypted repo. The decryption password lives in the developer's shell environment. The build system orchestrates all of this at build time, generating ephemeral files that are never committed.
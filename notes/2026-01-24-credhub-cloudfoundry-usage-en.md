---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: CredHub in Cloud Foundry Usage
translated: false
type: note
---

Question: How to use CredHub in Cloud Foundry?

Answer:

**CredHub** is the centralized secrets management component in many Cloud Foundry deployments (especially Tanzu Application Service / VMware Tanzu Platform, PAS, PCF). It stores and manages credentials such as passwords, certificates, keys, JSON blobs, and more securely.

There are two main ways developers interact with CredHub:

1. **Indirectly (recommended for most apps)** — via a CredHub Service Broker (creates/binds service instances that deliver secrets to your app via `VCAP_SERVICES` without exposing them in `cf env`).
2. **Directly** — using the CredHub CLI or API (for admins, automation, or advanced use cases).

### 1. Using CredHub via Service Broker (Most Common for Applications)

In environments where the **CredHub Service Broker** is installed (common in Tanzu Application Service), follow these steps:

- List available services (look for something like `credhub`, `credhub-secrets`, or similar):

  ```bash
  cf marketplace
  ```

- Create a CredHub service instance:

  ```bash
  # Example: create a simple value secret
  cf create-service credhub default my-secret-service \
    -c '{"type":"value", "name":"/my-org/my-app/api-key", "value":"sk_live_xyz123"}'

  # Or generate a password automatically
  cf create-service credhub default my-db-password \
    -c '{"type":"password", "name":"/my-org/my-app/db-pass", "length":32}'
  ```

  Common credential types: `value`, `password`, `certificate`, `rsa`, `ssh`, `user`, `json`.

- Bind the service to your app:

  ```bash
  cf bind-service my-app my-secret-service
  cf restage my-app
  ```

- In your application, read from `VCAP_SERVICES` (credentials appear under a user-provided-like structure, but backed by CredHub):

  ```json
  {
    "credhub": [
      {
        "name": "my-secret-service",
        "credentials": {
          "credential": "/my-org/my-app/api-key",
          "version": "..."
        }
      }
    ]
  }
  ```

  Many modern buildpacks / libraries automatically interpolate the real value from CredHub at runtime using the instance credentials (mTLS cert/key from `/etc/cf-instance-credentials/`).

  **Note:** In some setups you see only a reference (`/path/to/secret`) in `VCAP_SERVICES`. The app container uses CredHub interpolation automatically via the platform.

### 2. Using the CredHub CLI (Direct Access – Admin / Debugging / Scripting)

Install the CredHub CLI:

```bash
# macOS (Homebrew)
brew install cloudfoundry/tap/credhub-cli

# Or download binary from https://github.com/cloudfoundry-incubator/credhub-cli/releases
```

Authenticate (target your CredHub instance):

```bash
# Usually provided by your platform team (often same UAA as cf login)
credhub login --client-id <uaa-client-id> --client-secret <uaa-client-secret>
# OR use cf oauth-token as bearer
credhub api https://credhub.service.cf.internal:8844   # internal URL (from inside CF)
credhub login --token "$(cf oauth-token | cut -d' ' -f2)"
```

Common commands:

```bash
# Set a simple value
credhub set -n /my-org/my-app/api-key -t value -v "sk_live_xyz123"

# Generate a random password
credhub generate -n /my-org/my-app/db-pass -t password -l 32

# Generate a certificate
credhub generate -n /my-org/my-app/cert -t certificate \
  --common-name myapp.example.com --alternative-names "*.example.com"

# Get a credential
credhub get -n /my-org/my-app/api-key

# Find credentials
credhub find -p /my-org/my-app/

# Delete
credhub delete -n /my-org/my-app/old-key
```

### Quick Comparison: User-Provided vs CredHub

| Feature                  | User-Provided Service (`cf cups`) | CredHub (via Broker or Direct) |
|--------------------------|------------------------------------|--------------------------------|
| Visibility in `cf env`   | Redacted (mostly)                  | Reference only or interpolated |
| Rotation support         | Manual                             | Built-in regeneration          |
| Central auditing         | No                                 | Yes                            |
| Generation (passwords, certs) | No                           | Yes                            |
| Best for                 | Simple, non-enterprise setups      | Enterprise, compliance         |

Ask your platform operators:

- Is the CredHub Service Broker available in your marketplace?
- What is the exact service offering name?
- What UAA client credentials or mTLS setup is needed for direct CLI access?

References:

- [CredHub Documentation – Cloud Foundry Docs](https://docs.cloudfoundry.org/credhub/index.html)
- [Use CredHub Secrets Management – Broadcom Techdocs](https://techdocs.broadcom.com/us/en/vmware-tanzu/platform/credhub-secrets-management/services/credhub/using.html)
- [CredHub CLI Releases](https://github.com/cloudfoundry-incubator/credhub-cli/releases)
- [CredHub API Reference](https://docs.cloudfoundry.org/api/credhub)

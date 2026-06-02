---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Configuring Secrets in Cloud Foundry
translated: false
type: note
---

Question: How to configure secrets in Cloud Foundry?

Answer:

In **Cloud Foundry**, there is no built-in dedicated "secrets manager" like Vault, AWS Secrets Manager, or CredHub in every deployment (CredHub exists mainly in environments like Tanzu Application Service / PAS). However, there are several common and officially recommended ways to provide secrets (API keys, passwords, tokens, certificates, etc.) to your applications.

### Recommended Approaches (2025–2026 best practices)

1. **User-Provided Service Instances (Most common & recommended method for simple secrets)**
   This is the officially preferred way to deliver credentials/secrets instead of plain environment variables.

   - Secrets appear in `VCAP_SERVICES` (JSON structure)
   - Credentials are **redacted** in `cf env` output for most roles and in many logs
   - Apps use the same binding mechanism as marketplace services
   - Works in every Cloud Foundry foundation

   **Create a user-provided service with secrets:**

   ```bash
   # Non-interactive (most common)
   cf cups my-secrets-service \
     -p '{"api-key":"sk_live_abc123xyz","db-password":"verySecret2026!","external-token":"ghp_xxxxxxxxxxxxxxxx"}'
   ```

   **Interactive mode (prompts for keys):**

   ```bash
   cf cups my-secrets-service -p api-key,db-password,external-token
   ```

   **Bind to your app and restage:**

   ```bash
   cf bind-service my-app my-secrets-service
   cf restage my-app
   ```

   **How your app reads the secrets** (example in most languages):

   ```json
   // VCAP_SERVICES will contain something like:
   {
     "user-provided": [
       {
         "name": "my-secrets-service",
         "credentials": {
           "api-key": "sk_live_abc123xyz",
           "db-password": "verySecret2026!",
           "external-token": "ghp_xxxxxxxxxxxxxxxx"
         }
       }
     ]
   }
   ```

   Use libraries like `cfenv` (Node.js), `cloudfoundry-client` (Java), `vcap` helpers (Python), etc.

2. **Avoid: cf set-env (Plain user-provided environment variables)**

   ```bash
   cf set-env my-app DATABASE_PASSWORD "verySecret2026!"
   cf restage my-app
   ```

   **Why avoid for secrets?**
   - Visible in `cf env` output
   - Appear in Cloud Controller logs in many cases
   - Not redacted for most user roles
   Official docs explicitly say:
   > "Do not use user-provided environment variables for security-sensitive information such as credentials. Use user-provided service instances instead."

3. **Advanced / Enterprise-grade options (when available in your platform)**

   - **CredHub + CredHub Service Broker** (common in VMware Tanzu / PAS)
     Store secrets centrally in CredHub → bind via service broker → app gets fresh credentials.

   - **HashiCorp Vault + Vault Buildpack / Sidecar**
     Very popular in open-source Cloud Foundry setups.

   - **Conjur / CyberArk Conjur Service Broker**
     Policy-based secret retrieval.

   - **Spring Cloud Vault / Spring Cloud Config + CredHub** (Java/Spring Boot apps)

   Check with your platform team whether CredHub, Vault, Conjur, or another secret store is integrated.

### Quick Summary Table

| Method                        | Security Level | Redacted in `cf env`? | Recommended? | Use case                              |
|-------------------------------|----------------|-----------------------|--------------|---------------------------------------|
| `cf set-env`                  | Low            | No                    | No           | Non-sensitive config only             |
| User-Provided Service (`cups`)| Medium         | Yes (most roles)      | **Yes**      | Most secrets in standard CF           |
| CredHub / Vault / Conjur      | High           | Yes + rotation        | Yes (if available) | Enterprise, secret rotation, auditing |

**Best default choice in 2026 for most Cloud Foundry users →** Use **user-provided services** (`cf cups`).

References:

- [User-provided service instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html)
- [Cloud Foundry environment variables – security guidance](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html)
- [Delivering service credentials to an app](https://docs.cloudfoundry.org/devguide/services/application-binding.html)
- [Cloud Foundry security concepts](https://docs.cloudfoundry.org/concepts/security.html)

---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: SAML Authentication Flow in HashiCorp Vault
translated: false
type: note
---

HashiCorp Vault's SAML login works by integrating Vault with an external SAML Identity Provider (IdP) like Okta, Azure AD, or others. Here's how the authentication flow works:

**Initial Setup:**

- Vault is configured with the SAML auth method, which includes the IdP's metadata (SSO URL, entity ID, certificate)
- The IdP is configured with Vault as a Service Provider (SP), including Vault's callback URL and entity ID
- Policies in Vault are mapped to SAML assertions (like groups or attributes)

**Authentication Flow:**

1. **User initiates login** - The user navigates to Vault's SAML login endpoint or uses the CLI/API with the SAML method

2. **SAML request generation** - Vault generates a SAML authentication request and redirects the user's browser to the IdP's SSO URL

3. **IdP authentication** - The user authenticates with the IdP (username/password, MFA, etc.)

4. **SAML response** - After successful authentication, the IdP generates a signed SAML assertion containing user attributes (username, email, group memberships) and sends it back to Vault's callback URL

5. **Assertion validation** - Vault validates the SAML response by:
   - Verifying the digital signature using the IdP's certificate
   - Checking that the assertion hasn't expired
   - Validating the audience and recipient match Vault's configuration

6. **Token generation** - If validation succeeds, Vault:
   - Extracts user identity and attributes from the assertion
   - Maps SAML groups/attributes to Vault policies
   - Issues a Vault token with the appropriate policies attached

7. **Access granted** - The user can now use this token to access Vault resources according to their assigned policies

The key advantage is that Vault doesn't store or manage user credentials directly—it trusts the IdP's assertions and focuses on authorization through policy mappings.

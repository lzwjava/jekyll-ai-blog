---
audio: false
generated: true
image: false
lang: en
layout: post
title: How SSL Certificate Authentication Works
translated: false
type: note
---

**Question:** How does SSL/TLS certificate authentication work?

## Answer

SSL certificates solve a fundamental problem: how does a client trust a server it's never communicated with before? The solution chains asymmetric cryptography, digital signatures, and trusted intermediaries.

### The Core Mechanism: Digital Signatures

The foundation is **asymmetric cryptography** where you have a keypair:
- **Private key** (secret, kept by server): signs data
- **Public key** (distributed freely): verifies signatures

A digital signature proves three things:
1. The server owns the private key (proof of identity)
2. The data hasn't been tampered with
3. The server was present during the handshake (prevents replay attacks)

Here's a minimal Python example showing the principle:

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# Server generates keypair
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Server signs data with private key
data = b"hello from server"
signature = private_key.sign(data, padding.PSS(...), hashes.SHA256())

# Client verifies signature with public key
public_key.verify(signature, data, padding.PSS(...), hashes.SHA256())
# ✓ Signature valid — server owns that private key
```

### Certificate Structure: Identity Bound to Public Key

A certificate is a digital document that binds:
- The server's **public key**
- The server's **identity** (domain name, organization)
- **Metadata** (expiration, intended uses)

All signed by a Certificate Authority (CA).

The certificate structure (X.509):

```
Certificate {
  tbsCertificate {  // "to be signed"
    version: 3
    serialNumber: 01A2B3
    signature: sha256WithRSAEncryption
    issuer: CN=Let's Encrypt, O=Internet Security Research Group
    subject: CN=example.com, O=Example Inc
    validity: notBefore=2024-01-01, notAfter=2025-01-01
    subjectPublicKeyInfo: <server's public key>
    extensions: {
      subjectAltName: example.com, www.example.com
      keyUsage: digitalSignature, keyEncipherment
    }
  }
  signatureAlgorithm: sha256WithRSAEncryption
  signature: <CA's digital signature of the tbsCertificate>
}
```

The **CA's signature** is the critical part—it cryptographically asserts: "I, a trusted authority, verify that this public key belongs to example.com."

### Chain of Trust: The PKI Model

Clients can't verify every certificate directly. Instead, the certificate chain of trust is validated back to a trusted root CA. Typically:

```
End-entity cert (example.com)
  ↑ signed by
Intermediate CA cert
  ↑ signed by
Root CA cert
  ↑ self-signed (client trusts this by default)
```

Your OS/browser ships with root CAs pre-installed. When verifying a certificate:

```python
# Client has the certificate and CA's public key
cert = load_certificate("example.com.pem")
ca_public_key = load_public_key("letsencrypt-root.pem")

# Verify the CA's signature on the certificate
ca_public_key.verify(cert.signature, cert.tbs_certificate, ...)
# ✓ This certificate was issued by a trusted CA
```

### Verification Checklist: What the Client Actually Checks

Before key exchange, the client checks:
1. The CA's digital signature using the CA's public key (ensures authenticity)
2. The certificate hasn't expired
3. The certificate hasn't been revoked (CRL or OCSP)
4. The domain in the certificate's Subject Alternative Name (SAN) or Common Name (CN) matches the requested domain

Here's simplified verification logic:

```python
def verify_certificate(cert, trusted_ca_certs, requested_domain):
    # 1. Verify CA signature
    for ca_cert in trusted_ca_certs:
        try:
            ca_cert.public_key.verify(cert.signature, cert.tbs_certificate)
            issuer_found = True
            break
        except:
            pass
    assert issuer_found, "No trusted issuer found"

    # 2. Check expiration
    now = datetime.now()
    assert cert.notBefore < now < cert.notAfter, "Certificate expired"

    # 3. Check revocation (CRL/OCSP)
    assert not is_revoked(cert.serialNumber, cert.issuer), "Certificate revoked"

    # 4. Check domain match
    san = cert.extensions.get('subjectAltName')
    domains = san.split(',') if san else [cert.subject.commonName]
    assert requested_domain in domains, "Domain mismatch"

    return True
```

### The Handshake Flow (TLS 1.3)

1. **Client Hello** → sends supported TLS versions, cipher suites, random nonce
2. **Server Hello** → picks cipher, sends server random, sends certificate chain
3. **Certificate Verification** → client validates cert as above
4. **Key Exchange** → using asymmetric encryption (Diffie-Hellman variants like ECDHE), client and server securely establish a shared symmetric session key
5. **CertificateVerify** → server proves it owns the private key by signing the handshake transcript with the private key, proving server presence and preventing MITM attacks
6. **Finished** → both sides verify handshake integrity, switch to symmetric encryption

The key insight: **asymmetric crypto for identity, symmetric crypto for efficiency**. Public key operations are slow, so once trust is established, both parties derive a fast symmetric key and use that for all application data.

### Why This Prevents MITM

An attacker can't intercept without being detected because:
- To forge a certificate, they'd need the CA's private key (global secret)
- To complete the handshake, they'd need the server's private key (server's secret)
- Even with a forged cert, domain validation fails
- The server proves key ownership via CertificateVerify—can't fake without the private key

---

References:

- Practical Foundations in Cybersecurity - The SSL/TLS Handshake
- Encryption Consulting - Practical Guide to SSL/TLS Certificates
- RFC 5280 (X.509 certificates)
- RFC 8446 (TLS 1.3)

---
audio: false
generated: true
image: false
lang: en
layout: post
title: 360 Claw SSL Key Leak Scandal
translated: false
type: note
---

I'll search for information about 360 Claw and any SSL certificate leaks related to this Chinese cybersecurity company.Question: How did Qihoo 360 (a Chinese cybersecurity company) leak its SSL certificate in the portal?

Answer:

Qihoo 360 shipped its AI assistant "Security Claw" with the wildcard SSL private key for *.myclaw.360.cn inside the installer. The private key covers every subdomain on the platform and is valid until April 2027.

## How the SSL Certificate Was Leaked

The private key for *.myclaw.360.cn was bundled directly in the download package under the path `/namiclaw/components/OpenClaw/openclaw.7z/credentials`. This represents a critical failure in the software build and packaging process.

## Technical Impact

The certificate is valid until April 2027, and even if 360 revoked and reissued the certificate immediately, the window of exposure includes every user who connected to myclaw.360.cn between the installer's release and the revocation. Any traffic that was intercepted during that period using the leaked key is retroactively compromised.

## The Ironic Contradiction

Six days before the product launch, founder Zhou Hongyi announced "360 Security Claw" with a specific promise that it would "not damage the user's system, delete data, or leak passwords or other private information on the user's computer." The product leaked a private key during the release.

## Root Cause

The SSL key leak demonstrates a violation of the most basic security practice—not shipping private keys in client-facing packages. This suggests a build pipeline failure where credential files weren't excluded from the distribution archive.

## Security Implications

With the leaked SSL private key, attackers can now:

- Impersonate 360's servers
- Intercept user traffic
- Forge login pages and redirect users to malicious sites
- Potentially steal sensitive user data transmitted through these channels

References:

- [Awesome Agents - China's Top Cybersecurity Firm Ships SSL Key in AI App](https://awesomeagents.ai/news/qihoo-360-ssl-key-leak-openclaw/)
- [Phemex News - 360's OpenClaw AI Assistant Leaks SSL Key](https://phemex.com/news/article/360s-openclaw-ai-assistant-leaks-ssl-private-key-breaching-security-promises-66798)

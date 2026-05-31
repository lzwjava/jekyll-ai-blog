---
audio: false
generated: true
image: false
lang: en
layout: post
title: Team ID Is a Public Identifier
translated: false
type: note
---

No, it's not a security issue. The Team ID is a public identifier, not a secret.

What it is:
- Just a unique string Apple assigns to your developer account
- Anyone who downloads your .app can see it: codesign -dvv YourApp.app
- It's in every app you publish to the App Store
- It's like a username, not a password

What it CANNOT do:
- Can't sign apps (needs your private key in Keychain)
- Can't access your Apple Developer account
- Can't provision devices
- Can't steal your identity

The actual secret is your private key stored in your Mac's Keychain (the one behind `8802945277F81B11FB1744BBFE9F2E961CC5C508`). That never leaves your machine.

Same reason bundle identifiers like `com.lzw.TabsKiller` are public — they're identifiers, not credentials.
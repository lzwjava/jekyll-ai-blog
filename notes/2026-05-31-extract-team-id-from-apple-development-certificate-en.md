---
audio: false
generated: true
image: false
lang: en
layout: post
title: Extract Team ID from Apple Development Certificate
translated: false
type: note
---

Here's the method with your info redacted:

1. Find your signing identity:

   security find-identity -v -p codesigning

   Output:
   "Apple Development: <YOUR_EMAIL> (<IDENTITY_HASH>)"

2. Extract Team ID from the certificate (OU field):

   security find-certificate -c "Apple Development: <YOUR_EMAIL>" -p \
     | openssl x509 -noout -subject

   Output format:
   subject= /UID=<UID>/CN=Apple Development: <EMAIL> (<HASH>)/OU=<TEAM_ID>/O=<NAME>/C=<COUNTRY>

   The OU= value is your Team ID.

Or one-liner to extract just the Team ID:

   security find-certificate -c "Apple Development" -p \
     | openssl x509 -noout -subject \
     | grep -o 'OU=[^/]*' | cut -d= -f2
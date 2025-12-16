---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Storing GPG Public Keys in Git
translated: false
type: note
---

Question: Can we save a .gpg public key file in a Git repository?

Answer: 

Yes, it is safe and often recommended to store GPG **public key** files (typically exported as `.asc` or `.gpg` ASCII-armored files) in a Git repository.

GPG public keys are designed to be shared widely—this is fundamental to how asymmetric encryption works. Distributing your public key allows others to encrypt data for you or verify your signatures. There are no significant security risks in committing a public key to a Git repo, whether public or private:

- No sensitive information is exposed (the private key remains secret).
- It facilitates team workflows, such as verifying signed commits/tags or allowing tools like `git-secret` to encrypt secrets using team members' public keys.
- Common practices include storing maintainer/developer public keys in repositories for offline or firewalled environments, or embedding them as Git objects/blobs for verification.

**Important warnings**:
- Never commit the **private key** (or secret keyring)—this would be a severe security breach.
- If the repository is public, widely distributing the public key is fine, but ensure the key's associated email/identity matches your needs.
- For critical projects, pin the key by its fingerprint rather than relying solely on the file to avoid potential tampering (though this is rare in practice).

This is standard in open-source projects and supported by platforms like GitHub/GitLab, where public keys are routinely shared or uploaded for commit verification.

References:  

- [Reddit discussion on storing PGP public keys in repos](https://www.reddit.com/r/github/comments/1kn1hzu/is_it_safe_to_keep_a_pgp_key_in_a_public_repo_i/)
- [Stack Overflow: Sharing public key in Git repo for signing verification](https://stackoverflow.com/questions/46318599/should-we-share-the-public-key-for-checking-signing-in-the-git-repository)
- [GitHub Docs: Adding a GPG key](https://docs.github.com/en/authentication/managing-commit-signature-verification/adding-a-gpg-key-to-your-github-account)
- [Information Security Stack Exchange: Storing GPG encrypted data publicly](https://security.stackexchange.com/questions/193864/is-it-safe-to-store-gpg-encrypted-data-publicly-eg-on-github)
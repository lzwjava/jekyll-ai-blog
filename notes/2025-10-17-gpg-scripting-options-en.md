---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPG Command Options for Scripting
translated: false
type: note
---

### GPG Command Options Explanation

The options `--batch`, `--yes`, `-o`, and `--pinentry-mode` are common flags used with the `gpg` (GNU Privacy Guard) command for non-interactive or scripted operations, such as encryption, decryption, or signing. Here's a breakdown of each:

- **`--batch`**: Enables batch mode, which prevents `gpg` from asking any interactive questions or allowing interactive commands. This is useful for scripts or automation where user input isn't possible. It can be disabled with `--no-batch`.

- **`--yes`**: Automatically assumes "yes" as the answer to most confirmation prompts (e.g., overwriting files). This avoids halting execution due to yes/no questions.

- **`-o` (or `--output`)**: Specifies the output file for the operation. It must be followed by a filename, e.g., `-o output.txt`. Without this, output might go to stdout or a default location.

- **`--pinentry-mode`**: Controls how the PIN entry (passphrase prompt) is handled by the GPG agent. It takes a mode value like `ask` (default: pops up a graphical or console prompt), `loopback` (allows passphrases via stdin for scripts, without a popup), `cancel` (cancels operations needing a PIN), or `error` (returns an error instead of prompting). This is often used with `loopback` in batch scripts for secure, non-interactive passphrase input.

These options are frequently combined in scripts, e.g., `gpg --batch --yes -o decrypted.txt --pinentry-mode loopback --decrypt encrypted.gpg`, to run fully automated.

#### References

- [GPG Man Page](https://linux.die.net/man/1/gpg)
- [GnuPG Agent Options](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html)
- [GnuPG Manual](https://www.gnupg.org/documentation/manuals/gnupg/index.html)

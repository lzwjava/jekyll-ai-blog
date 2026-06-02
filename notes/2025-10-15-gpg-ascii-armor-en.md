---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: GPG ASCII Armor Explained
translated: false
type: note
---

In GPG (GNU Privacy Guard), "armor" refers to ASCII armor, a format that encodes binary OpenPGP data (like encrypted files, signatures, or keys) into a human-readable, text-based representation. This is useful for transmitting data over text-only channels, such as email, without corruption—similar to how uuencode or base64 works, but with added headers (e.g., "-----BEGIN PGP MESSAGE-----") and checksums for integrity.

You can enable it with the `--armor` (or `-a`) option during commands like encryption (`gpg -a -e file.txt`) or key export (`gpg --armor --export keyid`), which outputs the result in this armored text format instead of raw binary.

## References
- [What is the armored option for in GnuPG?](https://unix.stackexchange.com/questions/623375/what-is-the-armored-option-for-in-gnupg)
- [Exchanging keys - GnuPG](https://www.gnupg.org/gph/en/manual/x56.html)
- [13. ASCII armor - Notes on OpenPGP](https://openpgp.dev/book/armor.html)
- [GPG Input and Output (Using the GNU Privacy Guard)](https://www.gnupg.org/documentation/manuals/gnupg/GPG-Input-and-Output.html)

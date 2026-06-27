---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rsync vs SCP Speed Comparison
translated: false
type: note
---

Question: Is rsync slower than scp for transfers?

Answer:

Not generally — and especially not for what you're doing. For a fresh, one-shot bulk copy on a fast network, they're roughly equal because both are CPU-bound on the SSH cipher, not the protocol. rsync adds a small rolling-checksum/file-list overhead up front, so for a single huge file on a LAN scp can edge it out slightly. But that's a narrow case.

For your situation (a `.git` pack, repos, anything resumable or repeatable), rsync wins decisively:

- **Resumable.** `rsync --partial --append-verify` survives a dropped connection. scp restarts from zero. With a 5GB transfer at variable 400KB/s–12MB/s, this alone matters.
- **Delta transfer.** Re-running rsync only sends changed blocks. A second scp re-sends everything.
- **Skips unchanged files.** Matters for tree copies, not single packs.

Why your transfer feels slow — it's not rsync, it's two other things:

1. **SSH cipher CPU bound.** On older boxes the default cipher caps you. Force a fast one:

   ```bash
   rsync -a --info=progress2 \
     -e 'ssh -c aes128-gcm@openssh.com -o Compression=no' \
     src/ user@host:dst/
   ```

   `aes128-gcm` uses AES-NI; `Compression=no` matters because git packs are already compressed — gzip just burns CPU for nothing.

2. **Git packs don't compress.** Make sure you're *not* passing `-z`. That `400KB/s` floor smells like the remote CPU choking on compression of incompressible data.

For a `.git` directory specifically, the fastest path is often to skip the file-walk entirely:

```bash
# Let git do the packing/transfer — usually beats both rsync and scp
git clone --bare user@host:/path/to/repo.git
# or for an existing checkout, bundle it:
git bundle create linux.bundle --all   # then rsync the single .bundle file
```

A bundle is one contiguous file, so it transfers at line rate with no per-object overhead, and it's trivially resumable as a unit.

Bottom line: rsync isn't the bottleneck. Drop compression, pin a GCM cipher, and for git specifically prefer `git bundle` + transfer over walking the pack files live.

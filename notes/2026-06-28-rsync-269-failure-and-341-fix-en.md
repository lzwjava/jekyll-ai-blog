---
audio: false
generated: true
image: false
lang: en
layout: post
title: rsync 2.6.9 failure and 3.4.1 fix
translated: false
type: note
---

**Why rsync 2.6.9 was failing:**

rsync 2.6.9 ships with macOS (from 2006, Apple never updated it). It has several critical bugs/limitations:

1. **Broken I/O timeout handling** — rsync 2.6.9 has an internal I/O timeout (separate from `--timeout`). When the sender is building the file list or transferring data, the receiver expects periodic pings. On slow machines (old MacBook Pro HDD) or when transferring millions of tiny files (node_modules, Photos originals), the sender gets stuck scanning the filesystem and doesn't send pings in time. The receiver kills the connection → `io timeout after 1912 seconds -- exiting`.

2. **No proper SSH multiplexing** — rsync 2.6.9 opens a single SSH connection and pushes all data through it. When the connection stalls (WiFi hiccup, TCP buffer full, router NAT timeout), there's no recovery mechanism. The pipe breaks → `Broken pipe (32)`, `code 255`.

3. **No incremental file list transfer** — rsync 2.6.9 builds the complete file list on the sender side first, then sends it all at once. For Projects with 20,000+ files, this means a 30+ minute pause where no actual file data flows. During this pause, the SSH connection goes idle, and the router/OS kills it. rsync 3.x streams the file list incrementally — data starts flowing immediately.

4. **Worse symlink handling** — rsync 2.6.9 follows and re-resolves symlinks during the file list phase, which is extremely slow with node_modules (thousands of symlinks). Each symlink resolution is a separate stat() call on the old HDD.

**Why rsync 3.4.1 fixed it:**

1. **Better SSH keepalive** — rsync 3.x sends protocol-level keepalive pings during all phases (file list building, transfer). The connection stays alive even during long pauses.

2. **Incremental file list** — rsync 3.x starts transferring files as soon as it finds them, instead of waiting for the complete file list. Data flows from the first second.

3. **Better error recovery** — rsync 3.x can resume partial transfers more reliably with `--partial --append-verify`. When a connection does drop, it picks up from where it left off at the byte level, not the file level.

4. **Faster checksumming** — rsync 3.x has better delta transfer algorithms, so incremental syncs of already-transferred files are nearly instant.

5. **Protocol version 32 vs 29** — rsync 3.x uses protocol 32, which has better flow control and congestion handling over SSH tunnels.

The result: with 2.6.9, we got `code 255` on every single large transfer (Projects, Pictures). With 3.4.1, Projects completed in one shot, and Pictures completed in 3 runs (and even those runs only had drops on a few subdirs out of 16).

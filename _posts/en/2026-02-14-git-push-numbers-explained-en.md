---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Git Push Output Numbers Explained
translated: false
type: note
---

**Question:** Explain these numbers in this git push output

**Answer:**

This is a typical output from `git push` when you send new commits to GitHub (or another Git remote). Here's a breakdown of what each line and number actually means:

```text
Delta compression using up to 8 threads
```
Git is compressing the data you're sending using **delta compression** (storing changes relative to other objects instead of full copies).  
It decided to use up to **8 CPU threads** to do this compression in parallel.

```text
Compressing objects: 100% (4/4), done.
```
Git compressed **4** objects (usually commits + trees + blobs).  
All 4 were successfully compressed → **100% (4/4)**.

```text
Writing objects: 100% (4/4), 2.44 KiB | 2.44 MiB/s, done.
```
Git wrote **4** objects to the packfile that will be sent.  
Total size of these objects (after compression) = **2.44 KiB**  
Writing speed during this local pack creation = **2.44 MiB/s**

```text
Total 4 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
```
- **Total 4** objects are being sent  
- **delta 2** of them are stored as deltas (changes relative to other objects)  
- **reused 0** → no objects were reused from the local repository's existing packfiles  
- **pack-reused 0 (from 0)** → nothing was reused from previously sent packfiles either

```text
remote: Resolving deltas: 100% (2/2), completed with 2 local objects.
```
On **GitHub's side**:  
- There were **2** delta objects in the pack you sent  
- GitHub applied/reconstructed those deltas successfully (**100%**)  
- It used **2 local objects** (already existing on GitHub) as the base to apply those deltas

```text
Transferred: sent 6904, received 4540 bytes, in 18.9 seconds
```
Total network traffic during this push:

- You **sent** **6904 bytes** to GitHub  
- You **received** **4540 bytes** from GitHub (mostly status messages, refs update confirmation, capability negotiation, etc.)  
- The whole operation took **18.9 seconds**

```text
Bytes per second: sent 364.8, received 239.9
```
Effective transfer speeds (very low in this case):

- Upload speed ≈ **364.8 bytes/second** (~2.9 kbit/s)  
- Download speed ≈ **239.9 bytes/second** (~1.9 kbit/s)

```text
To github.com:lzwjava/blog-source.git
```
The final line just shows which remote repository you pushed to.

### Quick summary – what was actually sent?

- You pushed **4 new objects** (probably 1–3 commits + tree(s) + maybe a small file or two)  
- Compressed size ≈ **2.44 KiB**  
- On the wire you sent **~6.9 KB** (includes protocol overhead, sideband data, etc.)  
- The push took **almost 19 seconds** → very slow connection (~3 kbit/s upload)

This kind of output is typical when:
- you're pushing very small changes
- you have a very slow / high-latency / throttled internet connection
- or you're pushing to a repository for the first time after a long time (lots of negotiation)

**References:**  

- [Git Internals - Transfer Protocols](https://git-scm.com/book/en/v2/Git-Internals-Transfer-Protocols)  
- [Git push output explained (stackoverflow)](https://stackoverflow.com/questions/2251588/git-push-output-explained)
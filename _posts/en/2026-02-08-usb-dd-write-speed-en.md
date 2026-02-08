---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Decoding USB Write Speed in dd
translated: false
type: note
---

**Question:** What does this dd output mean? How is the disk write speed? Please convert it to human-readable format.

**Answer:**

This output comes from the macOS `dd` command (used with `sudo dd if=... of=/dev/rdisk10 bs=1m`), which is writing a Windows 11 ISO file to a USB flash drive (likely /dev/rdisk10 is your USB stick in raw mode for faster access).

`dd` periodically prints status when you press **Ctrl + T** during the copy (that's why you see multiple lines). Each line shows progress at that moment.

### Breakdown of one line (example):
```
866+0 records in
866+0 records out
908066816 bytes transferred in 43.725150 secs (20767609 bytes/sec)
```

- **records in / records out**: How many blocks were read from the ISO and written to the USB.  
  Here each record = **bs=1m** = 1 MiB = 1,048,576 bytes  
  So 866 records ≈ 866 MiB written so far.
- **bytes transferred**: Total data written up to now (in bytes).
- **in Xs secs**: How much real time has passed since dd started.
- **(N bytes/sec)**: **Current average write speed** up to this point.

### Your speeds in human-readable format (MB/s):

- First status:  ≈ **20.4 MB/s**  (20,439,149 bytes/sec ≈ 20.4 MiB/s)
- Second status: ≈ **20.6 MB/s**  (20,572,527 bytes/sec ≈ 20.6 MiB/s)
- Third status:  ≈ **20.8 MB/s**  (20,767,609 bytes/sec ≈ 20.8 MiB/s)
- Final status:  ≈ **15.5 MB/s**  (15,542,913 bytes/sec ≈ 15.5 MiB/s)

The overall average speed dropped to about **15.5–16 MB/s** toward the end.

### Is this speed good or bad?

- **Typical cheap / older USB 3.0 flash drives**: Sustained write 10–30 MB/s when writing large continuous data (like an ISO).  
- **Good USB 3.0/3.1 flash drives**: 40–100+ MB/s sustained write.  
- **Very fast modern ones** (USB 3.2 Gen 2, SLC/MLC, or premium models): 150–300+ MB/s possible, but rare for normal thumb drives.

**Your speed (15–21 MB/s)** is quite typical for:
- An average or budget USB 3.0 flash drive
- A USB 2.0 port (even if the drive is 3.0)
- A drive that's getting full / thermal throttling / fake-high-capacity fake drive

It's **not very fast**, but also **not unusually slow** for many common USB sticks when writing ~5–6 GB continuously.  
If you want faster ISO → USB creation (2–4× faster), try:
- A better USB flash drive (look for ones advertising 100+ MB/s write)
- Confirm you're using a real USB 3.0/3.1 port (blue port usually)
- Use tools like Balena Etcher or Rufus (they often achieve better performance)

**References:**

- [https://www.usbmemorydirect.com/blog/flash-drive-read-write-speed](https://www.usbmemorydirect.com/blog/flash-drive-read-write-speed)
- [https://superuser.com/questions/1785762/slow-write-speed-on-usb-3-0-thumb-drive](https://superuser.com/questions/1785762/slow-write-speed-on-usb-3-0-thumb-drive)
- [https://forums.anandtech.com/threads/usb-3-0-3-1-flash-drive-write-speeds.2497087](https://forums.anandtech.com/threads/usb-3-0-3-1-flash-drive-write-speeds.2497087)
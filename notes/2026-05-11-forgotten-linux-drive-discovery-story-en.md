---
audio: false
generated: true
image: false
lang: en
layout: post
title: Forgotten Linux Drive Discovery Story
translated: false
type: note
---

Question: What do you think about this funny/relatable Linux partition story — having a 2TB hard drive sitting unused for 3 years with no partition, only discovering it when trying to train GPT-3 on Ubuntu?

Answer:

## 😂 The Classic "Forgotten Hard Drive" Story

This is **extremely relatable** to anyone who's worked with Linux. Here's why it's both funny and painfully real:

---

### The Joke Breakdown

> *"I have a 2TB hard drive. Bought it, plugged it in, forgot about it for 3 years. The moment I desperately need storage to train GPT-3... I discover it was never partitioned. It's been sitting there, empty, judging me silently."*

---

### Why This Is So Funny (and Human)

| Stage | What happened | The feeling |
|---|---|---|
| Year 0 | Bought 2TB drive, plugged in | "I'm so prepared!" |
| Year 0–3 | Never partitioned it | Blissful ignorance |
| Year 3 | Need storage for GPT-3 training | Panic mode |
| Discovery | `lsblk` shows unpartitioned disk | 🤦 Facepalm of the century |

---

### The Linux Truth Nobody Tells Beginners

Unlike Windows, Linux does **not** auto-partition or auto-mount a new drive. You have to manually:

```bash
# Step 1: Find the disk
lsblk

# Step 2: Partition it
sudo fdisk /dev/sdb   # or gdisk for GPT

# Step 3: Format it
sudo mkfs.ext4 /dev/sdb1

# Step 4: Mount it
sudo mount /dev/sdb1 /mnt/data
```

If you skip these steps — the disk just **exists**, silently, doing absolutely nothing, like a very expensive paperweight.

---

### The Silver Lining

The good news? **3 years of zero use = zero wear**. Your 2TB drive is basically brand new. Perfect condition for training runs. 🎉

Now go partition that thing and train your model! 🚀

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kernel Maps Handles to Devices
translated: false
type: note
---

Question: **How does an OS assign the I/O devices needed by a user process?**

Answer: The key idea is: **a process usually does not get a physical I/O device directly. It gets an abstraction/handle, and the kernel maps that handle to a device driver + device.**

For example:

```text
User process
    |
    | read(fd=3, buf, 4096)
    v
Kernel
    |
    | fd 3 -> open file -> inode/vnode -> filesystem
    |
    v
Block device driver
    |
    v
NVMe controller
    |
    v
SSD
```

### 1. Process asks for a resource, not a device

Suppose:

```c
int fd = open("/tmp/a.txt", O_RDONLY);
read(fd, buf, 4096);
```

The process doesn't say:

> "Give me NVMe device #2."

Instead it says:

> "Open this file."

The kernel resolves `/tmp/a.txt` to a filesystem object, and eventually to the block device containing its data.

A simplified Linux structure is roughly:

```text
process
  |
  +-- fd table
        |
        +-- fd 3
             |
             v
          struct file
             |
             v
          inode
             |
             v
          filesystem
             |
             v
          block device
             |
             v
          device driver
             |
             v
          hardware
```

### 2. The important distinction: device allocation vs device access

There are actually two different questions.

**Who owns/controls the hardware?**

The **kernel/device driver** does.

**Which process is allowed to use it?**

The kernel controls this through abstractions and permissions.

For ordinary storage:

```text
SSD
 ^
 |
NVMe driver
 ^
 |
block layer
 ^
 |
filesystem
 ^
 |
file descriptor
 ^
 |
process
```

Multiple processes can simultaneously use the same SSD:

```text
P1 -- fd 3 --\
P2 -- fd 5 ---+--> filesystem --> block layer --> NVMe --> SSD
P3 -- fd 4 --/
```

The kernel doesn't normally "allocate the SSD to P1." It multiplexes requests from all processes.

---

### 3. For character devices, the mapping is more direct

Consider:

```bash
cat /dev/ttyUSB0
```

`/dev/ttyUSB0` is a **device node**.

Its metadata contains something conceptually like:

```text
/dev/ttyUSB0
    |
    +-- major = 188
    +-- minor = 0
```

The kernel uses the major/minor numbers to identify the device/driver.

Conceptually:

```text
open("/dev/ttyUSB0")
        |
        v
   VFS / device node
        |
        | major=188, minor=0
        v
   USB serial driver
        |
        v
    USB hardware
```

So this case is much closer to "process accesses a device."

---

### 4. What prevents two processes from fighting over the device?

The kernel's synchronization + driver model.

For example:

```text
P1: read(fd1)
P2: write(fd2)
P3: ioctl(fd3)
       |
       v
   kernel driver
       |
       +-- locks
       +-- queues
       +-- interrupts
       +-- DMA
```

The driver serializes or queues operations as appropriate.

For modern storage, the hardware itself can also have multiple queues:

```text
P1 ----\
P2 -----+--> kernel I/O queues --> NVMe submission queues --> SSD
P3 ----/
```

This is why "I/O device allocation" in OS textbooks can be slightly misleading. Modern OSes generally do **I/O multiplexing**, rather than assigning one physical device exclusively to one process.

---

### 5. Where does DMA fit?

The actual data movement often doesn't go:

```text
SSD -> CPU -> process memory
```

Instead:

```text
SSD
 |
 | DMA
 v
RAM
 |
 v
process buffer
```

A typical `read()` looks approximately like:

```text
read(fd, buf, 4096)
       |
       v
syscall
       |
       v
VFS/filesystem
       |
       v
block layer
       |
       v
NVMe driver
       |
       | create I/O request
       v
NVMe controller
       |
       | DMA
       v
user/kernel memory
       |
       v
wake process
```

The CPU mostly orchestrates the operation; the device can move the actual bytes using DMA.

---

### 6. The "allocation" happens at several layers

A useful mental model is:

```text
                 PROCESS
                    |
              file descriptor
                    |
                    v
                  VFS
                    |
              filesystem
                    |
                    v
               block layer
                    |
                    v
              I/O scheduler
                    |
                    v
              device driver
                    |
                    v
              controller
                    |
                    v
                 device
```

Different OS concepts operate at different layers:

| Problem                         | Mechanism                                              |
| ------------------------------- | ------------------------------------------------------ |
| Which file can process access?  | File descriptor + permissions                          |
| Which device contains the file? | Filesystem/block-device mapping                        |
| Which driver handles device?    | Device model / major-minor / bus                       |
| Multiple processes doing I/O    | Kernel multiplexing                                    |
| Ordering requests               | I/O queues/schedulers                                  |
| Moving data efficiently         | DMA                                                    |
| Preventing races                | Locks/queues/driver synchronization                    |
| Restricting device access       | Permissions, namespaces, capabilities, security policy |

So if your textbook says **"OS allocates I/O devices to user processes"**, read that as:

> **The OS provides each process with a controlled I/O abstraction and multiplexes access to the underlying physical devices.**

It is usually **not** a literal `process → physical device` allocation.

I can also walk through the exact Linux path of `read()` from `syscall` → VFS → filesystem → block layer → NVMe driver → DMA, which makes this much more concrete.

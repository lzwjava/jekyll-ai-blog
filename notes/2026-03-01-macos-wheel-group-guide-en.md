---
audio: false
generated: true
image: false
lang: en
layout: post
title: MacOS Wheel Group Explained Simply
translated: false
type: note
---

**Question:** What is the wheel group in macOS?

**Answer:**

The **wheel** group in macOS is a special user group inherited from its BSD Unix roots.

### Historical Background
- In traditional BSD Unix systems (which macOS is based on), the **wheel** group was used to control access to the `su` command (to become root/superuser).
- Only users who were members of the **wheel** group were allowed to use `su` to gain root privileges.
- The name "wheel" is slang for a powerful or important person ("big wheel").

### In modern macOS (including recent versions like macOS Ventura, Sonoma, Sequoia, etc.)
- The **wheel** group's original administrative role has been largely replaced by the **admin** group.
- Regular administrator accounts on macOS are added to the **admin** group (and usually also **staff**).
- The **admin** group controls most elevated privileges, including the ability to use `sudo` without restrictions (via the `/etc/sudoers` file).
- **wheel** still exists (it has GID 0, same as root has UID 0), but it is mostly a legacy/compatibility placeholder now.
- Typically, the only member is the **root** user itself.
- Normal admin users are **not** in the wheel group.

### Practical uses you might see today
- Many system files and directories (especially in `/System`, `/usr`, `/bin`, etc.) list **wheel** as their group owner.
- The `/private/tmp` (and therefore `/tmp`) directory is owned by group **wheel** → files you create there often show group **wheel** (this is normal and inherited from the parent directory; it doesn't give extra access because default permissions are usually 644/755).
- You may see **wheel** in file permissions in Finder's "Get Info" window or when running `ls -l` in Terminal.

In short:
On current macOS, **wheel** is mostly a historical artifact with very limited active meaning — the real administrative group is **admin**.

You can check group memberships with these commands in Terminal:

```bash
groups          # shows groups for your current user
id -Gn          # same, more detailed
dscl . -read /Groups/wheel
```

**References:**

- [What is the "wheel" user in macOS/OS X?](https://superuser.com/questions/191955/what-is-the-wheel-user-in-macos-os-x)
- [Wheel (computing) - Wikipedia](https://en.wikipedia.org/wiki/Wheel_(computing))
- [How does group 'wheel' get on my files? - Ask Different](https://apple.stackexchange.com/questions/275521/how-does-group-wheel-get-on-my-files)
- [What is the difference between the default groups on Mac OS X?](https://superuser.com/questions/20420/what-is-the-difference-between-the-default-groups-on-mac-os-x)

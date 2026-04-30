---
audio: false
generated: true
image: false
lang: en
layout: post
title: Manual Windows Program Registry Cleanup
translated: false
type: note
---

Question: If we delete a program (e.g., Control-M) in Windows by removing its directory instead of using the uninstaller, how can we find and clean related registry entries?

Answer:

When you delete a program manually (just removing its folder), Windows still keeps **residual data**—mainly in the registry, startup entries, services, and system folders. Cleaning it fully requires a careful, multi-step approach.

---

## 1. Understand Where Leftovers Exist

Typical locations where programs leave traces:

### Registry paths

* `HKEY_CURRENT_USER\Software\...`
* `HKEY_LOCAL_MACHINE\SOFTWARE\...`
* `HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\...` (for 32-bit apps on 64-bit systems)
* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services` (for services like Control-M)

---

## 2. Use Registry Editor (regedit)

### Step-by-step:

1. Press `Win + R`
2. Type `regedit`
3. Use **Edit → Find** (or `Ctrl + F`)
4. Search for:

   * Program name (e.g., `Control-M`)
   * Vendor name (e.g., BMC, if relevant)
5. Delete related keys carefully

👉 Press `F3` to jump to the next match and repeat.

⚠️ Be cautious:

* Only delete entries clearly tied to the program
* Wrong deletions can break Windows or other apps

---

## 3. Check Installed Programs List (Orphaned Entries)

Even if files are gone, the app may still appear in “Programs and Features”:

Registry location:

* `HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`

Delete the corresponding key if the app is still listed but no longer exists.

---

## 4. Remove Services (Important for tools like Control-M)

If the program installed Windows services:

### Check:

* Run `services.msc`
* Look for related service names

### Remove via command line:

```bash
sc delete "ServiceName"
```

Or inspect registry:

* `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services`

---

## 5. Clean Startup Items

Check:

* Task Manager → Startup tab
* Registry:

  * `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
  * `HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run`

---

## 6. Remove Scheduled Tasks

1. Open Task Scheduler (`taskschd.msc`)
2. Look for tasks related to the program
3. Delete them

---

## 7. Clean Remaining Files

Check these folders:

* `C:\Program Files\`
* `C:\Program Files (x86)\`
* `C:\ProgramData\`
* `C:\Users\<YourUser>\AppData\Local\`
* `C:\Users\<YourUser>\AppData\Roaming\`

---

## 8. Use Tools (Safer & Faster)

Instead of manual cleanup, tools can scan leftovers:

* CCleaner (registry cleaner)
* Revo Uninstaller (deep scan mode)
* Geek Uninstaller

These tools:

* Scan registry + filesystem
* Detect orphaned entries
* Reduce risk of deleting wrong keys

---

## 9. Advanced Tip (For Experts)

Use:

* `Process Monitor` (from Microsoft Sysinternals)
* Filter by process name before deletion (if still installed)
* Capture all registry/file interactions

This gives a **precise map of what the app uses**

---

## Key Insight

Manually deleting a program folder is **incomplete cleanup** because:

* Windows uses a **distributed configuration model** (registry + services + scheduled tasks)
* Installers often scatter data across the system

---

## Practical Recommendation

If the program is already deleted:

1. Try reinstalling it
2. Then uninstall properly
3. Use a tool like Revo for deep cleanup

This is often faster and safer than manual hunting.

---

If you want, I can walk through a **real Control-M cleanup checklist** (it’s a complex enterprise tool with services, agents, and ports).
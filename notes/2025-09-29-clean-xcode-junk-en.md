---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Free Up Disk Space Cleaning Xcode Junk
translated: false
type: note
---

Good question 👍 Xcode (and iOS Simulator) can accumulate a *lot* of junk over time—build cache, derived data, simulator devices, device support files, logs, etc. Cleaning them up frees gigabytes. Here’s a structured approach:

---

### 1. Clear Derived Data (Build Cache)

This removes old build products, intermediates, and indexes.

* From **Xcode UI**:
  `Xcode → Settings → Locations → Derived Data → click the arrow → delete folders.`
* From **Terminal**:

  ```bash
  rm -rf ~/Library/Developer/Xcode/DerivedData/*
  ```

---

### 2. Clean Simulator Data

* Reset or delete simulator contents:

  ```bash
  xcrun simctl erase all
  ```

  (erases apps & data, but keeps device definitions)

* To remove all unused simulator devices (if you’ve accumulated old iOS versions):

  ```bash
  xcrun simctl delete unavailable
  ```

* To delete all simulator devices (be careful, will remove everything):

  ```bash
  xcrun simctl delete all
  ```

* Manually delete heavy directories:

  ```bash
  rm -rf ~/Library/Developer/CoreSimulator/Devices/*
  ```

---

### 3. Remove Old Device Support Files

When you connect real devices, Xcode downloads debugging symbols for each iOS version. They pile up.

```bash
rm -rf ~/Library/Developer/Xcode/iOS\ DeviceSupport/*
```

---

### 4. Clean Archives

App archives from “Product → Archive” consume a lot.

* From Organizer in Xcode → Archives → delete old ones.
* Or via Terminal:

  ```bash
  rm -rf ~/Library/Developer/Xcode/Archives/*
  ```

---

### 5. Clean Logs

```bash
rm -rf ~/Library/Developer/Xcode/DocumentationCache/*
rm -rf ~/Library/Developer/Xcode/ios device logs/*
rm -rf ~/Library/Logs/CoreSimulator/*
```

---

### 6. Clean Derived Indexes & Module Cache

```bash
rm -rf ~/Library/Developer/Xcode/DerivedDataModuleCache/*
```

---

### 7. Optional: Full Reset

If you want to reset Xcode-related caches completely:

```bash
rm -rf ~/Library/Developer/Xcode/*
rm -rf ~/Library/Developer/CoreSimulator/*
```

(This removes everything: simulators, archives, derived data, etc. Next Xcode launch will feel “fresh install.”)

---

⚠️ **Tips**

* Always quit Xcode and Simulator before running these commands.
* Use `du -sh ~/Library/Developer/*` to see which folders are largest.
* Sometimes `Clean Build Folder` (`⇧⌘K`) in Xcode is enough, but deep cleaning saves more space.

---

Do you want me to give you a **single script** you can run to clean all the common junk in one go (with optional flags)?

---
audio: true
generated: false
image: false
lang: en
layout: post
title: Clean Up Startup Items in macOS
type: post
---

To manage applications and processes that launch automatically when you log in to macOS (including macOS 15.2 and later), you can adjust your startup items. Here's how:

### 1. **Using System Settings (or System Preferences)**

   - **Step 1:** Click the Apple menu () in the top-left corner of your screen and select **System Settings** (or **System Preferences** on older macOS versions).
   - **Step 2:** Go to **General** and then **Login Items**.
   - **Step 3:** A list of apps and services that launch at startup will be displayed. To remove an item, select it and click the **minus (–)** button below the list.
   - **Step 4:** Repeat this for all items you wish to remove.

### 2. **Adjusting App-Specific Settings**

   - Many applications include their own settings to control startup behavior. Look within the app's preferences or settings to disable automatic launching.

### 3. **Managing Launch Agents and Daemons (Advanced)**

   - Background processes can be managed by Launch Agents or Launch Daemons. These are typically located in the following directories:
     - `~/Library/LaunchAgents` (for user-specific agents)
     - `/Library/LaunchAgents` (for system-wide agents)
     - `/Library/LaunchDaemons` (for system-wide daemons)
   - **Caution:** Modifying these files can impact system stability. Proceed with care.

### Tips:

- **Restart Your Mac:** After making changes, restart your Mac to confirm that the startup items no longer launch.

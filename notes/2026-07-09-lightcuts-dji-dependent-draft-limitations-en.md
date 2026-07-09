---
audio: false
generated: true
image: false
lang: en
layout: post
title: LightCut's DJI-Dependent Draft Limitations
translated: false
type: note
---

**Question:** Why can't DJI LightCut save drafts locally? Why do my edited videos disappear unless I connect to a DJI device?

**Answer:**

This is one of the biggest complaints about **LightCut**. It is designed primarily as a companion app for DJI cameras, not as a full-featured video editor like InShot or CapCut.

A few reasons this happens:

1. **Projects are tied to imported media**

   * If your footage came directly from a DJI camera (Pocket, Action, Mini, Air, etc.), LightCut often stores references to those original files rather than creating a completely independent project.
   * If the media isn't available (e.g. the SD card is removed or the camera isn't connected), the project may not reopen correctly.

2. **Automatic editing workflow**

   * LightCut was built around AI templates:

     * Connect DJI device
     * Import clips
     * AI generates a draft
     * Export
   * DJI optimized for quick social media videos rather than long-term project management.

3. **Draft management is limited**

   * Many users report:

     * drafts disappearing after app updates
     * drafts not syncing across devices
     * projects only appearing if the original media is still accessible
     * no reliable "Save As Project" workflow

4. **No professional project database**
   Unlike editors such as:

   * InShot
   * CapCut
   * VN
   * LumaFusion
   * DaVinci Resolve

   LightCut doesn't expose a robust project library with autosave history, backups, duplicate project, etc.

---

### If you imported normal iPhone videos

Then you **shouldn't** need the DJI device.

If the draft disappeared, likely one of these happened:

* the app cache was cleared
* the app was reinstalled
* Photos permissions changed
* iCloud optimized away the original file temporarily
* a LightCut bug

---

### If you imported directly from a DJI camera

The app may expect:

```
Project
   ↓
Original file
   ↓
DJI camera / SD card
```

If the original footage isn't found, the project can appear missing or broken.

---

### Better alternatives

If you want reliable project saving on iPhone:

* **InShot** — excellent draft management, simple UI.
* **VN Video Editor** — free, timeline-based, reliable project storage.
* **CapCut** — very capable, though increasingly cloud-oriented.
* **LumaFusion** — professional-grade editor with robust local project management.

If you're building your own editor or studying UX, InShot's draft system is much closer to what users expect:

* local project database
* explicit drafts
* recoverable timeline
* media relinking
* independent editing sessions

That's one reason many people use LightCut only to transfer footage from DJI devices or generate quick AI edits, then switch to another editor for any serious editing work.

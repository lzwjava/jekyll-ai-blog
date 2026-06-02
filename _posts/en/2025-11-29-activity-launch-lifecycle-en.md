---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Android Activity Launch Lifecycle Sequence
translated: false
type: note
---

The correct answer is **A. onCreate() → onStart() → onResume()**

### Explanation of the Android Activity lifecycle when an Activity is first launched:

When an Activity is created for the first time (e.g., when the app is launched or the user navigates to a new Activity), the system calls the following callback methods in this exact order:

1. **onCreate()**
   - The Activity is being created.
   - You set up the layout (setContentView()), initialize views, and prepare essential components.
   - The Activity is not yet visible to the user.

2. **onStart()**
   - The Activity is becoming visible to the user.
   - It’s now on the screen but not yet interactive (not in the foreground).

3. **onResume()**
   - The Activity is now in the foreground and fully interactive.
   - It has focus and is running — this is the state where the user can interact with it.

So the correct sequence is:
**onCreate() → onStart() → onResume()**

The other options are incorrect because:
- **B and C** start with onStart() or onResume() — impossible, since onCreate() must happen first.
- **D** has onResume() before onStart() — wrong order, onStart() always precedes onResume().

Official reference: [Android Developer Documentation - Activity Lifecycle](https://developer.android.com/guide/components/activities/activity-lifecycle)

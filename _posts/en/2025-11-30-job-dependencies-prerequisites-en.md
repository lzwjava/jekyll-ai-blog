---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Control-M Job Dependencies and Prerequisites
translated: false
type: note
---

In BMC Control-M, if you want **Job B to start only after Job A has finished successfully** (the most common requirement), here are the most common and recommended ways to do it:

### 1. Prerequisites (In-Condition) – Most Popular & Recommended Method

1. Open **Job A** (the predecessor).
2. Go to the **Post-Processing** tab → **Add On-Do Actions** → **Add Condition**.
3. Create an outgoing condition, for example:
   - **Condition name**: `A-OK`
   - **Date**: ODAT (or a specific cyclic date if needed)
   - **Add** (this creates the condition when Job A ends OK)

4. Open **Job B** (the successor).
5. Go to the **General** or **Prerequisites** tab → **In-Conditions**.
6. Add a prerequisite condition:
   - **Condition name**: `A-OK`
   - **Date**: ODAT
   - **And/Or**: (leave as default)

Now Job B will wait until `A-OK` condition exists → Job B becomes eligible to run.

> This is the standard and most flexible way in Control-M.

### 2. Order Jobs in the Same Folder/Smart Folder (Simple, but less flexible)

If both jobs are in the same **Smart Folder** or regular **Folder**:

1. Open the folder in the Planning domain.
2. In the **Job Sequence** or just drag & drop the jobs so that:
   - Job A is above Job B
3. Right-click the connection line between A and B → make sure it says **“Complete”** (not “Not OK”).
   - Or simply select both jobs → right-click → **Order** → Job B will automatically wait for Job A to finish OK.

This automatically creates the `A-OK` → `B` prerequisite behind the scenes.

### 3. Using “Run After” in Job Definition (Control-M 9.0.20+ / Control-M Automation API)

In newer versions, when editing Job B, you can directly add:

- **Scheduling** tab → **Run After** → select Job A → “After completion”

Very intuitive, does the same as method 1.

### 4. If you want Job B to run even if Job A fails (rare)

Use two conditions from Job A:
- On OK → add condition `A-OK`
- On NOTOK → add condition `A-NOTOK`

Then on Job B add both conditions with **OR** logic.

### Quick Example Summary

**Job A (any type)**
Post-Processing → Add Condition:
`A-OK  ODAT  Add`

**Job B (any type)**
Prerequisites → In-Condition:
`A-OK  ODAT  And/Or: (blank)`

That’s it — Job B will start automatically as soon as Job A ends OK.

This works in all versions of Control-M (Desktop, CCM, Workbench, and Control-M Web). Let me know your Control-M version if you need screenshots or the exact menu names!

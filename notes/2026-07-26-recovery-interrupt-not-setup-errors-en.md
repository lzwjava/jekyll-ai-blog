---
audio: false
generated: true
image: false
lang: en
layout: post
title: Recovery Interrupt, Not Setup Errors
translated: false
type: note
---

Question: Confirming from setuperr.log — is the "recovery environment" trigger the actual fatal cause, or is one of the other errors (OneSettings, 0x80070490, 0x80072EE7) the real problem?

Answer: Those early errors are red herrings — ignore them:

- `0x80070490` (CUnattendManager) and `0x80072EE7` (OneSettings init failed) — these are just **Setup trying to phone home for updates/telemetry and failing because there's no internet connection** at that point in WinPE. This happens on almost every offline USB install and does **not** stop Setup from proceeding. `0x80072EE7` specifically is a DNS/name-resolution failure — totally normal with no network in WinPE.
- `0x80070002` (GetWuIdFromRegistry) — file/registry key not found, also routine during a clean install, not fatal.

**The actual fatal chain is exactly what I flagged before:**
```
CSetupManager::OnFinishLaunchChoiceAction(8149): Result = 0xC19001F4
```
This is the only error that cascades through every subsequent call and force-exits Setup (`CSetupHost::Execute(564): Result = 0xC19001F4`). It's triggered by a **user-requested recovery environment launch** — this is Setup being told to abandon install and jump to recovery, not a hardware/media/network failure.

So: confirmed, this was an interrupt (most likely a keypress) during the active install, not a corrupt ISO/USB or disk issue. **Retry the install and don't touch the keyboard once the progress bar starts** — go straight from disk selection to letting it run untouched through all reboots into OOBE.

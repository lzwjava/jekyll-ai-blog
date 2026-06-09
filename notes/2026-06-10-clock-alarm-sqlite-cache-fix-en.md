---
audio: false
generated: true
image: false
lang: en
layout: post
title: Clock Alarm SQLite Cache Fix
translated: false
type: note
---

Question: Why isn't the alarm appearing or working in Clock.app even after writing directly to the SQLite database and verifying it exists in the tables?

Answer:

Even though your script inserts the data into `local.sqlite` correctly, **Clock.app still won't show the alarm because it relies on a memory-cached Core Data stack managed by the background daemon (`mobiletimerd`).** When you mutate the SQLite file directly behind Core Data's back, the system daemon is completely unaware of the changes. It continues using its in-memory state and will eventually overwrite your manual SQLite entries with its own cache.

To make the changes take effect and sync to the Clock app UI, you need to notify the system or clear the daemon cache using the following steps:

### 1. Notify the System or Force a Daemon Reload

Simply checking `pgrep` isn't enough; you must force `mobiletimerd` to flush its cache and reread the database from the disk. You can safely kill the background process so it restarts fresh:

```bash
killall mobiletimerd

```

Alternatively, since Core Data on macOS often relies on cross-process notifications via `notifyd`, you might need to broadcast a state change notification using `notifyutil` if a basic process restart doesn't force a sync:

```bash
notifyutil -p com.apple.mobiletimerd.LocalAlarmChanged

```

### 2. Handle Core Data Write-Ahead Logging (WAL)

Core Data operates SQLite in `WAL` (Write-Ahead Logging) mode. When your script writes to `local.sqlite`, the data might only sit in `local.sqlite-wal` and not get fully checkpointed into the main database file before `mobiletimerd` reads it again.

Ensure your Python execution forces a checkpoint or closes the connection cleanly, and restart the daemon *after* the script fully finishes execution.

### 3. Verify the Core Data `Z_PRIMARYKEY` Increment

If you manually assigned `Z_PK` values when inserting into `ZMTCDALARM` and `ZMTCDSOUND`, you **must** update the `Z_MAX` column in the `Z_PRIMARYKEY` meta-table for both `MTCDAlarm` and `MTCDSound`.

If `Z_MAX` doesn't match or exceed your new `Z_PK`, Core Data will experience a primary key collision the next time you create an alarm through the UI, which silently fails or crashes the database load.

```sql
UPDATE Z_PRIMARYKEY SET Z_MAX = (SELECT MAX(Z_PK) FROM ZMTCDALARM) WHERE Z_NAME = 'MTCDAlarm';
UPDATE Z_PRIMARYKEY SET Z_MAX = (SELECT MAX(Z_PK) FROM ZMTCDSOUND) WHERE Z_NAME = 'MTCDSound';

```

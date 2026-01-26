---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: DBeaver DB2 Background Task Cancellation
translated: false
type: note
---

Question: In DBeaver when working with DB2, sometimes while loading items I need to cancel a background task, but the left panel (navigator) shows the table and the data can still load despite it showing "loading item".

Answer: 

This behavior is common in DBeaver with DB2 (especially DB2 LUW or z/OS), where background metadata loading or cache operations can appear stuck or take a very long time, while the main data fetch (e.g., opening a table's Data tab) often proceeds independently and shows results anyway.

### Why this happens
- DBeaver runs several background tasks when you expand schemas/tables or open objects, such as:
  - Loading table/column metadata
  - Building procedure/argument caches (`Load ArgumentsCache`)
  - Discovering result set metadata
  - Loading schema statistics or table cache (`Load DB2TableCache`)
- With DB2 these tasks can be slow due to:
  - Large number of objects
  - Remote/latency-heavy connection
  - DB2-specific JDBC driver behavior
  - Catalog queries that are expensive on the server side
- The "Loading item..." message in the navigator (left panel) or status bar usually comes from one of these auxiliary background jobs.
- The actual table data load (SELECT * FROM table FETCH FIRST 200 ROWS ONLY by default) is a separate operation and often completes much faster, so you see data even when the background task is still running or appears hung.

### What you can do
1. **Safely cancel the background task**  
   - Go to **Window → Show View → Background Tasks** (or click the progress indicator in the bottom-right corner).  
   - Find the long-running task (often named something like "Load DB2TableCache", "Load schema statistics", "Discover resultset metadata", etc.).  
   - Right-click → **Cancel** or use the red square/cancel button.  
   → In most cases this is safe when the data has already loaded — it just stops the extra metadata collection.

2. **Prevent or reduce these slow background tasks**  
   - In **Preferences → Connections → Metadata** → uncheck or limit options like "Load schema statistics on connection" or "Auto-discover metadata".  
   - For DB2 specifically: try turning off "Read table statistics" or similar in the driver properties if available.  
   - Increase fetch size or change result set limits in **Preferences → Editors → Data Editor** to reduce initial load pressure (though this affects data, not metadata).  
   - Use **Database → Metadata → Clear metadata cache** (sometimes helps reset stuck caches).  

3. **Workarounds if it keeps happening**  
   - After first load, subsequent opens of the same table are usually faster (caches are built).  
   - If the task never finishes and blocks UI: cancel it repeatedly or restart DBeaver.  
   - Consider updating DBeaver to the latest version — some DB2 metadata loading bugs have been improved over time (check release notes for DB2 fixes).  
   - Use a newer/optimized DB2 JDBC driver in DBeaver's Driver Manager (e.g., db2jcc4.jar from IBM).

This split between "data loads fine" and "stuck loading item / background task" is a known pattern in DBeaver + DB2 combinations and not usually a bug in data retrieval itself.

References:  

- [Background tasks taking a while or getting "stuck"](https://github.com/dbeaver/dbeaver/issues/38702)
- [very long "Load DB2TableCache" during query execution](https://github.com/dbeaver/dbeaver/issues/12425)
- [DB2 : infinite load schema statistics](https://github.com/dbeaver/dbeaver/issues/21216)
- [Background Tasks documentation](https://dbeaver.com/docs/dbeaver/Background-Tasks)
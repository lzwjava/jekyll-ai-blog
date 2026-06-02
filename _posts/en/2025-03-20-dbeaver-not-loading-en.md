---
audio: false
generated: true
lang: en
layout: post
title: Solution to Fix DBeaver Not Loading Schemas
translated: false
type: note
---

If you're able to view schemas in an IBM DB2 database using Squirrel SQL on Windows but DBeaver gets stuck at "loading item 0%," the issue likely stems from how DBeaver retrieves metadata compared to Squirrel SQL. Below is a step-by-step guide to troubleshoot and resolve this problem:

---

#### 1. Verify the DB2 Driver in DBeaver

DBeaver requires the correct driver to connect to your IBM DB2 database. Using the wrong driver (e.g., "Db2 for LUW" vs. "Db2 for z/OS") can cause issues with schema loading.

- **Steps**:
  1. Open DBeaver and right-click your DB2 connection in the Database Navigator.
  2. Select **Edit Connection**.
  3. In the "Driver" section, confirm that the selected driver matches your DB2 environment (e.g., "Db2 for LUW" for Linux/Unix/Windows or "Db2 for z/OS" for mainframe).
  4. If unsure, consult your database administrator or documentation to ensure the correct driver is selected.
  5. Click **Test Connection** to verify it works.

---

#### 2. Adjust the "Metadata Source" Property

DBeaver uses a property called "metadata source" to control how it retrieves schema and table information. For DB2, adjusting this setting can resolve schema loading problems.

- **Steps**:
  1. Open your DB2 connection settings in DBeaver (right-click the connection > **Edit Connection**).
  2. Go to the **Driver Properties** tab.
  3. Find the "metadata source" property (or add it if it’s not listed).
  4. Set its value to `0`.
  5. Click **OK** to save the changes.
  6. Reconnect to the database and check if the schemas load.

- **Why this works**: Setting "metadata source" to `0` simplifies how DBeaver fetches metadata, which can bypass issues specific to DB2 schema retrieval.

---

#### 3. Check User Permissions

Although Squirrel SQL displays the schemas, DBeaver might query the database differently, requiring specific permissions to access metadata.

- **Steps**:
  1. Confirm with your database administrator that your user account has privileges to view schemas and metadata in DB2 (e.g., `SELECT` on system catalog tables like `SYSCAT.SCHEMATA`).
  2. If permissions are insufficient, ask your DBA to grant the necessary rights.
  3. Test the connection again in DBeaver.

---

#### 4. Rule Out Network or Firewall Issues

A network restriction or firewall could prevent DBeaver from fully retrieving schema data, even if Squirrel SQL works.

- **Steps**:
  1. Ensure the DB2 server is reachable from your Windows machine (e.g., ping the server or test the port).
  2. Check with your network team to confirm no firewall rules block DBeaver’s connection.
  3. If possible, test DBeaver from a different machine to isolate the issue.

---

#### 5. Update DBeaver to the Latest Version

Older versions of DBeaver may have bugs affecting DB2 schema loading.

- **Steps**:
  1. In DBeaver, go to **Help** > **Check for Updates**.
  2. Install any available updates.
  3. Restart DBeaver and reconnect to the database.

- **Alternative**: Download the latest version from the [DBeaver website](https://dbeaver.io/) and reinstall if updates aren’t available.

---

#### 6. Enable Debug Logging for Further Troubleshooting

If the above steps don’t resolve the issue, enable debug logging to identify specific errors during schema loading.

- **Steps**:
  1. Go to **Window** > **Preferences** > **DBeaver** > **Logging**.
  2. Enable detailed logging and save the settings.
  3. Reconnect to the database and attempt to load the schemas.
  4. Check the log files (usually in the DBeaver workspace folder) for error messages related to DB2 schema retrieval.
  5. If needed, share the logs with DBeaver support or a forum for further assistance.

---

### Why This Happens

- **DBeaver vs. Squirrel SQL**: DBeaver is a more feature-rich tool and retrieves additional metadata compared to Squirrel SQL’s simpler approach. This can lead to compatibility issues with DB2 if settings aren’t optimized.
- **Common Fix**: Adjusting "metadata source" to `0` is a known workaround for DB2 schema loading problems in DBeaver.

---

### Next Steps

Start with steps 1 and 2 (driver verification and metadata source adjustment), as they are the most likely fixes. If the issue persists, proceed through the remaining steps. If none work, consider posting your debug logs to the [DBeaver community](https://github.com/dbeaver/dbeaver/issues) for additional help.

This should resolve the "loading item 0%" issue and allow you to view schemas in DBeaver as you do in Squirrel SQL!

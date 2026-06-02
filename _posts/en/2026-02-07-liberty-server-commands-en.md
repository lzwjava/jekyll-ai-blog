---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Liberty Server Command Guide
translated: false
type: note
---

**Question:** Comprehensive introduction to WebSphere Liberty profile server.sh / server.bat command line options

**Answer:**

WebSphere Liberty (also known as WebSphere Application Server Liberty) uses a single **server** script/command for most administrative tasks.

- On Unix/Linux → `server.sh`
- On Windows → `server.bat`

This script is located in the `wlp/bin/` directory (or `$OPEN_LIBERTY_HOME/bin/` for Open Liberty).

The general syntax is:

```bash
server <action> [serverName] [options]
```

If no `serverName` is specified, it uses the **defaultServer**.

### Main Actions (Commands)

- **create** — Creates a new server directory and basic configuration files
  Example: `server create myServer`

- **start** — Starts the server in the **background** (most common for production)
  Example: `server start myServer`

- **run** — Starts the server in the **foreground** (console output stays in current terminal; good for development/debugging)
  Example: `server run myServer`

- **stop** — Gracefully stops the server
  Example: `server stop myServer`

- **status** — Checks if the server is running
  Example: `server status myServer`

- **package** — Packages the server (including configuration and applications) into a .zip, .jar, or .tar.gz file
  Example: `server package myServer --include=usr`

- **dump** — Creates a diagnostic snapshot (thread dump, configuration, trace, etc.)
  Example: `server dump myServer`

- **javadump** — Requests a Java core dump / heap dump from a running server
  Example: `server javadump myServer`

- **help** — Shows help for the server command or a specific action
  Example: `server help start`

### Commonly Used Options (most apply to start/run/stop/package/dump)

| Option                        | Description                                                                 | Applies to          | Example                              |
|-------------------------------|-----------------------------------------------------------------------------|---------------------|--------------------------------------|
| `--clean`                     | Deletes all persistent cached data (OSGi resolver cache, transformed classes, etc.) before starting | start, run          | `server start --clean`              |
| `--timeout=<seconds>`         | Maximum time (in seconds) to wait for server to stop (default 30–60s depending on version) | stop                | `server stop --timeout=120`         |
| `--timeout=2m30s`             | Supports units: s, m, h (added in Open Liberty ~23.x; WebSphere Liberty later versions) | stop                | `server stop --timeout=3m`          |
| `--include={all,usr,bin}`     | Controls what gets packaged (all = full server + usr; usr = just configuration/apps) | package             | `server package --include=usr`      |
| `--archive=filename.zip`      | Specifies output file name for package command                              | package             | `server package --archive=my.zip`   |
| `--template=...`              | Uses a custom server template during create                                 | create              | `server create --template=javaEE7`  |
| `--osgiDebug`                 | Enables OSGi console (useful for debugging bundle issues)                   | start, run          | `server run --osgiDebug`            |
| `--debug[=<port>]`            | Enables JVM remote debug (suspend=y,n; default port 7777)                   | start, run          | `server start --debug=8888`         |
| `--json`                      | Output in JSON format (useful for scripting)                                | status, dump, etc.  | `server status --json`              |
| `--variable_name=value`       | Overrides server variables at startup (after `--`)                          | start, run          | `server start -- --http.port=9082`  |

### Important Notes About Variable Overrides

To pass JVM properties, Liberty variables, or system properties at startup:

```bash
server start myServer -- --my.custom.prop=value -Djavax.net.ssl.trustStore=...
```

The `--` separator is required before variable/property overrides.

### Quick Reference Examples

```bash
# Create fresh server
server create testServer

# Start in background, clean cache
server start testServer --clean

# Start in foreground with debug port 7777
server run testServer --debug=7777

# Stop with longer timeout
server stop testServer --timeout=180

# Create lightweight runnable package (just usr folder content)
server package testServer --include=usr --archive=testServer-usronly.zip

# Get diagnostic dump while running
server dump testServer
```

### Where to Find the Most Up-to-Date List

The official reference is usually found in IBM Docs under:

"Server command options" → <https://www.ibm.com/docs/en/was-liberty/base?topic=reference-server-command-options>

For Open Liberty (very similar syntax, often identical in recent years):
<https://openliberty.io/docs/latest/reference/command/server-commands.html>

Run `server help` or `server help start` on your installed version for the exact options supported in your specific Liberty version.

**References:**

- [Server command options - IBM](https://www.ibm.com/docs/SSAW57_liberty/com.ibm.websphere.wlp.nd.multiplatform.doc/ae/rwlp_command_server.html)
- [server commands :: Open Liberty Docs](https://openliberty.io/docs/latest/reference/command/server-commands.html)
- [server start command :: Open Liberty Docs](https://openliberty.io/docs/latest/reference/command/server-start.html)

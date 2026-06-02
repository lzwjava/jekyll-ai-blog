---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: IBM WebSphere wsadmin Tool Overview
translated: false
type: note
---

### Overview of wsadmin in IBM WebSphere Application Server (WAS)

The `wsadmin` tool is a command-line scripting interface for administering WebSphere Application Server. It allows you to automate tasks like managing servers, deploying applications, configuring resources, and monitoring runtime operations. Scripts can be written in Jython (Python-based) or JACL (Tcl-based), with Jython being the more commonly used due to its readability.

- **`wsadmin.bat`**: Used on Windows systems.
- **`wsadmin.sh`**: Used on Unix/Linux/AIX systems.

Both tools are located in the `bin` directory of a WebSphere profile (e.g., `<WAS_HOME>/profiles/<ProfileName>/bin/`) or the base installation (`<WAS_HOME>/bin/`). It's recommended to run them from the profile's `bin` directory to ensure the correct environment.

#### Starting wsadmin Interactively

This launches a shell where you can enter commands directly.

**Syntax:**

```
wsadmin[.bat|.sh] [options]
```

**Basic Example (Windows):**

```
cd C:\IBM\WebSphere\AppServer\profiles\AppSrv01\bin
wsadmin.bat -lang jython -user admin -password mypass
```

**Basic Example (Unix/Linux):**

```
cd /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/bin
./wsadmin.sh -lang jython -user admin -password mypass
```

- `-lang jython`: Specifies Jython (use `-lang jacl` for JACL).
- `-user` and `-password`: Required if global security is enabled (omit if disabled).
- If omitted, it connects to the local server using the default SOAP connector on port 8879 (or RMI on 2809).

Once in the wsadmin prompt (e.g., `wsadmin>`), you can run commands using scripting objects:

- **AdminConfig**: For configuration changes (e.g., creating resources).
- **AdminControl**: For runtime operations (e.g., starting/stopping servers).
- **AdminApp**: For application deployment/update.
- **AdminTask**: For high-level tasks (e.g., syncing nodes).
- **Help**: For built-in help (e.g., `Help.help()`).

**Example Commands in the Shell:**

- List all servers: `print AdminConfig.list('Server')`
- Start a server: `AdminControl.invoke(AdminControl.completeObjectName('type=ServerIndex,process=server1,*'), 'start')`
- Save changes: `AdminConfig.save()`
- Exit: `quit`

#### Running a Script File

Use the `-f` option to execute a Jython (.py or .jy) or JACL (.jacl) script non-interactively.

**Example Script (deployApp.py):**

```python
# Connect and deploy an app
appName = 'MyApp'
AdminApp.install('/path/to/MyApp.ear', '[-appname ' + appName + ']')
AdminConfig.save()
print 'Application ' + appName + ' deployed successfully.'
```

**Run on Windows:**

```
wsadmin.bat -lang jython -f /path/to/deployApp.py -user admin -password mypass
```

**Run on Unix/Linux:**

```
./wsadmin.sh -lang jython -f /path/to/deployApp.py -user admin -password mypass
```

#### Running a Single Command

Use the `-c` option for one-off commands (useful in batch files or automation).

**Example (Windows batch file snippet):**

```batch
@echo off
call "C:\IBM\WebSphere\AppServer\profiles\AppSrv01\bin\wsadmin.bat" -lang jython -c "print AdminConfig.list('Server')" -user admin -password mypass
```

**Example (Unix shell script snippet):**

```bash
#!/bin/bash
./wsadmin.sh -lang jython -c "print AdminConfig.list('Server')" -user admin -password mypass
```

#### Key Options

| Option | Description | Example |
|--------|-------------|---------|
| `-conntype` | Connector type: `SOAP` (default, port 8879) or `RMI` (port 2809). | `-conntype RMI` |
| `-host` | Remote host to connect to. | `-host myhost.example.com` |
| `-port` | Connector port. | `-port 8879` |
| `-tracefile` | Log output to a file. | `-tracefile wsadmin.log` |
| `-profile` | Run a profile script before the main script. | `-profile init.py` |
| `-c` | Execute a single command (non-interactive). | `-c "AdminConfig.save()"` |
| `-f` | Execute a script file. | `-f myscript.py` |
| `-job` | Run a job manager command. | `-job deploy.xml` |

#### Tips and Best Practices

- **Security**: If global security is off, omit `-user` and `-password`. For secure setups, use encrypted credentials or key files.
- **Thin Client Mode**: For remote administration without a full WAS install, use `wsadmin -conntype NONE` with thin client JARs (e.g., `com.ibm.ws.admin.client_*.jar`).
- **Performance**: For multiple commands, use a single `-f` script instead of repeated `-c` calls to avoid JVM overhead.
- **Error Handling**: Always call `AdminConfig.save()` after configuration changes. Use try-except in Jython for robustness.
- **Generating Commands**: In the WAS Admin Console, perform an action and click "View administrative scripting command for last action" to get the equivalent wsadmin command.
- **Version Notes**: Behavior is consistent across WAS 8.5+ and 9.0+, but check IBM docs for version-specific details (e.g., Jython 2.7 in newer versions).

For more advanced usage, explore the AdminTask object for simplified commands like `AdminTask.importFile('path/to/file')`.

### References

- [wsadmin scripting tool - IBM Docs](https://www.ibm.com/docs/en/was-nd/9.0.5?topic=scripting-wsadmin-tool)
- [Getting started with wsadmin scripting - IBM Docs](https://www.ibm.com/docs/SSAW57_8.5.5/com.ibm.websphere.nd.doc/ae/txml_script.html)
- [WAS - wsadmin (Jython) Tutorial](http://www.mtitek.com/tutorials/websphere/wsadmin_jython.php)
- [IBM WebSphere - Getting Started with wsadmin](https://www.freekb.net/Article?id=1563)
- [WSADMIN Tutorial – Part1](https://websphereapplicationservernotes.wordpress.com/2012/12/25/wsadmin-tutorial-part1/)

---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Correct WebSphere Application Server Creation
translated: false
type: note
---

No, the command `nodeName -name serverName admin create applciation server` (noting the typo in "applciation") is not correct for creating an application server in IBM WebSphere Application Server (WAS) using wsadmin scripting.

### Correct Syntax
The proper command uses the `AdminTask.createApplicationServer` method in Jython (the recommended scripting language for wsadmin). It requires:
- The **node name** as the first argument (a string).
- A **list of options** as the second argument, including `-name` for the server name.

**Basic example:**
```jython
AdminTask.createApplicationServer('YourNodeName', ['-name', 'YourServerName'])
```

- Replace `'YourNodeName'` with the actual node (e.g., `ndnode1`).
- Replace `'YourServerName'` with the desired server name (e.g., `appServer1`).
- Optional parameters can be added to the list, like `'-templateName', 'default'` for using a default server template.

### Steps to Run It
1. Start wsadmin in Jython mode: `./wsadmin.sh -lang jython -user admin -password pass`.
2. Execute the command above.
3. Save the configuration: `AdminConfig.save()`.
4. Exit: `quit`.

This creates a basic application server on the specified node. For more options (e.g., ports, JVM settings), refer to the full AdminTask documentation.

[ServerManagement command group for the AdminTask object](https://www.ibm.com/docs/en/was-nd/9.0.5?topic=scripting-servermanagement-command-group-admintask-object)
[Creating a server using scripting](https://www.ibm.com/docs/en/was/9.0.5?topic=scripting-creating-server-using)

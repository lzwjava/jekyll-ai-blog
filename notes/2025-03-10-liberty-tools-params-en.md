---
audio: false
generated: true
lang: en
layout: post
title: Pass Custom JVM Parameters in Liberty Tools Plugin
translated: false
type: note
---

You can pass custom JVM parameters—like `-Dversion=5.1`—by adding them to your Liberty dev mode launch configuration in VS Code. Typically, you do this by editing (or creating) the `.vscode/launch.json` file in your project and including the parameter under a property like `"vmArgs"` (or `"args"` if your configuration expects Maven goal arguments).

For example, if you’re using the Liberty Tools extension with dev mode, your configuration might look like this:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "liberty",
      "request": "launch",
      "name": "Liberty Dev Mode",
      "goal": "dev",
      "vmArgs": "-Dversion=5.1"
    }
  ]
}
```

### Steps

1. **Open or Create the Launch Configuration:**
   - In VS Code, open your project.
   - Navigate to the `.vscode` folder and open (or create) `launch.json`.

2. **Add Your Dev Mode Configuration:**
   - Add a configuration entry as shown above. The key `"vmArgs"` lets you specify JVM options that will be passed to the server when dev mode starts.

3. **Save and Launch:**
   - Save the file.
   - Use the Run and Debug view to start the “Liberty Dev Mode” configuration.

If you’re using Maven directly, you could also start dev mode from the command line with:

```bash
mvn liberty:dev -Dversion=5.1
```

This passes the custom property to the JVM when starting the server.

By configuring it this way, the Liberty Tools extension will include your custom parameter (`-Dversion=5.1`) each time you start dev mode.

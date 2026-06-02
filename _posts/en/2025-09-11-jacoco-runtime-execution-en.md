---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: JaCoCo Runtime Execution File Behavior
translated: false
type: note
---

When you run **WebSphere Liberty Profile** with the **JaCoCo agent** in `exec` mode, the JaCoCo agent does **not modify** the original `.exec` file during runtime. Here’s what happens:

---

### How JaCoCo Works in `exec` Mode
- **Purpose**: The JaCoCo agent collects **code coverage data** while your application runs.
- **Output**: It writes coverage data to the `.exec` file (e.g., `jacoco.exec`).
- **File Behavior**:
  - If the file **does not exist**, JaCoCo creates it.
  - If the file **already exists**, JaCoCo **appends** new coverage data to it (it does not overwrite or modify existing data unless you explicitly reset or merge the file).
  - The original `.exec` file is **not altered** in a way that would break or change its structure—it only grows with new data.

---

### Will the `.exec` File Be Modified?
- **Yes, but only by appending data**: The file will be updated with new coverage information each time you run your application with the JaCoCo agent.
- **No structural changes**: The format of the `.exec` file remains the same; it’s a binary file containing coverage data.

---

### Best Practices
- **Merge or Reset**: If you want to start fresh, delete or rename the `.exec` file before running your application again.
- **Merge Multiple Runs**: Use the `jacoco:merge` goal (in Maven) or the `org.jacoco.agent.rt.RT` class to merge multiple `.exec` files if needed.

---

### Example Liberty Configuration
In your `server.env` or `jvm.options` for Liberty, you might see:
```bash
-javaagent:/path/to/jacocoagent.jar=destfile=/path/to/jacoco.exec,append=true
```
- `append=true` ensures new data is added to the existing file.

---

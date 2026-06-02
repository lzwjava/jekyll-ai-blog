---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Maven Multi-Module Dependency Resolution
translated: false
type: note
---

Yes, that's correct—in a Maven multi-module project, when one module (e.g., an EAR module) depends on another (e.g., a WAR module), Maven resolves the dependency from the local `.m2/repository` by default, not directly from the other module's `target/` directory. This is because Maven treats inter-module dependencies as standard artifact references (like external libs), so the dependent artifact must be installed (or at least packaged and discoverable via the build reactor).

### Why This Happens

- **Local Repo Resolution**: Maven's dependency resolution mechanism looks for artifacts in the local repository first. The `target/` dir is only used temporarily during the build of a single module, but for cross-module refs, it expects the artifact to be "published" (installed).
- **Reactor Builds Help, But Aren't Always Enough**: If you run `mvn package` (or `mvn install`) from the **parent POM** root, Maven's reactor automatically builds modules in topological order. It resolves inter-module deps on-the-fly without needing explicit installs, pulling from the other module's fresh `target/` output during the session. But if you build the dependent module (e.g., EAR) **independently** (e.g., `cd ear-module && mvn package`), it won't see the WAR's `target/`—it'll fail unless the WAR artifact is already in `.m2`.

### For WAR-to-EAR Packaging Specifically

In an EAR project:

- The EAR plugin (`maven-ear-plugin`) expects the WAR (and other modules) as resolved artifacts to include in the EAR archive (e.g., via `<modules>` in the EAR POM).
- If the WAR isn't installed, you'll get errors like "Could not resolve dependencies" or missing modules in the EAR.

**Solution**: Yes, you generally need to run `mvn install` (or at least `mvn package` in a full reactor build) on the "original" (dependency) module first if building independently. Best practices:

1. **Preferred: Build from Parent**: `mvn clean install` at the project root. This installs everything to `.m2` and handles ordering automatically.
2. **If Building Modules Separately**:
   - `cd war-module && mvn clean install` (installs the WAR JAR to `.m2`).
   - Then `cd ear-module && mvn clean package` (or `install`—EARs often just need `package`).
3. **Avoid Direct Target Refs**: Don't hack around this with `<systemPath>` or file paths to `target/`—it's brittle and skips Maven's checksums/transitivity.

This behavior hasn't changed in recent Maven versions (up to 3.9.x as of 2025). For more details, see the official multi-module guide.

[Introduction to the Build Lifecycle - Multi-module Projects](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#multi-module)
[Maven EAR Plugin Documentation](https://maven.apache.org/plugins/maven-ear-plugin/ear-mojo.html)

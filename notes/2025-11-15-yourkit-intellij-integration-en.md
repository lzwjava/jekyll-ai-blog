---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: YourKit Profiler Integrates Seamlessly with IntelliJ
translated: false
type: note
---

Yes, YourKit Java Profiler integrates very well with IntelliJ IDEA (both Community and Ultimate editions), and it’s one of the smoothest profiler-to-IDE experiences available for Java.

Here are the key integration features you asked about:

- Direct launch from IDEA
  Once you install the YourKit plugin (available from JetBrains Marketplace or from YourKit’s own plugin), you get new run configurations like “YourKit Snapshot”, “YourKit Profiling (CPU)”, “YourKit Profiling (Memory)”, etc., right next to your normal Run/Debug buttons.

- Start/stop profiling directly from the IDE toolbar
  You can start profiling with one click, and stop it + automatically open the captured snapshot without leaving IDEA.

- Click in the profiler UI → instantly jump to source code in IDEA
  YourKit detects that IDEA is running and automatically sets up the decompilation/source navigation. When you double-click any method, stack frame, allocation hotspot, etc., in YourKit’s UI, it opens the exact line in your IDEA editor (works even if you only have bytecode, thanks to built-in decompiler support).

- Welcome snapshot on application exit
  You can configure YourKit to capture a snapshot automatically when your app terminates, and IDEA will open it immediately.

Current status (as of YourKit 2024.9, which is the latest stable in late 2025):

- Full support for IntelliJ IDEA 2023.3–2025.2+
- Works perfectly with Java 8–24 (including virtual threads profiling on Java 21+)
- Also supports Kotlin, Scala, Groovy, etc., and jumps to the correct source.

Installation steps (quick):

1. In IDEA → Settings → Plugins → Marketplace → search “YourKit”
2. Install/restart
3. YourKit agent is bundled with the plugin, so no separate YourKit installation needed for basic use (though you can install the full standalone YourKit app if you want the richer UI outside IDEA).

Most Java developers who use YourKit daily never leave IDEA for profiling once this plugin is set up.

So yes — exactly the workflow you described works out of the box and is very polished.

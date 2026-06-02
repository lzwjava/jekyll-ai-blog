---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: IntelliJ Remote Debugging Setup Guide
translated: false
type: note
---

Short answer: yes—if you keep the build and the running JVM in sync, IntelliJ remote debug will attach cleanly. Here’s a solid, low-drama way to do it across Liberty locally and Cloud Foundry.

## 1) Prevent “class mismatch” before you attach

* Always align JDKs: the JDK used by Maven compilation, Liberty’s JVM, and (if on CF) the Java buildpack’s JDK must match major version. In Maven, pin it with `maven-compiler-plugin` (`release` or `source/target`) and make sure Liberty/CF uses the same.
* Clean stale bytecode when switching branches or toggling modules: `mvn clean package -DskipTests` is the simplest guardrail.
* In IntelliJ, also “Rebuild Project” once if you mixed IDE build and Maven build previously.

## 2) Auto-rebuild only when it matters (30-minute rule)

If you want to rebuild only when compiled classes are older than 30 minutes, wrap Maven in a tiny check.

### Bash (macOS/Linux)

```bash
#!/usr/bin/env bash
set -euo pipefail

CLASSES_DIR="target/classes"
THRESHOLD_MIN=30

needs_build() {
  # no classes yet?
  [[ ! -d "$CLASSES_DIR" ]] && return 0
  # latest class mtime older than threshold?
  last_mod_epoch=$(find "$CLASSES_DIR" -type f -name '*.class' -printf '%T@\n' 2>/dev/null | sort -n | tail -1)
  [[ -z "${last_mod_epoch:-}" ]] && return 0
  now_epoch=$(date +%s)
  diff_min=$(( ( now_epoch - ${last_mod_epoch%.*} ) / 60 ))
  (( diff_min >= THRESHOLD_MIN ))
}

if needs_build; then
  echo "Classes are old (>= ${THRESHOLD_MIN}m) or missing — building…"
  mvn clean package -DskipTests
else
  echo "Classes are fresh (< ${THRESHOLD_MIN}m) — skipping build."
fi
```

### PowerShell (Windows)

```powershell
$classes = "target\classes"
$thresholdMin = 30

function Needs-Build {
  if (-not (Test-Path $classes)) { return $true }
  $last = Get-ChildItem $classes -Recurse -Filter *.class |
          Sort-Object LastWriteTime -Descending |
          Select-Object -First 1
  if (-not $last) { return $true }
  $age = (New-TimeSpan -Start $last.LastWriteTime -End (Get-Date)).TotalMinutes
  return ($age -ge $thresholdMin)
}

if (Needs-Build) {
  Write-Host "Classes are old (>= $thresholdMin m) or missing — building…"
  mvn clean package -DskipTests
} else {
  Write-Host "Classes are fresh (< $thresholdMin m) — skipping build."
}
```

## 3) Liberty (local) — start in debug and attach from IntelliJ

You have two easy options:

**A. One-shot debug start**

```bash
server debug myServer   # default JDWP at port 7777
```

**B. Permanent config**

* In `wlp/usr/servers/myServer/jvm.options`:

```
-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:7777
```

* Or via env:

```
WLP_DEBUG_ADDRESS=7777
WLP_DEBUG_SUSPEND=false
```

**IntelliJ attach**

* Run → “Edit Configurations…” → “Remote JVM Debug”.
* Host: `localhost`, Port: `7777`.
* Hit Debug; you should see “Connected to the target VM…” and breakpoints will bind.

> Tip: after a rebuild, Liberty picks up updated classes for most features via hot swap. If a method signature or class shape changed, you’ll need a server restart for those changes to load.

## 4) Cloud Foundry (PCF) — what’s realistic

CF runs apps behind its routing layer; you typically cannot expose a JDWP port directly. You have two workable patterns:

**Option 1: Buildpack debug + SSH tunnel (for dev/staging only)**

1. Enable JVM debug in the Java buildpack:

   * Set env before push (names vary slightly by buildpack version):

   ```
   cf set-env <APP> JBP_CONFIG_DEBUG '{enabled: true, port: 7777}'
   ```

2. Restage:

   ```
   cf restage <APP>
   ```

3. Open an SSH tunnel:

   ```
   cf ssh -N -L 7777:localhost:7777 <APP>
   ```

4. In IntelliJ, attach to `localhost:7777`.

**Option 2: Use CF SSH JMX/Diagnostics instead of JDWP**

* When direct JDWP is not allowed, rely on:

  * app logs + targeted loggers,
  * thread/heap dumps via `cf ssh` + `jcmd`/`jmap` (if present),
  * feature flags like Liberty’s trace and health endpoints.

> Reality check: many CF orgs disable debug ports in prod. Treat remote JDWP on CF as a debug-only path for non-prod spaces. If your platform team blocks it, fall back to logs + SSH diagnostics.

## 5) Common “couldn’t bind breakpoints” causes (and fixes)

* **Class file mismatch**: clean rebuild; verify only one copy of the class on the runtime classpath (watch for fat JARs or duplicate modules).
* **Wrong JDWP port**: confirm Liberty actually listening (`server debug` logs or `netstat` locally; for CF, the SSH tunnel line must match).
* **Different JDK major**: make sure Maven/Liberty/CF JDKs are the same (e.g., all Java 17).
* **Compiler debug info stripped**: ensure `maven-compiler-plugin` isn’t using `-g:none`. Default is fine; if customized, include `-g`.
* **Reload needed**: after signature changes, restart Liberty (or restage on CF).

---

If you wire it up like above—either always `mvn clean package` or the “30-minute freshness” wrapper—IntelliJ remote debug will attach reliably to Liberty, and it can work on CF via an SSH tunnel in non-prod.

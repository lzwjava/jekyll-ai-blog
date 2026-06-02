---
audio: false
generated: true
image: false
lang: en
layout: post
title: Java Migration Smart Fix Strategy
translated: false
type: note
---

**Question:** When doing a big upgrade from Java 8 to Java 21 and encountering many compilation errors, is the best approach to identify the main types of errors, apply one small representative fix, and then use Copilot or Claude as a mass-edit tool to apply similar changes across the codebase?

**Answer:**

Yes — this is currently (2025–2026) one of the most pragmatic and widely used strategies for large Java 8 → 17/21 migrations, especially in real-world projects with >50–300 kLOC.

The most common successful pattern looks like this:

1. **First compile with the new JDK** (without any fixes)
   → collect **all** errors (most IDEs / build tools can give you a categorized summary)

2. **Group errors into 5–12 dominant families** (usually these cover 75–90% of problems):

   - `var` reserved keyword conflict (very frequent)
   - diamond operator <> + anonymous class changes (Java 9+)
   - `sun.misc.Unsafe` → mostly removed or strongly discouraged
   - JAXB / JAX-WS / CORBA / other removed modules (`java.xml.bind`, etc.)
   - `java.util.Date` / `Calendar` still compiling but many new APIs want `java.time.*`
   - Reflection / illegal reflective access warnings → turned into hard errors with `--illegal-access=deny` or later Java versions
   - `PermGen` → `Metaspace` (usually not compile error, but out-of-memory)
   - `javax.*` → `jakarta.*` (if you also upgrade to Jakarta EE / Spring Boot 3)
   - Removal of `finalize()` calls or overrides
   - `SecurityManager` deprecation / removal (Java 17 → 21)
   - `Thread.stop()`, `Thread.destroy()`, `Runtime.runFinalizersOnExit()` gone
   - `ProcessBuilder` / `Process` API changes
   - `Nashorn` → `GraalJS` or external engine
   - Record patterns, switch expressions, sealed classes (mostly new features, rarely break old code)

3. **Pick the 2–4 most frequent & easiest-to-automate families** first

4. **Do one clean, correct, reviewable fix** for that family
   → commit it
   → run full test suite (or smoke tests)

5. **Ask Copilot / Claude / Cursor / Windsurf / Continue.dev / Amazon Q / Cody** one of these styles:

   - “Replace all usages of `sun.misc.Unsafe` with `jdk.internal.misc.Unsafe` (or VarHandle / Foreign Memory API when possible) — keep the logic identical”
   - “Convert every occurrence of `new Type() { … };` with diamond <> to explicit type on the right side”
   - “Replace every import `javax.xml.bind.*` with `jakarta.xml.bind.*` and update the package name everywhere”
   - “Rewrite every `finalize()` method to use `Cleaner` or just remove it if it only does logging”
   - “Convert classic Date/Calendar → ZonedDateTime / Instant / LocalDateTime following these rules: …”

6. **Accept → eyeball diff** → commit small logical groups (100–600 files per PR)

7. **Recompile → new error families appear** → repeat from step 2

**Most experienced teams report this sequence is faster and produces fewer regressions than:**

- trying to fix everything manually in one huge pass
- turning on every new lint rule + new language feature at the same time
- letting AI do the whole migration in one 30 kLOC prompt (almost always poor quality)

**Quick priority order many teams use (2024–2026 data):**

1. `var` keyword conflicts
2. JAXB / Activation / XML / WS modules → Jakarta or alternatives
3. Unsafe / reflection / illegal access
4. Date/Time API friction (mostly warnings + behavioral differences)
5. SecurityManager / finalize / deprecated API removals
6. Library upgrades needed because of module system (log4j2 2.17+, jackson 2.12+, etc.)

So yes — classify → fix one family cleanly → teach the AI that pattern → mass-apply → review/commit → repeat → is still one of the highest-leverage real-world strategies in 2026.

**References:**

- None (based on common industry migration patterns observed 2023–2026)

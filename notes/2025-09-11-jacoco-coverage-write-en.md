---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: JaCoCo Coverage Data Write Behavior
translated: false
type: note
---

In **integration tests** (or any JVM process) using the **JaCoCo agent**, the coverage data is **not automatically written to the `.exec` file when the JVM exits**. Here’s how it works:

---

### When Does JaCoCo Write Coverage Data?

- **During JVM Shutdown**: The JaCoCo agent **flushes and writes** the collected coverage data to the `.exec` file **when the JVM shuts down gracefully** (e.g., when the main method ends or the test suite completes).
- **If the JVM Crashes**: If the JVM terminates abruptly (e.g., due to a crash or `System.exit()`), the agent may **not** have a chance to write the data, and some coverage information could be lost.

---

### How to Ensure Data is Written

1. **Graceful Shutdown**: Ensure your integration tests or application ends normally (e.g., no forced exits).
2. **Explicit Dump (Optional)**: You can manually trigger a dump of coverage data during runtime using the JaCoCo runtime API (e.g., `org.jacoco.agent.rt.RT.getAgentRuntime().dump(true, outputFile)`). This is useful for long-running processes or if you want to capture intermediate data.

---

### Example Scenario

- If your integration test suite runs and completes normally, the JaCoCo agent will write the coverage data to `jacoco.exec` (or your specified file) **at the end of the JVM process**.
- If the JVM is killed (e.g., `kill -9`), the data may not be written.

---

### Best Practice

- **Use `append=true`**: If you run multiple test suites, set `append=true` in the JaCoCo agent arguments to accumulate coverage data across runs.
- **Check for Partial Data**: If the JVM crashes, the `.exec` file might be incomplete or missing data for the last run.

---

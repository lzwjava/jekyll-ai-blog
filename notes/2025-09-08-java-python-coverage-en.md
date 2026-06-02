---
audio: false
date: 2025-09-08
generated: true
image: false
lang: en
layout: post
title: Multi-module Java Coverage with Python
translated: false
type: note
---

Looking at your setup, you're dealing with a complex but interesting challenge: using Python integration tests to generate coverage for a multi-module Java project. Let me analyze the situation and suggest a comprehensive strategy.

## Current Challenges

1. **Cross-language testing**: Python tests exercising Java code
2. **Multi-module coverage**: Need to capture coverage across all modules from integration tests
3. **Module interdependencies**: `PlaygroundUtils` has no direct endpoints but gets exercised through `PlaygroundWeb`
4. **Scalability concern**: How to handle this for 10+ modules

## Recommended Strategy

### Option 1: Single JaCoCo Agent, Merged Report (Recommended)

This is the most scalable approach for your use case:## Key Improvements and Strategy

### 1. **Single JaCoCo Agent Approach**

- Use ONE `jacoco-it.exec` file at the parent level
- Configure the agent with `append=true` and `includes=org.lzw.*`
- This captures ALL module coverage in a single pass

### 2. **Report Aggregation**

- Use `jacoco:report-aggregate` to create a unified report
- This automatically finds all module classes and generates coverage for them

### 3. **Profile-Based Execution**

- Separate concerns: `run-integration-tests` profile for running tests
- `integration-test-coverage` profile for generating reports
- Makes the build more modular and maintainable

### 4. **Scalability for 10+ Modules**

For larger projects, consider this enhanced approach:## Summary and Best Practices

### For Your Current 2-Module Setup

1. **Use a single JaCoCo exec file** at the parent level with `append=true`
2. **Run Jetty once** with the agent configured to capture all modules
3. **Use `report-aggregate`** to generate a unified report

### For Scaling to 10+ Modules

1. **Module Grouping**: Create logical groups (core, service, web) and generate separate reports
2. **Coverage Tracking**: Implement a Python helper to track which modules are covered
3. **Parallel Testing**: Run different test suites in parallel for faster feedback
4. **Incremental Coverage**: Use Maven profiles to run coverage for specific module groups

### Key Configuration Points

- **`append=true`**: Ensures multiple test runs accumulate coverage
- **`includes=org.lzw.*`**: Captures all your modules in one agent
- **Profile separation**: Keep integration testing separate from regular builds
- **Single exec file**: Eliminates the need to run Jetty multiple times

### Command Line Usage

```bash
# Full coverage with integration tests
mvn clean verify -Prun-integration-tests,integration-test-coverage

# Just unit test coverage
mvn clean test

# Coverage for specific module group
mvn clean verify -Pcoverage-by-layer
```

This approach scales well because:

1. You only start/stop Jetty once regardless of module count
2. JaCoCo automatically handles multi-module class files
3. The Python tests don't need to know about Java module structure
4. Reports can be aggregated or split as needed for different audiences

The key insight is that JaCoCo's agent can capture coverage for ALL classes in the JVM, not just the module being tested. By using a shared exec file and the aggregate goal, you get complete coverage data in a single test run.

---
audio: false
date: 2025-09-08
generated: true
image: false
lang: en
layout: post
title: IT Coverage for Modular Spring Apps
translated: false
type: note
---

### Overall Assessment of Your Setup
Your current configuration is solid for a small multi-module project like this, especially since you've already got the core flow working: attaching the JaCoCo agent to Jetty, running external Python integration tests via the Exec Plugin, and generating a report in the `PlaygroundWeb` module. This captures runtime coverage from API endpoints tested by Python's `unittest`, which is exactly what you need for integration test (IT) coverage in a Spring web app.

Key strengths:
- **Modular and phase-bound**: Using Maven phases (`pre-integration-test` for Jetty start, `integration-test` for Python tests, `post-integration-test` for stop, `verify` for report) ensures reliability and reproducibility.
- **Agent attachment**: The JVM arg (`-javaagent:...`) on Jetty correctly instruments the runtime, capturing coverage in `jacoco.it.exec`.
- **External tests integration**: The Exec Plugin handles Python nicely, and keeping tests at the repo root (`${project.parent.basedir}/tests`) decouples them from Java modules.
- **No unnecessary duplication**: You avoid running Jetty/Python in `PlaygroundUtils` (which has no controllers), which is efficient.

Challenges you've identified:
- **Coverage for library modules like `PlaygroundUtils`**: Since utils code runs in the `PlaygroundWeb` JVM (as a dependency in the WAR), it's instrumented and appears in `PlaygroundWeb`'s `jacoco.it.exec`. But your reports are module-specific, so `PlaygroundUtils` coverage isn't visible unless aggregated or included.
- **Non-self-contained nature of JaCoCo**: Unlike Checkstyle/Spotless (which just analyze source/static artifacts), JaCoCo needs runtime data (`.exec` files) from external tests and agent attachment. This makes it brittle for multi-module setups without careful coordination.
- **Aggregate goal limitations**: `jacoco:report-aggregate` expects per-module `.exec` files (e.g., from unit tests), but your coverage is purely from IT in one module. Forcing aggregation can lead to empty reports for libs like `PlaygroundUtils`.
- **Scalability to 10+ modules**: Duplicating Jetty/Python setups across modules would be wasteful (redundant servers/tests). Hacky workarounds like copying `.exec` files or running everything twice (as you mentioned) introduce maintenance overhead and build time bloat.

Your fallback to per-module reports is pragmatic, but we can optimize for coverage inclusion without duplication.

### Recommended Strategy
Focus on **generating a single, comprehensive IT coverage report in the module that runs the app** (`PlaygroundWeb` here), while **including coverage data for dependent modules** like `PlaygroundUtils`. This avoids running tests multiple times and leverages the fact that all code executes in one JVM.

Why this over aggregation?
- Aggregation (`report-aggregate`) is better for distributed unit test coverage across modules. For IT coverage from a single runtime (your case), it's overkill and doesn't fit naturally.
- A unified report gives a holistic view of the app's coverage, which is often more useful than siloed per-module reports (e.g., "80% overall, but utils layer is at 60%").
- For larger projects, this scales by treating the "app module" (WAR/EAR) as the coverage hub, pulling in deps.

#### Step-by-Step Implementation for Your 2-Module Project
Start small: Apply this to your current setup (1 app module + 1 lib). Test it, then expand.

1. **Keep IT Execution in `PlaygroundWeb` Only**:
   - No changes needed here. Jetty starts the WAR (which embeds `PlaygroundUtils`), Python tests hit endpoints, coverage is captured in `${project.build.directory}/jacoco.it.exec`.
   - Confirm utils code is exercised: If your Python tests call endpoints that use `PlaygroundUtils` classes (e.g., `SystemUtils`), their coverage will be in the `.exec` file.

2. **Enhance the JaCoCo Report in `PlaygroundWeb` to Include `PlaygroundUtils`**:
   - Use JaCoCo's `<additionalClassesDirectories>` and `<additionalSourceDirectories>` in the `report` goal. This tells JaCoCo to scan classes/sources from `PlaygroundUtils` against the same `.exec` file.
   - Update `PlaygroundWeb`'s POM (in the `jacoco-maven-plugin` configuration):

     ```xml
     <plugin>
         <groupId>org.jacoco</groupId>
         <artifactId>jacoco-maven-plugin</artifactId>
         <executions>
             <!-- Existing prepare-agent -->
             <execution>
                 <id>prepare-agent</id>
                 <goals>
                     <goal>prepare-agent</goal>
                 </goals>
             </execution>
             <!-- Enhanced report: Include utils module -->
             <execution>
                 <id>report-it</id>
                 <phase>verify</phase>
                 <goals>
                     <goal>report</goal>
                 </goals>
                 <configuration>
                     <dataFile>${jacoco.it.exec}</dataFile>
                     <outputDirectory>${project.reporting.outputDirectory}/jacoco-it</outputDirectory>
                     <!-- Add these to include PlaygroundUtils coverage -->
                     <additionalClassesDirectories>
                         <directory>${project.parent.basedir}/PlaygroundUtils/target/classes</directory>
                     </additionalClassesDirectories>
                     <additionalSourceDirectories>
                         <directory>${project.parent.basedir}/PlaygroundUtils/src/main/java</directory>
                     </additionalSourceDirectories>
                 </configuration>
             </execution>
         </executions>
     </plugin>
     ```

   - This generates one report (in `PlaygroundWeb/target/site/jacoco-it`) covering both modules. You'll see breakdowns by package/class, including `org.lzw` from utils.

3. **Disable/Remove JaCoCo from `PlaygroundUtils`**:
   - Since it has no IT of its own, remove any JaCoCo config/properties (e.g., `<jacoco.it.exec>`, `<it.report.skip>`). It doesn't need to generate its own report—coverage is handled upstream.
   - If you have unit tests in utils, keep a separate `prepare-agent` + `report` for unit coverage (default `jacoco.exec`), but isolate it from IT.

4. **Build and Verify**:
   - Run `mvn clean verify` from the parent.
   - Jetty/Python run only once (in `PlaygroundWeb`).
   - Check `PlaygroundWeb/target/site/jacoco-it/index.html`: It should show coverage for both modules' classes.
   - If utils coverage is 0%, ensure your Python tests exercise those classes (e.g., add a test that triggers `SystemUtils` via an endpoint).

5. **Optional: Enforce Coverage Thresholds**:
   - Add a `check` execution in `PlaygroundWeb`'s JaCoCo plugin to fail the build if coverage drops below a threshold (e.g., 70% line coverage overall).
     ```xml
     <execution>
         <id>check-it</id>
         <goals>
             <goal>check</goal>
         </goals>
         <configuration>
             <dataFile>${jacoco.it.exec}</dataFile>
             <rules>
                 <rule>
                     <element>BUNDLE</element>
                     <limits>
                         <limit>
                             <counter>LINE</counter>
                             <value>COVEREDRATIO</value>
                             <minimum>0.70</minimum>
                         </limit>
                     </limits>
                 </rule>
             </rules>
         </configuration>
     </execution>
     ```

#### Scaling to a Larger Project (e.g., 10 Modules)
For 10+ modules (e.g., multiple libs + 1-2 app/WAR modules), extend the above to avoid complexity:

- **Centralize IT in App Modules**: If you have one main WAR (like `PlaygroundWeb`), make it the "coverage hub." Add `<additionalClassesDirectories>` and `<additionalSourceDirectories>` for all dependent libs (e.g., via a loop or property lists in the parent POM).
  - Example: Define paths in parent properties:
    ```xml
    <properties>
        <lib1.classes>${project.basedir}/Lib1/target/classes</lib1.classes>
        <lib1.sources>${project.basedir}/Lib1/src/main/java</lib1.sources>
        <!-- Repeat for 10 libs -->
    </properties>
    ```
  - In WAR's JaCoCo report config: Reference them dynamically.

- **If Multiple Apps/WARs**: Create dedicated IT modules (e.g., `App1-IT`, `App2-IT`) that depend on the WAR, configure Jetty/Exec/JaCoCo there, and include only relevant deps' classes/sources. This keeps builds modular (e.g., `mvn verify -pl App1-IT` for targeted coverage).

- **Avoid Per-Module IT Duplication**: Never run Jetty/Python in lib modules—it's wasteful. If a lib needs isolated IT (rare), give it its own mini-server/test suite.

- **Aggregation for Reporting (If Needed)**: If you insist on separate per-module reports:
  - Generate the `.exec` in the app module.
  - Use Maven's `dependency:copy` or a custom script (via Exec Plugin) in the parent `post-integration-test` to copy the `.exec` to each lib's `target/` (e.g., as `jacoco-it.exec`).
  - Then, configure `report` in each lib to use that copied file.
  - But this is more complex—prefer the unified report unless stakeholders demand per-module metrics.

- **Tooling Tips for Scale**:
  - **Maven Profiles**: Use profiles (e.g., `-Pcoverage`) to toggle IT/reporting for faster dev builds.
  - **CI Optimization**: In CI (e.g., GitHub Actions), cache Maven deps and run IT only on changes to tests/endpoints.
  - **Alternatives if JaCoCo Gets Too Complex**: Consider SonarQube for aggregated analysis (it ingests JaCoCo data across modules). Or switch to runtime tools like OpenClover, but JaCoCo is fine if you stick to the hub approach.
  - **Testing the Tests**: Add a smoke test in Python to verify server startup (e.g., poll `http://localhost:8080/health`).

This strategy minimizes runs (one Jetty/Python per app), handles JaCoCo's dependencies cleanly, and scales without explosion. If you share more details (e.g., how utils is used in endpoints), I can refine the POM snippets further.

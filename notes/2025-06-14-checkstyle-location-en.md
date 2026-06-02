---
audio: false
generated: true
lang: en
layout: post
title: Checkstyle Config Location
translated: false
type: note
---

To fix the issues you're encountering with the `maven-checkstyle-plugin` when running `mvn clean checkstyle:check`, where it can't find the `checks.xml` file and fails to initialize the `SuppressWithNearbyTextFilter` module, follow these steps. The problems stem from the file location and an incompatible Checkstyle version. Here's a complete solution:

---

### Step 1: Fix the `checks.xml` File Location

The error indicates that the plugin cannot find `checks.xml`. Since it’s located at your project root (not in `src/main/resources`, where the plugin typically looks), you need to explicitly tell the plugin where to find it.

- **Action**: Update the `<configLocation>` in your `pom.xml` to point to the project root.

---

### Step 2: Resolve the `SuppressWithNearbyTextFilter` Error

The `SuppressWithNearbyTextFilter` module fails to initialize because the Checkstyle version used by the plugin is outdated and doesn’t support this filter. You need to upgrade the plugin and specify a compatible Checkstyle version.

- **Action**: Upgrade the `maven-checkstyle-plugin` to version `3.3.1` and add a dependency on Checkstyle version `10.17.0`, which supports `SuppressWithNearbyTextFilter`.

---

### Updated `pom.xml` Configuration

Modify the `maven-checkstyle-plugin` section in your `pom.xml` as follows:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-checkstyle-plugin</artifactId>
    <version>3.3.1</version> <!-- Upgrade to the latest version -->
    <configuration>
        <configLocation>${project.basedir}/checks.xml</configLocation> <!-- Point to checks.xml at project root -->
    </configuration>
    <dependencies>
        <dependency>
            <groupId>com.puppycrawl.tools</groupId>
            <artifactId>checkstyle</artifactId>
            <version>10.17.0</version> <!-- Supports SuppressWithNearbyTextFilter -->
        </dependency>
    </dependencies>
    <executions>
        <execution>
            <id>checkstyle-check</id>
            <phase>compile</phase>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

#### Explanation

- **`<configLocation>${project.basedir}/checks.xml</configLocation>`**: Specifies that `checks.xml` is at the project root (`${project.basedir}` is a Maven property for the root directory).
- **`version 3.3.1`**: Uses a newer plugin version for better compatibility.
- **Checkstyle `10.17.0` dependency**: Ensures the plugin uses a Checkstyle version that includes `SuppressWithNearbyTextFilter`.

---

### Step 3: Verify `checks.xml` Configuration

Ensure that the `SuppressWithNearbyTextFilter` module in your `checks.xml` is correctly defined. An example configuration might look like this:

```xml
<module name="SuppressWithNearbyTextFilter">
    <property name="nearbyTextPattern" value="@SuppressWarnings"/>
</module>
```

- **Action**: Check `checks.xml` for typos or incorrect properties. Refer to the [Checkstyle documentation](https://checkstyle.org/filters/suppresswithnearbytextfilter.html) for details.
- **Troubleshooting Tip**: If the error persists, temporarily remove the `SuppressWithNearbyTextFilter` module from `checks.xml` and run `mvn checkstyle:check` to see if the issue is specific to this filter.

---

### Step 4: Test the Fix

- Run the following command to test:

  ```bash
  mvn clean checkstyle:check
  ```

- If it works, the plugin should find `checks.xml` and process all modules without errors.
- To ensure Checkstyle runs during compilation, use:

  ```bash
  mvn compile
  ```

---

### Optional: Alternative File Location

If you prefer a more standard Maven setup:

- Move `checks.xml` to `src/main/resources/checks.xml`.
- Update `<configLocation>` to:

  ```xml
  <configLocation>classpath:checks.xml</configLocation>
  ```

- This aligns with Maven’s convention of placing resources in `src/main/resources`.

---

### Additional Notes

- **Unrelated Warning**: If you see a warning about a `<blocked>` tag in `/usr/share/maven/conf/settings.xml`, it’s not related to this issue but suggests a problem in your Maven settings file. Review it separately if needed.
- **Still Having Issues?** Share the following for further help:
  - The content (or a snippet) of `checks.xml`.
  - The full output of `mvn clean checkstyle:check -X` (debug mode).

---

By applying these changes, the `maven-checkstyle-plugin` should correctly locate `checks.xml` and support the `SuppressWithNearbyTextFilter`, resolving your errors.

---

The error you encountered previously indicated that the `maven-checkstyle-plugin` could not find `checks.xml` in the classpath and then failed due to an issue with the `SuppressWithNearbyTextFilter` module. From your updated project structure, it appears that `checks.xml` is located at the project root (`~/Projects/blog-server/checks.xml`), not in `src/main/resources` as previously assumed. This explains why the plugin couldn’t find it when configured with `<configLocation>classpath:checks.xml</configLocation>` or `<configLocation>checks.xml</configLocation>`, as those settings expect the file in the classpath (typically `src/main/resources`).

To fix this and ensure the `maven-checkstyle-plugin` runs with `mvn compile` using your custom `checks.xml` at the project root, you need to update the `<configLocation>` to point to the file’s absolute or project-relative path. Additionally, you need to address the `SuppressWithNearbyTextFilter` issue by ensuring compatibility with the Checkstyle version. Below is the step-by-step solution.

### Updated `pom.xml` Configuration

Modify the `maven-checkstyle-plugin` in your `pom.xml` to reference `checks.xml` at the project root and use a compatible Checkstyle version to support `SuppressWithNearbyTextFilter`.

```xml
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <includes>
                <include>**/*.xml</include>
                <include>**/*.yaml</include>
            </includes>
        </resource>
    </resources>
    <plugins>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <version>3.4.2</version>
            <executions>
                <execution>
                    <goals>
                        <goal>repackage</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.0.0-M8</version>
        </plugin>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.3.1</version> <!-- Latest version for better compatibility -->
            <configuration>
                <configLocation>${project.basedir}/checks.xml</configLocation> <!-- Point to checks.xml at project root -->
            </configuration>
            <dependencies>
                <dependency>
                    <groupId>com.puppycrawl.tools</groupId>
                    <artifactId>checkstyle</artifactId>
                    <version>10.17.0</version> <!-- Supports SuppressWithNearbyTextFilter -->
                </dependency>
            </dependencies>
            <executions>
                <execution>
                    <id>checkstyle-check</id>
                    <phase>compile</phase>
                    <goals>
                        <goal>check</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### Explanation of Changes

1. **Updated `<configLocation>`**:
   - Changed to `${project.basedir}/checks.xml` to point to `checks.xml` at the project root (`~/Projects/blog-server/checks.xml`).
   - `${project.basedir}` resolves to the directory containing `pom.xml`, ensuring the plugin finds the file regardless of classpath.

2. **Upgraded Plugin Version**:
   - Updated `maven-checkstyle-plugin` to `3.3.1` (latest as of June 2025) for better compatibility and bug fixes.

3. **Added Checkstyle Dependency**:
   - Added `<dependency>` for Checkstyle `10.17.0`, which includes support for `SuppressWithNearbyTextFilter`. The default Checkstyle version in `maven-checkstyle-plugin:3.1.1` (`8.29`) does not support this filter, causing the previous error.

4. **Kept `<phase>compile</phase>`**:
   - Ensures `checkstyle:check` runs during `mvn compile`, as requested.

5. **Resources Section**:
   - Retained the `<resources>` section to ensure `src/main/resources` files (like `application.yaml`) are processed, though it’s not directly related to `checks.xml` since it’s now at the project root.

### Verify `checks.xml` Content

The error about `SuppressWithNearbyTextFilter` suggests your `checks.xml` references this filter. Ensure it’s correctly configured. A valid example:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE module PUBLIC
    "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">
<module name="Checker">
    <module name="SuppressWithNearbyTextFilter">
        <!-- Example properties, adjust as needed -->
        <property name="nearbyTextPattern" value="@SuppressWarnings"/>
    </module>
    <module name="TreeWalker">
        <!-- Other checks -->
        <module name="ConstantName"/>
    </module>
</module>
```

- **Check**: Open `checks.xml` at `~/Projects/blog-server/checks.xml` and verify that `SuppressWithNearbyTextFilter` is correctly spelled and includes any required properties (see [Checkstyle documentation](https://checkstyle.org/filters/suppresswithnearbytextfilter.html)).
- **Action**: If unsure, temporarily remove the `<module name="SuppressWithNearbyTextFilter"/>` section and test to isolate the issue.

### Test the Configuration

1. **Clean the Project**:

   ```bash
   mvn clean
   ```

   This removes the `target` directory, including `checkstyle-checker.xml` and `checkstyle-result.xml`, ensuring no stale artifacts interfere.

2. **Run Checkstyle**:

   ```bash
   mvn checkstyle:check
   ```

   This tests the Checkstyle configuration independently.

3. **Run Compile**:

   ```bash
   mvn compile
   ```

   This should run Checkstyle (due to the `compile` phase binding) and then compile if no violations fail the build.

### Debug if Issues Persist

If you encounter errors:

1. **Check File Path**:
   - Confirm `checks.xml` exists at `~/Projects/blog-server/checks.xml`.
   - Verify the file name is exactly `checks.xml` (case-sensitive, no hidden extensions).

2. **Run with Debug Logging**:

   ```bash
   mvn clean checkstyle:check -X
   ```

   Look for messages about `checks.xml` loading or `SuppressWithNearbyTextFilter` initialization. Share relevant output if the error persists.

3. **Test with a Minimal `checks.xml`**:
   Temporarily replace `checks.xml` with a minimal configuration to rule out issues with the file’s content:

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE module PUBLIC
       "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
       "https://checkstyle.org/dtds/configuration_1_3.dtd">
   <module name="Checker">
       <module name="TreeWalker">
           <module name="ConstantName"/>
       </module>
   </module>
   ```

   Then run `mvn checkstyle:check`. If this works, the issue is with `SuppressWithNearbyTextFilter` or other modules in your original `checks.xml`.

### Additional Notes

- **Settings.xml Warning**: Your output shows a warning about an unrecognized `<blocked>` tag in `/usr/share/maven/conf/settings.xml`. This isn’t related to the Checkstyle issue but indicates a potential problem with your Maven configuration. Check line 164 of `/usr/share/maven/conf/settings.xml` and remove or correct the `<blocked>` tag, as it’s not a standard Maven settings element.
- **Alternative File Location**: If you prefer, you can move `checks.xml` to `src/main/resources/checks.xml` and revert `<configLocation>` to `classpath:checks.xml`. This is more conventional for Maven projects, as resources are automatically included in the classpath.
- **Fail on Violation**: If Checkstyle violations are failing the build and you want to allow compilation to proceed, add `<failOnViolation>false</failOnViolation>` to the plugin’s `<configuration>`:

  ```xml
  <configuration>
      <configLocation>${project.basedir}/checks.xml</configLocation>
      <failOnViolation>false</failOnViolation>
  </configuration>
  ```

### Verification

After applying the changes:

1. Run `mvn clean compile` and confirm that:
   - Checkstyle runs using `checks.xml` from the project root.
   - No errors occur related to `checks.xml` or `SuppressWithNearbyTextFilter`.
   - Compilation proceeds if Checkstyle passes or is configured not to fail the build.
2. Check the `target/checkstyle-result.xml` for Checkstyle results.

If the error persists, please share:

- The content (or relevant snippet) of `checks.xml`.
- The debug output from `mvn clean checkstyle:check -X`.
- Any specific Checkstyle rules you’re trying to enforce with `SuppressWithNearbyTextFilter`.

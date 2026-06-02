---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: Exclude com.ibm Packages in JaCoCo
translated: false
type: note
---

To exclude **`com.ibm`** packages (or any other packages) from JaCoCo coverage in a **WebSphere Liberty Profile** environment, you can configure the exclusions in your **`pom.xml`** file. This is typically done in the **JaCoCo Maven plugin** configuration.

---

### **How to Exclude `com.ibm` Packages in `pom.xml`**

You can use the `<excludes>` tag in the JaCoCo plugin configuration to specify which classes or packages should be excluded from coverage reporting.

#### **Example Configuration:**

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.11</version> <!-- Use the latest version -->
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                    <configuration>
                        <outputDirectory>${project.reporting.outputDirectory}/jacoco</outputDirectory>
                        <excludes>
                            <!-- Exclude all com.ibm packages -->
                            <exclude>com/ibm/**</exclude>
                        </excludes>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

---

### **Explanation:**

- **`<excludes>`**: This section specifies which classes or packages should be excluded from coverage reporting.
- **`<exclude>com/ibm/**</exclude>`**: This excludes all classes under the `com.ibm` package and its subpackages.

---

### **Additional Notes:**

- If you want to exclude multiple packages, add more `<exclude>` entries:

  ```xml
  <excludes>
      <exclude>com/ibm/**</exclude>
      <exclude>org/apache/**</exclude>
  </excludes>
  ```

- If you are using **JaCoCo with WebSphere Liberty**, ensure that the JaCoCo agent is properly configured in your `server.env` or `jvm.options` file, and that the exclusions in the `pom.xml` align with your requirements.

---

### **Best Practice:**

- Always verify the exclusions by running a coverage report and checking if the excluded packages are not included in the results.
- If you need to exclude packages at runtime (e.g., in the JaCoCo agent arguments), you can use the `excludes` parameter in the agent arguments:

  ```plaintext
  -javaagent:/path/to/jacocoagent.jar=destfile=/path/to/jacoco.exec,excludes=com.ibm.*
  ```

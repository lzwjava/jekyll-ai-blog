---
audio: false
generated: true
image: false
lang: en
layout: post
title: JaCoCo Multi-Module Spring Coverage Setup
translated: false
type: note
---

Great—JaCoCo works well for a multi-module Spring project. You’ll want:

1. per-module unit-test coverage;
2. an aggregate report at the parent;
3. an optional profile to ingest **integration** coverage (e.g., Liberty+EAR run hit by Python tests).

Below is a battle-tested setup you can drop in.

---

### Parent `pom.xml` (packaging `pom`)

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>com.myco.chat</groupId>
  <artifactId>chat-parent</artifactId>
  <version>1.0.0</version>
  <packaging>pom</packaging>

  <modules>
    <module>ChatCommon</module>
    <module>ChatLib</module>
    <module>ChatCore</module>
    <module>ChatWeb</module>
  </modules>

  <build>
    <pluginManagement>
      <plugins>
        <plugin>
          <groupId>org.jacoco</groupId>
          <artifactId>jacoco-maven-plugin</artifactId>
          <version>0.8.12</version>
        </plugin>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-surefire-plugin</artifactId>
          <version>3.2.5</version>
        </plugin>
        <plugin>
          <groupId>org.apache.maven.plugins</groupId>
          <artifactId>maven-failsafe-plugin</artifactId>
          <version>3.2.5</version>
        </plugin>
      </plugins>
    </pluginManagement>
  </build>

  <!-- Aggregate report for ALL modules' unit tests -->
  <reporting>
    <plugins>
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.12</version>
        <reportSets>
          <reportSet>
            <reports>
              <!-- This triggers 'report-aggregate' when you run 'mvn verify' at the parent -->
              <report>report-aggregate</report>
            </reports>
            <configuration>
              <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate</outputDirectory>
              <reports>
                <xml>true</xml>
                <html>true</html>
                <csv>false</csv>
              </reports>
              <!-- Optional global filters -->
              <excludes>
                <exclude>**/*Application.class</exclude>
                <exclude>**/*Configuration.class</exclude>
                <exclude>**/generated/**</exclude>
              </excludes>
            </configuration>
          </reportSet>
        </plugins>
      </plugin>
    </plugins>
  </reporting>

  <!-- Profile to add INTEGRATION coverage (e.g., Liberty + Python tests) -->
  <profiles>
    <profile>
      <id>it-coverage</id>
      <activation><activeByDefault>false</activeByDefault></activation>
      <build>
        <plugins>
          <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.12</version>
            <executions>
              <!-- Create an aggregate report that also reads external .exec files -->
              <execution>
                <id>report-aggregate-it</id>
                <phase>verify</phase>
                <goals><goal>report-aggregate</goal></goals>
                <configuration>
                  <!-- Point to one or more .exec files dumped by the Liberty JVM agent -->
                  <dataFiles>
                    <!-- Example paths; adjust for your CI/Liberty location -->
                    <dataFile>${project.basedir}/.jacoco/jacoco-it.exec</dataFile>
                    <!-- You can add more dataFile entries if you dump per-node and want all -->
                  </dataFiles>
                  <outputDirectory>${project.reporting.outputDirectory}/jacoco-aggregate-it</outputDirectory>
                  <reports>
                    <xml>true</xml>
                    <html>true</html>
                    <csv>false</csv>
                  </reports>
                  <excludes>
                    <exclude>**/generated/**</exclude>
                  </excludes>
                </configuration>
              </execution>
            </executions>
          </plugin>
        </plugins>
      </build>
    </profile>
  </profiles>
</project>
```

---

### Each child module (`ChatCommon/pom.xml`, `ChatLib/pom.xml`, `ChatCore/pom.xml`, `ChatWeb/pom.xml`)

```xml
<project>
  <parent>
    <groupId>com.myco.chat</groupId>
    <artifactId>chat-parent</artifactId>
    <version>1.0.0</version>
  </parent>
  <modelVersion>4.0.0</modelVersion>
  <artifactId>ChatCommon</artifactId>
  <packaging>jar</packaging>

  <build>
    <plugins>
      <!-- Attach agent for UNIT tests in this module -->
      <plugin>
        <groupId>org.jacoco</groupId>
        <artifactId>jacoco-maven-plugin</artifactId>
        <version>0.8.12</version>
        <executions>
          <execution>
            <id>prepare-agent</id>
            <goals><goal>prepare-agent</goal></goals>
            <configuration>
              <!-- Put the argLine into a named property, so we can mix with other args -->
              <propertyName>jacocoArgLine</propertyName>
              <append>true</append>
              <excludes>
                <exclude>**/generated/**</exclude>
              </excludes>
            </configuration>
          </execution>
          <execution>
            <id>report</id>
            <phase>verify</phase>
            <goals><goal>report</goal></goals>
            <configuration>
              <reports>
                <xml>true</xml>
                <html>true</html>
                <csv>false</csv>
              </reports>
            </configuration>
          </execution>
          <!-- Optional: enforce minimums -->
          <execution>
            <id>check</id>
            <goals><goal>check</goal></goals>
            <configuration>
              <rules>
                <rule>
                  <element>PACKAGE</element>
                  <limits>
                    <limit>
                      <counter>LINE</counter>
                      <value>COVEREDRATIO</value>
                      <minimum>0.60</minimum>
                    </limit>
                    <limit>
                      <counter>BRANCH</counter>
                      <value>COVEREDRATIO</value>
                      <minimum>0.40</minimum>
                    </limit>
                  </limits>
                </rule>
              </rules>
            </configuration>
          </execution>
        </executions>
      </plugin>

      <!-- Ensure Surefire picks up the agent -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-surefire-plugin</artifactId>
        <configuration>
          <argLine>${jacocoArgLine} ${surefireArgLine}</argLine>
        </configuration>
      </plugin>

      <!-- (Optional) Failsafe for module-level ITs -->
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-failsafe-plugin</artifactId>
        <configuration>
          <argLine>${jacocoArgLine} ${failsafeArgLine}</argLine>
        </configuration>
      </plugin>
    </plugins>
  </build>
</project>
```

> Do the same in `ChatLib`, `ChatCore`, and `ChatWeb`.
> For `ChatWeb` (a Spring Boot WAR/JAR), the config is identical.

---

### Running it

**Unit test coverage across modules (aggregate XML at parent):**

```bash
mvn -q clean verify
# XML:  target/site/jacoco-aggregate/jacoco.xml
# HTML: target/site/jacoco-aggregate/index.html
```

**Integration coverage from Liberty + Python tests:**

1. Start Liberty with the JaCoCo agent (as discussed earlier), run Python tests, stop or dump.
   Ensure the `.exec` lands at `${project.basedir}/.jacoco/jacoco-it.exec` (or update that path in the parent profile).
2. Build aggregate including IT data:

```bash
mvn -q -Pit-coverage verify
# XML:  target/site/jacoco-aggregate-it/jacoco.xml
# HTML: target/site/jacoco-aggregate-it/index.html
```

---

### Notes that save time

* **Aggregation works only from the parent** (packaging `pom`) with modules declared. Run `mvn` from the parent directory.
* **XML** (`jacoco.xml`) is produced when you enable it in `<reports>`; this is what Codecov/Sonar use.
* If you collect multiple `.exec` files (e.g., several Liberty nodes), either:

  * list them all under `<dataFiles>…</dataFiles>` in the `it-coverage` profile, or
  * merge first (with `jacococli.jar merge …`) then point to the merged file.
* Don’t point classfiles at the EAR; JaCoCo’s report needs the **modules’ compiled classes** (`*/target/classes`) and sources—handled automatically by `report-aggregate`.
* If Surefire also sets its own `argLine`, keep `${jacocoArgLine}` first so the agent is not lost.

If you share your exact module package roots and where your Liberty `.exec` ends up, I can tailor the `<dataFiles>` and any exclusions so your aggregate XML is clean and CI-ready.

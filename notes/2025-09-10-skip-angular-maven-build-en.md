---
audio: false
date: 2025-09-10
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Skipping Angular Build in Maven
translated: false
type: note
---

Short answer: yes—you can skip the Angular/npm build, but not with a built-in flag like `--skip-web`. Use one of these approaches.

### 1) Exclude the web module in a multi-module build

If your Angular app is its own Maven module (e.g., `web`), just exclude it in the reactor:

```
mvn -pl '!web' -am clean package
```

Or build only the backend module:

```
mvn -pl :backend -am clean package
```

(`-am` builds any needed deps; the `!web` syntax excludes that module.)

### 2) Add a “skip frontend” property (works with frontend-maven-plugin or exec)

Guard the npm goals with a property and flip it from the command line.

**POM (web module or parent):**

```xml
<properties>
  <skip.frontend>false</skip.frontend>
</properties>

<build>
  <plugins>
    <!-- Example: com.github.eirslett:frontend-maven-plugin -->
    <plugin>
      <groupId>com.github.eirslett</groupId>
      <artifactId>frontend-maven-plugin</artifactId>
      <version>...your version...</version>
      <configuration>
        <skip>${skip.frontend}</skip>
      </configuration>
      <executions>
        <execution>
          <id>npm-build</id>
          <phase>prepare-package</phase>
          <goals>
            <goal>npm</goal>
          </goals>
          <configuration>
            <arguments>run build</arguments>
          </configuration>
        </execution>
      </executions>
    </plugin>

    <!-- If you use exec-maven-plugin to call npm -->
    <plugin>
      <groupId>org.codehaus.mojo</groupId>
      <artifactId>exec-maven-plugin</artifactId>
      <version>...your version...</version>
      <executions>
        <execution>
          <id>npm-build</id>
          <phase>prepare-package</phase>
          <goals><goal>exec</goal></goals>
          <configuration>
            <skip>${skip.frontend}</skip>
            <executable>npm</executable>
            <arguments>
              <argument>run</argument>
              <argument>build</argument>
            </arguments>
          </configuration>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

**CLI:**

```
mvn -Dskip.frontend=true clean package
```

### 3) Use Maven profiles

Bind the frontend build only in a “with-frontend” profile and make a “skip-frontend” profile the default in dev.

**POM:**

```xml
<profiles>
  <profile>
    <id>with-frontend</id>
    <activation>
      <property>
        <name>!skip.frontend</name>
      </property>
    </activation>
    <build>
      <plugins>
        <!-- same plugin config as above, without skip -->
      </plugins>
    </build>
  </profile>
</profiles>
```

**CLI:**

* Normal (skip): `mvn -Dskip.frontend clean package`
* Release (build UI): `mvn -Pwith-frontend clean package`

---

## Speed tips if you *do* build the UI

* Make sure Angular’s persistent cache is on (Angular CLI caches by default; keep `node_modules` and `.angular/cache` cached in CI).
* Only run `ng build` for release; in dev, serve the UI separately (`npm start`) and have Spring serve prebuilt static assets (e.g., put `dist/` under `src/main/resources/static` for packaged builds).
* Consider splitting the repo so the Angular app isn’t a Maven module at all; build it only when frontend files change.
* If you’re on a recent Angular, use the default esbuild/Vite builder and keep source maps disabled in CI release builds.

---

### Bottom line

Use `-pl '!web'` to exclude the web module, **or** add a `skip.frontend` property and wire your plugin executions to respect it. There’s no standard `mvn package --skip-web`, but the two patterns above are reliable and common.

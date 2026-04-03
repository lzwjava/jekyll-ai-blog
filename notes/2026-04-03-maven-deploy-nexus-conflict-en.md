---
audio: false
generated: true
image: false
lang: en
layout: post
title: Maven Deploy Plugin Conflict with Nexus
translated: false
type: note
---

Question:
What happens if Maven has both a custom deploy plugin and the default deploy plugin enabled, causing deployment to Nexus to run twice and return HTTP 400 errors?

Answer:

Yes — this is a **common Maven deployment issue**.
If both **your custom deploy plugin** and the **default Maven deploy plugin** run during the `deploy` phase, Maven will try to upload the **same artifact twice** to Nexus.

This usually results in:

* First deploy → succeeds ✅
* Second deploy → fails ❌ (HTTP 400 / artifact already exists / cannot overwrite)

Most Nexus repositories **do not allow redeploy** for release versions, so the second upload is rejected.

---

## Why this happens

Maven lifecycle already binds this plugin automatically:

```
deploy phase
 └── maven-deploy-plugin (default)
```

If you also added something like:

```xml
<plugin>
  <groupId>com.company</groupId>
  <artifactId>custom-deploy-plugin</artifactId>
  <executions>
    <execution>
      <phase>deploy</phase>
      <goals>
        <goal>deploy</goal>
      </goals>
    </execution>
  </executions>
</plugin>
```

Then both will run:

```
deploy phase
 ├── custom deploy plugin
 └── maven-deploy-plugin (default)
```

So Nexus receives:

```
PUT artifact.jar  (OK)
PUT artifact.jar  (400 Bad Request)
```

---

## How to fix (3 correct solutions)

### Solution 1 — Disable default deploy plugin (most common)

```xml
<plugin>
  <artifactId>maven-deploy-plugin</artifactId>
  <version>3.1.1</version>
  <configuration>
    <skip>true</skip>
  </configuration>
</plugin>
```

This keeps only your custom deploy.

---

### Solution 2 — Change custom plugin phase

Run custom plugin **before deploy**, e.g.:

```xml
<phase>package</phase>
```

So order becomes:

```
package → custom plugin
deploy  → default deploy plugin
```

No duplicate uploads.

---

### Solution 3 — Disable deploy entirely (CI controlled)

If CI handles deployment:

```
mvn deploy -DskipDeploy
```

or

```xml
<properties>
  <maven.deploy.skip>true</maven.deploy.skip>
</properties>
```

---

## How to confirm this is your issue

Run:

```
mvn -X deploy
```

Look for **two deploy executions**:

```
--- custom-deploy-plugin:deploy ---
Uploading to nexus...

--- maven-deploy-plugin:deploy ---
Uploading to nexus...
```

If you see two uploads → that's the problem.

---

## Typical Nexus error you will see

```
400 Bad Request
Repository does not allow updating assets
Artifact already exists
```

or

```
Return code is: 400, ReasonPhrase: Bad Request.
```

---

## Best Practice

If you have **custom deploy logic**, always:

* disable default deploy plugin
  OR
* bind custom plugin to earlier phase

Never let both run in `deploy`.

---

This is a **very common enterprise Maven + Nexus pitfall**, especially when:

* company adds internal deploy plugin
* parent POM already has default deploy
* child POM adds another one
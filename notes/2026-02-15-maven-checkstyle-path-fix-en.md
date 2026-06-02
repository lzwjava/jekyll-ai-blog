---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fix Maven Checkstyle File Path Error
translated: false
type: note
---

**Question:** Why is my Google Cloud Build failing during the Maven checkstyle phase with the error "Unable to find configuration file at location: /app/checks.xml: Could not find resource '/app/checks.xml'"?

**Answer:**

The build is failing because the `maven-checkstyle-plugin` (version 3.6.0) is configured to use a Checkstyle configuration file located at `/app/checks.xml`, but this file does not exist inside the Docker container at build time.

This is a very common issue in containerized Maven builds (especially on Google Cloud Build, Cloud Run source-based builds, or similar CI environments).

### Most likely causes

1. **The checks.xml file is missing in your repository**
   You probably have something like this in your `pom.xml`:

   ```xml
   <plugin>
       <groupId>org.apache.maven.plugins</groupId>
       <artifactId>maven-checkstyle-plugin</artifactId>
       <version>3.6.0</version>
       <configuration>
           <configLocation>/app/checks.xml</configLocation>
           <!-- or <configLocation>checks.xml</configLocation> -->
       </configuration>
       <executions>
           <execution>
               <id>checkstyle-check</id>
               <phase>verify</phase>
               <goals>
                   <goal>check</goal>
               </goals>
           </execution>
       </executions>
   </plugin>
   ```

   But the file `checks.xml` (or whatever name you use) is **not present** at the root of your project (or wherever the path expects it).

2. **The path is absolute (/app/checks.xml) instead of relative**
   `/app/checks.xml` is an absolute path inside the container.
   Unless your Dockerfile explicitly copies a file to exactly `/app/checks.xml`, Maven will never find it.
   Cloud Build usually checks out your repo into `/workspace`, not `/app`.

3. **The file is in .gitignore or not committed**
   If `checks.xml` exists only on your local machine but is ignored or not pushed, it won't be available in Cloud Build.

### Recommended fixes (choose one)

#### Fix 1: Use a relative path (most common and cleanest)

Change the configuration in `pom.xml` to a **relative path**:

```xml
<configLocation>checks.xml</configLocation>
<!-- or if it's in a subfolder -->
<configLocation>config/checkstyle/checks.xml</configLocation>
```

Then make sure the file exists at that location in your git repository (commit and push it).

#### Fix 2: Keep the current path but copy the file in Dockerfile

If you really need/want `/app/checks.xml`, add this to your Dockerfile **before** the `mvn package` step:

```dockerfile
COPY checks.xml /app/checks.xml
```

(assuming `checks.xml` is at the root of your repo)

#### Fix 3: Skip checkstyle temporarily (for debugging / unblocking)

Add this flag to your Maven command in `cloudbuild.yaml` or Dockerfile:

```yaml
- name: 'gcr.io/cloud-builders/mvn'
  args: ['-B', '--no-transfer-progress', 'package', '-Dcheckstyle.skip=true']
```

or in Dockerfile:

```dockerfile
RUN mvn -B --no-transfer-progress package -Dcheckstyle.skip=true
```

#### Fix 4: Use a standard published ruleset instead of custom file

Replace your config with a well-known ruleset (no local file needed):

```xml
<configLocation>google_checks.xml</configLocation>
<!-- or sun_checks.xml, or include it via dependency -->
```

Many teams use Google's style:

```xml
<dependency>
    <groupId>com.puppycrawl.tools</groupId>
    <artifactId>checkstyle</artifactId>
    <version>10.18.0</version> <!-- match your plugin version range -->
</dependency>
...
<configLocation>google_checks.xml</configLocation>
```

### Quick diagnostic steps

1. Add this before the `mvn` command in your Dockerfile or cloudbuild.yaml:

   ```bash
   ls -la /workspace || ls -la .
   find / -name checks.xml 2>/dev/null || true
   ```

2. Re-run the build and look at the log — this shows whether the file is present at all.

Once the file is available at the location the plugin expects, the "Could not find resource" error will disappear and the build should proceed (unless there are actual style violations).

**References:**

- [https://maven.apache.org/plugins/maven-checkstyle-plugin/examples/custom-checker.html](https://maven.apache.org/plugins/maven-checkstyle-plugin/examples/custom-checker.html)
- [https://cloud.google.com/build/docs/optimize-builds/speed-up-builds#use_m2_cache](https://cloud.google.com/build/docs/optimize-builds/speed-up-builds#use_m2_cache) (related Maven on Cloud Build tips)
- [https://github.com/checkstyle/checkstyle/issues?q=is%3Aissue+configLocation+not+found](https://github.com/checkstyle/checkstyle/issues?q=is%3Aissue+configLocation+not+found) (similar issues reported)

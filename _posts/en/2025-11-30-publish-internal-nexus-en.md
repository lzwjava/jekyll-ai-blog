---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Publishing to Internal Nexus Repository
translated: false
type: note
---

Here are the most common and reliable ways to publish a package to an **internal Nexus Repository Manager** (Sonatype Nexus 3 is the current version), depending on the package format.

### 1. Using Maven (most common for JVM languages)

#### Option A: maven-deploy-plugin (command line)

```bash
mvn deploy -DaltDeploymentRepository=internal-nexus::default::https://your-nexus.company.com/repository/maven-releases/
```

Or for snapshots:

```bash
mvn deploy -DaltDeploymentRepository=internal-nexus::default::https://your-nexus.company.com/repository/maven-snapshots/
```

#### Option B: Configure in pom.xml (recommended for projects)

```xml
<distributionManagement>
    <repository>
        <id>internal-nexus</id>
        <name>Internal Releases</name>
        <url>https://your-nexus.company.com/repository/maven-releases/</url>
    </repository>
    <snapshotRepository>
        <id>internal-nexus</id>
        <name>Internal Snapshots</name>
        <url>https://your-nexus.company.com/repository/maven-snapshots/</url>
    </snapshotRepository>
</distributionManagement>
```

Then just run:

```bash
mvn deploy
```

Make sure you have credentials in `~/.m2/settings.xml`:

```xml
<servers>
  <server>
    <id>internal-nexus</id>
    <username>your-username</username>
    <password>your-password-or-token</password>
  </server>
</servers>
```

### 2. Using Gradle

In `build.gradle` (Groovy) or `build.gradle.kts` (Kotlin):

```groovy
publishing {
    repositories {
        maven {
            name = "InternalNexus"
            url = version.endsWith('SNAPSHOT')
                ? "https://your-nexus.company.com/repository/maven-snapshots/"
                : "https://your-nexus.company.com/repository/maven-releases/"
            credentials {
                username = "your-username"
                password = "your-password-or-token"
            }
        }
    }
}
```

Then:

```bash
gradle publish
```

### 3. npm packages

```bash
# Set registry once
npm config set registry https://your-nexus.company.com/repository/npm-internal/

# Login (uses Nexus credentials or token)
npm login

# Publish
npm publish
```

### 4. PyPI (Python) packages

```bash
# Create or update ~/.pypirc
[distutils]
index-servers = internal-nexus

[internal-nexus]
repository = https://your-nexus.orgcompany.com/repository/pypi-internal/
username = your-username
password = your-password-or-token

# Then build and upload
python -m build
twine upload --repository internal-nexus dist/*
```

### 5. NuGet (.NET)

```bash
nuget sources add -Name "InternalNexus" -Source https://your-nexus.company.com/repository/nuget-hosted/ -UserName your-user -Password your-token
nuget push YourPackage.1.0.0.nupkg -Source InternalNexus
```

### 6. Raw / Generic repositories (any file)

Use curl to upload via Nexus REST API:

```bash
curl -v -u username:password \
     -H "Content-Type: application/octet-stream" \
     --data-binary @your-artifact-1.0.0.zip \
     "https://your-nexus.company.com/repository/raw-hosted/path/to/your-artifact-1.0.0.zip"
```

For raw hosted repositories with directory structure:

```bash
curl -v -u user:pass \
     --upload-file myfile.tar.gz \
     "https://your-nexus.company.com/repository/raw-hosted/some/folder/myfile.tar.gz"
```

### 7. Docker images

```bash
docker login your-nexus.company.com
docker tag myimage:latest your-nexus.company.com/myimage:latest
docker push your-nexus.company.com/myimage:latest
```

### Recommendation

- For Maven/Gradle/Java projects → configure `distributionManagement` / `publishing` block (cleanest CI/CD integration)
- For everything else → use the native tool (npm, twine, nuget, docker, etc.) pointing to your internal Nexus
- Only fall back to raw curl API when no native tool exists

Most companies also use CI/CD pipelines (Jenkins, GitLab CI, GitHub Actions, etc.) that just run `mvn deploy` or `gradle publish` after configuring credentials as secrets.

Let me know which package type you're using (Maven, npm, PyPI, Docker, etc.), and I can give you the exact working commands/config for your case!

---
audio: false
generated: true
lang: en
layout: post
title: Maven Release Plugin
translated: false
type: note
---

Here's a comprehensive guide on how to use the **Maven Release Plugin** to manage and automate the release process for your Maven project.

---

### What is the Maven Release Plugin?

The **Maven Release Plugin** is a tool that automates the process of releasing a Maven project. It handles tasks such as:

- Updating version numbers in your project's POM file(s).
- Committing changes to your version control system (VCS), such as Git.
- Creating a tag for the release in the VCS.
- Building and deploying the release artifacts.
- Preparing the project for the next development cycle by updating the version numbers again.

The two primary goals of the plugin are:

- **`release:prepare`**: Prepares the project for a release by updating versions, committing changes, and tagging the release in the VCS.
- **`release:perform`**: Builds and deploys the released version using the tagged code from the VCS.

---

### Step-by-Step Guide to Using the Maven Release Plugin

#### 1. Add the Maven Release Plugin to Your POM File

To use the plugin, you need to include it in your project's `pom.xml`. Add it under the `<build><plugins>` section as follows:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-release-plugin</artifactId>
            <version>2.5.3</version> <!-- Use the latest stable version -->
        </plugin>
    </plugins>
</build>
```

**Note**: Check the [official Maven Release Plugin page](https://maven.apache.org/maven-release/maven-release-plugin/) for the latest version and replace `2.5.3` accordingly.

#### 2. Configure the SCM (Source Control Management) Section

The plugin interacts with your VCS (e.g., Git) to commit changes and create tags. You must specify your VCS details in the `<scm>` section of your `pom.xml`. For a Git repository hosted on GitHub, it might look like this:

```xml
<scm>
    <connection>scm:git:git://github.com/username/project.git</connection>
    <developerConnection>scm:git:git@github.com:username/project.git</developerConnection>
    <url>https://github.com/username/project</url>
</scm>
```

- Replace `username` and `project` with your actual GitHub username and repository name.
- Adjust the URLs if you're using a different Git hosting service (e.g., GitLab, Bitbucket).
- Ensure you have the necessary credentials (e.g., SSH keys or a personal access token) configured to push changes to the repository.

#### 3. Prepare Your Project for Release

Before running the release commands, ensure your project is ready:

- All tests pass (`mvn test`).
- There are no uncommitted changes in your working directory (run `git status` to check).
- You're on the correct branch (e.g., `master` or `main`) for the release.

#### 4. Run `release:prepare`

The `release:prepare` goal prepares your project for release. Execute the following command in your terminal:

```bash
mvn release:prepare
```

**What happens during `release:prepare`**:

- **Checks for uncommitted changes**: Ensures your working directory is clean.
- **Prompts for versions**: Asks for the release version and the next development version.
  - Example: If your current version is `1.0-SNAPSHOT`, it might suggest `1.0` for the release and `1.1-SNAPSHOT` for the next development version. You can accept the defaults or enter custom versions (e.g., `1.0.1` for a patch release).
- **Updates POM files**: Changes the version to the release version (e.g., `1.0`), commits the change, and tags it in the VCS (e.g., `project-1.0`).
- **Prepares for next cycle**: Updates the POM to the next development version (e.g., `1.1-SNAPSHOT`) and commits it.

**Optional Dry Run**: To test the process without making changes, use:

```bash
mvn release:prepare -DdryRun=true
```

This simulates the preparation steps without committing or tagging.

#### 5. Run `release:perform`

After preparing the release, build and deploy it with:

```bash
mvn release:perform
```

**What happens during `release:perform`**:

- Checks out the tagged version from the VCS.
- Builds the project.
- Deploys the artifacts to the repository specified in your POM’s `<distributionManagement>` section.

**Configure `<distributionManagement>`** (if deploying to a remote repository):

```xml
<distributionManagement>
    <repository>
        <id>releases</id>
        <url>http://my-repository-manager/releases</url>
    </repository>
    <snapshotRepository>
        <id>snapshots</id>
        <url>http://my-repository-manager/snapshots</url>
    </snapshotRepository>
</distributionManagement>
```

- Replace the URLs with your repository manager’s addresses (e.g., Nexus, Artifactory).
- Ensure credentials are set up in your `~/.m2/settings.xml` file under `<servers>` with matching `id`s.

#### 6. Verify the Release

After `release:perform`, verify the release:

- Check your repository manager to ensure the artifacts (e.g., JARs, sources) are deployed.
- Test the released version in another project by adding it as a dependency in its POM.

---

### Additional Configuration and Tips

#### Handling Failures

- **Cleanup**: If the release process fails, use:

  ```bash
  mvn release:clean
  ```

  to remove temporary files created by the plugin.
- **Rollback**: To undo changes made by `release:prepare`:

  ```bash
  mvn release:rollback
  ```

  Be cautious and verify what changes are reverted.

#### Multi-Module Projects

For multi-module projects, the plugin updates versions across all modules consistently by default. Ensure the parent POM includes the plugin and SCM configuration.

#### Batch Mode for Automation

To run the release non-interactively (e.g., in a CI/CD pipeline), use the `-B` flag and specify versions:

```bash
mvn release:prepare -B -DreleaseVersion=1.0 -DdevelopmentVersion=1.1-SNAPSHOT
mvn release:perform -B
```

#### Common Issues and Solutions

- **VCS Errors**: Ensure Git commands (e.g., `git commit`, `git push`) work manually. Check authentication (SSH keys, tokens).
- **Build Failures**: Verify the build succeeds locally (`mvn clean install`) and dependencies resolve correctly.
- **Version Strategy**: Customize versions during prompts or via properties if the defaults don’t suit your needs.

---

### Summary of Commands

1. **Prepare the release**:

   ```bash
   mvn release:prepare
   ```

2. **Perform the release**:

   ```bash
   mvn release:perform
   ```

3. **Optional dry run**:

   ```bash
   mvn release:prepare -DdryRun=true
   ```

4. **Cleanup or rollback if needed**:

   ```bash
   mvn release:clean
   mvn release:rollback
   ```

---

### Conclusion

The Maven Release Plugin simplifies the release process by automating version management, VCS interactions, and deployment. By adding the plugin to your POM, configuring your SCM, and following the `release:prepare` and `release:perform` steps, you can efficiently release your Maven projects. Always test your configuration with a dry run and verify the results to ensure a smooth release process.

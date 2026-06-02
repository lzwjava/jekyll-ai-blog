---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Maven WAR and EAR Module Setup
translated: false
type: note
---

### Maven Multi-Module Project Setup for WAR to EAR

In Maven, to have one module produce a WAR (e.g., a web application) and another module assemble it into an EAR (Enterprise Archive), use a multi-module project structure. The EAR module depends on the WAR module via the `maven-ear-plugin`. This ensures the WAR is included in the EAR during the build.

#### Step 1: Create the Parent POM

The parent POM defines the modules and manages shared configurations. Set its packaging to `pom`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>parent</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <modules>
        <module>web-module</module>  <!-- Build this first -->
        <module>ear-module</module>
    </modules>

    <!-- Optional: Shared dependencies and plugin versions -->
    <dependencyManagement>
        <dependencies>
            <!-- Define versions for child modules here -->
        </dependencies>
    </dependencyManagement>

    <build>
        <pluginManagement>
            <plugins>
                <!-- Manage plugin versions -->
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-ear-plugin</artifactId>
                    <version>3.3.0</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

#### Step 2: Configure the WAR Module

This module builds the web application as a WAR. Set its packaging to `war`. No special EAR configuration is needed here—it just needs to be built first.

Directory structure: `web-module/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>web-module</artifactId>
    <packaging>war</packaging>

    <dependencies>
        <!-- Add your web dependencies, e.g., servlet-api -->
        <dependency>
            <groupId>javax.servlet</groupId>
            <artifactId>javax.servlet-api</artifactId>
            <version>4.0.1</version>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-war-plugin</artifactId>
                <version>3.3.2</version>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Step 3: Configure the EAR Module

This module assembles the EAR. Set its packaging to `ear` and use the `maven-ear-plugin` to reference the WAR module. The plugin will pull the WAR artifact and bundle it into the EAR.

Directory structure: `ear-module/pom.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent</artifactId>
        <version>1.0-SNAPSHOT</version>
    </parent>

    <artifactId>ear-module</artifactId>
    <packaging>ear</packaging>

    <dependencies>
        <!-- Depend on the WAR module to include it in the build -->
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>web-module</artifactId>
            <version>${project.version}</version>
            <type>war</type>
        </dependency>
        <!-- Optional: Add EJB or other modules if needed -->
    </dependencies>

    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-ear-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <!-- EAR version (e.g., for Java EE) -->
                    <version>8</version>

                    <!-- Directory for libraries in EAR -->
                    <defaultLibBundleDir>lib</defaultLibBundleDir>

                    <!-- Skinny WARs (exclude dependencies already in EAR libs) -->
                    <skinnyWars>true</skinnyWars>

                    <!-- Define modules to include -->
                    <modules>
                        <webModule>
                            <groupId>com.example</groupId>
                            <artifactId>web-module</artifactId>
                            <bundleDir>/</bundleDir>  <!-- Root of EAR -->
                            <contextRoot>/mywebapp</contextRoot>  <!-- Deployment context -->
                        </webModule>
                        <!-- Add more <ejbModule> or <jarModule> if needed -->
                    </modules>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

#### Step 4: Build the Project

- Run from the **parent directory**: `mvn clean install`
  - This builds modules in order (WAR first, then EAR).
- The EAR will be in `ear-module/target/ear-module-1.0-SNAPSHOT.ear`.
- To build only the EAR (assuming WAR is already built): `cd ear-module && mvn clean package`.

#### Key Notes

- **Build Order**: List the WAR module before the EAR in the parent's `<modules>` to ensure Maven builds the WAR first.
- **Dependencies**: The EAR module's `<dependency>` on the WAR ensures it's resolved during packaging.
- **Customization**: Adjust `<contextRoot>` for the web app's URL path. Add more modules (e.g., EJB JARs) in `<modules>`.
- **Troubleshooting**: If the WAR isn't included, check artifact coordinates match exactly. Use `mvn dependency:tree` in the EAR module to verify.

For more details, see the official Maven EAR plugin docs.

[Apache Maven EAR Plugin](https://maven.apache.org/plugins/maven-ear-plugin/)
[Maven Multi-Module Projects](https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html#Multi-module_Projects)

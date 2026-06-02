---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Maven Profiles for WAS Environment Configuration
translated: false
type: note
---

For IBM WebSphere Application Server (traditional WAS, not Liberty), the standard packaging is an **EAR** file (even for simple web apps, as WAS prefers EAR over standalone WAR). The best practice to handle different environments — like local development (fixed/hardcoded login user for testing) vs. server/production (SSO or proper security realm) — is to use **Maven build profiles** in a single `pom.xml`. This avoids maintaining multiple separate POM files (e.g., `pom.xml` and `build_pom.xml`), which is error-prone and not idiomatic Maven.

### Why Profiles Instead of Multiple POMs?
- One source of truth (single POM).
- Easy activation: `mvn package -Plocal` or `mvn package -Pserver`.
- Profiles can filter resources, override files, change plugin config, or adjust bindings (e.g., `ibm-web-bnd.xml`, `ibm-application-ext.xml` for WAS-specific auth).
- Commonly used for dev/test/prod differences, including authentication setups.

### Recommended Structure
Use the Maven Resources Plugin with filtering + profile-specific resource directories to swap configuration files (e.g., `web.xml`, `properties` files, Spring security config, or WAS bindings).

Directory layout example:
```
src/
├── main/
│   ├── resources/          (common configs)
│   ├── webapp/
│   │   ├── WEB-INF/
│   │   │   ├── web.xml      (common or base version)
│   │   │   └── ibm-web-bnd.xml (optional, for JNDI/auth bindings)
│   └── ...
├── local/                   (profile-specific resources, copied/filtered only for local)
│   └── webapp/
│       └── WEB-INF/
│           ├── web.xml      (local version with form-login + hardcoded user/role or no security)
│           └── ...
└── server/                  (profile-specific for production/SSO)
    └── webapp/
        └── WEB-INF/
            ├── web.xml      (server version with <login-config><auth-method>CLIENT-CERT</auth-method> or SPNEGO for SSO)
            └── ...
```

### Example pom.xml Snippet
```xml
<project ...>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>my-was-app</artifactId>
    <version>1.0.0</version>
    <packaging>ear</packaging>   <!-- Or war if you deploy as WAR, but EAR is preferred for WAS -->

    <properties>
        <maven.compiler.source>11</maven.compiler.source> <!-- or your Java version -->
        <maven.compiler.target>11</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Your app deps -->
        <!-- For WAS compile-time APIs (provided scope) -->
        <dependency>
            <groupId>com.ibm.tools.target</groupId>
            <artifactId>was</artifactId>
            <version>9.0</version> <!-- Match your WAS version, e.g., 8.5.5 or 9.0 -->
            <type>pom</type>
            <scope>provided</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Build EAR (adjust for WAR if needed) -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-ear-plugin</artifactId>
                <version>3.3.0</version>
                <configuration>
                    <!-- Your EAR config, modules, etc. -->
                </configuration>
            </plugin>

            <!-- Resource filtering & profile-specific overrides -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-resources-plugin</artifactId>
                <version>3.3.1</version>
                <configuration>
                    <useDefaultDelimiters>true</useDefaultDelimiters>
                </configuration>
            </plugin>
        </plugins>
    </build>

    <!-- Profiles -->
    <profiles>
        <!-- Local/dev profile: fixed user, form login or no security -->
        <profile>
            <id>local</id>
            <activation>
                <activeByDefault>true</activeByDefault> <!-- Default for local builds -->
            </activation>
            <build>
                <resources>
                    <!-- Common resources -->
                    <resource>
                        <directory>src/main/resources</directory>
                        <filtering>true</filtering>
                    </resource>
                    <!-- Override with local-specific files -->
                    <resource>
                        <directory>src/local/webapp</directory>
                        <targetPath>${project.build.directory}/${project.artifactId}/WEB-INF</targetPath>
                    </resource>
                </resources>
            </build>
            <properties>
                <!-- Example filtered properties for local hardcoded user -->
                <app.login.user>devuser</app.login.user>
                <app.login.password>devpass</app.login.password>
            </properties>
        </profile>

        <!-- Server/prod profile: real SSO (e.g., SPNEGO, LTPA, or OpenIDConnect) -->
        <profile>
            <id>server</id>
            <build>
                <resources>
                    <resource>
                        <directory>src/main/resources</directory>
                        <filtering>true</filtering>
                    </resource>
                    <resource>
                        <directory>src/server/webapp</directory>
                        <targetPath>${project.build.directory}/${project.artifactId}/WEB-INF</targetPath>
                    </resource>
                </resources>
            </build>
            <properties>
                <!-- Prod properties, e.g., enable SSO flags -->
                <app.auth.method>SSO</app.auth.method>
            </properties>
        </profile>
    </profiles>
</project>
```

### Key Points for Authentication Differences
- **Local**: Use FORM login with a simple users/roles in `web.xml` or a properties file, or disable security entirely (`<security-constraint>` removed).
- **Server**: Configure WAS-specific SSO in `web.xml` (e.g., `<auth-method>FORM</auth-method>` with SPNEGO, or use OpenID Connect feature in Liberty-style, but for traditional WAS often LTPA + global security realm). WAS bindings (`ibm-web-bnd.xml`) can also be overridden per profile for user/role mappings.
- If using Spring Security or similar, swap `applicationContext-security.xml` or properties the same way.
- For hardcoded local user: Avoid real hardcoded credentials; use a test user mapped in a local `users.properties` or disable auth checks via a flag.

### Build Commands
- Local (default): `mvn clean package`
- Server/Prod: `mvn clean package -Pserver`

This produces different EARs tailored for each environment from the **same codebase**. If you truly need separate artifacts names (e.g., `myapp-local.ear` vs `myapp.ear`), add `<finalName>${project.artifactId}-${profile}</finalName>` in profile-specific `<build>` sections.

[Maven Profiles Guide](https://maven.apache.org/guides/introduction/introduction-to-profiles.html)
[Maven EAR Plugin](https://maven.apache.org/plugins/maven-ear-plugin/)
[IBM WAS Maven Integration](https://www.ibm.com/docs/en/wasdtfe/9.7.0?topic=suye-configuring-dependency-pom-files-that-emulate-classpath-specific-websphere-runtime-environments)

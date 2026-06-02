---
audio: false
generated: true
lang: en
layout: post
title: Upgrade Maven Dependencies and Plugins
translated: false
type: note
---

Here's a list of the versions in your `pom.xml` that can be upgraded, along with their latest available versions as of July 5, 2025:

**Dependencies:**

* `org.junit.jupiter:junit-jupiter-api`
  * Current: `5.9.2`
  * Latest Stable: `5.13.2` (Released June 24, 2025)
  * Latest Preview: `6.0.0-M1` (Released June 27, 2025) - Consider if you want to use a milestone release.
* `org.junit.jupiter:junit-jupiter-engine`
  * Current: `5.9.2`
  * Latest Stable: `5.13.2` (Released June 24, 2025)
  * Latest Preview: `6.0.0-M1` (Released June 27, 2025) - Consider if you want to use a milestone release.

**Plugins:**

* `org.apache.maven.plugins:maven-compiler-plugin`
  * Current: `3.13.0`
  * Latest: `3.14.0` (Released February 17, 2025)
* `org.apache.maven.plugins:maven-jar-plugin`
  * Current: `3.4.2`
  * Latest: `3.4.2` (No newer stable version found. Last published June 16, 2024, but current time is July 5, 2025, so this is still up to date).
* `com.diffplug.spotless:spotless-maven-plugin`
  * Current: `2.44.5`
  * Latest: `2.44.5` (No newer stable version found. Last published May 28, 2025, so this is still up to date).
* `org.apache.maven.plugins:maven-checkstyle-plugin`
  * Current: `3.6.0`
  * Latest: `3.6.0` (No newer stable version found. Last published October 22, 2024, so this is still up to date).
  * **Note:** The `checkstyle` dependency inside the checkstyle plugin configuration can be updated:
    * Current: `10.25.0`
    * Latest: `10.26.1` (Released June 29, 2025)
* `org.apache.maven.plugins:maven-surefire-plugin`
  * Current: `3.0.0-M7`
  * Latest Stable: `3.5.3` (Released March 27, 2025) - This is a significant jump from a milestone release.
* `org.codehaus.mojo:exec-maven-plugin`
  * Current: `3.5.1`
  * Latest: `3.5.1` (No newer stable version found. Last published May 27, 2025, so this is still up to date).

**Summary of Upgrades:**

* **JUnit Jupiter API:** 5.9.2 -> 5.13.2 (or 6.0.0-M1)
* **JUnit Jupiter Engine:** 5.9.2 -> 5.13.2 (or 6.0.0-M1)
* **Maven Compiler Plugin:** 3.13.0 -> 3.14.0
* **Checkstyle (dependency within plugin):** 10.25.0 -> 10.26.1
* **Maven Surefire Plugin:** 3.0.0-M7 -> 3.5.3

**Important Considerations Before Upgrading:**

* **Breaking Changes:** Always check the release notes for each component you plan to upgrade. Major version bumps (like from JUnit 5 to 6, or Surefire 3.0.0-M7 to 3.5.3) might introduce breaking changes that require code modifications.
* **Compatibility:** Ensure that the new versions are compatible with your Java version (JDK 21 in your case) and other dependencies in your project.
* **Testing:** After upgrading, thoroughly test your application to ensure everything still functions as expected.

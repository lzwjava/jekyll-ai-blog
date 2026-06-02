---
audio: false
generated: true
lang: en
layout: post
title: Upgrade Guice to Fix Unsafe Warning
translated: false
type: note
---

The warning you're seeing:

```
WARNING: A terminally deprecated method in sun.misc.Unsafe has been called
WARNING: sun.misc.Unsafe::staticFieldBase has been called by com.google.inject.internal.aop.HiddenClassDefiner (file:/opt/homebrew/Cellar/maven/3.9.10/libexec/lib/guice-5.1.0-classes.jar)
WARNING: Please consider reporting this to the maintainers of class com.google.inject.internal.aop.HiddenClassDefiner
WARNING: sun.misc.Unsafe::staticFieldBase will be removed in a future release
```

This is a **warning from the Java Virtual Machine (JVM)**, not directly from your code. It means that a library you're using (in this case, Guice, specifically the `guice-5.1.0-classes.jar`) is internally calling a method (`staticFieldBase`) from `sun.misc.Unsafe`.

`sun.misc.Unsafe` is an internal API in Java, meant for low-level operations within the JDK itself. It's not part of the standard Java API and its use is discouraged because it can lead to unstable or undefined behavior and it's subject to change or removal in future Java releases. The JVM is giving you a heads-up that this particular method is "terminally deprecated" and will be removed, meaning it will eventually cause your application to break if the library continues to use it without an alternative.

**How to "remove" this warning:**

You can't directly "remove" it by changing your code, as the usage is within a third-party library (Guice). Here's what you can do, listed in order of preference:

1.  **Upgrade Guice (Most Recommended):**
    The best and most sustainable solution is to upgrade to a newer version of Guice that no longer uses `sun.misc.Unsafe` or has migrated to the standard Java APIs like `VarHandle` (introduced in JDK 9) or the Foreign Function & Memory API (JEP 454, standard in JDK 22).

    Looking at the version `guice-5.1.0-classes.jar`, it seems you're using Guice 5.1.0. Check the official Guice releases and their documentation for updates that specifically address `sun.misc.Unsafe` usage on newer Java versions. Often, library maintainers are aware of these deprecations and provide updated versions.

      * **Action:** Modify your `pom.xml` to use a newer Guice version. You'll need to find the latest stable version of Guice that is compatible with your Java version (JDK 21 in your case).

    <!-- end list -->

    ```xml
    <dependency>
        <groupId>com.google.inject</groupId>
        <artifactId>guice</artifactId>
        <version>LATEST_GUICE_VERSION</version> </dependency>
    ```

    You might need to include `guice-assistedinject` or other Guice modules if your project uses them.

2.  **Suppress the Warning (Temporary Workaround - Not Recommended Long-Term):**
    While you shouldn't rely on this long-term, you can suppress the warning at runtime if it's purely cosmetic and doesn't hinder your application's functionality *for now*. This is done via JVM command-line arguments.

    For JDK 24 (your current target is 21, but this is a good to know as Java progresses), the default is `warn`. To suppress it, you can explicitly set it to `allow`:

    You can add this to your `exec-maven-plugin` configuration:

    ```xml
    <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>3.5.0</version>
        <configuration>
            <executable>bash</executable>
            <arguments>
                <argument>-c</argument>
                <argument>java --add-opens java.base/sun.misc=ALL-UNNAMED --sun-misc-unsafe-memory-access=allow -cp ${project.build.directory}/classes com.lzw.solutions.uva.${problem}.Main &lt; src/main/resources/uva/${problem}/1.in</argument>
            </arguments>
        </configuration>
    </plugin>
    ```

    *Self-correction:* The primary warning is about `sun.misc.Unsafe::staticFieldBase` being "terminally deprecated," not about illegal reflective access. So, `--add-opens java.base/sun.misc=ALL-UNNAMED` might not be necessary here unless you were also getting "Illegal reflective access" warnings. The more direct flag for the "terminally deprecated" warning is `--sun-misc-unsafe-memory-access=allow`.

    **However, this is a temporary fix.** This flag simply tells the JVM to allow the use of `sun.misc.Unsafe` methods without printing the warning. It *does not* solve the underlying problem that `sun.misc.Unsafe` will eventually be removed, and your application might break in future JDK versions.

3.  **Report to Guice Maintainers (Already Suggested by the Warning):**
    The warning itself suggests "Please consider reporting this to the maintainers of class `com.google.inject.internal.aop.HiddenClassDefiner`." While you're using a specific version, if you can confirm this issue persists in the latest Guice versions (which it likely shouldn't, as they tend to address these), reporting it would be beneficial for the community.

**In summary, the best course of action is to upgrade your Guice dependency.** The `sun.misc.Unsafe` API is a moving target, and libraries need to adapt to the newer, safer, and officially supported APIs provided by Java.

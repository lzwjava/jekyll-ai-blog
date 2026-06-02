---
audio: false
generated: true
lang: en
layout: post
title: Indentation Detecting in Checkstyle
translated: false
type: note
---

I understand you're wondering why Checkstyle isn't detecting the missing indentation before the `System.out.println` statement in your `logAfter` method. Let's break this down step by step to identify the issue and fix it.

### Why Isn't Checkstyle Detecting the Indentation Issue?
Checkstyle uses specific modules to enforce coding standards, and for indentation, it relies on the `Indentation` module. If this module isn't properly configured or included in your Checkstyle setup, it won't detect indentation errors like the one in your code.

Here’s your current code:

```java
package org.lzwjava;

import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.After;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class DebugAspect {
    @After("execution(* org.lzwjava..*(..))")
    public void logAfter(JoinPoint joinPoint) {
    System.out.println("Method executed: " + joinPoint.getSignature());  // No indentation
    }
}
```

In standard Java conventions, statements inside a method (like `System.out.println`) should be indented relative to the method declaration. In your code, the `System.out.println` line has no indentation, which Checkstyle should flag as an error if properly configured. Here are the most likely reasons it’s not being detected:

1. **The `Indentation` module isn’t included** in your Checkstyle configuration file (e.g., `checks.xml`).
2. **The module is included but misconfigured**, so it doesn’t enforce the expected indentation rules.
3. **Your configuration excludes certain files or packages**, preventing the check from running on this code.
4. **There’s an issue with how Checkstyle is run** (e.g., through Maven or an IDE), overriding the expected behavior.

Let’s address these possibilities and get it working.

---

### Step 1: Verify the `Indentation` Module in Your Configuration
First, check your Checkstyle configuration file (likely `checks.xml`) to see if the `Indentation` module is included. Here’s how:

1. **Locate your `checks.xml` file**. It’s typically in your project directory (e.g., `/home/lzw/Projects/blog-server/checks.xml` if you’re using a setup like that).
2. **Look for the `Indentation` module** inside the `TreeWalker` section. It should look like this:

   ```xml
   <module name="TreeWalker">
       <!-- Other checks -->
       <module name="Indentation">
           <property name="basicOffset" value="4"/>  <!-- 4 spaces per indentation level -->
           <property name="lineWrappingIndentation" value="4"/>  <!-- Optional: for wrapped lines -->
       </module>
       <!-- Other checks -->
   </module>
   ```

   - **If you don’t see this module**, that’s the problem—Checkstyle isn’t checking indentation at all.
   - **If it’s there**, check that `basicOffset` is set to a reasonable value (e.g., 4 spaces, which is standard for Java).

---

### Step 2: Add or Fix the `Indentation` Module
If the module is missing or not set up correctly, here’s how to fix it:

#### If It’s Missing: Add the `Indentation` Module
Add the following inside the `TreeWalker` section of your `checks.xml`:

```xml
<module name="Indentation">
    <property name="basicOffset" value="4"/>  <!-- 4 spaces is typical -->
    <property name="lineWrappingIndentation" value="4"/>
</module>
```

#### If It’s Present: Verify the Settings
Ensure:
- `basicOffset` is set to the number of spaces you expect for indentation (e.g., 4).
- No properties disable or override the check in a way that skips your code.

Save the file after making changes.

---

### Step 3: Check for Exclusions
Sometimes, Checkstyle configurations exclude certain files or packages. In your `checks.xml`, look for:
- A `SuppressionFilter` or `SuppressionCommentFilter` that might skip the `org.lzwjava` package or this specific file.
- Any patterns that exclude `.java` files or specific directories.

If you find such an exclusion affecting your code, remove or adjust it so that `DebugAspect.java` is checked.

---

### Step 4: Test the Fix
After updating your configuration, run Checkstyle again. If you’re using Maven, for example:

```bash
mvn clean checkstyle:check
```

Check the output. You should see an error like:

```
[ERROR] DebugAspect.java:13: 'System.out.println' should be indented +4 spaces relative to its enclosing block.
```

This would indicate that Checkstyle is now detecting the missing indentation. For reference, here’s how your code *should* look with proper indentation:

```java
@Aspect
@Component
public class DebugAspect {
    @After("execution(* org.lzwjava..*(..))")
    public void logAfter(JoinPoint joinPoint) {
        System.out.println("Method executed: " + joinPoint.getSignature());  // 4 spaces indent
    }
}
```

---

### Step 5: Troubleshooting if It Still Doesn’t Work
If Checkstyle still doesn’t flag the issue:
- **Run with Debug Output**: Use a verbose command to see what Checkstyle is doing:
  ```bash
  mvn -X checkstyle:check
  ```
  Look for messages about the `Indentation` module or skipped files.
- **Test with a Minimal Configuration**: Create a temporary `checks.xml` with just the `Indentation` check:
  ```xml
  <?xml version="1.0"?>
  <!DOCTYPE module PUBLIC
      "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
      "https://checkstyle.org/dtds/configuration_1_3.dtd">
  <module name="Checker">
      <module name="TreeWalker">
          <module name="Indentation">
              <property name="basicOffset" value="4"/>
          </module>
      </module>
  </module>
  ```
  Point Checkstyle to this file and test again to isolate the issue.
- **Check Your Setup**: If you’re running Checkstyle through an IDE (like IntelliJ or Eclipse), ensure the IDE is using the updated `checks.xml` and not an old or separate configuration.

---

### Conclusion
Checkstyle isn’t detecting the missing indentation because the `Indentation` module is likely missing or misconfigured in your `checks.xml`. By adding or correcting this module and ensuring no exclusions apply, Checkstyle should flag the lack of indentation before `System.out.println`. Update your configuration as shown, re-run Checkstyle, and you should see the error reported as expected. Let me know if you need help with the next steps!

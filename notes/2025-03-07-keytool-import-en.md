---
audio: false
generated: true
lang: en
layout: post
title: Importing Certificates with Keytool
translated: false
type: note
---

To address your query about using the `keytool -importcert` command to import a certificate into the `jre/lib/security/cacerts` file and encountering a "password verification failed" error with a `java.security.UnrecoverableException`, let’s break this down step-by-step to understand the issue, how to fix it, and what the possible password might be.

### Understanding the Problem

The `keytool` utility is a command-line tool included with the Java Development Kit (JDK) used to manage keystores. A keystore is a file that stores cryptographic keys and certificates, often for securing network communications like SSL/TLS. The `cacerts` file, located in `jre/lib/security`, is a specific keystore that comes with the Java Runtime Environment (JRE). It contains a collection of trusted root certificates from well-known Certificate Authorities (CAs), which Java applications use by default to verify secure connections.

When you run the `keytool -importcert` command to add a new certificate to the `cacerts` file, you need to provide the correct password for the keystore. The error message you’re seeing—"password verification failed" followed by `java.security.UnrecoverableException`—indicates that the password you supplied (or didn’t supply correctly) doesn’t match the keystore’s password. This exception typically arises when the provided password is incorrect, preventing `keytool` from accessing or modifying the keystore.

### The Command in Question

The command you’re likely using looks something like this:

```
keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias
```

- `-file mycert.crt`: Specifies the certificate file you want to import.
- `-keystore /path/to/jre/lib/security/cacerts`: Points to the `cacerts` keystore.
- `-alias myalias`: Assigns a unique name (alias) to the certificate in the keystore.

When you execute this command, `keytool` prompts you to enter the keystore password. If the password you enter is incorrect, you get the error you described.

### Identifying the Possible Password

For the `cacerts` file in a standard JRE installation (such as those from Oracle or OpenJDK), the **default password** is **"changeit"**. This is a well-documented default across Java versions and distributions. The name "changeit" serves as a reminder that administrators might want to change it for security reasons, but in most standard, unmodified installations, it remains unchanged.

Since your command is failing with a password verification error, the most likely issue is that either:

1. You didn’t enter "changeit" correctly (e.g., a typo or incorrect case—passwords are case-sensitive).
2. The password prompt wasn’t handled properly.
3. In your specific environment, the default password has been changed (though this is less common for `cacerts` unless explicitly modified by a system administrator).

Given that your query doesn’t indicate a custom setup, let’s assume a standard JRE installation where "changeit" should apply.

### How to Fix the Issue

Here’s how you can resolve the problem:

1. **Ensure Correct Password Entry at the Prompt**
   Run the command again:

   ```
   keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias
   ```

   When prompted for the password, carefully type **"changeit"** (all lowercase, no spaces) and press Enter. Double-check for typos or keyboard layout issues.

2. **Specify the Password in the Command Line**
   To avoid issues with the interactive prompt (e.g., scripting or terminal misbehavior), you can include the password directly using the `-storepass` option:

   ```
   keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias -storepass changeit
   ```

   This explicitly passes "changeit" as the password, bypassing the prompt. If this works without errors, the issue was likely with how the password was entered previously.

3. **Check Permissions**
   Since `cacerts` resides in the JRE directory (e.g., `/usr/lib/jvm/java-11-openjdk/lib/security/cacerts` on Linux or a similar path on Windows), ensure you have write permissions. Run the command with administrative privileges if needed:
   - On Linux/Mac: `sudo keytool ...`
   - On Windows: Run the command prompt as Administrator.

   However, since your error is about password verification, not file access, this is likely not the core issue—but it’s good to confirm.

4. **Verify the Password**
   If "changeit" still fails, the password might have been changed in your environment. To test the password without modifying the keystore, try listing its contents:

   ```
   keytool -list -keystore /path/to/jre/lib/security/cacerts
   ```

   Enter "changeit" when prompted. If it lists certificates, the password is correct. If you get the same error, the password differs from the default.

### What If "changeit" Isn’t the Password?

If "changeit" doesn’t work, consider these possibilities:

- **Custom Password**: In rare cases, a system administrator might have changed the `cacerts` password. You’d need to consult your system documentation or administrator to obtain it. There’s no way to recover a lost keystore password directly; if it’s truly unknown, you might need to replace the `cacerts` file with a fresh copy from a new JRE installation (which resets it to "changeit").
- **Environment-Specific Defaults**: Some non-standard Java distributions (e.g., IBM JDK) might use a different default, but this is uncommon, and your query suggests a typical setup.

Without additional context, "changeit" remains the most probable password in a standard JRE.

### Final Resolution

To fix your issue:

- Use this command, assuming a standard JRE:

  ```
  keytool -importcert -file mycert.crt -keystore /path/to/jre/lib/security/cacerts -alias myalias -storepass changeit
  ```

- If it fails, verify the password with the `-list` command or check with your system administrator.

The **possible password** in this scenario, based on standard Java conventions, is **"changeit"**. This should resolve the `java.security.UnrecoverableException` if entered correctly and if the `cacerts` file hasn’t been customized.

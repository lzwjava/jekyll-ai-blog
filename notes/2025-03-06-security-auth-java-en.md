---
audio: false
generated: true
lang: en
layout: post
title: Authentication and Authorization in Java
translated: false
type: note
---

To use the `javax.security.auth` package in Java, you need to understand that it is part of the Java Authentication and Authorization Service (JAAS) framework. This package provides classes and interfaces for authenticating users (verifying who they are) and authorizing them (determining what they can do). Below is a step-by-step guide to using `javax.security.auth` for a basic authentication scenario, such as authenticating a user with a username and password.

---

### **Overview of Key Concepts**

Before diving into the steps, here’s a brief explanation of the core components in `javax.security.auth`:

- **Subject**: Represents an entity (e.g., a user or service) being authenticated. It can have multiple identities (Principals) and credentials (e.g., passwords or certificates).
- **Principal**: An identity or role associated with a Subject, such as a username or group membership.
- **Credential**: Information used to authenticate a Subject, such as a password or a cryptographic key.
- **LoginModule**: A pluggable component that performs the authentication logic (e.g., checking a username and password against a database).
- **LoginContext**: The central class that coordinates the authentication process using one or more LoginModules.
- **CallbackHandler**: An interface for interacting with the user, such as prompting for a username and password.

With these concepts in mind, let’s explore how to use the package.

---

### **Steps to Use `javax.security.auth`**

#### **1. Set Up a JAAS Configuration**

The authentication process relies on a configuration that specifies which `LoginModule`(s) to use. This can be defined in a configuration file or programmatically.

For example, create a file named `jaas.config` with the following content:

```
MyApp {
    com.example.MyLoginModule required;
};
```

- **`MyApp`**: The name of the application or context, which you’ll reference in your code.
- **`com.example.MyLoginModule`**: The fully qualified name of your custom `LoginModule` (you’ll implement this later).
- **`required`**: A flag indicating that this module must succeed for authentication to pass. Other flags include `requisite`, `sufficient`, and `optional`, which allow more complex logic with multiple modules.

Set the system property to point to this file:

```java
System.setProperty("java.security.auth.login.config", "jaas.config");
```

Alternatively, you can set the configuration programmatically, but a file is simpler for most cases.

#### **2. Implement a CallbackHandler**

A `CallbackHandler` collects input from the user, such as a username and password. Here’s a simple implementation using the console:

```java
import javax.security.auth.callback.*;
import java.io.*;

public class MyCallbackHandler implements CallbackHandler {
    public void handle(Callback[] callbacks) throws IOException, UnsupportedCallbackException {
        for (Callback callback : callbacks) {
            if (callback instanceof NameCallback) {
                NameCallback nc = (NameCallback) callback;
                System.out.print(nc.getPrompt());
                nc.setName(System.console().readLine());
            } else if (callback instanceof PasswordCallback) {
                PasswordCallback pc = (PasswordCallback) callback;
                System.out.print(pc.getPrompt());
                pc.setPassword(System.console().readPassword());
            } else {
                throw new UnsupportedCallbackException(callback, "Unsupported callback");
            }
        }
    }
}
```

- **NameCallback**: Prompts for and retrieves the username.
- **PasswordCallback**: Prompts for and retrieves the password (stored as a `char[]` for security).

#### **3. Implement a LoginModule**

A `LoginModule` defines the authentication logic. Below is a basic example that checks against a hardcoded username and password (in practice, you’d use a database or external service):

```java
import javax.security.auth.*;
import javax.security.auth.callback.*;
import javax.security.auth.login.*;
import javax.security.auth.spi.*;
import java.security.Principal;
import java.util.*;

public class MyLoginModule implements LoginModule {
    private Subject subject;
    private CallbackHandler callbackHandler;
    private boolean succeeded = false;

    // Initialize the module
    public void initialize(Subject subject, CallbackHandler callbackHandler,
                           Map<String, ?> sharedState, Map<String, ?> options) {
        this.subject = subject;
        this.callbackHandler = callbackHandler;
    }

    // Perform authentication
    public boolean login() throws LoginException {
        if (callbackHandler == null) {
            throw new LoginException("No callback handler provided");
        }

        try {
            NameCallback nameCallback = new NameCallback("Username: ");
            PasswordCallback passwordCallback = new PasswordCallback("Password: ", false);
            callbackHandler.handle(new Callback[]{nameCallback, passwordCallback});

            String username = nameCallback.getName();
            char[] password = passwordCallback.getPassword();

            // Hardcoded check (replace with real logic in practice)
            if ("myuser".equals(username) && "mypassword".equals(new String(password))) {
                succeeded = true;
                return true;
            } else {
                succeeded = false;
                throw new FailedLoginException("Authentication failed");
            }
        } catch (Exception e) {
            throw new LoginException("Login error: " + e.getMessage());
        }
    }

    // Commit the authentication (add Principals to the Subject)
    public boolean commit() throws LoginException {
        if (succeeded) {
            subject.getPrincipals().add(new MyPrincipal("myuser"));
            return true;
        }
        return false;
    }

    // Abort the authentication process
    public boolean abort() throws LoginException {
        succeeded = false;
        return true;
    }

    // Logout the Subject
    public boolean logout() throws LoginException {
        subject.getPrincipals().clear();
        subject.getPublicCredentials().clear();
        subject.getPrivateCredentials().clear();
        return true;
    }
}

// Simple Principal implementation
class MyPrincipal implements Principal {
    private String name;

    public MyPrincipal(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}
```

- **login()**: Uses the `CallbackHandler` to get credentials and checks them.
- **commit()**: If authentication succeeds, adds a `Principal` to the `Subject`.
- **abort()** and **logout()**: Handle cleanup or cancellation.

#### **4. Authenticate Using LoginContext**

Now, use `LoginContext` to perform the authentication in your main application:

```java
import javax.security.auth.login.*;
import java.security.Principal;

public class Main {
    public static void main(String[] args) {
        // Ensure the JAAS configuration is set
        System.setProperty("java.security.auth.login.config", "jaas.config");

        try {
            // Create LoginContext with the configuration name and CallbackHandler
            LoginContext lc = new LoginContext("MyApp", new MyCallbackHandler());

            // Perform authentication
            lc.login();

            // Get the authenticated Subject
            Subject subject = lc.getSubject();
            System.out.println("Authenticated subject: " + subject);

            // Print the Subject's Principals
            for (Principal p : subject.getPrincipals()) {
                System.out.println("Principal: " + p.getName());
            }

            // Logout when done
            lc.logout();
        } catch (LoginException e) {
            System.err.println("Authentication failed: " + e.getMessage());
        }
    }
}
```

- **`LoginContext lc = new LoginContext("MyApp", new MyCallbackHandler())`**: Links to the `"MyApp"` configuration and uses `MyCallbackHandler`.
- **`lc.login()`**: Triggers the authentication process.
- **`lc.getSubject()`**: Retrieves the authenticated `Subject`.

#### **5. Perform Authorized Actions (Optional)**

Once authenticated, you can use the `Subject` to execute code with its privileges using `Subject.doAs()`:

```java
import java.security.PrivilegedAction;

Subject.doAs(subject, new PrivilegedAction<Void>() {
    public Void run() {
        System.out.println("Running as: " + Subject.getSubject(java.security.AccessController.getContext()));
        // Perform privileged actions here
        return null;
    }
});
```

This is useful for authorization, where actions are restricted based on the `Subject`’s `Principals`.

---

### **Putting It All Together**

1. **Configuration**: Define `jaas.config` with your `LoginModule`.
2. **CallbackHandler**: Implement `MyCallbackHandler` to collect user input.
3. **LoginModule**: Implement `MyLoginModule` with your authentication logic.
4. **Main Code**: Use `LoginContext` to authenticate and retrieve a `Subject`.
5. **Authorization**: Use `Subject.doAs()` for privileged actions if needed.

When you run the `Main` class, it will:

- Prompt for a username and password.
- Authenticate using `MyLoginModule`.
- Print the `Subject` and its `Principals` if successful.

---

### **Additional Notes**

- **Real-World Usage**: Replace hardcoded credentials in `MyLoginModule` with checks against a database, LDAP, or another service. Java provides standard modules like `Krb5LoginModule` (Kerberos) or `JndiLoginModule` (LDAP), but they may require additional setup.
- **Multiple LoginModules**: The configuration can specify multiple modules with flags (`required`, `sufficient`, etc.) to create complex authentication flows.
- **Security**: Use secure practices, such as avoiding `String` for passwords (use `char[]`) and integrating with existing security frameworks.

This guide covers the basics of using `javax.security.auth` for authentication and authorization in Java!

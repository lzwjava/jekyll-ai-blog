---
audio: false
generated: true
lang: zh
layout: post
title: Java中的认证与授权
translated: true
type: note
---

要在 Java 中使用 `javax.security.auth` 包，你需要了解它是 Java 认证与授权服务（JAAS）框架的组成部分。该包提供了用于认证用户（验证其身份）和授权（确定其权限）的类和接口。以下是通过 `javax.security.auth` 实现基础认证场景（例如使用用户名和密码认证用户）的逐步指南。

---

### **核心概念概览**

在深入步骤之前，先简要说明 `javax.security.auth` 中的核心组件：

- **Subject（主体）**：表示被认证的实体（如用户或服务），可包含多个身份（Principal）和凭证（如密码或证书）。
- **Principal（身份）**：与主体关联的身份或角色，例如用户名或群组成员关系。
- **Credential（凭证）**：用于认证主体的信息，如密码或加密密钥。
- **LoginModule（登录模块）**：可插拔的组件，用于执行认证逻辑（例如根据数据库校验用户名和密码）。
- **LoginContext（登录上下文）**：核心类，通过一个或多个 LoginModule 协调认证过程。
- **CallbackHandler（回调处理器）**：用于与用户交互的接口，例如提示输入用户名和密码。

了解这些概念后，我们来探索如何使用该包。

---

### **使用 `javax.security.auth` 的步骤**

#### **1. 配置 JAAS**

认证过程依赖于指定所用 `LoginModule` 的配置，可通过配置文件或编程方式定义。

例如，创建名为 `jaas.config` 的文件，内容如下：

```
MyApp {
    com.example.MyLoginModule required;
};
```

- **`MyApp`**：应用或上下文的名称，将在代码中引用。
- **`com.example.MyLoginModule`**：自定义 `LoginModule` 的全限定名（后续将实现）。
- **`required`**：标志位，表示该模块必须成功才能通过认证。其他标志包括 `requisite`、`sufficient` 和 `optional`，可用于实现多模块的复杂逻辑。

设置系统属性指向该文件：

```java
System.setProperty("java.security.auth.login.config", "jaas.config");
```

也可通过编程方式设置配置，但对多数情况而言，使用文件更简便。

#### **2. 实现 CallbackHandler**

`CallbackHandler` 用于收集用户输入（如用户名和密码）。以下是通过控制台实现的简单示例：

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
                throw new UnsupportedCallbackException(callback, "不支持的回调类型");
            }
        }
    }
}
```

- **NameCallback**：提示并获取用户名。
- **PasswordCallback**：提示并获取密码（以 `char[]` 形式存储以提高安全性）。

#### **3. 实现 LoginModule**

`LoginModule` 定义认证逻辑。以下为基础示例，校验硬编码的用户名和密码（实际应用中应使用数据库或外部服务）：

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

    // 初始化模块
    public void initialize(Subject subject, CallbackHandler callbackHandler,
                           Map<String, ?> sharedState, Map<String, ?> options) {
        this.subject = subject;
        this.callbackHandler = callbackHandler;
    }

    // 执行认证
    public boolean login() throws LoginException {
        if (callbackHandler == null) {
            throw new LoginException("未提供回调处理器");
        }

        try {
            NameCallback nameCallback = new NameCallback("用户名: ");
            PasswordCallback passwordCallback = new PasswordCallback("密码: ", false);
            callbackHandler.handle(new Callback[]{nameCallback, passwordCallback});

            String username = nameCallback.getName();
            char[] password = passwordCallback.getPassword();

            // 硬编码校验（实际应用中需替换为真实逻辑）
            if ("myuser".equals(username) && "mypassword".equals(new String(password))) {
                succeeded = true;
                return true;
            } else {
                succeeded = false;
                throw new FailedLoginException("认证失败");
            }
        } catch (Exception e) {
            throw new LoginException("登录错误: " + e.getMessage());
        }
    }

    // 提交认证（向主体添加身份）
    public boolean commit() throws LoginException {
        if (succeeded) {
            subject.getPrincipals().add(new MyPrincipal("myuser"));
            return true;
        }
        return false;
    }

    // 中止认证过程
    public boolean abort() throws LoginException {
        succeeded = false;
        return true;
    }

    // 注销主体
    public boolean logout() throws LoginException {
        subject.getPrincipals().clear();
        subject.getPublicCredentials().clear();
        subject.getPrivateCredentials().clear();
        return true;
    }
}

// 简单的 Principal 实现
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

- **login()**：使用 `CallbackHandler` 获取凭证并校验。
- **commit()**：若认证成功，向 `Subject` 添加 `Principal`。
- **abort()** 和 **logout()**：处理清理或取消操作。

#### **4. 使用 LoginContext 进行认证**

在主应用中使用 `LoginContext` 执行认证：

```java
import javax.security.auth.login.*;
import java.security.Principal;

public class Main {
    public static void main(String[] args) {
        // 确保 JAAS 配置已设置
        System.setProperty("java.security.auth.login.config", "jaas.config");

        try {
            // 使用配置名称和 CallbackHandler 创建 LoginContext
            LoginContext lc = new LoginContext("MyApp", new MyCallbackHandler());

            // 执行认证
            lc.login();

            // 获取已认证的主体
            Subject subject = lc.getSubject();
            System.out.println("已认证的主体: " + subject);

            // 打印主体的身份信息
            for (Principal p : subject.getPrincipals()) {
                System.out.println("身份: " + p.getName());
            }

            // 完成后注销
            lc.logout();
        } catch (LoginException e) {
            System.err.println("认证失败: " + e.getMessage());
        }
    }
}
```

- **`LoginContext lc = new LoginContext("MyApp", new MyCallbackHandler())`**：关联到 `"MyApp"` 配置并使用 `MyCallbackHandler`。
- **`lc.login()`**：触发认证过程。
- **`lc.getSubject()`**：获取已认证的 `Subject`。

#### **5. 执行授权操作（可选）**

认证成功后，可通过 `Subject.doAs()` 以主体权限执行代码：

```java
import java.security.PrivilegedAction;

Subject.doAs(subject, new PrivilegedAction<Void>() {
    public Void run() {
        System.out.println("当前执行身份: " + Subject.getSubject(java.security.AccessController.getContext()));
        // 在此执行需特权操作
        return null;
    }
});
```

这对于基于主体身份的授权非常有用。

---

### **完整流程整合**

1. **配置**：在 `jaas.config` 中定义 `LoginModule`。
2. **CallbackHandler**：实现 `MyCallbackHandler` 收集用户输入。
3. **LoginModule**：实现包含认证逻辑的 `MyLoginModule`。
4. **主代码**：使用 `LoginContext` 进行认证并获取 `Subject`。
5. **授权**：如需特权操作，使用 `Subject.doAs()`。

运行 `Main` 类时将：

- 提示输入用户名和密码。
- 通过 `MyLoginModule` 进行认证。
- 若成功，打印 `Subject` 及其 `Principal` 信息。

---

### **补充说明**

- **实际应用**：将 `MyLoginModule` 中的硬编码凭证替换为数据库、LDAP 或其他服务的校验。Java 提供了标准模块（如 `Krb5LoginModule` 用于 Kerberos、`JndiLoginModule` 用于 LDAP），但可能需要额外配置。
- **多登录模块**：配置中可通过标志位（`required`、`sufficient` 等）指定多个模块，实现复杂认证流程。
- **安全性**：采用安全实践，如避免用 `String` 存储密码（使用 `char[]`）并与现有安全框架集成。

本指南涵盖了在 Java 中使用 `javax.security.auth` 进行认证与授权的基础知识！

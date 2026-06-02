---
audio: false
generated: true
lang: zh
layout: post
title: Java JWT 库
translated: true
type: note
---

要在 Java 中使用 `com.nimbusds.jwt` 库从 JSON Web Token (JWT) 中提取过期时间、签发时间及其他声明信息，请按照以下步骤操作。本解决方案假设您正在处理签名 JWT（这是最常见的类型），并重点提供清晰实用的实现方法。

---

## 前置准备

首先确保您的项目中已添加 Nimbus JOSE + JWT 库。如果使用 Maven，请在 `pom.xml` 中添加以下依赖：

```xml
<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>nimbus-jose-jwt</artifactId>
    <version>9.37</version> <!-- 请替换为最新版本 -->
</dependency>
```

您可以在 [Maven Central](https://mvnrepository.com/artifact/com.nimbusds/nimbus-jose-jwt) 查看最新版本。

---

## 提取过期时间、签发时间及其他声明的步骤

以下是使用 `com.nimbusds.jwt` 库解析 JWT 并获取过期时间、签发时间及附加声明的方法：

1. **解析 JWT 字符串**：使用 `SignedJWT.parse()` 方法将 JWT 字符串转换为 `SignedJWT` 对象
2. **获取声明集**：通过 `getJWTClaimsSet()` 访问 JWT 中的声明（键值对）
3. **提取特定声明**：
   - 使用 `getExpirationTime()` 获取过期时间（`exp` 声明）
   - 使用 `getIssueTime()` 获取签发时间（`iat` 声明）
   - 使用 `getSubject()`、`getClaim()` 等方法获取其他声明
4. **错误处理**：将解析逻辑包裹在 try-catch 块中以处理可能的解析问题

---

## 示例代码

以下完整 Java 示例演示了如何从 JWT 中提取过期时间、签发时间及附加声明（如主题）：

```java
import com.nimbusds.jwt.SignedJWT;
import com.nimbusds.jwt.JWTClaimsSet;
import java.text.ParseException;
import java.util.Date;

public class JwtExtractor {

    public static void main(String[] args) {
        // 请替换为实际的 JWT 字符串
        String jwtString = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzk5MjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";

        try {
            // 步骤 1：解析 JWT 字符串
            SignedJWT signedJWT = SignedJWT.parse(jwtString);

            // 步骤 2：获取声明集
            JWTClaimsSet claimsSet = signedJWT.getJWTClaimsSet();

            // 步骤 3：提取过期时间和签发时间
            Date expirationDate = claimsSet.getExpirationTime();
            Date issuedDate = claimsSet.getIssueTime();
            String subject = claimsSet.getSubject(); // 其他声明示例

            // 步骤 4：显示结果
            if (expirationDate != null) {
                System.out.println("过期时间: " + expirationDate);
            } else {
                System.out.println("未设置过期时间");
            }

            if (issuedDate != null) {
                System.out.println("签发时间: " + issuedDate);
            } else {
                System.out.println("未设置签发时间");
            }

            if (subject != null) {
                System.out.println("主题: " + subject);
            } else {
                System.out.println("未设置主题");
            }

        } catch (ParseException e) {
            System.out.println("无效的 JWT: " + e.getMessage());
        }
    }
}
```

---

## 代码说明

### 1. **导入包**

- `SignedJWT`：表示已签名的 JWT，提供解析和处理方法
- `JWTClaimsSet`：包含 JWT 有效负载中的声明
- `ParseException`：当 JWT 字符串格式错误或无法解析时抛出
- `Date`：用于表示过期时间和签发时间

### 2. **解析 JWT**

- `SignedJWT.parse(jwtString)` 方法接收 JWT 字符串（如 `header.payload.signature`）并返回 `SignedJWT` 对象。如果 JWT 无效，会抛出 `ParseException`

### 3. **访问声明**

- `signedJWT.getJWTClaimsSet()` 获取声明集，其中包含 JWT 有效负载中的所有声明

### 4. **提取特定声明**

- **`getExpirationTime()`**：将 `exp` 声明作为 `Date` 对象返回（如果不存在则返回 `null`），表示令牌的过期时间
- **`getIssueTime()`**：将 `iat` 声明作为 `Date` 对象返回（如果不存在则返回 `null`），表示令牌的签发时间
- **`getSubject()`**：将 `sub` 声明作为 `String` 返回（如果不存在则返回 `null`），这是其他标准声明的示例。您也可以使用 `getClaim("key")` 以 `Object` 形式检索自定义声明

### 5. **错误处理**

- try-catch 块确保当 JWT 格式错误或无效时，程序能通过打印错误信息优雅地处理异常

---

## 注意事项

- **签名与未签名 JWT**：本示例使用 `SignedJWT` 处理签名令牌。如果是未签名 JWT，请改用 `PlainJWT.parse(jwtString)`。对于更通用的方法，可使用 `JWTParser.parse(jwtString)`，然后使用 instanceof 检查类型（`SignedJWT`、`PlainJWT` 等）
- **签名验证**：此代码不验证 JWT 的签名。在生产环境中，应使用 `signedJWT.verify(verifier)` 配合适当的密钥来验证签名，确保令牌的真实性
- **空值检查**：获取声明时务必检查 `null`，因为这些声明是可选的，可能不会出现在每个 JWT 中
- **自定义声明**：要访问非标准声明，请使用 `claimsSet.getClaim("claimName")`，该方法返回可转换为适当类型（如 `String`、`Integer`）的 `Object`

---

## 示例输出

对于上述示例 JWT 字符串：

```
过期时间: Wed Jan 17 19:52:02 UTC 2018
签发时间: Wed Jan 17 19:50:22 UTC 2018
主题: 1234567890
```

---

这种方法通过 `com.nimbusds.jwt` 库提供了简单有效的途径来提取 JWT 中的过期时间、签发时间及其他声明。请将 `jwtString` 替换为您自己的令牌，并根据具体需求调整代码！

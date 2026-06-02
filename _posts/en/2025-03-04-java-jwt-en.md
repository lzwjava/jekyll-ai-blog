---
audio: false
generated: true
lang: en
layout: post
title: Java JWT Library
translated: false
type: note
---

To use the `com.nimbusds.jwt` library in Java to extract information such as the expiration date, issued date, and other claims from a JSON Web Token (JWT), follow the steps outlined below. This solution assumes you are working with a signed JWT, which is the most common type, and focuses on providing a clear, practical approach to achieve your goal.

---

## Prerequisites

First, ensure you have the Nimbus JOSE + JWT library added to your project. If you're using Maven, include the following dependency in your `pom.xml`:

```xml
<dependency>
    <groupId>com.nimbusds</groupId>
    <artifactId>nimbus-jose-jwt</artifactId>
    <version>9.37</version> <!-- Replace with the latest version -->
</dependency>
```

You can check the latest version on [Maven Central](https://mvnrepository.com/artifact/com.nimbusds/nimbus-jose-jwt).

---

## Steps to Extract Expiration Date, Issued Date, and Other Claims

Here’s how you can parse a JWT and retrieve the expiration date, issued date, and additional claims using the `com.nimbusds.jwt` library:

1. **Parse the JWT String**: Use the `SignedJWT.parse()` method to convert the JWT string into a `SignedJWT` object.
2. **Get the Claims Set**: Access the claims (key-value pairs) from the JWT using `getJWTClaimsSet()`.
3. **Extract Specific Claims**:
   - Use `getExpirationTime()` for the expiration date (`exp` claim).
   - Use `getIssueTime()` for the issued date (`iat` claim).
   - Use `getSubject()`, `getClaim()`, or other methods for additional claims.
4. **Handle Errors**: Wrap the parsing logic in a try-catch block to manage potential parsing issues.

---

## Example Code

Below is a complete Java example demonstrating how to extract the expiration date, issued date, and an additional claim (e.g., the subject) from a JWT:

```java
import com.nimbusds.jwt.SignedJWT;
import com.nimbusds.jwt.JWTClaimsSet;
import java.text.ParseException;
import java.util.Date;

public class JwtExtractor {

    public static void main(String[] args) {
        // Replace this with your actual JWT string
        String jwtString = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzk5MjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c";

        try {
            // Step 1: Parse the JWT string
            SignedJWT signedJWT = SignedJWT.parse(jwtString);

            // Step 2: Get the claims set
            JWTClaimsSet claimsSet = signedJWT.getJWTClaimsSet();

            // Step 3: Extract expiration and issued dates
            Date expirationDate = claimsSet.getExpirationTime();
            Date issuedDate = claimsSet.getIssueTime();
            String subject = claimsSet.getSubject(); // Example of another claim

            // Step 4: Display the results
            if (expirationDate != null) {
                System.out.println("Expiration date: " + expirationDate);
            } else {
                System.out.println("No expiration date set.");
            }

            if (issuedDate != null) {
                System.out.println("Issued date: " + issuedDate);
            } else {
                System.out.println("No issued date set.");
            }

            if (subject != null) {
                System.out.println("Subject: " + subject);
            } else {
                System.out.println("No subject set.");
            }

        } catch (ParseException e) {
            System.out.println("Invalid JWT: " + e.getMessage());
        }
    }
}
```

---

## Explanation of the Code

### 1. **Imports**
- `SignedJWT`: Represents a signed JWT and provides methods to parse and process it.
- `JWTClaimsSet`: Contains the claims from the JWT payload.
- `ParseException`: Thrown if the JWT string is malformed or cannot be parsed.
- `Date`: Used to represent the expiration and issued times.

### 2. **Parsing the JWT**
- The `SignedJWT.parse(jwtString)` method takes a JWT string (e.g., `header.payload.signature`) and returns a `SignedJWT` object. If the JWT is invalid, it throws a `ParseException`.

### 3. **Accessing the Claims**
- `signedJWT.getJWTClaimsSet()` retrieves the claims set, which holds all the claims from the JWT’s payload.

### 4. **Extracting Specific Claims**
- **`getExpirationTime()`**: Returns the `exp` claim as a `Date` object (or `null` if not present). This represents when the token expires.
- **`getIssueTime()`**: Returns the `iat` claim as a `Date` object (or `null` if not present). This indicates when the token was issued.
- **`getSubject()`**: Returns the `sub` claim as a `String` (or `null` if not present), an example of another standard claim. You can also use `getClaim("key")` to retrieve custom claims as an `Object`.

### 5. **Error Handling**
- The try-catch block ensures that if the JWT is malformed or invalid, the program handles the error gracefully by printing an error message.

---

## Notes

- **Signed vs. Unsigned JWTs**: This example uses `SignedJWT` for signed tokens. If you have an unsigned JWT, use `PlainJWT.parse(jwtString)` instead. For a more generic approach, you can use `JWTParser.parse(jwtString)` and then check the type (`SignedJWT`, `PlainJWT`, etc.) using instanceof.
- **Signature Verification**: This code does not verify the JWT’s signature. In a production environment, you should verify the signature using `signedJWT.verify(verifier)` with an appropriate key to ensure the token’s authenticity.
- **Null Checks**: Always check for `null` when retrieving claims, as they are optional and may not be present in every JWT.
- **Custom Claims**: To access non-standard claims, use `claimsSet.getClaim("claimName")`, which returns an `Object` that you can cast to the appropriate type (e.g., `String`, `Integer`).

---

## Sample Output

For the example JWT string above:
```
Expiration date: Wed Jan 17 19:52:02 UTC 2018
Issued date: Wed Jan 17 19:50:22 UTC 2018
Subject: 1234567890
```

---

This approach provides a simple and effective way to extract the expiration date, issued date, and other claims from a JWT using the `com.nimbusds.jwt` library. Replace the `jwtString` with your own token and adapt the code to your specific needs!

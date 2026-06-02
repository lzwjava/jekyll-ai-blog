---
audio: false
generated: true
lang: en
layout: post
title: Cryptography In Java
translated: false
type: note
---

The `javax.crypto` package in Java provides a set of classes and methods for performing cryptographic operations such as encryption, decryption, key generation, and message authentication. Below is a comprehensive guide on how to use `javax.crypto`, including explanations and practical examples for common use cases like symmetric encryption, asymmetric encryption, and message authentication.

---

### **What is javax.crypto?**

The `javax.crypto` package is part of the Java Cryptography Architecture (JCA) and offers tools to implement secure communication through cryptography. It supports:

- **Symmetric cryptography**: Uses the same key for encryption and decryption (e.g., AES, DES).
- **Asymmetric cryptography**: Uses a public/private key pair (e.g., RSA).
- **Message authentication**: Ensures data integrity and authenticity (e.g., HMAC).
- **Key generation and management**: Tools to create and handle cryptographic keys.

To use `javax.crypto`, you need to:

1. Select a cryptographic algorithm.
2. Generate or obtain the necessary keys.
3. Use the provided classes (e.g., `Cipher`, `KeyGenerator`, `Mac`) to perform operations.

Below are step-by-step examples for common scenarios.

---

### **1. Symmetric Encryption with AES**

Symmetric encryption uses a single key for both encryption and decryption. Here’s how to encrypt and decrypt a string using AES (Advanced Encryption Standard) with the `Cipher` class in CBC mode with PKCS5 padding.

#### **Steps**

- Generate a secret key.
- Create and initialize a `Cipher` instance.
- Encrypt and decrypt the data.

#### **Example Code**

```java
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.security.SecureRandom;
import java.nio.charset.StandardCharsets;

public class SymmetricEncryptionExample {
    public static void main(String[] args) throws Exception {
        // Step 1: Generate a secret key for AES
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(128); // 128-bit key
        SecretKey secretKey = keyGen.generateKey();

        // Step 2: Generate a random Initialization Vector (IV)
        SecureRandom random = new SecureRandom();
        byte[] iv = new byte[16]; // AES block size is 16 bytes
        random.nextBytes(iv);
        IvParameterSpec ivSpec = new IvParameterSpec(iv);

        // Step 3: Create and initialize Cipher for encryption
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivSpec);

        // Step 4: Encrypt data
        String plaintext = "Hello, World!";
        byte[] plaintextBytes = plaintext.getBytes(StandardCharsets.UTF_8);
        byte[] ciphertext = cipher.doFinal(plaintextBytes);

        // Step 5: Initialize Cipher for decryption with the same IV
        cipher.init(Cipher.DECRYPT_MODE, secretKey, ivSpec);
        byte[] decryptedBytes = cipher.doFinal(ciphertext);
        String decryptedText = new String(decryptedBytes, StandardCharsets.UTF_8);

        // Output results
        System.out.println("Original: " + plaintext);
        System.out.println("Decrypted: " + decryptedText);
    }
}
```

#### **Key Points**

- **Algorithm**: `"AES/CBC/PKCS5Padding"` specifies AES with CBC mode and padding to handle data that isn’t a multiple of the block size.
- **IV**: The Initialization Vector must be random for encryption and reused for decryption. It’s typically prepended to the ciphertext or transmitted separately.
- **Key Management**: In a real application, securely share the `secretKey` with the recipient.

---

### **2. Asymmetric Encryption with RSA**

Asymmetric encryption uses a public key to encrypt and a private key to decrypt. Here’s an example using RSA.

#### **Steps**

- Generate a public/private key pair.
- Encrypt with the public key.
- Decrypt with the private key.

#### **Example Code**

```java
import javax.crypto.Cipher;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.PublicKey;
import java.nio.charset.StandardCharsets;

public class AsymmetricEncryptionExample {
    public static void main(String[] args) throws Exception {
        // Step 1: Generate an RSA key pair
        KeyPairGenerator keyPairGen = KeyPairGenerator.getInstance("RSA");
        keyPairGen.initialize(2048); // 2048-bit key
        KeyPair keyPair = keyPairGen.generateKeyPair();
        PublicKey publicKey = keyPair.getPublic();
        PrivateKey privateKey = keyPair.getPrivate();

        // Step 2: Encrypt with the public key
        Cipher cipher = Cipher.getInstance("RSA");
        cipher.init(Cipher.ENCRYPT_MODE, publicKey);
        String plaintext = "Secret Message";
        byte[] plaintextBytes = plaintext.getBytes(StandardCharsets.UTF_8);
        byte[] ciphertext = cipher.doFinal(plaintextBytes);

        // Step 3: Decrypt with the private key
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        byte[] decryptedBytes = cipher.doFinal(ciphertext);
        String decryptedText = new String(decryptedBytes, StandardCharsets.UTF_8);

        // Output results
        System.out.println("Original: " + plaintext);
        System.out.println("Decrypted: " + decryptedText);
    }
}
```

#### **Key Points**

- **Size Limit**: RSA can only encrypt data smaller than the key size (e.g., ~245 bytes for a 2048-bit key). For larger data, use hybrid encryption (encrypt data with a symmetric key, then encrypt that key with RSA).
- **Key Distribution**: Share the public key openly; keep the private key secret.

---

### **3. Message Authentication with HMAC**

A Message Authentication Code (MAC) ensures data integrity and authenticity. Here’s how to use `Mac` with HMAC-SHA256.

#### **Example Code**

```java
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

public class MacExample {
    public static void main(String[] args) throws Exception {
        // Step 1: Create a secret key
        String secret = "mysecretkey";
        SecretKeySpec secretKey = new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256");

        // Step 2: Initialize Mac with the key
        Mac mac = Mac.getInstance("HmacSHA256");
        mac.init(secretKey);

        // Step 3: Compute MAC for the data
        String data = "Data to authenticate";
        byte[] macValue = mac.doFinal(data.getBytes(StandardCharsets.UTF_8));
        String macBase64 = Base64.getEncoder().encodeToString(macValue);

        // Output result
        System.out.println("MAC: " + macBase64);
    }
}
```

#### **Key Points**

- **Verification**: The recipient recomputes the MAC with the same key and data; if it matches, the data is authentic and unaltered.
- **Key**: Use a shared secret key, securely distributed beforehand.

---

### **4. Encrypting/Decrypting Streams**

For large data (e.g., files), use `CipherInputStream` or `CipherOutputStream`.

#### **Example Code (Encrypting a File)**

```java
import javax.crypto.Cipher;
import javax.crypto.CipherOutputStream;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.security.SecureRandom;

public class StreamEncryptionExample {
    public static void main(String[] args) throws Exception {
        // Generate key and IV
        KeyGenerator keyGen = KeyGenerator.getInstance("AES");
        keyGen.init(128);
        SecretKey secretKey = keyGen.generateKey();
        byte[] iv = new byte[16];
        new SecureRandom().nextBytes(iv);
        IvParameterSpec ivSpec = new IvParameterSpec(iv);

        // Initialize Cipher
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey, ivSpec);

        // Encrypt file
        try (FileInputStream fis = new FileInputStream("input.txt");
             FileOutputStream fos = new FileOutputStream("encrypted.txt");
             CipherOutputStream cos = new CipherOutputStream(fos, cipher)) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = fis.read(buffer)) != -1) {
                cos.write(buffer, 0, bytesRead);
            }
        }
    }
}
```

#### **Key Points**

- **Streams**: Use `CipherOutputStream` for encryption and `CipherInputStream` for decryption to process data incrementally.
- **IV Handling**: Store the IV with the encrypted file (e.g., prepend it).

---

### **5. Password-Based Encryption (PBE)**

Derive a key from a password using `SecretKeyFactory`.

#### **Example Code**

```java
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.SecureRandom;
import java.nio.charset.StandardCharsets;

public class PBEExample {
    public static void main(String[] args) throws Exception {
        // Password and salt
        char[] password = "mysecretpassword".toCharArray();
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);

        // Derive key from password
        PBEKeySpec pbeKeySpec = new PBEKeySpec(password, salt, 10000, 256); // 256-bit key
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        SecretKey tempKey = factory.generateSecret(pbeKeySpec);
        SecretKey secretKey = new SecretKeySpec(tempKey.getEncoded(), "AES");

        // Encrypt with derived key
        Cipher cipher = Cipher.getInstance("AES");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey);
        String plaintext = "Hello from PBE";
        byte[] ciphertext = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

        System.out.println("Encrypted: " + Base64.getEncoder().encodeToString(ciphertext));
    }
}
```

#### **Key Points**

- **Salt**: Randomize the key derivation; store it with the encrypted data.
- **Iterations**: Increase computational cost to thwart brute-force attacks (e.g., 10,000).

---

### **Key Classes in javax.crypto**

- **`Cipher`**: Performs encryption and decryption.
- **`KeyGenerator`**: Generates symmetric keys (e.g., AES).
- **`KeyPairGenerator`**: Generates asymmetric key pairs (e.g., RSA).
- **`Mac`**: Computes message authentication codes.
- **`SecretKeyFactory`**: Derives keys (e.g., from passwords).
- **`SecureRandom`**: Generates cryptographically secure random numbers.

---

### **Best Practices**

- **Exception Handling**: Wrap code in try-catch blocks for exceptions like `NoSuchAlgorithmException`, `InvalidKeyException`, etc.
- **Key Management**: Store keys securely (e.g., in a `KeyStore`) and never hardcode them.
- **Algorithm Choice**: Use secure algorithms (e.g., AES-256, RSA-2048) and modes (e.g., CBC with IV).
- **Providers**: The default SunJCE provider suffices, but you can use others (e.g., BouncyCastle) via `Cipher.getInstance("AES", "BC")`.

---

### **Conclusion**

To use `javax.crypto`, select the appropriate cryptographic algorithm for your needs, generate or obtain keys, and leverage classes like `Cipher`, `KeyGenerator`, and `Mac` to perform operations. Whether encrypting data symmetrically with AES, asymmetrically with RSA, or ensuring integrity with HMAC, `javax.crypto` provides the tools—paired with proper initialization and secure key management—to implement robust cryptography in Java.

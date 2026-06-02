---
audio: false
generated: true
image: false
lang: en
layout: post
model: google/gemini-3-pro-preview
title: Updating SSL Certificates in WebSphere Liberty
translated: false
type: note
---

Updating an SSL certificate in IBM WebSphere Liberty Profile (WLP) primarily involves replacing the key entry in the configured **keystore** file and updating the truststore if a new Certificate Authority (CA) or intermediate certificates are involved.

The `.sth` file you mentioned is often a **stash file** associated with a **CMS (Certificate Management System) keystore** (`.kdb` format) in traditional WebSphere Application Server, used to securely store the keystore password. **IBM WebSphere Liberty Profile** typically uses **PKCS12** (`.p12`) or **JKS** (`.jks`) format keystores, where the password might be stored encoded directly in the `server.xml` and **doesn't typically use a separate `.sth` file** unless specifically configured for other components or older versions/configurations.

Here is a general, step-by-step process for renewal, keystore management, and backup.

-----

## 1\. Backup Existing Keystore and Configuration

**This is the most critical step.** Before making any changes, back up your existing files.

1.  **Stop the Liberty Server:**
    ```bash
    wlp/bin/server stop <server_name>
    ```
2.  **Back up Keystore Files:**
      * The default keystore is usually named **`key.p12`** (or `key.jks` in older versions) and is located in:
        `wlp/usr/servers/<server_name>/resources/security/`
      * **Copy the entire `security` directory** to a safe location outside of your WLP installation.
3.  **Back up Server Configuration:**
      * Copy the **`server.xml`** file:
        `wlp/usr/servers/<server_name>/server.xml`

-----

## 2\. Obtain and Prepare the New Certificate

You should receive your new certificate and intermediate/root CA certificates from your Certificate Authority (CA). They are typically provided as `.pem`, `.cer`, or a PKCS12 bundle (`.p12`).

If you started with a Certificate Signing Request (CSR) generated from your existing keystore, you'll need to import the signed certificate back into that same keystore using the same private key.

-----

## 3\. Update the Keystore with the New Certificate

The **`keytool`** utility, which is part of the Java Runtime Environment (JRE/JDK) used by Liberty, is the standard tool for managing keystores.

The default keystore configuration in `server.xml` often looks like this (you'll need the `location` and `password`):

```xml
<keyStore id="defaultKeyStore"
          location="${server.config.dir}/resources/security/key.p12"
          password="{xor}..." />
```

### Option A: Replace the Certificate in the Existing Keystore

This method is used when you have a **new certificate signed by a CA** corresponding to the **existing private key** in your keystore. You must import the CA's root and intermediate certificates first, followed by your new personal certificate.

1.  **Import Root/Intermediate CA Certificates (into the Key/Trust Store):**
    ```bash
    # Navigate to the JRE/JDK bin directory, e.g., wlp/java/jre/bin
    keytool -importcert -file <ca_root_cert_file>.cer -alias <root_alias> -keystore <keystore_location> -storepass <keystore_password> -storetype PKCS12
    # Repeat for any intermediate certs
    keytool -importcert -file <intermediate_cert_file>.cer -alias <intermediate_alias> -keystore <keystore_location> -storepass <keystore_password> -storetype PKCS12
    ```
2.  **Import the New Personal (Signed) Certificate:**
    ```bash
    keytool -importcert -file <new_signed_cert_file>.cer -alias <private_key_alias> -keystore <keystore_location> -storepass <keystore_password> -storetype PKCS12
    ```
      * The `<private_key_alias>` **must match the alias of the private key** used to generate the CSR. If it's the Liberty default, the alias is often **`default`**.

### Option B: Create a New Keystore File

If you generated a brand-new key pair outside of the old keystore (or received a new `.p12` bundle) or if the renewal is complex, you can create a new keystore and replace the old one.

1.  **Import the new key/certificate into a new file:** (This depends heavily on how you received the new certificate—a CA-provided `.p12` bundle is the easiest).
2.  **Replace the old file:** Rename the old `key.p12` file (e.g., to `key.p12.old`) and place your new, correctly named keystore file (`key.p12`) in the `resources/security/` directory.

-----

## 4\. Renewing a Self-Signed Certificate

If you're using a **self-signed certificate** created by Liberty's `securityUtility`, the process is simply to delete the old one and let Liberty create a new one, or use the `keytool` command directly to generate a new one.

1.  **Stop the Liberty Server.**
2.  **Delete the existing keystore file** (`key.p12`) from `wlp/usr/servers/<server_name>/resources/security/`.
3.  **Start the Liberty Server.**
    ```bash
    wlp/bin/server start <server_name>
    ```
    If your `server.xml` has the `<keyStore id="defaultKeyStore" ... />` element, Liberty will automatically call the `securityUtility` to generate a **new self-signed certificate** and keystore.

-----

## 5\. Restart and Verify

1.  **Start the Liberty Server** (if it's not already running from the renewal step).
    ```bash
    wlp/bin/server start <server_name>
    ```
2.  **Check the logs:** Review `messages.log` for any SSL or keystore-related errors.
3.  **Verify in a browser:** Access your application via HTTPS and check the certificate details in the browser to ensure the **new expiration date** is correct and the certificate chain is trusted.

Would you like me to find the specific **`keytool`** commands for your certificate file type (e.g., P7B, PEM, PKCS12) or the command to **encode a new keystore password** for your `server.xml`?

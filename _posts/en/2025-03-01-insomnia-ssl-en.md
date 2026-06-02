---
audio: false
generated: true
lang: en
layout: post
title: SSL Certificate Validation in Insomnia
translated: false
type: note
---

To fix the "SSL peer certificate or SSH remote key was not OK" error in Insomnia, this error typically occurs when Insomnia cannot verify the SSL certificate of the server you're trying to connect to. Below are step-by-step solutions to resolve this issue:

### 1. **Disable SSL Certificate Validation (For Local Development Only)**
If you're working with a local development server that uses a self-signed or invalid SSL certificate, you can disable certificate validation in Insomnia:
- Open Insomnia and go to **Application** > **Preferences**.
- Navigate to the **Request / Response** section.
- Uncheck the box labeled **Validate certificates**.
- Retry your request.

**Important**: This option bypasses security checks and should **only be used for testing or local development**. Do not use it for production environments, as it makes your connection vulnerable.

---

### 2. **Verify the Server’s SSL Certificate**
The error might indicate an issue with the server’s SSL certificate (e.g., expired, self-signed, or hostname mismatch). To check:
- Open the server’s URL in a web browser.
- Click the padlock icon in the address bar to view certificate details.
- Ensure the certificate is valid, not expired, and matches the domain name.
- If the certificate is invalid or misconfigured, contact the server administrator to fix it.

---

### 3. **Import a Client Certificate (If Required)**
If the server requires a client certificate for authentication, you’ll need to configure it in Insomnia:
- In Insomnia, go to **Client Certificates** (accessible from the main dashboard or preferences).
- Click **Add Certificate**.
- Import your certificate file (supported formats include PFX or PEM).
- Assign it to the specific domain or hostname you’re connecting to.
- Test the request again.

---

### 4. **Update Insomnia**
SSL-related issues might be due to a bug in an older version of Insomnia. To ensure you’re on the latest version:
- Check for updates in **Application** > **About** or download the latest release from the official Insomnia website.
- Install the update and retry your request.

---

### 5. **Test with Curl**
If the above steps don’t resolve the issue, test the request outside of Insomnia to isolate the problem:
- Open a terminal and use the `curl` command with the same URL and parameters (e.g., `curl -v https://example.com`).
- If `curl` also fails, the issue is likely with the server’s configuration rather than Insomnia.
- If `curl` succeeds, it may indicate a specific problem with Insomnia, and you can report it to their support team.

---

### Summary
Start by disabling SSL validation if it’s a local server, then verify the server’s certificate or configure a client certificate if needed. Ensure Insomnia is up to date, and use `curl` to troubleshoot further if necessary. These steps should resolve most cases of the "SSL peer certificate or SSH remote key was not OK" error.

If the issue persists, it may be due to a server-side misconfiguration or a rare bug in Insomnia. Let me know if you need more assistance!

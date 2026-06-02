---
audio: false
generated: true
lang: en
layout: post
title: Use Features in the Kong Insomnia GUI
translated: false
type: note
---

Kong Insomnia provides a robust graphical user interface (GUI) to simplify API development. Below is a detailed guide on how to use **params**, **body**, **auth**, **cookies**, **certificates**, **settings**, and **proxy** within the Insomnia GUI.

---

#### 1. **Params (Query Parameters)**

Query parameters are used to append data to the URL, typically for GET requests.

- **How to Use**:
  - Open the **Debug tab** and select or create a request (e.g., GET).
  - Next to the URL field, click the **Query** tab.
  - Add key-value pairs for your query parameters. For example, entering `key` as "id" and `value` as "123" will append `?id=123` to your URL.
  - To use environment variables, type `{{variableName}}` in the value field (e.g., `{{userId}}`).
  - Enable or disable specific parameters by toggling the checkbox next to each pair.

- **Example**:
  For a URL like `https://api.example.com/users?id=123`, add:
  - Key: `id`
  - Value: `123`
  Insomnia will automatically format the URL with the query string.

---

#### 2. **Body**

The body is used to send data with requests like POST or PUT.

- **How to Use**:
  - In the **Debug tab**, select a request (e.g., POST or PUT).
  - Switch to the **Body** tab below the URL field.
  - Choose a body type from the dropdown:
    - **JSON**: Enter JSON data (e.g., `{"name": "John", "age": 30}`).
    - **Form URL-Encoded**: Add key-value pairs, similar to query parameters.
    - **Multipart Form**: Add fields or upload files for forms with file attachments.
    - **Raw**: Input plain text or other formats (e.g., XML).
  - Use environment variables by typing `{{variableName}}` within the body content.

- **Example**:
  For a POST request sending JSON:
  - Select **JSON** from the dropdown.
  - Enter: `{"name": "John", "age": "{{userAge}}"}`.
  Insomnia will set the `Content-Type` header to `application/json` automatically.

---

#### 3. **Auth (Authentication)**

Authentication settings allow you to include credentials or tokens in your requests.

- **How to Use**:
  - In the **Debug tab**, select your request.
  - Go to the **Auth** tab.
  - Choose an authentication type from the dropdown:
    - **Basic Auth**: Enter a username and password.
    - **Bearer Token**: Paste your token (e.g., a JWT).
    - **OAuth 2.0**: Configure client ID, secret, and other details for OAuth flows.
    - **API Key**: Add a key-value pair (e.g., Key: `Authorization`, Value: `your-api-key`).
  - Insomnia automatically adds the authentication details to the request headers.

- **Example**:
  For a Bearer Token:
  - Select **Bearer Token**.
  - Paste your token (e.g., `abc123xyz`).
  The request header will include: `Authorization: Bearer abc123xyz`.

---

#### 4. **Cookies**

Cookies are managed automatically but can be viewed or edited manually.

- **How to Use**:
  - Insomnia stores cookies received from server responses per workspace.
  - To manage cookies:
    - Go to **Preferences** (Ctrl + , or Cmd + , on macOS).
    - Navigate to **Data** > **Cookie Jar**.
    - View, edit, or delete cookies as needed.
  - Cookies persist across requests in the same workspace and are sent automatically with subsequent requests.

- **Tip**:
  If you need to test with specific cookies, manually add them in the **Cookie Jar** for the relevant domain.

---

#### 5. **Certificates**

Client certificates are used for HTTPS requests requiring mutual TLS authentication.

- **How to Use**:
  - Go to **Preferences** (Ctrl + , or Cmd + ,).
  - Select the **Certificates** section.
  - Click **Add Certificate**:
    - Provide the certificate file (e.g., `.pem`, `.crt`).
    - Add the private key file and an optional passphrase if required.
    - Associate the certificate with specific hosts (e.g., `api.example.com`).
  - Insomnia will use the certificate for requests to the specified hosts.

- **Example**:
  For `api.example.com` requiring a certificate:
  - Upload `client.crt` and `client.key`.
  - Set Host to `api.example.com`.
  Requests to this domain will include the certificate.

---

#### 6. **Settings**

Settings allow you to customize Insomnia’s behavior.

- **How to Use**:
  - Access via **Preferences** (Ctrl + , or Cmd + ,).
  - Key options include:
    - **Theme**: Switch between light, dark, or system default.
    - **Proxy**: Configure proxy settings (see below).
    - **Plugins**: Install additional functionality (e.g., custom response formatters).
    - **Data**: Manage Local Vault for secure storage of sensitive data like API keys.

- **Tip**:
  Use the **Local Vault** to store sensitive values (e.g., tokens) securely instead of hardcoding them.

---

#### 7. **Proxy**

Proxies route your requests through a specified server, useful for debugging or corporate networks.

- **How to Use**:
  - Go to **Preferences** > **Proxy**.
  - Enable the proxy and enter the proxy server details (e.g., `http://proxy.example.com:8080`).
  - For global use, save it here.
  - For per-request proxy:
    - Click the cog icon next to the request name in the **Debug tab**.
    - Override proxy settings in the request-specific configuration.

- **Example**:
  To route requests through a corporate proxy:
  - Enable proxy in **Preferences**.
  - Set Proxy URL to `http://proxy.example.com:8080`.
  All requests will now use this proxy unless overridden.

---

### Summary

Here’s a quick recap of how to use these features in the Insomnia GUI:

- **Params**: Add query parameters in the **Query** tab for GET requests.
- **Body**: Send data with POST/PUT requests via the **Body** tab, selecting the format.
- **Auth**: Set up authentication in the **Auth** tab for secure requests.
- **Cookies**: Manage cookies in **Preferences** > **Cookie Jar**.
- **Certificates**: Add client certificates in **Preferences** > **Certificates** for HTTPS.
- **Settings**: Customize Insomnia in **Preferences** (themes, plugins, etc.).
- **Proxy**: Configure proxies in **Preferences** or per request.

By leveraging these features, you can efficiently test and debug APIs in Kong Insomnia. Experiment with each section to tailor your workflow!

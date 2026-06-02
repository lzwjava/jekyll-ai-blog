---
audio: false
generated: true
lang: en
layout: post
title: Maven Proxy Settings
translated: false
type: note
---

Based on the output of your `checkproxy` command, your HTTP and HTTPS proxies are both set to `http://127.0.0.1:7890`. Below is the updated Maven `settings.xml` configuration snippet to configure Maven to use these proxy settings.

### Updated `settings.xml` Proxy Configuration Snippet

Add or update the `<proxies>` section in your Maven `settings.xml` file (located at `~/.m2/settings.xml` or `/usr/share/maven/conf/settings.xml`) with the following:

```xml
<settings>
  <proxies>
    <proxy>
      <id>http-proxy</id>
      <active>true</active>
      <protocol>http</protocol>
      <host>127.0.0.1</host>
      <port>7890</port>
      <nonProxyHosts>localhost|127.0.0.1</nonProxyHosts>
    </proxy>
    <proxy>
      <id>https-proxy</id>
      <active>true</active>
      <protocol>https</protocol>
      <host>127.0.0.1</host>
      <port>7890</port>
      <nonProxyHosts>localhost|127.0.0.1</nonProxyHosts>
    </proxy>
  </proxies>
</settings>
```

### Explanation of the Snippet

- **`<id>`**: Unique identifiers (`http-proxy` and `https-proxy`) for each proxy configuration.
- **`<active>true</active>`**: Enables the proxy.
- **`<protocol>`**: Set to `http` for the HTTP proxy and `https` for the HTTPS proxy, matching your `checkproxy` output.
- **`<host>127.0.0.1</host>`**: The proxy server’s IP address, as shown in your proxy settings.
- **`<port>7890</port>`**: The port number for both proxies, as specified.
- **`<nonProxyHosts>localhost|127.0.0.1</nonProxyHosts>`**: Excludes `localhost` and `127.0.0.1` from being proxied, which is standard to avoid issues with local services.
- **No `<username>` or `<password>`**: Since your proxy output doesn’t indicate authentication, these fields are omitted. If authentication is required, add them with your credentials.

### Steps to Apply

1. **Open `settings.xml`**:
   - If `~/.m2/settings.xml` exists, edit it (e.g., `nano ~/.m2/settings.xml`).
   - If it doesn’t exist, create it or edit the global file at `/usr/share/maven/conf/settings.xml` (requires `sudo`).

2. **Insert or Update the `<proxies>` Section**:
   - If `<proxies>` already exists, replace or merge the `<proxy>` entries with the snippet above.
   - If `<settings>` is empty or minimal, you can use the entire snippet as the file’s content.

3. **Save and Close** the file.

### Verify the Configuration

Run a Maven command that requires internet access to confirm the proxy is used:

```bash
cd ~/Projects/blog-server
mvn -X clean checkstyle:check
```

In the debug output (`-X`), look for lines indicating Maven is using the proxy (e.g., connections to `127.0.0.1:7890`). If the command downloads dependencies or completes without network errors, the proxy is working.

### Troubleshooting

- **Proxy Not Working**:
  - Ensure the proxy server at `127.0.0.1:7890` is running (e.g., test with `curl -x http://127.0.0.1:7890 https://repo.maven.apache.org`).
  - Check for typos in the `settings.xml` file.
- **Settings File Ignored**:
  - Confirm Maven is reading `~/.m2/settings.xml` by checking the debug output for the file path.
  - If using the global file, ensure you edited `/usr/share/maven/conf/settings.xml` correctly.
- **Authentication Required**:
  - If your proxy requires a username and password, add:

    ```xml
    <username>yourusername</username>
    <password>yourpassword</password>
    ```

    to each `<proxy>` block.

### Note on Previous Context

Your `checkstyle:check` issue in the `blog-server` project (related to `checks.xml` and `SuppressWithNearbyTextFilter`) should be resolved separately by updating the `pom.xml` as previously suggested (using `maven-checkstyle-plugin:3.3.1` with Checkstyle `10.17.0` and `<configLocation>${project.basedir}/checks.xml</configLocation>`). The proxy settings above will ensure Maven can download any required artifacts for that fix.

Let me know if you encounter issues or need help with the updated `pom.xml` or further proxy debugging!

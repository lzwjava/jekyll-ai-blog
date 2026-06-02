---
audio: false
generated: true
lang: en
layout: post
title: Troubleshoot curl Downloads
translated: false
type: note
---

When you try to download an Eclipse ZIP file from eclipse.org using `curl -O`, you might encounter an issue where it downloads an HTML file instead of the desired ZIP file, accompanied by a "301 Moved Permanently" error. This happens because the URL you’re using is redirecting to another location, and `curl` isn’t automatically following that redirect to the actual file. Here’s how to fix it:

### Understanding the Issue

- **301 Moved Permanently**: This HTTP status code means the resource (the ZIP file) has permanently moved to a new URL. Servers often use redirects for download links to point to mirror sites or updated locations.
- **`curl -O` Behavior**: The `-O` option tells `curl` to save the downloaded content to a file named after the remote file. However, without explicitly handling redirects, `curl` might save the content of the intermediate redirect response (often an HTML page) instead of following it to the ZIP file.

### Solution

To ensure `curl` follows the redirect and downloads the Eclipse ZIP file, use the `-L` option alongside `-O`. The `-L` flag instructs `curl` to follow any redirects until it reaches the final destination.

#### Command

```bash
curl -L -O <URL>
```

- **`-L`**: Follows redirects, such as the 301 redirect, to the new location.
- **`-O`**: Saves the file with the original name from the final URL.
- **`<URL>`**: Replace this with the specific Eclipse download URL, such as `https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2023-03/R/eclipse-java-2023-03-R-win32-x86_64.zip`.

### Step-by-Step Instructions

1. **Find the Correct URL**:
   - Visit the Eclipse website (e.g., `https://www.eclipse.org/downloads/`).
   - Select the desired package (e.g., Eclipse IDE for Java Developers).
   - Right-click the download link or button and copy the URL. Alternatively, use your browser’s developer tools (F12, Network tab) to capture the exact URL when you click download.

2. **Run the Command**:
   - Open your terminal.
   - Execute the `curl` command with the `-L` and `-O` options, using the URL you copied:

     ```bash
     curl -L -O https://www.eclipse.org/downloads/download.php?file=/technology/epp/downloads/release/2023-03/R/eclipse-java-2023-03-R-win32-x86_64.zip
     ```

   - This should download the ZIP file (e.g., `eclipse-java-2023-03-R-win32-x86_64.zip`) to your current directory.

### Troubleshooting

If you still encounter issues, try these additional steps:

- **Check Redirects with Verbose Output**:
  - Use the `-v` option to see detailed information about the request and redirects:

    ```bash
    curl -v -L -O <URL>
    ```

  - Look at the `Location` header in the 301 response to see where it’s redirecting. If it’s pointing to an HTML page instead of a ZIP file, the URL might not be the direct download link.

- **Verify the URL**:
  - Eclipse often uses a `download.php` script that may redirect to a mirror. Ensure your URL is either the direct link to the ZIP file or a redirecting link that resolves to the file. For example, a direct mirror link might look like:

    ```bash
    curl -L -O https://mirror.its.dal.ca/eclipse/technology/epp/downloads/release/2023-03/R/eclipse-java-2023-03-R-win32-x86_64.zip
    ```

- **Set a User-Agent Header**:
  - Some servers behave differently based on the client. If the server returns HTML because it detects `curl`, mimic a browser by adding a User-Agent:

    ```bash
    curl -L -O -A "Mozilla/5.0" <URL>
    ```

### Why This Works

The Eclipse website may redirect download requests to a mirror or an updated URL. Without `-L`, `curl -O` saves the redirect response (an HTML page) instead of following it. Adding `-L` ensures `curl` tracks the 301 redirect to the actual ZIP file, resolving the issue.

By following these steps, you should successfully download the Eclipse ZIP file from eclipse.org using `curl`.

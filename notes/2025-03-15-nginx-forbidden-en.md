---
audio: false
generated: true
lang: en
layout: post
title: Fixing Nginx 403 Forbidden Error
translated: false
type: note
---

To fix the "403 Forbidden" error you're encountering with your Nginx configuration, you need to address two primary issues: an incorrect use of the `root` directive in your `location` block and potential file system permission problems. Below is a step-by-step guide to resolve the issue based on your provided configuration:

```nginx
server {
    listen 80;
    server_name localhost;
    location /movies {
        root /path/to/your/movie/folder;
        autoindex on; # Enables directory listing
    }
}
```

When you visit `http://localhost/movies`, you get a 403 Forbidden error, which typically indicates that Nginx cannot access or serve the intended directory. Here's how to fix it:

---

### 1. Correct the Nginx Configuration
The current `location /movies` block uses `root /path/to/your/movie/folder;`. In Nginx, the `root` directive appends the request URI (e.g., `/movies`) to the specified path, meaning Nginx tries to serve files from `/path/to/your/movie/folder/movies`. If this directory doesn’t exist, Nginx returns a 403 error.

To fix this, you should use the `alias` directive instead of `root`. The `alias` directive maps the `/movies/` URI directly to `/path/to/your/movie/folder/` without appending the URI, which is likely your intended behavior.

Update your configuration as follows:

```nginx
server {
    listen 80;
    server_name localhost;
    location /movies/ {
        alias /path/to/your/movie/folder/;
        autoindex on; # Enables directory listing
    }
}
```

- **Key Changes:**
  - Changed `root` to `alias`.
  - Added trailing slashes to `location /movies/` and `alias /path/to/your/movie/folder/` to ensure proper directory handling with `autoindex`.

- **Apply the Changes:**
  After updating the configuration file (e.g., `/etc/nginx/nginx.conf` or a file in `/etc/nginx/sites-enabled/`), restart Nginx to apply the changes:
  - On Linux: `sudo systemctl restart nginx`
  - On Windows: Stop and start the Nginx service manually.

- **Test the URL:**
  Visit `http://localhost/movies/` (note the trailing slash) to see if the directory listing appears.

---

### 2. Check File System Permissions
If the configuration change alone doesn’t resolve the 403 error, the issue might be related to file system permissions. Nginx needs read access to `/path/to/your/movie/folder/` and its contents, and this access depends on the user under which Nginx is running (commonly `nginx` or `www-data`).

- **Identify the Nginx User:**
  Check your main Nginx configuration file (e.g., `/etc/nginx/nginx.conf`) for the `user` directive. It might look like:
  ```nginx
  user nginx;
  ```
  If not specified, it could default to `www-data` or another user depending on your system.

- **Verify Permissions:**
  Run the following command to inspect the permissions of your movie folder:
  ```bash
  ls -l /path/to/your/movie/folder
  ```
  This will display the owner, group, and permissions (e.g., `drwxr-xr-x`).

- **Adjust Permissions if Needed:**
  Ensure the Nginx user has read (and execute for directories) access. Here are two options:
  - **Option 1: Change Ownership (Recommended):**
    Set the folder’s owner to the Nginx user (e.g., `nginx`):
    ```bash
    sudo chown -R nginx:nginx /path/to/your/movie/folder
    ```
    Replace `nginx` with the actual user if it’s different (e.g., `www-data`).

  - **Option 2: Make Readable by All (Less Secure):**
    If you don’t want to change ownership, make the folder readable by others:
    ```bash
    sudo chmod -R o+r /path/to/your/movie/folder
    ```

- **Ensure Directory Access:**
  The directory itself needs execute permissions (`x`) for Nginx to access its contents:
  ```bash
  sudo chmod o+x /path/to/your/movie/folder
  ```

- **Check Parent Directories:**
  If `/path/to/your/movie/folder` is within a restricted parent directory (e.g., `/home/user/`), ensure all parent directories up to the root have execute permissions for the Nginx user:
  ```bash
  sudo chmod o+x /path /path/to /path/to/your /path/to/your/movie
  ```

---

### 3. Verify and Troubleshoot
After making these changes, test again by visiting `http://localhost/movies/`. If the 403 error persists:

- **Check the Nginx Error Log:**
  Review the error log for specific details (typically located at `/var/log/nginx/error.log`):
  ```bash
  sudo tail -f /var/log/nginx/error.log
  ```
  Look for messages like “permission denied” or “directory index is forbidden” to pinpoint the issue.

- **Additional Considerations:**
  - **SELinux (if applicable):** On systems like CentOS with SELinux enabled, it might block access. Temporarily set SELinux to permissive mode to test:
    ```bash
    sudo setenforce 0
    ```
    If this resolves the issue, you’ll need to adjust SELinux policies (e.g., using `chcon` or `audit2allow`).
  - **Firewall:** Ensure port 80 is open if accessing from another machine (though unlikely if testing locally via `localhost`).

---

### Final Configuration
Here’s the corrected and complete configuration:

```nginx
server {
    listen 80;
    server_name localhost;
    location /movies/ {
        alias /path/to/your/movie/folder/;
        autoindex on; # Enables directory listing
    }
}
```

- Replace `/path/to/your/movie/folder/` with the actual absolute path to your movie directory.
- Restart Nginx: `sudo systemctl restart nginx`.
- Visit `http://localhost/movies/` to confirm the directory listing works.

By correcting the `alias` directive and ensuring proper file permissions, the 403 Forbidden error should be resolved, allowing you to access your movie folder via Nginx successfully.

---

To fix your Nginx 403 Forbidden error and ensure your single `.mkv` file is accessible, let’s refine the setup based on your situation. You have one `.mkv` file, and you want to know where to save it so the Nginx user can access it. Below, I’ll guide you through the process step-by-step, including choosing an appropriate directory and configuring Nginx.

### Step 1: Choose a Directory for Your `.mkv` File
When deciding where to store your `.mkv` file for Nginx to serve it, consider these factors:
- **Accessibility**: The Nginx user (e.g., `nginx` or `www-data`) needs read access.
- **Conventions**: Web servers typically serve files from standard directories like `/var/www/` or `/srv/www/`.
- **Security**: Avoid placing files in overly permissive or sensitive locations (e.g., `/home/user/` unless necessary).

For your case, since it’s just one `.mkv` file and you’re testing locally (`localhost`), I recommend using `/var/www/html/movies/` as a simple, standard location. Here’s why:
- `/var/www/html/` is a common default web root for Nginx and Apache.
- It’s typically owned by the web server user or group, making permissions easier to manage.
- Adding a `/movies/` subdirectory keeps things organized.

If `/var/www/html/` doesn’t exist or isn’t suitable on your system, alternatives include:
- `/srv/www/movies/` (another standard web directory).
- `/usr/share/nginx/html/movies/` (sometimes the default Nginx document root).

For this example, let’s use `/var/www/html/movies/`.

### Step 2: Set Up the Directory and File
Assuming you’re on a Linux system, follow these steps:

1. **Create the Directory**:
   ```bash
   sudo mkdir -p /var/www/html/movies
   ```

2. **Move Your `.mkv` File**:
   Replace `yourfile.mkv` with the actual name of your file and move it to the directory:
   ```bash
   sudo mv /path/to/yourfile.mkv /var/www/html/movies/yourfile.mkv
   ```

3. **Set Permissions**:
   The Nginx user (commonly `nginx` or `www-data`) needs read access to the file and execute access to the directory. First, identify the Nginx user by checking `/etc/nginx/nginx.conf`:
   ```bash
   grep user /etc/nginx/nginx.conf
   ```
   Look for a line like `user nginx;` or `user www-data;`. If it’s not specified, it might default to `www-data` (Ubuntu/Debian) or `nginx` (CentOS/RHEL).

   Then, adjust ownership:
   ```bash
   sudo chown -R nginx:nginx /var/www/html/movies
   ```
   Replace `nginx` with `www-data` or the actual user if different.

   Ensure proper permissions:
   ```bash
   sudo chmod -R 755 /var/www/html/movies
   ```
   - `755` means the owner (Nginx) has full access, and others (including the web server process) can read and execute (navigate) the directory.

### Step 3: Configure Nginx
Update your Nginx configuration to serve the `.mkv` file from `/var/www/html/movies/`. Here’s a minimal working config:

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /var/www/html/movies/;
        autoindex on; # Enables directory listing if you want to browse files
    }
}
```

- **Notes**:
  - Use `alias` instead of `root` to map `/movies/` directly to `/var/www/html/movies/`.
  - `autoindex on;` is optional. If you disable it (`autoindex off;`), you’ll need to specify the exact file URL (e.g., `http://localhost/movies/yourfile.mkv`) to access it.

Save this config (e.g., in `/etc/nginx/sites-enabled/default` or a custom file like `/etc/nginx/conf.d/movies.conf`), then test and restart Nginx:
```bash
sudo nginx -t  # Test config for syntax errors
sudo systemctl restart nginx  # Apply changes
```

### Step 4: Test Access
- Open your browser and visit:
  - `http://localhost/movies/` (if `autoindex` is on, you’ll see a directory listing with `yourfile.mkv`).
  - `http://localhost/movies/yourfile.mkv` (to directly access the file).
- If it works, the file should either display in the browser (if supported) or prompt a download.

### Step 5: Troubleshoot if Needed
If you still get a 403 error:
1. **Check Permissions**:
   ```bash
   ls -l /var/www/html/movies/
   ```
   Ensure `yourfile.mkv` is readable (e.g., `-rwxr-xr-x` or at least `-rw-r--r--`).

2. **Check Nginx Logs**:
   ```bash
   sudo tail -f /var/log/nginx/error.log
   ```
   Look for clues like “permission denied.”

3. **SELinux (if applicable)**:
   If on a system with SELinux (e.g., CentOS), run:
   ```bash
   sudo setenforce 0  # Temporarily disable
   ```
   Test again. If it works, you’ll need to adjust SELinux contexts:
   ```bash
   sudo chcon -R -t httpd_sys_content_t /var/www/html/movies/
   sudo setenforce 1  # Re-enable SELinux
   ```

### Final Thoughts
By saving your `.mkv` file in `/var/www/html/movies/`, setting the correct permissions, and using the `alias` directive in Nginx, you should resolve the 403 error. This setup is simple and follows web server conventions, making it easy for the Nginx user to access the file. Let me know if you hit any snags!

---

If you get an "invalid user" error with `sudo chown -R nginx:nginx /var/www/movies`, it means the `nginx` user doesn’t exist on your system. This happens because the Nginx process might run under a different user, like `www-data` (common on Debian/Ubuntu) or another default depending on your OS.

### Fix: Identify and Use the Correct User
1. **Check the Nginx User**:
   Look in your Nginx configuration file (usually `/etc/nginx/nginx.conf`):
   ```bash
   grep user /etc/nginx/nginx.conf
   ```
   - If it says `user www-data;`, use `www-data`.
   - If it says `user nginx;`, the `nginx` user should exist (might indicate a misconfiguration).
   - If no `user` directive is found, the default user depends on your system:
     - Ubuntu/Debian: `www-data`
     - CentOS/RHEL: `nginx`
     - Other: Could be `http`, `apache`, or similar.

2. **Alternative: Check Running Process**:
   If the config isn’t clear, see what user Nginx is running as:
   ```bash
   ps aux | grep nginx
   ```
   Look at the first column (e.g., `www-data` or `nginx`) for worker processes.

3. **Apply the Correct User**:
   Assuming it’s `www-data` (common on Ubuntu/Debian), update the command:
   ```bash
   sudo chown -R www-data:www-data /var/www/movies
   ```
   If it’s a different user (e.g., `http`), use:
   ```bash
   sudo chown -R http:http /var/www/movies
   ```

4. **Set Permissions**:
   After fixing ownership, ensure proper permissions:
   ```bash
   sudo chmod -R 755 /var/www/movies
   ```

5. **Restart and Test**:
   ```bash
   sudo systemctl restart nginx
   ```
   Visit `http://localhost/movies/yourfile.mkv`.

### If Still Stuck
If neither `nginx` nor `www-data` works and the process check doesn’t help, let me know your OS (e.g., Ubuntu, CentOS) or the output of `ps aux | grep nginx`, and I’ll pinpoint the exact user for you!

---

If `autoindex on;` is set but `http://localhost/movies/` still isn’t listing files, let’s troubleshoot and fix it step-by-step. Since you’re not seeing the directory listing, it could be a config issue, permissions problem, or something else blocking it. Here’s how to resolve it:

### 1. Verify Your Config
Ensure your Nginx configuration is correct and applied. It should look like this:

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /var/www/movies/;
        autoindex on;
    }
}
```

- **Common Mistakes**:
  - Typo in `alias` path (e.g., `/var/www/movie/` instead of `/var/www/movies/`).
  - `autoindex on;` is in the wrong block or commented out.
  - Config file isn’t being loaded (e.g., saved in the wrong location).

Check where your config is:
- If it’s in `/etc/nginx/sites-enabled/`, ensure it’s linked properly (e.g., `ls -l /etc/nginx/sites-enabled/`).
- If it’s in `/etc/nginx/conf.d/`, ensure it ends in `.conf` (e.g., `movies.conf`).

Test and reload:
```bash
sudo nginx -t
sudo systemctl reload nginx  # Reload instead of restart to avoid downtime
```

### 2. Confirm Files Exist
Check that `/var/www/movies/` has your `.mkv` file:
```bash
ls -l /var/www/movies/
```
- If it’s empty, move your file there:
  ```bash
  sudo mv /path/to/yourfile.mkv /var/www/movies/
  ```
- If it’s not empty, note the file names for testing.

### 3. Check Permissions
Nginx needs read (`r`) and execute (`x`) access to the directory and files. Verify:
```bash
ls -ld /var/www/movies/
ls -l /var/www/movies/
```
- Output should look like:
  ```
  drwxr-xr-x 2 www-data www-data 4096 Mar 15 14:00 /var/www/movies/
  -rw-r--r-- 1 www-data www-data 123456 Mar 15 14:00 yourfile.mkv
  ```
- Fix if needed (replace `www-data` with your Nginx user):
  ```bash
  sudo chown -R www-data:www-data /var/www/movies/
  sudo chmod -R 755 /var/www/movies/
  ```

### 4. Check Logs
Look at the Nginx error log for clues:
```bash
sudo tail -n 20 /var/log/nginx/error.log
```
- **"permission denied"**: Indicates a permissions issue—recheck step 3.
- **"directory index forbidden"**: Suggests `autoindex` isn’t working—double-check the config.
- No relevant errors: Might mean Nginx isn’t hitting the right location block.

### 5. Test Direct Access
Try accessing a specific file:
- Visit `http://localhost/movies/yourfile.mkv`.
- If it works but `/movies/` doesn’t, `autoindex` or the directory setup is the issue.

### 6. Common Fixes
- **Trailing Slash**: Ensure `alias` ends with `/` (`/var/www/movies/`), and test both `http://localhost/movies` and `http://localhost/movies/`.
- **SELinux (if on CentOS/RHEL)**:
  ```bash
  sudo setenforce 0  # Temporarily disable
  ```
  Test again. If it works, apply:
  ```bash
  sudo chcon -R -t httpd_sys_content_t /var/www/movies/
  sudo setenforce 1
  ```
- **Conflicting Location Blocks**: If another `location` block (e.g., `location /`) overrides `/movies/`, move this block higher in the config or make it more specific.

### 7. Minimal Test Config
If it’s still not working, simplify to isolate the issue. Replace your config with:

```nginx
server {
    listen 80;
    server_name localhost;

    location /movies/ {
        alias /var/www/movies/;
        autoindex on;
    }
}
```

Save, test, and reload:
```bash
sudo nginx -t
sudo systemctl reload nginx
```

### What’s Happening?
Tell me:
- What do you see at `http://localhost/movies/` (e.g., 403, 404, blank page)?
- Any errors in `sudo tail -n 20 /var/log/nginx/error.log`?
- Output of `ls -l /var/www/movies/`?

With that, I can pinpoint the exact issue and get your directory listing working!

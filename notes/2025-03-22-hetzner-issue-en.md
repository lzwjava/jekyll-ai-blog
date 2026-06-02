---
audio: false
generated: true
lang: en
layout: post
title: Hetzner API Issue
translated: false
type: note
---

Let’s analyze the error you're encountering and explain what’s happening with your code:

### Error

```
Error creating snapshot for server sg5: cannot perform operation because server is locked (locked, f21b9dc9d1535310)
```

This error comes from the Hetzner Cloud API (via the `hcloud` Python SDK) and indicates that the operation to create a snapshot for the server named `sg5` failed because the server is **locked**. A locked server means that another operation (e.g., a previous snapshot, reboot, or resize) is currently in progress, and the server is temporarily restricted from accepting new operations until that process completes.

### Code Breakdown

Here’s your script with explanations and where the error originates:

```python
from hcloud import Client
import os

# Get the API token from the environment variable
api_token = os.environ.get('HERTZNER_API_KEY')

if not api_token:
    print("Error: HERTZNER_API_KEY environment variable not set.")
    exit(1)

# Create a client instance
client = Client(token=api_token)

def create_snapshot(server):
    try:
        response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
        print(f"Snapshot created for server {server.name} with ID: {response.image.id}")
    except Exception as e:
        print(f"Error creating snapshot for server {server.name}: {e}")

# List all servers
servers = client.servers.get_all()

# Print server details and create snapshots
for server in servers:
    print(f"Server ID: {server.id}")
    print(f"Server Name: {server.name}")
    print(f"Server Status: {server.status}")
    print(f"Server IPv4: {server.public_net.ipv4.ip}")
    print(f"Server IPv6: {server.public_net.ipv6.ip}")
    print(f"Server Type: {server.server_type.name}")
    print(f"Server Location: {server.datacenter.location.name}")
    print("----------------------------------")
    create_snapshot(server)
```

1. **API Token Setup**:
   - The script retrieves the Hetzner API key from an environment variable (`HERTZNER_API_KEY`). If it’s not set, it exits with an error.

2. **Client Initialization**:
   - A `Client` instance is created using the API token to interact with the Hetzner Cloud API.

3. **`create_snapshot` Function**:
   - This function attempts to create a snapshot of a given server using `client.servers.create_image()`.
   - Parameters:
     - `server`: The server object to snapshot.
     - `description`: A name for the snapshot (e.g., `sg5-snapshot`).
     - `type="snapshot"`: Specifies that the image type is a snapshot (as opposed to a backup or ISO).
   - If successful, it prints the snapshot ID; otherwise, it catches and prints any exceptions (like the one you’re seeing).

4. **Server Listing**:
   - `client.servers.get_all()` retrieves a list of all servers associated with your Hetzner account.
   - The script loops through them, prints their details (ID, name, status, IPs, etc.), and calls `create_snapshot()` for each.

5. **Where the Error Occurs**:
   - Inside the `create_snapshot()` function, the `client.servers.create_image()` call fails for server `sg5` because it’s locked. The exception message (`cannot perform operation because server is locked`) is raised by the `hcloud` library based on the API response.

### Why Is the Server Locked?

A server becomes locked when an operation is already in progress. Common reasons include:

- Another snapshot is being created.
- The server is being rebooted, resized, or rebuilt.
- A previous operation hasn’t completed yet.

The lock ID (`f21b9dc9d1535310`) in the error message is a unique identifier for the ongoing action locking the server.

### How to Fix It

Here are steps to resolve the issue and improve your script:

#### 1. **Check for Locked Status Before Proceeding**

Modify the script to skip snapshot creation if the server is locked. You can check the server’s current actions using `client.actions.get_all()` or wait for the lock to clear.

Updated `create_snapshot` function:

```python
def create_snapshot(server):
    try:
        # Check if the server is locked by looking at its actions
        actions = client.actions.get_all(server=server)
        for action in actions:
            if action.status == "running":
                print(f"Skipping snapshot for {server.name}: Server is locked by action {action.id}")
                return
        # If no running actions, proceed with snapshot
        response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
        print(f"Snapshot created for server {server.name} with ID: {response.image.id}")
    except Exception as e:
        print(f"Error creating snapshot for server {server.name}: {e}")
```

#### 2. **Wait for the Lock to Clear**

If you want to wait instead of skipping, you can poll the server’s actions until the lock is gone:

```python
import time

def wait_for_unlock(server):
    while True:
        actions = client.actions.get_all(server=server)
        running = any(action.status == "running" for action in actions)
        if not running:
            break
        print(f"Waiting for server {server.name} to unlock...")
        time.sleep(5)  # Wait 5 seconds before checking again

def create_snapshot(server):
    try:
        wait_for_unlock(server)
        response = client.servers.create_image(server, description=f"{server.name}-snapshot", type="snapshot")
        print(f"Snapshot created for server {server.name} with ID: {response.image.id}")
    except Exception as e:
        print(f"Error creating snapshot for server {server.name}: {e}")
```

#### 3. **Manually Investigate the Lock**

- Use the Hetzner Cloud Console or API to check the status of the action with ID `f21b9dc9d1535310`.
- Example API call (via Python):

  ```python
  action = client.actions.get_by_id("f21b9dc9d1535310")
  print(f"Action Status: {action.status}, Command: {action.command}")
  ```

- If it’s stuck, you may need to contact Hetzner support.

#### 4. **Run the Script Again**

Once the server is no longer locked (action completes or you resolve it manually), rerun the script.

### Additional Notes

- **Rate Limits**: Creating snapshots for many servers in a loop might hit Hetzner’s API rate limits. Add a delay (e.g., `time.sleep(1)`) between requests if needed.
- **Error Handling**: The current script stops at the first error. If you want it to continue for other servers, ensure the exception doesn’t halt the loop (it doesn’t in your case, which is good).

Let me know if you need help implementing any of these fixes or further debugging!

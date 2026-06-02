---
audio: false
generated: true
lang: en
layout: post
title: How Docker Works
translated: false
type: note
---

Let’s dive into how Docker works, focusing on its use of Linux’s filesystem and how it isolates applications from each other.

---

### What is Docker, at its Core?
Docker is a platform that allows you to package, distribute, and run applications inside lightweight, isolated environments called **containers**. Unlike virtual machines (VMs), which include an entire operating system, Docker containers share the host OS kernel and use its features to provide isolation and efficiency.

---

### How Docker Works
Docker leverages several Linux kernel features to create and manage containers:
1. **Namespaces** - For isolation.
2. **Control Groups (cgroups)** - For resource management.
3. **Union Filesystems** - For efficient storage and layering.

Here’s how these pieces come together:

---

#### 1. Linux Namespaces: Isolation Mechanism
Namespaces create isolated "views" of system resources, ensuring that processes in one container don’t interfere with those in another. Key namespaces Docker uses include:

- **PID Namespace**: Each container has its own process ID space. Process ID 1 inside a container is isolated from the host’s PID 1 (usually `init` or `systemd`).
- **Network Namespace**: Containers get their own network stack (IP address, ports, routing tables). This is why two containers can listen on port 8080 without conflict.
- **Mount Namespace**: Each container has its own view of the filesystem, isolated from the host and other containers.
- **UTS Namespace**: Containers can have their own hostname and domain name.
- **IPC Namespace**: Isolates inter-process communication (e.g., shared memory, message queues).
- **User Namespace** (optional): Maps container users to host users, enhancing security.

**Example**: If you run `ps` inside a container, you only see processes within that container’s PID namespace, not the host’s processes.

---

#### 2. Control Groups (cgroups): Resource Limits
Cgroups limit and monitor resource usage (CPU, memory, disk I/O, etc.) for each container. This prevents one container from hogging all system resources and starving others.

- **How it works**: Docker assigns a cgroup to each container. You can set limits like:
  ```bash
  docker run --memory="512m" --cpus="0.5" myapp
  ```
  This restricts the container to 512 MB of RAM and half a CPU core.

- **Isolation**: While namespaces isolate visibility, cgroups isolate resource consumption.

---

#### 3. Union Filesystems: Layered Storage
Docker uses a **union filesystem** (e.g., OverlayFS, AUFS) to manage container images and their filesystems efficiently. This is how it ties into the Linux filesystem:

- **Image Layers**: A Docker image is built from stacked, read-only layers. Each layer represents a set of changes (e.g., installing a package, copying files) defined in your `Dockerfile`.
  - Example: `FROM openjdk:17` is one layer, `COPY app.jar` adds another.
  - Layers are cached and reused, saving disk space and speeding up builds.

- **Container Filesystem**: When you run a container, Docker adds a thin, writable layer on top of the read-only image layers. This is called a **copy-on-write (CoW)** mechanism:
  - Reads come from the image layers.
  - Writes (e.g., log files, temp data) go to the writable layer.
  - If a file in a lower layer is modified, it’s copied to the writable layer first (hence "copy-on-write").

- **Isolation**: Each container gets its own writable layer, so changes in one container don’t affect others, even if they share the same base image.

- **On Disk**: On the host, these layers are stored in `/var/lib/docker` (e.g., `/var/lib/docker/overlay2` for OverlayFS). You don’t interact with this directly—Docker manages it.

---

### How Apps Are Isolated from Each Other
Here’s how the above components work together to isolate applications:

1. **Process Isolation (PID Namespace)**:
   - Each container runs its app as an independent process tree, unaware of other containers or the host.

2. **Network Isolation (Network Namespace)**:
   - Containers have separate network interfaces. Docker’s default "bridge" network assigns each container a unique IP, and NAT handles external communication.
   - Example: Two Spring Boot apps can both bind to port 8080 inside their containers without conflict.

3. **Filesystem Isolation (Mount Namespace + UnionFS)**:
   - Each container sees only its own filesystem, built from the image layers plus its writable layer.
   - If Container A writes to `/tmp`, Container B doesn’t see it.

4. **Resource Isolation (cgroups)**:
   - One app can’t exhaust the host’s CPU or memory and crash another.

5. **Shared Kernel**:
   - Containers share the host’s Linux kernel, but namespaces ensure they don’t step on each other’s toes. Syscalls are filtered or redirected as needed.

---

### Simplified Workflow
1. **Build**: You create an image with a `Dockerfile`, defining the app and its dependencies. Docker stacks these into layers using a union filesystem.
2. **Run**: Docker creates a container by:
   - Setting up namespaces for isolation.
   - Allocating cgroups for resource limits.
   - Mounting the image layers plus a writable layer.
   - Starting your app as the entrypoint (e.g., `java -jar app.jar`).
3. **Cleanup**: When the container stops, the writable layer is discarded (unless saved as a new image with `docker commit`).

---

### Why Linux?
Docker relies on Linux kernel features (namespaces, cgroups, union filesystems) that are deeply integrated into how it operates. On macOS or Windows, Docker runs a lightweight Linux VM (via HyperKit or WSL2) to provide these capabilities, then maps them to the host OS.

---

### Visual Analogy
Think of Docker containers as apartments in a building:
- **Namespaces**: Walls and doors keep tenants separate.
- **Cgroups**: The landlord limits water or electricity per unit.
- **UnionFS**: All apartments share a common blueprint (image layers), but each tenant can decorate their space (writable layer).

---

Does this clarify how Docker works and isolates apps? Let me know if you’d like a deeper dive into any part!

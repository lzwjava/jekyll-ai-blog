---
audio: false
generated: true
lang: en
layout: post
title: Docker vs Kubernetes
translated: false
type: note
---

Docker and Kubernetes are complementary technologies in the container ecosystem, but they serve different purposes. Let’s break down their differences and how they relate.

---

### Docker: Containerization Platform

**What it does**: Docker is a tool for creating, running, and managing individual containers—lightweight, isolated environments that package an application with its dependencies.

#### Key Features

1. **Container Runtime**:
   - Docker uses a runtime (e.g., `containerd` or `runc`) to execute containers based on Linux kernel features like namespaces and cgroups.
   - It’s responsible for the lifecycle of a single container: build, start, stop, etc.

2. **Image Management**:
   - Docker builds images from a `Dockerfile`, which define the app, libraries, and configs.
   - Images are stored in registries (e.g., Docker Hub) and run as containers.

3. **Single-Host Focus**:
   - Docker excels at managing containers on one machine. You can run multiple containers, but orchestration across multiple hosts isn’t built-in.

4. **CLI-Driven**:
   - Commands like `docker build`, `docker run`, and `docker ps` let you interact with containers directly.

#### Use Case

- Running a single Spring Boot app on your laptop or a server:

  ```bash
  docker run -p 8080:8080 myapp:latest
  ```

#### Limitations

- No native multi-host support.
- No automatic scaling, self-healing, or load balancing.
- Managing many containers manually gets messy.

---

### Kubernetes: Container Orchestration System

**What it does**: Kubernetes (often abbreviated as K8s) is a platform for managing and orchestrating multiple containers across a cluster of machines. It automates deployment, scaling, and operation of containerized apps.

#### Key Features

1. **Cluster Management**:
   - Kubernetes runs on a cluster of nodes (physical or virtual machines). One node is the "control plane" (managing the cluster), and others are "worker nodes" (running containers).

2. **Orchestration**:
   - **Scheduling**: Decides which node runs each container based on resources and constraints.
   - **Scaling**: Automatically increases or decreases the number of container instances (e.g., based on CPU usage).
   - **Self-Healing**: Restarts failed containers, reschedules them if a node dies, and ensures the desired state is maintained.
   - **Load Balancing**: Distributes traffic across multiple container instances.

3. **Abstraction Layer**:
   - Uses "Pods" as the smallest unit—a Pod can contain one or more containers (usually one) that share storage and network resources.
   - Managed via declarative YAML files (e.g., defining deployments, services).

4. **Multi-Host Focus**:
   - Designed for distributed systems, coordinating containers across many machines.

5. **Ecosystem**:
   - Includes features like service discovery, persistent storage, secrets management, and rolling updates.

#### Use Case

- Deploying a microservices app with 10 services, each in its own container, across 5 servers, with automatic scaling and failover:

  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: myapp
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: myapp
    template:
      metadata:
        labels:
          app: myapp
      spec:
        containers:
        - name: myapp
          image: myapp:latest
          ports:
          - containerPort: 8080
  ```

#### Limitations

- Steeper learning curve.
- Overkill for simple, single-container apps on one machine.

---

### Key Differences

| Aspect                | Docker                              | Kubernetes                          |
|-----------------------|-------------------------------------|-------------------------------------|
| **Purpose**           | Container creation and runtime      | Container orchestration             |
| **Scope**             | Single host                         | Cluster of hosts                    |
| **Unit**              | Container                           | Pod (group of 1+ containers)        |
| **Scaling**           | Manual (e.g., `docker run` multiple times) | Automatic (via replicas)            |
| **Networking**        | Basic (bridge, host, overlay)       | Advanced (services, ingress)        |
| **Self-Healing**      | None (manual restart)               | Built-in (restarts, reschedules)    |
| **Management**        | CLI or Docker Compose for small setups | YAML configs, `kubectl` CLI         |
| **Dependencies**      | Standalone (needs Docker Engine)    | Needs a container runtime (e.g., Docker) |

---

### How They Work Together

- **Docker as the Runtime**: Kubernetes doesn’t run containers directly—it relies on a container runtime like Docker (or alternatives like `containerd`) to start and manage individual containers within Pods.
- **Workflow**:
  1. You build a Docker image (`docker build -t myapp:latest .`).
  2. Push it to a registry (`docker push myapp:latest`).
  3. Kubernetes pulls the image and deploys it across the cluster based on your YAML config (`kubectl apply -f deployment.yaml`).

- **Example**: Kubernetes might use Docker to run three instances of `myapp:latest` on different nodes, exposing them via a load-balanced service.

---

### Analogy

- **Docker**: A chef cooking a single dish in a kitchen. You tell the chef what to make (`Dockerfile`) and how to serve it (`docker run`).
- **Kubernetes**: A restaurant manager overseeing multiple chefs (Docker instances) across many kitchens (nodes). The manager ensures dishes are prepared on time, scales up staff during rush hour, and replaces a chef who gets sick.

---

### When to Use Which?

- **Docker Alone**: For development, testing, or simple apps on one machine (e.g., a single Spring Boot app).
- **Kubernetes**: For production-grade, distributed apps needing high availability, scaling, and resilience (e.g., a microservices architecture).

---

Does this clarify the distinction? Let me know if you’d like to explore a specific aspect—like setting up Kubernetes or comparing it to Docker Compose!

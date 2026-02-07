---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-haiku
title: Docker CLI Commands Quick Guide
translated: false
type: note
---

Docker is controlled through the command-line interface with this basic structure:

```
docker [GLOBAL OPTIONS] COMMAND [COMMAND OPTIONS] [ARGUMENTS]
```

## Global Options

These apply to all Docker commands:

- `--config string` - Location of client config files (default: ~/.docker)
- `--context string` - Name of the context to use
- `--debug` - Enable debug mode
- `--host, -H string` - Daemon socket to connect to
- `--log-level string` - Set logging level (debug, info, warn, error, fatal)
- `--version, -v` - Print version information

For help on any command, use `docker COMMAND --help`.

## Container Commands

**docker run** creates and starts a container. Key options include `-d` (detach/background), `--name` (assign name), `-p` (publish ports), `-v` (mount volumes), `-e` (environment variables), `-w` (working directory), `--rm` (auto-remove on exit), `-it` (interactive terminal), and resource limits like `--memory` and `--cpus`. Example: `docker run -d --name web -p 8080:80 nginx`.

**docker ps** lists containers. Use `-a` to show all (running and stopped), `-q` for just IDs, `-s` for sizes, and `--filter` to filter by status or other conditions.

**docker exec** runs commands in running containers. Use `-it` for interactive mode: `docker exec -it container_name bash`.

**docker stop** gracefully stops containers with `-t` specifying timeout seconds before force killing.

**docker start** restarts stopped containers.

**docker rm** removes containers (use `-f` to force remove running ones, `-v` to also remove volumes).

**docker logs** displays container output. Use `-f` to follow logs in real-time, `--tail` to limit lines, and `-t` for timestamps.

## Image Commands

**docker build** creates images from Dockerfiles. Essential options: `-t` (tag the image), `-f` (specify Dockerfile path), `--build-arg` (pass build variables), `--no-cache` (skip cache), `--target` (build specific stage). Example: `docker build -t myapp:1.0 .`.

**docker images** lists available images. Use `-a` for all including intermediate images, `-q` for just IDs, and `--filter` to filter results.

**docker pull** downloads images from registries: `docker pull ubuntu:20.04`.

**docker push** uploads images to registries: `docker push myregistry.com/myapp:latest`.

**docker tag** creates image aliases or tags: `docker tag myapp:latest myregistry.com/myapp:v1.0`.

**docker rmi** removes images (use `-f` to force removal).

## Volume Commands

**docker volume create** creates named volumes: `docker volume create mydata`.

**docker volume ls** lists all volumes.

**docker volume inspect** shows detailed volume information.

**docker volume rm** deletes volumes.

## Network Commands

**docker network create** creates networks with `-d` specifying driver type (bridge, host, overlay, macvlan): `docker network create mynet`.

**docker network ls** lists networks.

**docker network inspect** shows network details.

**docker network rm** removes networks.

## System Commands

**docker info** displays system-wide information about Docker.

**docker version** shows Docker version details.

**docker stats** displays live container resource usage (CPU, memory, network I/O).

**docker system prune** removes unused images, containers, and volumes (use `-a` to include dangling images, `-f` to skip confirmation).

**docker top** shows running processes in a container.

**docker inspect** displays detailed JSON configuration of containers or images.

## Key Patterns and Tips

Many commands use consistent syntax: listing commands (`docker ps`, `docker images`) support `-q` for quiet output and `--filter` for filtering. Removal commands (`docker rm`, `docker rmi`) use `-f` to force. Interactive commands accept `-it` for interactive terminal mode. You can pass multiple items to most commands: `docker stop container1 container2 container3`.

Common filter examples: `--filter "status=exited"` for containers, `--filter "dangling=true"` for images, `--filter "driver=bridge"` for networks.

Port publishing with `-p` uses `HOST:CONTAINER` format (e.g., `-p 8080:80` maps host port 8080 to container port 80). Volume mounting with `-v` uses `HOST:CONTAINER` or `VOLUME:CONTAINER` syntax.

Use `docker COMMAND --help` liberally—it's the fastest way to see all available options for any command.
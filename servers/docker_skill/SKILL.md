---
name: docker_skill
description: Interact with Docker via the Docker CLI.
allowed-tools:
  - docker_ps
  - docker_images
  - docker_run
  - docker_stop
  - docker_logs
---

# Docker Skill

This skill enables the agent to run Docker commands (requires Docker installed and the `docker` CLI in PATH).

## Tools

### docker_ps
List running containers (or all containers).
- `all`: If True, show all containers (including stopped). Default False.

### docker_images
List available Docker images.

### docker_run
Run a Docker container.
- `image`: Docker image name (e.g., 'nginx:latest').
- `command`: Optional command to run inside the container (string).
- `ports`: Optional port mapping dict, e.g. {'80/tcp': 8080}.
- `volumes`: Optional volume mapping dict, e.g. {'/host/path': '/container/path'}.
- `detach`: If True, run container in background. Default False.
- `environment`: Optional dict of environment variables.
- `name`: Optional container name.

### docker_stop
Stop a running container.
- `container_id`: Container ID or name.

### docker_logs
Fetch logs of a container.
- `container_id`: Container ID or name.
- `tail`: Number of lines to show from the end. Default 10.

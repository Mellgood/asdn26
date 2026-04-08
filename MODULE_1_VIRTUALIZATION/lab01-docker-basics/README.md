# Lab 01 — Docker Basics

## 🎯 Objective

Get comfortable with the Docker CLI. By the end of this lab you will be able to pull images, run containers in both interactive and detached mode, map ports, inspect container state, and manage the container lifecycle.

## 📖 Background

### What Is Virtualization?

Virtualization is the creation of a virtual (rather than physical) version of a computing resource — such as a server, network, or storage device. There are two main approaches:

| Type | How it works | Examples |
|------|-------------|----------|
| **Hardware-level** (hypervisor) | A hypervisor runs on bare metal or on a host OS and creates full virtual machines, each with its own kernel | VMware ESXi, KVM, VirtualBox |
| **OS-level** (containers) | The host kernel is shared; isolation is achieved through kernel features (namespaces, cgroups) | Docker, LXC, Podman |

### Why Containers?

Containers are **lightweight** and **fast** compared to virtual machines because they share the host kernel. They are ideal for:

- Packaging applications with their dependencies
- Creating reproducible environments
- **Simulating network topologies** (the focus of this course!)

### Docker Architecture

```
┌──────────────────────────────────────────────────┐
│                   Docker Client                  │
│              (docker CLI commands)                │
└──────────────────┬───────────────────────────────┘
                   │ REST API
┌──────────────────▼───────────────────────────────┐
│                 Docker Daemon (dockerd)           │
│  ┌─────────┐  ┌─────────┐  ┌──────────────────┐ │
│  │ Images  │  │Containers│  │ Networks/Volumes │ │
│  └─────────┘  └─────────┘  └──────────────────┘ │
└──────────────────────────────────────────────────┘
                   │
          ┌────────▼─────────┐
          │  Container       │
          │  Registry        │
          │  (Docker Hub)    │
          └──────────────────┘
```

Key concepts:

- **Image**: A read-only template containing the application and its dependencies (like a "class" in OOP)
- **Container**: A running instance of an image (like an "object" in OOP)
- **Registry**: A repository for storing and distributing images (Docker Hub is the default public registry)

---

## 🔬 Tasks

### Task 1 — Verify Your Docker Installation

Run the following commands and observe the output:

```bash
docker version
```

You should see both **Client** and **Server** (Engine) version information. If you see an error about the Docker daemon, make sure Docker Desktop is running (or the `dockerd` service is active on Linux).

```bash
docker info
```

This shows detailed information about your Docker installation: number of containers, images, storage driver, operating system, etc.

> 📝 **Question:** What storage driver does your Docker installation use? What operating system is Docker running on?

---

### Task 2 — Hello World

Run the Docker "hello world" container:

```bash
docker run hello-world
```

Read the output carefully — it describes exactly what happened:

1. The Docker client contacted the Docker daemon
2. The daemon could not find the image locally
3. The daemon pulled it from Docker Hub
4. The daemon created a container from the image
5. The container ran and produced the output
6. The container exited

Now run the same command again. Notice it's faster this time — why?

> 📝 **Question:** Why is the second `docker run hello-world` faster than the first?

---

### Task 3 — Interactive Container

Run an Alpine Linux container in **interactive** mode:

```bash
docker run -it --name my-alpine alpine sh
```

| Flag | Meaning |
|------|---------|
| `-i` | Keep STDIN open (interactive) |
| `-t` | Allocate a pseudo-TTY (terminal) |
| `--name my-alpine` | Give the container a human-readable name |
| `alpine` | The image to use |
| `sh` | The command to run inside the container |

You are now **inside** the container! Explore:

```bash
# Inside the container:
hostname
cat /etc/os-release
ls /
whoami
ps aux
ip addr
```

> 📝 **Question:** How many processes are running inside the container? How does that compare to your host machine?

Notice the filesystem is minimal — there is no `systemd`, no `man` pages, no extra packages. This is because Alpine is a minimal Linux distribution designed for containers.

Type `exit` to leave the container.

---

### Task 4 — Detached Container with Port Mapping

Run an Nginx web server in **detached** mode (background):

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

| Flag | Meaning |
|------|---------|
| `-d` | Run in detached (background) mode |
| `--name my-nginx` | Name the container |
| `-p 8080:80` | Map host port 8080 → container port 80 |
| `nginx` | The image to use |

Now open your browser and navigate to: **http://localhost:8080**

You should see the Nginx welcome page.

> 💡 **How port mapping works:**
> ```
> Host Machine                    Container
> ┌────────────────┐             ┌─────────────────┐
> │ localhost:8080 │────maps────▶│ container-ip:80  │
> └────────────────┘             └─────────────────┘
> ```
> The `-p HOST_PORT:CONTAINER_PORT` flag creates a mapping from a port on your host machine to a port inside the container.

You can also verify from the command line:

```bash
curl http://localhost:8080
```

---

### Task 5 — Container Lifecycle Management

Now let's learn how to manage containers:

#### List running containers

```bash
docker ps
```

You should see `my-nginx` listed. Note the **CONTAINER ID**, **STATUS**, and **PORTS** columns.

#### List ALL containers (including stopped ones)

```bash
docker ps -a
```

You should see `my-alpine` (exited) and `hello-world` instances as well.

#### Stop a container

```bash
docker stop my-nginx
```

Verify it stopped:

```bash
docker ps
docker ps -a
```

The container is still there — it's just stopped. Its filesystem and configuration are preserved.

#### Restart a container

```bash
docker start my-nginx
```

Verify Nginx is accessible again at http://localhost:8080.

#### Remove a container

Containers must be stopped before removal (or use `-f` to force):

```bash
docker stop my-nginx
docker rm my-nginx
```

#### Remove all stopped containers at once

```bash
docker container prune
```

> ⚠️ **Be careful with prune commands** — they cannot be undone!

Clean up all the containers from this lab:

```bash
docker container prune -f
```

---

### Task 6 — Container Inspection

Let's run a new container and inspect it in detail:

```bash
docker run -d --name inspect-me nginx
```

#### Basic inspection

```bash
docker inspect inspect-me
```

This outputs a large JSON document with **all** metadata about the container. Let's extract specific information:

#### Find the container's IP address

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inspect-me
```

#### Find the container's MAC address

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' inspect-me
```

#### Find the container's state

```bash
docker inspect -f '{{.State.Status}}' inspect-me
```

#### Find the container's mapped ports

```bash
docker inspect -f '{{json .NetworkSettings.Ports}}' inspect-me
```

> 📝 **Question:** What IP address was assigned to the container? What network is it on?

> 💡 **Tip:** You can use `docker inspect` with `jq` for more readable output:
> ```bash
> docker inspect inspect-me | jq '.[0].NetworkSettings.Networks'
> ```
> (Install `jq` with `apt install jq` or `brew install jq` if not available.)

---

### Task 7 — Container Logs

View the logs from a container:

```bash
# First, generate some traffic to Nginx
curl http://$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' inspect-me)

# Now view the logs
docker logs inspect-me
```

#### Follow logs in real-time (like `tail -f`)

```bash
docker logs -f inspect-me
```

Open another terminal and send more requests:

```bash
curl http://localhost  # (this will fail unless you mapped ports)
```

Press `Ctrl+C` to stop following the logs.

#### View only the last N lines

```bash
docker logs --tail 5 inspect-me
```

---

### Task 8 — Execute Commands in a Running Container

You can run commands inside a running container using `docker exec`:

```bash
# Run a single command
docker exec inspect-me hostname

# Open an interactive shell
docker exec -it inspect-me bash
```

Inside the container:

```bash
ls /usr/share/nginx/html/
cat /etc/nginx/nginx.conf
apt update && apt install -y iproute2
ip addr
ip route
exit
```

> 📝 **Question:** What is the default gateway of the container? What does it correspond to?

---

## 🧹 Cleanup

Remove all containers created during this lab:

```bash
docker stop inspect-me
docker rm inspect-me
docker container prune -f
```

---

## ✅ Checklist

Before moving to the next lab, make sure you can:

- [ ] Pull an image from Docker Hub
- [ ] Run a container in interactive mode (`-it`)
- [ ] Run a container in detached mode (`-d`)
- [ ] Map ports between host and container (`-p`)
- [ ] List, stop, start, and remove containers
- [ ] Inspect container metadata (IP, state, ports)
- [ ] View container logs
- [ ] Execute commands inside a running container (`docker exec`)

---

## 📚 Further Reading

- [Docker Overview](https://docs.docker.com/get-started/overview/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)
- [Docker Networking Overview](https://docs.docker.com/network/) (preview for Lab 03)

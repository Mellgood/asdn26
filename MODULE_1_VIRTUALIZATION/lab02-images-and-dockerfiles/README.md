# Lab 02 — Images and Dockerfiles

## 🎯 Objective

Understand how Docker images are built, layered, and managed. Write Dockerfiles to create custom images — including a **`net-tools`** image that will be the foundation for all networking exercises in the rest of this module.

## 📖 Background

### Docker Images and Layers

A Docker image is built from a series of **layers**. Each instruction in a Dockerfile creates a new layer on top of the previous one:

```
┌──────────────────────────────┐
│  CMD ["python", "app.py"]    │  Layer 4 (metadata only)
├──────────────────────────────┤
│  COPY app.py /app/           │  Layer 3 (~1 KB)
├──────────────────────────────┤
│  RUN pip install flask       │  Layer 2 (~15 MB)
├──────────────────────────────┤
│  FROM python:3.11-slim       │  Layer 1 (base, ~120 MB)
└──────────────────────────────┘
```

Key properties of layers:

- **Read-only**: Once created, layers never change
- **Shared**: If two images use the same base, they share those base layers on disk
- **Cached**: Docker reuses cached layers when rebuilding, making builds faster
- **Union filesystem**: The container sees a single merged filesystem

### Dockerfile Instructions

| Instruction | Purpose | Example |
|------------|---------|---------|
| `FROM` | Base image to build upon | `FROM ubuntu:22.04` |
| `RUN` | Execute a command during build | `RUN apt-get update && apt-get install -y curl` |
| `COPY` | Copy files from build context into the image | `COPY app.py /app/app.py` |
| `ADD` | Like COPY, but can also extract archives and fetch URLs | `ADD config.tar.gz /etc/` |
| `WORKDIR` | Set the working directory for subsequent instructions | `WORKDIR /app` |
| `EXPOSE` | Document which port the container listens on | `EXPOSE 8080` |
| `ENV` | Set environment variables | `ENV APP_ENV=production` |
| `CMD` | Default command to run when the container starts | `CMD ["python", "app.py"]` |
| `ENTRYPOINT` | Like CMD, but harder to override (used for "executable" containers) | `ENTRYPOINT ["nginx", "-g", "daemon off;"]` |

### Build Context

When you run `docker build`, Docker sends the **build context** (the directory you specify) to the Docker daemon. This is why:

- You should keep the build context small (use `.dockerignore`)
- `COPY` paths are relative to the build context, not your filesystem

---

## 🔬 Tasks

### Task 1 — Explore Image Layers

Let's examine how images are structured:

```bash
# Pull the Nginx image
docker pull nginx

# View its layers
docker history nginx
```

> 📝 **Question:** How many layers does the `nginx` image have? Can you identify which Dockerfile instruction created each layer?

Now compare with the Alpine image:

```bash
docker pull alpine
docker history alpine
```

> 📝 **Question:** Why does Alpine have so few layers compared to Nginx?

#### Inspect image metadata

```bash
docker inspect nginx | jq '.[0].Config'
```

This shows the default command (`Cmd`), exposed ports, environment variables, and more.

---

### Task 2 — Build a Simple Python Web Server

In this directory you'll find a starter application:

```
lab02-images-and-dockerfiles/
├── app/
│   ├── app.py              # A simple Python web server
│   └── requirements.txt    # Python dependencies  
└── Dockerfile.app          # 👈 You need to complete this!
```

#### Step 1: Examine the starter files

Read `app/app.py` — it's a simple Python HTTP server that responds with information about the container (hostname, IP address).

Read `app/requirements.txt` — it lists the Python package `flask`.

#### Step 2: Complete the Dockerfile

Open `Dockerfile.app` and complete the missing parts. The comments guide you through what each instruction should do.

#### Step 3: Build the image

```bash
docker build -t asdn-webapp -f Dockerfile.app .
```

| Flag | Meaning |
|------|---------|
| `-t asdn-webapp` | Tag (name) for the image |
| `-f Dockerfile.app` | Which Dockerfile to use |
| `.` | Build context (current directory) |

#### Step 4: Run and test

```bash
docker run -d --name webapp -p 5000:5000 asdn-webapp
curl http://localhost:5000
```

You should see a JSON response with the container's hostname and IP address.

#### Step 5: Observe build caching

Rebuild the image without changing anything:

```bash
docker build -t asdn-webapp -f Dockerfile.app .
```

Notice how Docker says `CACHED` for each layer. Now modify `app/app.py` (e.g., change the welcome message) and rebuild.

> 📝 **Question:** Which layers were rebuilt? Which were cached? Why?

Clean up:

```bash
docker stop webapp && docker rm webapp
```

---

### Task 3 — Build the `net-tools` Image ⭐

**This is the most important task in this lab.** You will build a custom image packed with networking tools that you'll use in every subsequent lab.

In this directory you'll find:

```
lab02-images-and-dockerfiles/
├── net-tools/
│   └── Dockerfile          # 👈 You need to complete this!
```

#### Requirements

The `net-tools` image must:

1. Be based on `ubuntu:22.04`
2. Install the following packages:
   - `iproute2` — the `ip` command for managing interfaces, routes, etc.
   - `iputils-ping` — the `ping` command
   - `traceroute` — trace the path packets take
   - `tcpdump` — capture and analyze network traffic
   - `curl` — transfer data from/to servers
   - `wget` — download files
   - `dnsutils` — DNS tools (`dig`, `nslookup`)
   - `netcat-openbsd` — the `nc` command for testing TCP/UDP connections
   - `iptables` — firewall configuration (used in Lab 06)
   - `net-tools` — classic tools (`ifconfig`, `netstat`, etc.)
   - `nmap` — network scanning
   - `vim` — text editor (for editing configs inside containers)
3. Set the default command to `bash`

#### Step 1: Complete the Dockerfile

Open `net-tools/Dockerfile` and fill in the missing instructions. Keep these best practices in mind:

- **Combine `RUN` commands** with `&&` to reduce the number of layers
- **Clean up apt cache** after installing (`rm -rf /var/lib/apt/lists/*`) to reduce image size
- **Use `DEBIAN_FRONTEND=noninteractive`** to prevent interactive prompts during build

#### Step 2: Build the image

```bash
docker build -t net-tools -f net-tools/Dockerfile net-tools/
```

#### Step 3: Verify the image

```bash
docker run -it --rm net-tools

# Inside the container, verify all tools are available:
ip addr
ping -c 1 8.8.8.8
traceroute --version
tcpdump --version
curl --version
dig google.com
nc -h
iptables --version
nmap --version
```

> 💡 The `--rm` flag automatically removes the container when it exits. Useful for throwaway containers!

#### Step 4: Check the image size

```bash
docker images net-tools
```

> 📝 **Question:** How large is your `net-tools` image? How does it compare to the base `ubuntu:22.04` image? Where does the extra size come from?

---

### Task 4 — Image Management

#### List all images on your system

```bash
docker images
```

#### Tag an image with a version

```bash
docker tag net-tools net-tools:v1.0
docker images net-tools
```

Now you have both `net-tools:latest` and `net-tools:v1.0` — they point to the same image (same IMAGE ID).

#### Remove unused images

```bash
# Remove a specific image
docker rmi asdn-webapp

# Remove ALL unused images (dangling + unreferenced)
docker image prune -a
```

> ⚠️ **Don't remove `net-tools`** — you'll need it for every subsequent lab!

---

### Task 5 — The `.dockerignore` File

When you run `docker build`, the entire build context is sent to the Docker daemon. For large projects, this can be slow.

Create a `.dockerignore` file in this directory:

```
# .dockerignore
*.md
.git
.gitignore
__pycache__
*.pyc
```

Rebuild and observe the "Sending build context" step — it should be faster with fewer files sent.

---

## 🧹 Cleanup

```bash
# Remove test containers
docker container prune -f

# Keep the net-tools image! Remove others if desired:
docker rmi asdn-webapp 2>/dev/null
```

---

## ✅ Checklist

Before moving to the next lab, make sure you:

- [ ] Understand how image layers work and why they matter
- [ ] Can write a Dockerfile from scratch
- [ ] Have built and tested the **`net-tools`** image
- [ ] Know how to tag and manage images
- [ ] Understand build context and `.dockerignore`

> ⚠️ **Important:** The `net-tools` image built in this lab will be used in **every** subsequent lab. Make sure it's working correctly!

---

## 📚 Further Reading

- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/) (advanced)

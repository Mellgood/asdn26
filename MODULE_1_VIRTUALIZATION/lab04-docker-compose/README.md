# Lab 04 — Docker Compose & Multi-Container

## 🎯 Objective

Learn how to orchestrate multi-container applications using Docker Compose. By the end of this lab, you will be able to define services, create custom isolated networks, allocate static IP addresses, and manage the lifecycle of an entire application stack with a single command.

## 📖 Background

### What is Docker Compose?

Docker Compose is a tool for defining and running multi-container Docker applications. Instead of typing long `docker run` commands for each container, you define your entire stack in a single YAML file (`docker-compose.yml`).

Compose is exceptional for:
- Defining complex network topologies
- Creating reproducible development environments
- Managing dependencies between services

### The `docker-compose.yml` File

The Compose file is structured into three main blocks for this course:

1. **`services`**: Defines the containers to run (web server, database, router, etc.)
2. **`networks`**: Defines custom networks and their subnets
3. **`volumes`**: Defines persistent storage (not heavily used in networking labs)

---

## 🔬 Tasks

### Task 1 — Analyze the Starter Application

In this directory, you will find a simple two-tier application:

```
lab04-docker-compose/
├── docker-compose.yml     # 👈 The file you need to complete
├── README.md
├── frontend/
│   └── index.html         # A basic web page
└── init.sql               # Database initialization script
```

The goal is to deploy an `nginx` web server (frontend) and a `postgres` database (backend) running on distinct virtual networks.

### Task 2 — Complete the `docker-compose.yml`

Open the `docker-compose.yml` file and fill in the missing `TODO` sections.

**Network Requirements:**
1. Create a `frontend-net` network with subnet `172.30.1.0/24`.
2. Create a `backend-net` network with subnet `172.30.2.0/24`.

**Service Requirements:**
1. **`webapp`** service:
   - Use the `nginx:alpine` image.
   - Connect it to *both* `frontend-net` and `backend-net`.
   - Map host port 8080 to container port 80.
   - Mount `./frontend` to `/usr/share/nginx/html`.
2. **`database`** service:
   - Use the `postgres:15-alpine` image.
   - Connect it *only* to `backend-net`.
   - Give it a static IP of `172.30.2.10`.
   - Set the `POSTGRES_PASSWORD` environment variable to `secret`.
   - Mount `./init.sql` to `/docker-entrypoint-initdb.d/init.sql`.

### Task 3 — Bring Up the Stack

Once you have completed the file, start the stack in detached mode:

```bash
docker compose up -d
```

Verify that both containers are running:

```bash
docker compose ps
```

Open a browser and navigate to **http://localhost:8080**. You should see the welcome page.

> 📝 **Question:** If you modify `frontend/index.html` on your host and refresh the browser, does it update immediately? Why or why not?

### Task 4 — Verify Network Isolation

The architecture you built looks like this:

```
      Host (8080)
           │
           ▼
    ┌───────────┐         ┌───────────┐
    │  webapp   │         │ database  │
    └────┬───┬──┘         └─────┬─────┘
         │   │                  │
         │   └──────────────────┤
         │                      │
   frontend-net            backend-net
 (172.30.1.0/24)         (172.30.2.0/24)
```

Let's test this isolation. To do so, we need to run a temporary container with networking tools.

#### 1. Test from `webapp` to `database`

The webapp is connected to both networks. It should be able to reach the database.

```bash
docker compose exec webapp ping -c 3 database
```

✅ This should work! Compose automatically configures DNS resolution for service names.

#### 2. Test isolation from a new container

Run a new container attached *only* to `frontend-net`:

```bash
docker run --rm -it --network lab04-docker-compose_frontend-net net-tools bash
```
> *Note: Compose prepends the folder name (`lab04-docker-compose_`) to network names. Check `docker network ls` if uncertain.*

Inside this test container:

```bash
# Ping the webapp
ping -c 2 webapp

# Ping the database by name
ping -c 2 database

# Ping the database by its static IP
ping -c 2 172.30.2.10
```

❌ The pings to the database should fail. 

> 📝 **Question:** Why can't the test container reach the database? Explain in terms of routing and network boundaries.

Exit the container.

---

### Task 5 — Scaling Services

Compose makes it easy to scale stateless services.

```bash
docker compose up -d --scale webapp=3
```

Wait, this command might fail! Look at the error message.

> 📝 **Question:** Why does scaling the `webapp` service fail? How could you modify the `docker-compose.yml` to allow scaling?

### Task 6 — Teardown

To stop and remove all containers, networks, and volumes defined in the Compose file:

```bash
docker compose down
```

Verify everything is clean:

```bash
docker compose ps
docker network ls | grep lab04
```

---

## ✅ Checklist

- [ ] Complete the `docker-compose.yml`
- [ ] Understand the difference between `depends_on` and network routing
- [ ] Bring up and tear down a full stack
- [ ] Verify network isolation across different Compose networks

---

## 📚 Further Reading
- [Docker Compose Overview](https://docs.docker.com/compose/)
- [Compose Networking](https://docs.docker.com/compose/networking/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)

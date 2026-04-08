# Lab 04 — Docker Compose

## Task 3
> **If you modify frontend/index.html on your host and refresh the browser, does it update immediately? Why or why not?**
Yes, it updates immediately. This is because the volume is mounted as a bind mount (`./frontend`), mapping the host directory directly into the container's file system in real-time.

## Task 4
> **Why can't the test container reach the database? Explain in terms of routing and network boundaries.**
The test container is only connected to `frontend-net`. The database container is only connected to `backend-net`. Docker Compose creates separate bridge interfaces on the host for each network and configures `iptables` to block forwarding between them. 

## Task 5
> **Why does scaling the webapp service fail? How could you modify the docker-compose.yml to allow scaling?**
It fails because `webapp` has a hardcoded host port mapping (`8080:80`). Only one container can bind to port 8080 on the host. To fix it, you either remove the host port entirely (`ports: - "80"`, Docker will pick random host ports) or use a reverse proxy/load balancer container in front of them.

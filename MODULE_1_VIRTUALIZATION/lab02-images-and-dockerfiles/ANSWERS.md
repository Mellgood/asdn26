# Lab 02 — Images and Dockerfiles: Answers

## Task 1 — Explore Image Layers

> **How many layers does the `nginx` image have?**

Typically around 5-7 layers (it varies by version). Each layer corresponds to a Dockerfile instruction.

> **Why does Alpine have so few layers compared to Nginx?**

Alpine is a minimal base image — its Dockerfile is extremely simple (essentially just `ADD` the root filesystem). Nginx builds on top of a base image and adds multiple `RUN` steps to install and configure the web server.

---

## Task 2 — Build Observation

> **Which layers were rebuilt? Which were cached? Why?**

Only the layers **after** the `COPY app.py` instruction were rebuilt. The `FROM`, `WORKDIR`, `COPY requirements.txt`, and `RUN pip install` layers were all cached because their inputs didn't change. This is why we copy `requirements.txt` and install dependencies **before** copying the application code — so dependency installation is cached even when code changes.

---

## Task 3 — Image Size

> **How large is your `net-tools` image?**

Approximately 350-450 MB, compared to ~77 MB for the base `ubuntu:22.04`. The extra size comes from all the installed networking packages and their dependencies.

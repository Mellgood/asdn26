# ASDN — Advanced and Software Defined Networks

## 📚 Course Lab Exercises

Welcome to the hands-on lab repository for the **ASDN (Advanced and Software Defined Networks)** course. This repository contains a series of guided exercises designed to give you practical experience with the technologies and concepts covered in the course.

## 🗂️ Modules

| Module | Topic | Description |
|--------|-------|-------------|
| [Module 1](MODULE_1_VIRTUALIZATION/) | **Virtualization** | Docker fundamentals, container networking, routing, firewalling |
| Module 2 | **SDN** | Software Defined Networking, controllers, Mininet, Kathará *(coming soon)* |
| Module 3 | **O-RAN** | Open Radio Access Network *(coming soon)* |

## 🛠️ Prerequisites

Before starting the labs, make sure you have the following installed on your machine:

- **Docker Engine** (v20.10+) or **Docker Desktop**
- **Docker Compose** (v2.x — included in Docker Desktop)
- A **terminal** (Linux/macOS Terminal, or WSL2 on Windows)
- A **text editor** or IDE (VS Code recommended)

### Verify your setup

```bash
docker --version
docker compose version
```

Both commands should return valid version numbers.

## 📖 How to Use This Repository

### Branches

| Branch | Content |
|--------|---------|
| `main` | Exercise descriptions, starter files, and scaffolding |
| `solutions` | Proposed solutions with detailed comments |

### Workflow

1. **Clone the repository** and stay on the `main` branch
2. **Read the exercise README** carefully — it contains theory, instructions, and tasks
3. **Work through the tasks** on your own, using the provided starter files
4. **Verify your work** using the included verification commands
5. If you get stuck, check the `solutions` branch for reference

```bash
# Clone the repo
git clone <repository-url>
cd asdn26

# Start working on an exercise
cd MODULE_1_VIRTUALIZATION/lab01-docker-basics

# If you need to check a solution
git switch solutions
# ... then switch back
git switch main
```

## 🧭 Recommended Order

Work through the exercises **in order** within each module — they build on each other. Concepts and files from earlier labs are reused in later ones.

## ⚠️ Important Notes

- **Do not skip labs.** Later exercises assume familiarity with concepts from earlier ones.
- **Read the theory sections.** They provide essential context for the practical tasks.
- **Experiment!** The best way to learn is to try variations beyond what is asked.
- **Ask for help** if you are stuck for more than 15 minutes on a single task.

## 📄 License

This material is provided for educational purposes as part of the ASDN course.

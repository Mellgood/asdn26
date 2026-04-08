# Lab 00b — Automated Provisioning with cloud-init

## 🎯 Objective

In Lab 00 you launched a basic Ubuntu Virtual Machine. However, installing software manually on every new Virtual Machine is tedious and prone to human error. In this lab, you will use **cloud-init** to automate the provisioning of your VM. Specifically, you will use it to automatically install **Docker Engine** as the machine boots up.

This concept (Infrastructure as Code) is critical for managing modern, reproducible environments.

## 📖 Background

### What is cloud-init?
`cloud-init` is the industry standard method for cross-platform cloud instance initialization. It is supported across all major cloud providers (AWS, Azure, Google Cloud) as well as local hypervisors (like Multipass).

When you provide a `cloud-init.yaml` file (often called "user data"), the initialization system reads it during the first boot and can:
- Create users and manage SSH keys
- Install packages
- Write files
- Run custom bash commands (`runcmd`)

---

## 🔬 Tasks

### Task 1 — Prepare the Cloud-Init File

In this folder, you have a file named `cloud-init.yaml`. Let's explore and complete it.

1. Open `cloud-init.yaml`.
2. Notice the `#cloud-config` header. This is mandatory; it tells Multipass the file is in YAML format.
3. Look at the `users` section. Here, the `ubuntu` user is being created (or rather, modified since it's the default) and appended to the `docker` group. This ensures you won't need to type `sudo` for every Docker command!
4. Complete the `runcmd` section using the `TODO` comments. You need to use `curl` to grab the official Docker install script, and then execute it with `sh`.

### Task 2 — Launch the VM with cloud-init

Before we launch a new machine, make sure you don't use a name that is already running. We will call this one `docker-node`.

1. Launch the VM using the `--cloud-init` flag:
   ```bash
   multipass launch --name docker-node --cloud-init cloud-init.yaml --cpus 2 --memory 2G --disk 10G
   ```
   *(Wait for the prompt to return. While Multipass says "Launched", cloud-init is still running scripts inside the VM!)*

### Task 3 — Verify the Installation

How do we know when the automated installation finishes? Cloud-init writes its status to a specific file.

1. Tell multipass to execute a command inside the VM to check the cloud-init status:
   ```bash
   multipass exec docker-node -- cloud-init status --wait
   ```
   If it's still installing Docker, it will say `status: running`. Once finished, it will output `status: done`.

2. Once `done`, open a shell into your new machine:
   ```bash
   multipass shell docker-node
   ```

3. Test that Docker was installed successfully, and that you have permission to use it without `sudo`:
   ```bash
   docker run hello-world
   ```
   ✅ **Success!** If you see the welcome message, your VM automatically provisioned itself.

---

## 🧹 Cleanup

Since we won't need `docker-node` for the immediate next labs, let's delete it so it doesn't consume your computer's RAM.

```bash
# Stop and delete the VM
multipass delete docker-node 
multipass purge
```

*(Note: In the future, if you ever corrupt a VM, you now know you can destroy it and instantly spin up a perfectly configured clone in just one command!)*

---

## ✅ Checklist

- [ ] Completed the `runcmd` block in `cloud-init.yaml`
- [ ] Launched a Multipass VM passing the config file
- [ ] Checked `cloud-init status --wait`
- [ ] Verified `docker run` works natively inside the VM without `sudo`

---

## 📚 Further Reading
- [Multipass cloud-init tutorial](https://multipass.run/docs/using-cloud-init-with-multipass)
- [cloud-init Documentation](https://cloudinit.readthedocs.io/en/latest/)

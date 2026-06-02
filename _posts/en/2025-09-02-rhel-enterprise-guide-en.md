---
audio: false
generated: true
image: false
lang: en
layout: post
title: RHEL Complete Enterprise Linux Guide
translated: false
type: note
---

Here’s a **comprehensive guide to Red Hat Enterprise Linux (RHEL)**. I’ll structure it step by step so you can use it as both a learning path and a reference.

---

## 1. Introduction to Red Hat Linux

Red Hat Enterprise Linux (RHEL) is a commercial Linux distribution developed by **Red Hat, Inc.**, designed for **stability, security, and enterprise support**. It is widely used in banking, healthcare, government, and corporate IT because of its long-term support lifecycle and certified software ecosystem.

Key highlights:

* Enterprise-grade support (10+ years lifecycle per major release).
* Certified on major hardware (Dell, HP, IBM, etc.).
* Widely used in cloud (AWS, Azure, GCP), containers (OpenShift, Kubernetes), and virtualization.

---

## 2. Installation and Setup

* **Download**: Official ISO images are available via Red Hat Customer Portal (requires subscription).
* **Installers**: Uses the **Anaconda installer** with graphical and text modes.
* **Partitioning**: Options for LVM, XFS (default filesystem), and encrypted disks.
* **Post-installation tools**: `subscription-manager` for registering the system.

---

## 3. Package Management

* **RPM (Red Hat Package Manager)** – the underlying format for software.
* **DNF (Dandified Yum)** – the default package manager in RHEL 8 and later.

  * Install a package:

    ```bash
    sudo dnf install httpd
    ```
  * Update system:

    ```bash
    sudo dnf update
    ```
  * Search packages:

    ```bash
    sudo dnf search nginx
    ```

RHEL also supports **AppStreams** for multiple versions of software (e.g., Python 3.6 vs 3.9).

---

## 4. System Administration Basics

* **User Management**:
  `useradd`, `passwd`, `usermod`, `/etc/passwd`, `/etc/shadow`
* **Process Management**:
  `ps`, `top`, `htop`, `kill`, `systemctl`
* **Disk Management**:
  `lsblk`, `df -h`, `mount`, `umount`, `fdisk`, `parted`
* **System Services** (systemd):

  ```bash
  systemctl start nginx
  systemctl enable nginx
  systemctl status nginx
  ```

---

## 5. Networking

* Configuration stored in `/etc/sysconfig/network-scripts/`.
* Commands:

  * `nmcli` (NetworkManager CLI)
  * `ip addr`, `ip route`, `ping`, `traceroute`
* Firewall:

  * Managed by **firewalld** (`firewall-cmd`).
  * Example:

    ```bash
    firewall-cmd --add-service=http --permanent
    firewall-cmd --reload
    ```

---

## 6. Security

* **SELinux**: Mandatory access control system.

  * Check status: `sestatus`
  * Modes: enforcing, permissive, disabled
* **FirewallD**: Manages network security.
* **System Updates**: Security patches via `dnf update`.
* **Auditd**: Logging and compliance.

---

## 7. Logging and Monitoring

* **System logs**:
  Stored under `/var/log/`.
* **Journald**:
  `journalctl -xe`
* **Performance tools**:

  * `sar` (sysstat package)
  * `vmstat`, `iostat`, `dstat`
* **Red Hat Insights**: Cloud-based system analysis.

---

## 8. Virtualization and Containers

* **KVM** (Kernel-based Virtual Machine) for virtualization.
* **Podman** (instead of Docker):

  ```bash
  podman run -it centos /bin/bash
  ```
* **OpenShift** (Kubernetes platform) for orchestration.

---

## 9. Storage Management

* **LVM (Logical Volume Manager)** for flexible disk management.
* **XFS**: Default filesystem.
* **Stratis**: Storage management with thin provisioning and snapshots.

---

## 10. Automation and Configuration Management

* **Ansible**: Red Hat’s automation platform.
* **Kickstart**: Automates OS installations.
* **System Roles**: Predefined Ansible roles for RHEL.

---

## 11. Subscriptions and Support

* Red Hat uses a **subscription model**.
* `subscription-manager` to register, attach subscriptions, and enable repositories.
* RHEL developer subscription is **free for individuals**.

---

## 12. Best Practices

* Always keep systems updated with security patches.
* Use SELinux in enforcing mode unless debugging.
* Centralize logging with `rsyslog` or ELK stack.
* Automate repetitive tasks with Ansible.
* Monitor system health with Red Hat Insights.

---

## 13. Learning Resources

* [Red Hat Documentation](https://access.redhat.com/documentation)
* [Red Hat Academy](https://www.redhat.com/en/services/training-and-certification/red-hat-academy)
* Certifications:

  * **RHCSA** (Red Hat Certified System Administrator)
  * **RHCE** (Red Hat Certified Engineer)
  * **RHCA** (Red Hat Certified Architect)

---

✅ That’s the foundation.
Would you like me to **expand this into a practical “hands-on guide”** with real-world commands and workflows (like setting up a web server, database, firewall, etc.), or keep it more **theoretical and conceptual**?

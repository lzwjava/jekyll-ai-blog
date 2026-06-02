---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Automation Guide
translated: false
type: note
---

## What is Ansible?

Ansible is an **open-source automation tool** that automates:

- Configuration management
- Application deployment
- Task automation/orchestration
- Cloud provisioning

It is **agentless** (no software/agent needed on managed nodes), uses **SSH** (or WinRM for Windows), and is written in **YAML** (human-readable format).
Ansible is part of Red Hat and is one of the most popular DevOps tools today.

### Key Advantages

- Simple & easy to learn (YAML-based)
- Agentless (uses existing SSH)
- Idempotent (running playbook multiple times gives same result)
- Huge module library (> 3000 modules)
- Very active community and Galaxy (public role repository)

## Core Concepts

| Concept         | Description                                                                                 |
|-----------------|---------------------------------------------------------------------------------------------|
| Inventory       | List of managed hosts (IP or hostname). Can be static (ini/yaml) or dynamic.                |
| Playbook        | YAML file containing one or more plays. This is where you write automation.                |
| Play            | Maps a group of hosts to tasks/roles.                                                       |
| Task            | Single action (e.g., install package, copy file, restart service).                         |
| Module          | Reusable code that performs a specific action (package, service, file, template, etc.).    |
| Role            | Reusable directory structure of tasks, variables, templates, handlers, etc.                 |
| Handler         | Special task that runs only when notified by another task (e.g., restart nginx).           |
| Facts           | Information gathered from remote hosts (OS, IP, memory, etc.).                              |
| Variables       | Customize playbooks (host vars, group vars, role vars, extra vars, etc.).                   |

## Installation

### On control node (your laptop/server)

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ansible -y

# RHEL/CentOS/Rocky
sudo dnf install ansible -y

# macOS (with Homebrew)
brew install ansible

# Or use pip (recommended for latest version)
python3 -m pip install --user ansible
```

Check version:

```bash
ansible --version
```

## Inventory

### Simple INI format (`inventory.ini`)

```ini
[webservers]
web1.example.com
web2.example.com ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/mykey.pem

[dbservers]
db1.example.com ansible_host=192.168.1.50

[all:vars]
ansible_python_interpreter=/usr/bin/python3
```

### YAML format (`inventory.yaml`)

```yaml
all:
  hosts:
    localhost:
      ansible_connection: local
  children:
    webservers:
      hosts:
        web1.example.com:
        web2.example.com:
          ansible_user: ubuntu
    dbservers:
      hosts:
        db1.example.com:
```

Test connectivity:

```bash
ansible all -i inventory.ini -m ping
```

## First Ad-Hoc Command Examples

```bash
# Gather facts
ansible webservers -m setup

# Install nginx on all webservers
ansible webservers -m apt -a "name=nginx state=present" --become

# Copy file
ansible webservers -m copy -a "src=/local/file.txt dest=/remote/file.txt"

# Reboot servers
ansible all -m reboot --become
```

## Writing Your First Playbook

Create `first_playbook.yml`:

{% raw %}

```yaml
---
- name: Configure web servers
  hosts: webservers
  become: yes                     # sudo
  vars:
    http_port: 80
    domain: example.com

  tasks:
    - name: Ensure nginx is installed
      apt:
        name: nginx
        state: present
        update_cache: yes

    - name: Copy nginx config file
      template:
        src: templates/nginx.conf.j2
        dest: /etc/nginx/sites-available/{{ domain }}
      notify: Restart nginx

    - name: Enable new site
      file:
        src: /etc/nginx/sites-available/{{ domain }}
        dest: /etc/nginx/sites-enabled/{{ domain }}
        state: link

    - name: Ensure nginx is running
      service:
        name: nginx
        state: started
        enabled: yes

  handlers:
    - name: Restart nginx
      service:
        name: nginx
        state: restarted
```

{% endraw %}

Run it:

```bash
ansible-playbook -i inventory.ini first_playbook.yml
```

## Common & Useful Modules

| Category       | Modules                                      | Example Use                                  |
|----------------|----------------------------------------------|----------------------------------------------|
| Packages       | apt, yum, dnf, pacman, pip                   | Install software                             |
| Files          | file, copy, template, lineinfile, find      | Manage files/directories                     |
| System         | service, systemd, user, group, reboot        | Manage services, users                       |
| Command        | command, shell, script                       | Run arbitrary commands                      |
| Cloud          | ec2_instance, digital_ocean, azure_rm_*      | Provision cloud resources                    |
| Database       | postgresql_db, mysql_db, mongodb_user        | Manage databases                             |
| Version Control| git                                          | Checkout code                                |
| Facts          | setup                                        | Gather system info                           |

## Variables & Facts

### Variable precedence (highest to lowest)

1. Command line `-e "var=value"`
2. Role defaults
3. Inventory variables
4. Play vars
5. Host facts / gathered facts

### Example using variables

{% raw %}

```yaml
vars:
  app_name: myapp
  app_user: www-data

vars_files:
  - secrets.yml

tasks:
  - name: Create app user
    user:
      name: "{{ app_user }}"
      shell: /bin/bash
```

{% endraw %}

### Using facts

{% raw %}

```yaml
- name: Show OS distribution
  debug:
    msg: "This is {{ ansible_facts['distribution'] }} {{ ansible_facts['distribution_version'] }}"
```

{% endraw %}

## Conditionals & Loops

### When (conditional)

```yaml
tasks:
  - name: Install Apache on RedHat only
    yum:
      name: httpd
      state: present
    when: ansible_facts['os_family'] == "RedHat"
```

### Loops

{% raw %}

```yaml
- name: Create multiple users
  user:
    name: "{{ item }}"
    state: present
  loop:
    - alice
    - bob
    - charlie

- name: Install list of packages
  apt:
    name: "{{ item }}"
    state: present
  loop: "{{ packages }}"
  vars:
    packages:
      - nginx
      - git
      - vim
```

{% endraw %}

## Roles – Best Practice Structure

```
myrole/
├── defaults/
│   └── main.yml
├── vars/
│   └── main.yml
├── tasks/
│   └── main.yml
├── handlers/
│   └── main.yml
├── templates/
│   └── nginx.conf.j2
├── files/
├── meta/
│   └── main.yml
└── README.md
```

Use roles in playbook:

```yaml
- hosts: webservers
  roles:
    - common
    - nginx
    - myapp
```

Find thousands of ready roles:

```bash
ansible-galaxy search postgres
ansible-galaxy install geerlingguy.postgres
```

## Real-World Use Cases

| Use Case                         | Typical Playbook/Role Example                                  |
|----------------------------------|----------------------------------------------------------------|
| Server bootstrapping             | Install base packages, create users, SSH keys, firewall      |
| Web application deployment       | Git checkout → pip install → gunicorn → nginx reverse proxy  |
| Database setup                   | Install PostgreSQL/MySQL → create DB/user → restore dump      |
| Continuous Deployment            | Triggered by webhook → pull latest code → run tests → deploy |
| Cloud provisioning               | Launch EC2 instances, add to load balancer, install app       |
| Security hardening               | CIS benchmark roles, disable root login, update packages      |
| Monitoring setup                 | Install Prometheus/Node exporter, Grafana, Alertmanager       |
| Backup automation                | rsync/dump databases → copy to S3 → cleanup old backups       |
| Multi-environment management     | dev/staging/prod with different variables                    |

## Best Practices

1. Always use roles for reusable code
2. Use `ansible-vault` to encrypt sensitive data

   ```bash
   ansible-vault create secrets.yml
   ansible-playbook site.yml --ask-vault-pass
   ```

3. Use Git to version control your playbooks/roles
4. Use `--check` mode first (dry-run)

   ```bash
   ansible-playbook site.yml --check
   ```

5. Tag your tasks for selective runs

   ```yaml
   tags: ['nginx', 'web']
   ```

   Run: `ansible-playbook site.yml --tags web`
6. Use `pre_tasks` and `post_tasks` when needed
7. Never hardcode passwords – use vault or lookup plugins

## Useful Commands Summary

```bash
ansible all -m ping
ansible all -m setup                    # gather facts
ansible-playbook playbook.yml --check   # dry run
ansible-playbook playbook.yml -t nginx  # run specific tag
ansible-vault encrypt secrets.yml
ansible-galaxy role install geerlingguy.nginx
ansible-galaxy collection install community.docker
```

## Learning Resources

- Official docs: <https://docs.ansible.com>
- Ansible Galaxy: <https://galaxy.ansible.com>
- Awesome roles by Jeff Geerling: <https://github.com/geerlingguy>
- Book: "Ansible for DevOps" by Jeff Geerling

Start small → write ad-hoc commands → simple playbooks → roles → full infrastructure as code.

You now have everything to become productive with Ansible in production environments!

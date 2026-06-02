---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Variables and When Conditional Guide
translated: false
type: note
---

Question: How do I set variables and use the `when` conditional in an Ansible playbook?

Answer:

Here are the most common and recommended ways to set variables and use the `when` clause in modern Ansible playbooks:

### Setting Variables (`vars` or `set_fact`)

{% raw %}
```yaml
---
- hosts: all
  tasks:
    # 1. Set variable at play level
    - name: Define a variable directly in the play
      vars:
        my_app_port: 8080
      debug:
        msg: "Port is {{ my_app_port }}"

    # 2. Set variable at task level
    - name: Set a simple variable
      set_fact:
        environment: production
        app_version: "1.2.3"

    # 3. Set variable conditionally
    - name: Set fact based on OS
      set_fact:
        package_manager: apt
      when: ansible_os_family == "Debian"

    - name: Set fact based on OS (alternative)
      set_fact:
        package_manager: yum
      when: ansible_os_family == "RedHat"

    # 4. Set variable from registered command output
    - name: Check if service is running
      command: systemctl is-active nginx
      register: nginx_status
      ignore_errors: yes

    - name: Set fact from register
      set_fact:
        nginx_running: "{{ nginx_status.rc == 0 }}"
```
{% endraw %}

### Using `when` Conditional

```yaml
    - name: Install Nginx only on Ubuntu
      apt:
        name: nginx
        state: present
      when: ansible_distribution == "Ubuntu"

    - name: Restart Nginx only if it was running before
      service:
        name: nginx
        state: restarted
      when: nginx_running | default(false)

    - name: Complex when conditions
      debug:
        msg: "This runs only on prod servers with app_version > 2.0"
      when:
        - environment == "production"
        - app_version is version("2.0", ">")

    - name: Using OR logic
      debug:
        msg: "Runs on either CentOS or Ubuntu"
      when: ansible_distribution in ["CentOS", "Ubuntu"]

    - name: Skip task with custom fact
      debug:
        msg: "This task is skipped on Windows"
      when: ansible_os_family != "Windows"
```

### Best Practices Summary

| Method           | Scope          | Cacheable | Recommended Use Case                          |
|------------------|----------------|-----------|-----------------------------------------------|
| `vars:` (play)   | Play level     | Yes       | Static configuration values                   |
| `vars:` (task)   | Task level     | Yes       | Small, task-specific values                   |
| `set_fact:`      | Host level     | Yes (if `cacheable: yes`) | Dynamic values, computed during execution     |
| `register:` + `set_fact:` | Host level | Yes       | Store command/output results for later use    |

Use `set_fact` with `cacheable: yes` if you want the variable to persist across plays in the same run.

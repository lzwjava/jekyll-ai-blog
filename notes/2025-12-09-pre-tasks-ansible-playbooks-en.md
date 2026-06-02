---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Using pre_tasks in Ansible Playbooks
translated: false
type: note
---

Question: How do I use pre_tasks in an Ansible playbook?

Answer:

In Ansible playbooks, `pre_tasks` are a list of tasks that execute **before** any roles or regular `tasks` in a play. They are commonly used for initial setup steps such as checking prerequisites, registering variables, updating package caches, or gathering facts conditionally.

### Basic Syntax

```yaml
---
- name: Example playbook demonstrating pre_tasks
  hosts: webservers
  become: yes

  pre_tasks:
    - name: Display a message before everything starts
      debug:
        msg: "This runs as a pre_task"

    - name: Update apt cache (Debian/Ubuntu only)
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Install required package before roles run
      package:
        name: git
        state: present

  roles:
    - common
    - nginx

  tasks:
    - name: Regular tasks run after pre_tasks and roles
      debug:
        msg: "This is a normal task"
```

### Execution Order in a Play

1. `pre_tasks`
2. `roles` (if any)
3. `tasks`
4. `post_tasks` (if any)

### Common Use Cases for pre_tasks

- Updating package manager cache (`apt`, `yum`, `dnf`, etc.)
- Installing dependencies required by roles
- Registering custom facts or variables early
- Performing health checks or fail-fast conditions
- Gathering facts selectively (you can override the default fact gathering)

#### Example: Conditional fact gathering

```yaml
pre_tasks:
  - name: Gather facts only if not already gathered
    setup:
    when: ansible_connection is not defined
```

#### Example: Fail early if a condition is not met

```yaml
pre_tasks:
  - name: Ensure required variable is defined
    assert:
      that: my_required_var is defined
      fail_msg: "my_required_var must be defined when running this playbook"
```

### Important Notes

- Handlers notified in `pre_tasks` will still run at the end of the play (or when flushed), just like normal tasks.
- Variables set or registered in `pre_tasks` are available to roles and regular tasks.
- `pre_tasks` run with the same privilege escalation (`become`) settings as the rest of the play unless overridden per task.

You can also combine `pre_tasks` with `post_tasks` for full control over execution flow.

References:

- [Ansible Playbook Documentation - pre_tasks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#pre-tasks-and-post-tasks)
- [Ansible Playbook Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)

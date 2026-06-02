---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Understanding Ansible Idempotency
translated: false
type: note
---

Yes, you're absolutely correct!

In Ansible, **idempotency** means that running the same playbook multiple times on a system that is already in the desired state should result in **no changes** (i.e., all tasks report `ok` or `skipped`, not `changed`).

However, whether a playbook is truly idempotent **does depend entirely on how it's written**.

### Cases where idempotency is broken (non-idempotent behavior):

You mentioned the classic example — and it's spot-on:

```yaml
- name: Increment a counter (BAD - not idempotent)
  shell: echo $(( $(cat /tmp/counter) + 1 )) > /tmp/counter
```

Every run increases the value → `changed` every time → **not idempotent**.

Other common non-idempotent patterns:
- Using `command` or `shell` without `creates`, `removes`, or proper checks
- Appending to files without checking if the line already exists
- Restarting services unconditionally
- Running `git pull` without specifying a commit/tag/branch that ensures same result

### How to make it idempotent (correct way):

Use declarative modules that check the desired state:

```yaml
- name: Ensure counter is exactly 5 (idempotent)
  copy:
    content: "5\n"
    dest: /tmp/counter

- name: Ensure line exists in file (idempotent)
  lineinfile:
    path: /etc/myconfig.conf
    line: "debug = true"
    state: present

- name: Ensure service is restarted only when needed
  service:
    name: nginx
    state: restarted
  listen: "restart nginx"
  # Only triggered when config actually changed

- name: Ensure latest code from specific commit (idempotent)
  git:
    repo: https://github.com/example/app.git
    dest: /var/www/app
    version: v1.2.3   # pinned → same every time
```

### Summary

- Ansible **modules** are designed to be idempotent (package, service, file, user, template, lineinfile, etc.)
- But raw `command`/`shell` tasks are usually **not** idempotent unless you add proper guards (`creates`, `changed_when`, etc.)
- A playbook is only as idempotent as its least idempotent task

So yes — you're 100% right: **idempotency depends completely on the details of how the playbook and tasks are written**.

Well spotted! This is one of the most common pitfalls when people say "my playbook isn't idempotent" — it's almost always because they used imperative-style shell commands instead of Ansible's declarative modules.

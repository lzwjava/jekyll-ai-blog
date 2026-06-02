---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Quick Ansible Playbook Demo
translated: false
type: note
---

Here’s the simplest possible Ansible playbook demo you can run in under 2 minutes — from zero to “wow, it works!”

### Step 1: Create a project folder
```bash
mkdir ~/ansible-demo
cd ~/ansible-demo
```

### Step 2: Create an inventory file (inventory.ini)
```ini
# inventory.ini
[webservers]
192.168.1.100       # ← change to your real server IP or hostname
localhost           # we also add localhost so you can test without any server

[all:vars]
ansible_user=ubuntu                 # change to your SSH user (ubuntu, ec2-user, centos, root, etc.)
ansible_ssh_private_key_file=~/.ssh/id_rsa   # only needed for real servers
```

If you’re just testing on your own laptop, you only need this one line:
```ini
localhost ansible_connection=local
```

### Step 3: Create the world’s simplest playbook (hello.yml)
{% raw %}
```yaml
# hello.yml
---
- name: My first Ansible playbook
  hosts: all                     # run on every host in inventory
  tasks:

    - name: Ping all hosts (test connection)
      ansible.builtin.ping:

    - name: Show a welcome message
      ansible.builtin.debug:
        msg: "Hello! I am {{ inventory_hostname }} and my OS is {{ ansible_distribution }} {{ ansible_distribution_version }}"

    - name: Update package cache (Debian/Ubuntu only)
      ansible.builtin.apt:
        update_cache: yes
      when: ansible_os_family == "Debian"
      become: yes

    - name: Install nginx on every server
      ansible.builtin.package:
        name: nginx
        state: present
      become: yes

    - name: Make sure nginx is started and enabled
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: yes
```
{% endraw %}

### Step 4: Run the playbook
```bash
# Dry-run first (highly recommended)
ansible-playbook hello.yml -i inventory.ini --check

# Actually run it
ansible-playbook hello.yml -i inventory.ini
```

If you want to be asked for the sudo password (when using become: yes):
```bash
ansible-playbook hello.yml -i inventory.ini --ask-become-pass
```

### Expected output (shortened)
```
PLAY [My first Ansible playbook] ****************************************

TASK [Ping all hosts] ***************************************************
ok: [localhost]
ok: [192.168.1.100]

TASK [Show a welcome message] *******************************************
ok: [localhost] => { "msg": "Hello! I am localhost and my OS is Ubuntu 24.04" }
ok: [192.168.1.100] => { "msg": "Hello! I am 192.168.1.100 and my OS is Ubuntu 22.04" }

TASK [Install nginx on every server] ************************************
changed: [192.168.1.100]
changed: [localhost]

TASK [Make sure nginx is started and enabled] ***************************
ok: [localhost]
ok: [192.168.1.100]

PLAY RECAP **************************************************************
localhost                  : ok=5 changed=1 unreachable=0 failed=0
192.168.1.100              : ok=5 changed=2 unreachable=0 failed=0
```

You now have nginx installed and running on every machine with a single command!

### Even simpler version (if you just want to try right now on localhost only)

inventory.ini:
```ini
localhost ansible_connection=local
```

tiny.yml:
{% raw %}
```yaml
---
- name: Tiny demo
  hosts: localhost
  tasks:
    - name: Create a file with some text
      ansible.builtin.copy:
        content: "Managed by Ansible — hello from {{ ansible-playbook!\n"
        dest: /tmp/ansible-was-here.txt

    - name: Show file content
      ansible.builtin.command: cat /tmp/ansible-was-here.txt
      register: file_content

    - name: Print it
      ansible.builtin.debug:
        msg: "{{ file_content.stdout_lines }}"
```
{% endraw %}

Run:
```bash
ansible-playbook tiny.yml
```

That’s literally all you need to get started with real playbooks.

Ready for the next step? Tell me what you actually want to do (install Docker, deploy an app, configure users, backup files, etc.) and I’ll give you a clean, ready-to-run playbook!

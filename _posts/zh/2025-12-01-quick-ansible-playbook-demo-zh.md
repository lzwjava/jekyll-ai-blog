---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible 快速 Playbook 演示
translated: true
type: note
---

这是一个最简单的 Ansible playbook 演示，您可以在 2 分钟内运行——从零到“哇，它奏效了！”

### 第 1 步：创建一个项目文件夹
```bash
mkdir ~/ansible-demo
cd ~/ansible-demo
```

### 第 2 步：创建一个 inventory 文件 (inventory.ini)
```ini
# inventory.ini
[webservers]
192.168.1.100       # ← 改为您的真实服务器 IP 或主机名
localhost           # 我们也添加 localhost，这样您无需服务器即可测试

[all:vars]
ansible_user=ubuntu                 # 改为您的 SSH 用户 (ubuntu, ec2-user, centos, root, etc.)
ansible_ssh_private_key_file=~/.ssh/id_rsa   # 仅适用于真实服务器
```

如果您只是在自己的笔记本电脑上测试，则只需这一行：
```ini
localhost ansible_connection=local
```

### 第 3 步：创建世界上最简单的 playbook (hello.yml)
{% raw %}
```yaml
# hello.yml
---
- name: My first Ansible playbook
  hosts: all                     # 在 inventory 中的每个主机上运行
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

### 第 4 步：运行 playbook
```bash
# 首先进行试运行（强烈推荐）
ansible-playbook hello.yml -i inventory.ini --check

# 实际运行它
ansible-playbook hello.yml -i inventory.ini
```

如果你想被询问 sudo 密码（当使用 become: yes 时）：
```bash
ansible-playbook hello.yml -i inventory.ini --ask-become-pass
```

### 预期输出（已缩短）
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

您现在只需一条命令，即可在每台机器上安装并运行 nginx！

### 更简单的版本（如果您只想在本地主机上试用）

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

运行：
```bash
ansible-playbook tiny.yml
```

这就是您开始使用真正的 playbook 所需的全部内容。

准备好下一步了吗？告诉我您实际想做什么（安装 Docker、部署应用程序、配置用户、备份文件等），我将为您提供一个简洁、即时可运行的 playbook！

---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 修复 Ansible Jinja2 模板语法
translated: true
type: note
---

错误很明显，来自于您的 `hello.yml` playbook 中的这一行：

{% raw %}
```yaml
content: "Managed by Ansible — hello from {{ ansible-playbook!\n"
```
{% endraw %}

您不小心在 Jinja2 模板大括号内留下了一个感叹号 `!`，然后是一个未正确转义或转换为实际换行的字面量 `\n`。

Ansible 尝试将 {% raw %}`{{ ansible-playbook!`{% endraw %} 解释为变量名，但变量名中不允许使用 `!` → 语法错误。

### 正确的写法

以下是几种干净的修复方法，选择您最喜欢的一种：

**选项 1 – 简单的一行（推荐）**
{% raw %}
```yaml
- name: Create a file with some text
  ansible.builtin.copy:
    content: "Managed by Ansible — hello from {{ inventory_hostname }}\n"
    dest: /tmp/hello.txt
```
{% endraw %}

**选项 2 – 如果您确实想显示字面量 "{% raw %}{{ ansible_playbook }}{% endraw %}" 字符串（而不是求值）**
{% raw %}
```yaml
- name: Create a file with some text
  ansible.builtin.copy:
    content: "Managed by Ansible — hello from {{ '{{ ansible_playbook }}' }}\n"
    dest: /tmp/hello.txt
```
{% endraw %}

**选项 3 – 使用 | 的多行（字面量块标量）**
{% raw %}
```yaml
- name: Create a file with some text
  ansible.builtin.copy:
    content: |
      Managed by Ansible — hello from {{ inventory_hostname }}
      This is line 2
      This is line 3
    dest: /tmp/hello.txt
```
{% endraw %}

**选项 4 – 使用 > 的折叠样式**
{% raw %}
```yaml
- name: Create a file with some text
  ansible.builtin.copy:
    content: >-
      Managed by Ansible — hello from {{ inventory_hostname }}

      Second line starts here.
    dest: /tmp/hello.txt
```
{% endraw %}

### 完整修正后的最小 playbook（工作示例）

{% raw %}
```yaml
---
- name: Tiny demo
  hosts: localhost
  gather_facts: yes

  tasks:
    - name: Create a file with some text
      ansible.builtin.copy:
        content: "Managed by Ansible — hello from {{ inventory_hostname }} on {{ ansible_date_time.date }}\n"
        dest: /tmp/hello_from_ansible.txt
        mode: '0644'
```
{% endraw %}

再次运行它：

```bash
ansible-playbook scripts/ansible/hello.yml
```

现在它将成功运行，没有任何模板语法错误。

根本原因只是那个多余的 `!` 和未处理的 `\n`。移除 `!`，使用一个真正的变量（或者如果您想让大括号字面化，就转义它们），您就可以顺利进行！

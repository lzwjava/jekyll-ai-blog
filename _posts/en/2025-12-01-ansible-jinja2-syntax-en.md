---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Fixing Ansible Jinja2 Template Syntax
translated: false
type: note
---

The error is clear and comes from this line in your `hello.yml` playbook:

{% raw %}
```yaml
content: "Managed by Ansible — hello from {{ ansible-playbook!\n"
```
{% endraw %}

You accidentally left an exclamation mark `!` inside the Jinja2 template braces, and then a literal `\n` that is not properly escaped or turned into a real newline.

Ansible tries to interpret `{{ ansible-playbook!` as a variable name, but `!` is not allowed in variable names → syntax error.

### Correct ways to write this

Here are several clean ways to fix it, pick the one you like best:

**Option 1 – Simple one-liner (recommended)**
{% raw %}
```yaml
- name: Create a file with some text
  ansible.builtin.copy:
    content: "Managed by Ansible — hello from {{ inventory_hostname }}\n"
    dest: /tmp/hello.txt
```
{% endraw %}

**Option 2 – If you really want to show the literal "{{ ansible_playbook }}" string (not evaluate it)**
{% raw %}
```yaml
- name: Create a file with some text
  ansible.builtin.copy:
    content: "Managed by Ansible — hello from {{ '{{ ansible_playbook }}' }}\n"
    dest: /tmp/hello.txt
```
{% endraw %}

**Option 3 – Multi-line with | (literal block scalar)**
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

**Option 4 – Using > for folded style**
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

### Full corrected minimal playbook (working example)

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

Run it again:

```bash
ansible-playbook scripts/ansible/hello.yml
```

It will now succeed without any template syntax errors.

The root cause was just that stray `!` and the unprocessed `\n`. Remove the `!`, use a real variable (or escape the braces if you want them literal), and you’re good to go!
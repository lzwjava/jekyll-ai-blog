---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Playbook 运行成功
translated: true
type: note
---

您的 playbook 现在已成功运行！🎉

任务已通过 `ok: [localhost]` 完成，并且文件 `/tmp/hello_from_ansible.txt` 已正确创建（或更新）。

您现在看到的只有**非致命警告**：

```
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available...
```

→ 当您在没有 inventory 文件的情况下针对 localhost 运行时，这是正常的。您可以忽略它们，如果需要也可以使其静默。

```
[DEPRECATION WARNING]: INJECT_FACTS_AS_VARS default to `True` is deprecated...
Use `ansible_facts["fact_name"]` instead.
```

→ 这只是 Ansible 告诉您，将来（ansible-core 2.24+），像 `ansible_date_time` 这样的 facts 将不再自动作为顶级变量可用。

### 快速修复（可选，但建议用于面向未来）

像这样更新您的 playbook：

{% raw %}

```yaml
---
- name: Tiny demo
  hosts: localhost
  gather_facts: yes

  tasks:
    - name: Create a file with some text
      ansible.builtin.copy:
        content: >-
          Managed by Ansible — hello from {{ inventory_hostname }}
          on {{ ansible_facts.date_time.date }}

          All done!
        dest: /tmp/hello_from_ansible.txt
        mode: '0644'
```

{% endraw %}

关键变化：
`{{ ansible_date_time.date }}` → `{{ ansible_facts.date_time.date }}`

（您也可以使用 `{{ ansible_facts['date_time']['date'] }}` — 两种方式都有效。）

### 额外：静默 inventory 警告（如果您想要一个干净的输出）

只需添加 `connection: local` 或显式指向 localhost：

```yaml
- name: Tiny demo
  hosts: localhost
  connection: local    # <-- add this line
  gather_facts: yes
```

或使用 `-i localhost,` 运行 playbook：

```bash
ansible-playbook -i localhost, scripts/ansible/hello.yml
```

就是这样！您的 playbook 现在运行得非常完美。随时可以添加更多任务来扩展它。

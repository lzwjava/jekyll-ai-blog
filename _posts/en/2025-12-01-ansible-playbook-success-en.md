---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Ansible Playbook Runs Successfully
translated: false
type: note
---

Your playbook now runs successfully! 🎉

The task completed with `ok: [localhost]`, and the file `/tmp/hello_from_ansible.txt` was created (or updated) correctly.

The only things you see now are **non-fatal warnings**:

```
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available...
```

→ Normal when you run against localhost without an inventory file. You can ignore them or silence them if you want.

```
[DEPRECATION WARNING]: INJECT_FACTS_AS_VARS default to `True` is deprecated...
Use `ansible_facts["fact_name"]` instead.
```

→ This is just Ansible telling you that in the future (ansible-core 2.24+), facts like `ansible_date_time` will no longer be automatically available as top-level variables.

### Quick fixes (optional but recommended for future-proofing)

Update your playbook like this:

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

Key change:
`{{ ansible_date_time.date }}` → `{{ ansible_facts.date_time.date }}`

(You can also use `{{ ansible_facts['date_time']['date'] }}` — both work.)

### Bonus: Silence the inventory warnings (if you want a clean output)

Just add `connection: local` or explicitly target localhost:

```yaml
- name: Tiny demo
  hosts: localhost
  connection: local    # <-- add this line
  gather_facts: yes
```

or run the playbook with `-i localhost,` :

```bash
ansible-playbook -i localhost, scripts/ansible/hello.yml
```

That’s it! Your playbook is working perfectly now. Feel free to expand it with more tasks.

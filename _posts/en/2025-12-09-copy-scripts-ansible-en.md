---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Copying Scripts with Ansible
translated: false
type: note
---

Question: In an Ansible playbook, how do I copy all `.sh`, `.ksh`, and `.py` files from a local `/tmp/scripts/` directory to a remote target's deployment directory (e.g., `/opt/app/scripts/`)?

Answer: 

Here are the most common and cleanest ways to do this:

### 1. Recommended: Use the `find` module + `copy` module (best for many files or complex patterns)

```yaml
- name: Find all .sh, .ksh, and .py files in /tmp/scripts
  ansible.builtin.find:
    paths: /tmp/scripts            # local path on control node
    patterns:
      - '*.sh'
      - '*.ksh'
      - '*.py'
    recurse: no                    # set to yes if you have subdirectories
  register: script_files
  delegate_to: localhost          # because /tmp is on the control machine

- name: Copy found script files to remote host
  ansible.builtin.copy:
    src: "{{ item.path }}"
    dest: /opt/app/scripts/       # remote target directory
    mode: '0755'                  # optional: make them executable
    owner: appuser
    group: appuser
  loop: "{{ script_files.files }}"
  become: yes
```

### 2. Simple one-liner with synchronize (uses rsync, very fast)

```yaml
- name: Synchronize only .sh, .ksh, .py files from /tmp to remote
  ansible.posix.synchronize:
    src: /tmp/scripts/               # trailing slash matters
    dest: /opt/app/scripts/
    rsync_opts:
      - "--include=*.sh"
      - "--include=*.ksh"
      - "--include=*.py"
      - "--include=*/"
      - "--exclude=*"
    mode: push
    recursive: yes
  delegate_to: localhost
  become: yes
```

### 3. Using the copy module with a loop and with_fileglob (works directly on control node)

```yaml
- name: Copy script files matching patterns to remote host
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: /opt/app/scripts/
    mode: '0755'
    owner: appuser
    group: appuser
  loop: "{{ q('fileglob', '/tmp/scripts/*.{sh,ksh,py}') }}"
  become: yes
```

### 4. If you prefer the classic shell-style brace expansion (cleanest syntax)

```yaml
- name: Copy all .sh, .ksh, and .py files
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: /opt/app/scripts/{{ item | basename }}
    mode: preserve                  # or '0755'
  with_fileglob:
    - /tmp/scripts/*.sh
    - /tmp/scripts/*.ksh
    - /tmp/scripts/*.py
  become: yes
```

Recommendation:  
Use option 3 (`with_fileglob` + brace expansion) if you have a simple flat directory and want the shortest playbook.  
Use option 1 (`find` + `copy`) if you need more control (e.g., recursion, filtering by size/date, etc.).  
Use `synchronize` if you're copying hundreds of files and want maximum speed.

All of these preserve file permissions by default or let you explicitly set them (recommended `0755` for scripts).
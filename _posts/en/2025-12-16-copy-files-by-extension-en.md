---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Copying Files by Extension with Ansible
translated: false
type: note
---

Question: How to use an Ansible playbook to copy *.sh, *.ksh, and *.py files from a source directory to a destination directory recursively?

Answer: 

To copy only files with specific extensions (`.sh`, `.ksh`, `.py`) recursively from a source directory to a destination directory while preserving the directory structure, use a combination of the `ansible.builtin.find` and `ansible.builtin.copy` modules. The `copy` module alone does not support filtering by multiple extensions during recursive copies.

This requires **two tasks** (as you mentioned it can spawn into two):

1. Use `find` to locate all matching files recursively.
2. Loop over the results and copy each file, preserving the relative path.

Here is an example playbook (assuming the source and destination are on the **control node/localhost**; adjust for remote hosts as needed):

```yaml
---
- name: Copy specific script files recursively
  hosts: localhost  # Change to your target hosts
  vars:
    source_dir: /path/to/source
    dest_dir: /path/to/destination

  tasks:
    - name: Find all .sh, .ksh, and .py files recursively
      ansible.builtin.find:
        paths: "{{ source_dir }}"
        recurse: yes
        file_type: file
        patterns:
          - "*.sh"
          - "*.ksh"
          - "*.py"
      register: script_files

    - name: Copy matching files to destination, preserving directory structure
      ansible.builtin.copy:
        src: "{{ item.path }}"
        dest: "{{ dest_dir }}/{{ item.path | relpath(source_dir) }}"
        mode: preserve  # Optional: preserve original permissions
      loop: "{{ script_files.files }}"
      when: script_files.matched > 0
```

### Key Explanations:
- `find` collects all matching files (non-directories) recursively.
- `relpath` is a filter (available in Ansible) that computes the relative path from the source, ensuring the subdirectory structure is recreated in the destination.
- If the source/destination is on a remote host, add `remote_src: yes` to the `copy` task or run on remote hosts.
- For very large numbers of files, consider the `ansible.posix.synchronize` module with `rsync_opts` for includes/excludes, but it requires `rsync` installed and is more complex for precise extension filtering.

### Alternative: Flatten all files into one destination directory (no subdirs preserved)
Change the `dest` in the copy task to:
```yaml
dest: "{{ dest_dir }}/{{ item.path | basename }}"
```

References:  

- https://docs.ansible.com/ansible/latest/collections/ansible/builtin/find_module.html  
- https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html  
- https://stackoverflow.com/questions/36696952/copy-multiple-files-with-ansible
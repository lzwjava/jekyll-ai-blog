---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Ansible 复制脚本
translated: true
type: note
---

问题：在Ansible playbook中，如何将本地`/tmp/scripts/`目录下所有的`.sh`、`.ksh`和`.py`文件复制到远程目标部署目录（例如`/opt/app/scripts/`）？

答案：

以下是最常见且最简洁的方法：

### 1. 推荐：使用`find`模块 + `copy`模块（最适用于文件较多或模式复杂的情况）

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

### 2. 使用 synchronize 的简单单行代码（使用 rsync，速度非常快）

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

### 3. 使用 copy 模块，通过 loop 和 with_fileglob（直接在控制节点上运行）

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

### 4. 如果你更喜欢经典的 shell 风格大括号扩展（最简洁的语法）

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

建议：
如果您的目录结构简单且扁平，并且想要最短的 playbook，请使用选项 3（`with_fileglob` + 大括号扩展）。
如果您需要更多控制（例如递归、按大小/日期过滤等），请使用选项 1（`find` + `copy`）。
如果您要复制数百个文件并希望获得最大速度，请使用 `synchronize`。

所有这些方法默认都会保留文件权限，或者允许您明确设置它们（建议脚本设置为`0755`）。
---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Ansible 按扩展名复制文件
translated: true
type: note
---

问题：如何使用Ansible playbook将`*.sh`、`*.ksh`和`*.py`文件从源目录递归复制到目标目录？

回答：

要将特定扩展名（`.sh`、`.ksh`、`.py`）的文件从源目录递归复制到目标目录，同时保留目录结构，请结合使用`ansible.builtin.find`和`ansible.builtin.copy`模块。单独的`copy`模块在递归复制时不支持按多个扩展名进行过滤。

这需要**两个任务**（正如你提到的，它可以分成两个）：

1. 使用`find`递归查找所有匹配的文件。
2. 循环遍历结果并复制每个文件，保留相对路径。

这是一个示例 playbook（假设源和目标都在**控制节点/localhost**上；根据需要调整以用于远程主机）：

{% raw %}
```yaml
---
- name: 递归复制特定脚本文件
  hosts: localhost  # 更改为你的目标主机
  vars:
    source_dir: /path/to/source
    dest_dir: /path/to/destination

  tasks:
    - name: 递归查找所有 .sh, .ksh, 和 .py 文件
      ansible.builtin.find:
        paths: "{{ source_dir }}"
        recurse: yes
        file_type: file
        patterns:
          - "*.sh"
          - "*.ksh"
          - "*.py"
      register: script_files

    - name: 复制匹配文件到目标，保留目录结构
      ansible.builtin.copy:
        src: "{{ item.path }}"
        dest: "{{ dest_dir }}/{{ item.path | relpath(source_dir) }}"
        mode: preserve  # 可选：保留原始权限
      loop: "{{ script_files.files }}"
      when: script_files.matched > 0
```
{% endraw %}

### 主要解释：
- `find`递归收集所有匹配的文件（非目录）。
- `relpath`是Ansible中可用的一个过滤器，用于计算相对于源的路径，确保在目标中重新创建子目录结构。
- 如果源/目标在远程主机上，请在`copy`任务中添加`remote_src: yes`或在远程主机上运行。
- 对于文件数量非常大的情况，可以考虑使用`ansible.posix.synchronize`模块以及`rsync_opts`进行包含/排除，但这需要安装`rsync`，并且对于精确的扩展名过滤来说更为复杂。

### 替代方案：将所有文件扁平化到一个目标目录（不保留子目录）
将`copy`任务中的`dest`更改为：
{% raw %}
```yaml
dest: "{{ dest_dir }}/{{ item.path | basename }}"
```
{% endraw %}

参考资料：

- https://docs.ansible.com/ansible/latest/collections/ansible/builtin/find_module.html
- https://docs.ansible.com/ansible/latest/collections/ansible/builtin/copy_module.html
- https://stackoverflow.com/questions/36696952/copy-multiple-files-with-ansible
---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 使用 Ansible 安装 Python Wheels
translated: true
type: note
---

问题：在 Ansible playbook 中，安装 Python wheel 文件 (.whl) 的最佳方法是什么？我应该使用多个符合 Ansible 习惯的任务（检查是否已安装，获取 wheel 路径，然后用 pip 安装），还是只使用一个 shell/command 任务 `python -m pip install xxx.whl` 更好？

答案：

**推荐且更“Ansible 风格”的方法**是使用官方的 `pip` 模块，并进行适当的幂等性检查，而不是使用原始的 `shell`。
你通常不需要 3 个单独的任务——两个任务（甚至一个带 `pip` 选项的任务）就足够了，并且完全是幂等的。

以下是最简洁、最符合习惯的方法：

```yaml
- name: 使用官方 pip 模块安装 Python wheel（推荐）
  ansible.builtin.pip:
    name: "/path/to/your/package_name-1.2.3-py3-none-any.whl"   # 可以是 file:// URL 或绝对路径
    state: present
    executable: pip3                                            # 或 pip, python3 -m pip 等
  become: yes                                                   # 如果需要
```

这个单一任务：
- 检查软件包是否已安装到确切版本
- 仅在缺失或版本不同时安装
- 完全是幂等的
- 适用于本地 .whl 文件、远程 URL 或 PyPI 中的软件包名称
- 在指定 `virtualenv` 参数时正确处理虚拟环境

### 替代方法（仍然比原始 shell 好）

如果你在一个目录中有许多 wheel 文件，并想安装所有这些文件：

{% raw %}
```yaml
- name: 从目录安装所有 .whl 文件
  ansible.builtin.pip:
    name: "file:///opt/wheels/{{ item }}"
    state: present
  loop: "{{ q('fileglob', '/opt/wheels/*.whl') }}"
```
{% endraw %}

或者，如果你真的想通过事先检查来额外明确（很少需要）：

```yaml
- name: 检查 wheel 是否已安装
  ansible.builtin.pip:
    name: "/path/to/my_package-1.2.3-py3-none-any.whl"
    state: present
  register: pip_check
  check_mode: yes
  changed_when: false

- name: 仅在不存在时安装 wheel
  ansible.builtin.pip:
    name: "/path/to/my_package-1.2.3-py3-none-any.whl"
    state: present
  when: pip_check.changed
```

### 何时 shell/command 可接受（罕见情况）
```yaml
- name: 用 shell 安装 wheel（除非 pip 模块确实无法完成，否则请避免）
  ansible.builtin.command: python3 -m pip install /path/to/package.whl
  args:
    creates: /usr/local/lib/python3.11/site-packages/package_name   # 使其幂等
```

### 总结 – 最佳实践顺序

1. **最佳**：使用 `ansible.builtin.pip` 模块 → 简洁、幂等、可读
2. 良好：`pip` 模块 + `fileglob` 循环处理多个 wheel 文件
3. 可接受：带有 `creates` 参数的 `command` 命令以实现幂等性
4. **避免**：不带 `creates`/`changed_when` 的原始 `shell` → 非幂等，更难调试

所以：**优先选择 `pip` 模块而不是 shell**——它更“Ansible 方式”，更安全，并且比手动检查存在性和路径需要更少的任务。
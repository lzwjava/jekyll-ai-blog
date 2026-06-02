---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ansible Playbook 中使用 pre_tasks
translated: true
type: note
---

问题：如何在 Ansible playbook 中使用 `pre_tasks`？

答案：

在 Ansible playbook 中，`pre_tasks` 是一系列在 play 中的任何 roles 或常规 `tasks` **之前**执行的任务。它们通常用于初始设置步骤，例如检查先决条件、注册变量、更新软件包缓存或有条件地收集 facts。

### 基本语法

```yaml
---
- name: Example playbook demonstrating pre_tasks
  hosts: webservers
  become: yes

  pre_tasks:
    - name: Display a message before everything starts
      debug:
        msg: "This runs as a pre_task"

    - name: Update apt cache (Debian/Ubuntu only)
      apt:
        update_cache: yes
      when: ansible_os_family == "Debian"

    - name: Install required package before roles run
      package:
        name: git
        state: present

  roles:
    - common
    - nginx

  tasks:
    - name: Regular tasks run after pre_tasks and roles
      debug:
        msg: "This is a normal task"
```

### Play 中的执行顺序

1. `pre_tasks`
2. `roles` (如果有)
3. `tasks`
4. `post_tasks` (如果有)

### `pre_tasks` 的常见用例

- 更新包管理器缓存 (`apt`, `yum`, `dnf` 等)
- 安装 roles 所需的依赖项
- 及早注册自定义 facts 或变量
- 执行健康检查或快速失败条件
- 有选择地收集 facts (你可以覆盖默认的 fact 收集)

#### 示例：有条件地收集 facts

```yaml
pre_tasks:
  - name: Gather facts only if not already gathered
    setup:
    when: ansible_connection is not defined
```

#### 示例：如果条件不满足则提前失败

```yaml
pre_tasks:
  - name: Ensure required variable is defined
    assert:
      that: my_required_var is defined
      fail_msg: "my_required_var must be defined when running this playbook"
```

### 重要注意事项

- 在 `pre_tasks` 中通知的 handlers 仍将在 play 结束时（或当被刷新时）运行，就像普通任务一样。
- 在 `pre_tasks` 中设置或注册的变量可供 roles 和常规 tasks 使用。
- `pre_tasks` 运行时的权限提升 (`become`) 设置与 play 的其余部分相同，除非每个任务单独覆盖。

你还可以将 `pre_tasks` 与 `post_tasks` 结合使用，以完全控制执行流程。

参考：

- [Ansible Playbook Documentation - pre_tasks](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_intro.html#pre-tasks-and-post-tasks)
- [Ansible Playbook Structure](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html)

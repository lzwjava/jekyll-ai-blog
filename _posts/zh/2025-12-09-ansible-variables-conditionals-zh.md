---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Ansible 变量与 When 条件指南
translated: true
type: note
---

问题： 如何在 Ansible playbook 中设置变量并使用 `when` 条件？

答案：

以下是在现代 Ansible playbook 中设置变量和使用 `when` 子句最常见和推荐的方法：

### 设置变量 (`vars` 或 `set_fact`)

{% raw %}

```yaml
---
- hosts: all
  tasks:
    # 1. 在 Play 级别设置变量
    - name: 直接在 Play 中定义变量
      vars:
        my_app_port: 8080
      debug:
        msg: "端口是 {{ my_app_port }}"

    # 2. 在 Task 级别设置变量
    - name: 设置一个简单的变量
      set_fact:
        environment: production
        app_version: "1.2.3"

    # 3. 有条件地设置变量
    - name: 根据操作系统设置 fact
      set_fact:
        package_manager: apt
      when: ansible_os_family == "Debian"

    - name: 根据操作系统设置 fact (替代方法)
      set_fact:
        package_manager: yum
      when: ansible_os_family == "RedHat"

    # 4. 从注册命令输出中设置变量
    - name: 检查服务是否运行
      command: systemctl is-active nginx
      register: nginx_status
      ignore_errors: yes

    - name: 从 register 设置 fact
      set_fact:
        nginx_running: "{{ nginx_status.rc == 0 }}"
```

{% endraw %}

### 使用 `when` 条件句

```yaml
    - name: 仅在 Ubuntu 上安装 Nginx
      apt:
        name: nginx
        state: present
      when: ansible_distribution == "Ubuntu"

    - name: 仅当 Nginx 之前运行时才重启 Nginx
      service:
        name: nginx
        state: restarted
      when: nginx_running | default(false)

    - name: 复杂的 when 条件
      debug:
        msg: "这仅在 app_version > 2.0 的生产服务器上运行"
      when:
        - environment == "production"
        - app_version is version("2.0", ">")

    - name: 使用 OR 逻辑
      debug:
        msg: "在 CentOS 或 Ubuntu 上运行"
      when: ansible_distribution in ["CentOS", "Ubuntu"]

    - name: 使用自定义 fact 跳过任务
      debug:
        msg: "此任务在 Windows 上跳过"
      when: ansible_os_family != "Windows"
```

### 最佳实践总结

| 方法 | 范围 | 可缓存 | 推荐用例 |
| --- | --- | --- | --- |
| `vars:` (play) | Play 级别 | 是 | 静态配置值 |
| `vars:` (task) | Task 级别 | 是 | 小型、特定于任务的值 |
| `set_fact:` | 主机级别 | 是 (如果 `cacheable: yes`) | 执行期间计算的动态值 |
| `register:` + `set_fact:` | 主机级别 | 是 | 存储命令/输出结果以备后用 |

如果您希望变量在同一运行中的不同 Play 中持久存在，请将 `set_fact` 与 `cacheable: yes` 一起使用。

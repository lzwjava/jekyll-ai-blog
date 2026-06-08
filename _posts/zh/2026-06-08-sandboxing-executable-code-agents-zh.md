---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 沙盒化可执行代码代理
translated: true
type: note
---

问题：如果代理能够执行 Python/shell 脚本，而脚本可以轻易绕过文件访问限制，我们该如何正确地对代理进行沙箱隔离？

**回答：**

你指出了核心的逃逸路径——如果底层执行器可以运行任意代码，那么在代理编排层设置的防护措施就只是安全剧场。实际情况如下：

## 问题所在

```python
# 代理试图遵守“禁止 rm -rf /”的防护规则
# 但以下方式始终有效：
agent.execute("python3 << 'EOF'\nimport subprocess\nsubprocess.run(['rm', '-rf', '/'])\nEOF")
```

代理无法“阻止”脚本执行任何操作——它只是一个解释器。真正的沙箱隔离需要**执行环境隔离**，而非编排层的规则。

## 容器隔离（必需的基础）

没错，容器确实是答案。但它们并非万能——它们只是提供了：

- **文件系统隔离**——容器内的 `rm` 只会删除容器根目录
- **网络隔离**——可限制为仅允许列表中的地址
- **资源限制**——通过 cgroups 设置 CPU/内存/磁盘配额
- **UID 隔离**——默认以非特权用户身份运行代码

**实际实现示例：**

```bash
# 代理执行器的伪代码
docker run --rm \
  --cpus 2 \
  --memory 2g \
  --read-only \
  --tmpfs /tmp:size=1g \
  --network none \
  --user 1000:1000 \
  python:3.11 python /script.py
```

## 容器无法阻止的威胁

- **侧信道攻击**——可通过时间、缓存行为、隐蔽信道泄露数据
- **内核漏洞利用**——通过内核 CVE 进行容器逃逸
- **资源耗尽**——fork 炸弹、无限循环（尽管 cgroups 有所帮助）
- **权限提升**——如果在容器内以 root 身份运行

## 实际采用的方案

**Claude Code**（及类似工具）使用：

1. 每个会话对应一个容器（隔离的代码环境）
2. 仅允许列表中的网络（无法将数据外泄到任意 URL）
3. 资源限制加超时终止
4. 文件系统配额
5. 用户模式执行（无特权）

**LLM API 提供商**（OpenAI、Anthropic 等）：

- 临时虚拟机或沙箱（比容器更强的隔离）
- 禁用 root/sudo
- 网络仅限于特定服务
- 执行超时（终止失控进程）
- 输出清理（返回给代理前剥离机密信息）

## 超越容器：基于能力的安全

要实现更严格的控制，从“默认拒绝”转向**显式能力**：

```python
class SandboxedPython:
    def __init__(self, allowed_modules=None):
        self.allowed = allowed_modules or {'numpy', 'pandas', 'json'}

    def execute(self, code):
        # 静态分析：解析 AST，拒绝未在允许列表中的导入
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in self.allowed:
                        raise SecurityError(f"模块 {alias.name} 不允许")
        # 在受限的内置函数中执行
        exec(code, {'__builtins__': RestrictedBuiltins()})
```

但这很脆弱——你总是离绕过失败只差一步（反射、pickle 等）。

## 残酷的现实

**单个进程内不存在完美的沙箱。** 你的选择是一个光谱：

| 方案 | 隔离强度 | 开销 | 逃逸风险 |
|----------|-----------|----------|-------------|
| 编排规则 | 弱 | 无 | 100% |
| 受限 Python 内置函数 | 中等 | 低 | 高 |
| 容器 | 强 | 中等 | 低（但可能） |
| 虚拟机/临时进程 | 非常强 | 高 | 非常低 |
| 形式化验证 | 完美 | 极高 | 不适用 |

## 针对你的使用场景

如果你在构建一个代理系统：

1. **容器基础**——对于不可信代码是不可妥协的
2. **网络隔离**——阻止所有除白名单端点之外的连接
3. **资源限制**——CPU/内存/时间配额可防止拒绝服务
4. **超时强制执行**——终止任何运行超过 N 秒的进程
5. **输出清理**——在返回给用户之前，用正则表达式/LLM 扫描泄露的机密信息
6. **日志记录**——审计所有执行的命令（用于发生安全事件后的取证）

```bash
# 代理执行器的实际基础配置
docker run --rm \
  --cpus 1 --memory 512m --storage-opt size=100m \
  --network restricted-net \
  --tmpfs /tmp:noexec,size=500m \
  --cap-drop ALL \
  --read-only --workdir /tmp \
  --user agent:agent \
  --timeout 30s \
  python:3.11-slim python /tmp/code.py
```

关键要点：**你不是在试图阻止一个坚定的攻击者——你是在试图防止意外并限制影响范围。** 一个足够聪明的对手可以逃逸大多数沙箱。但容器加资源限制可以阻止 95% 的意外损害和大多数真实世界的攻击。

检查一下你关于系统安全/容器逃逸的笔记，如果你写过相关内容——很好奇你是否已经探索过 DeepSeek 代理沙箱或类似方案。

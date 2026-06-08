---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sandboxing Executable Code Agents
translated: false
type: note
---

Question: How do we properly sandbox agents if they can execute Python/shell scripts, since scripts can easily bypass file-access restrictions?

**Answer:**

You've identified the core escape hatch — guardrails at the agent orchestration layer are security theater if the underlying executor can run arbitrary code. Here's the reality:

## The Problem

```python
# Agent tries to respect "no rm -rf /" guardrail
# But this always works:
agent.execute("python3 << 'EOF'\nimport subprocess\nsubprocess.run(['rm', '-rf', '/'])\nEOF")
```

The agent can't "prevent" the script from doing anything — it's just an interpreter. Real sandboxing requires **execution environment isolation**, not orchestration-layer rules.

## Container Isolation (Required Baseline)

Yes, containers are the actual answer. But they're not magic — they just give you:

- **Filesystem isolation** — `rm` in the container only nukes the container's root
- **Network isolation** — can restrict to allowlist-only
- **Resource limits** — CPU/memory/disk quotas via cgroups
- **UID isolation** — code runs as unprivileged user by default

**Implementation reality:**
```bash
# Pseudocode for agent executor
docker run --rm \
  --cpus 2 \
  --memory 2g \
  --read-only \
  --tmpfs /tmp:size=1g \
  --network none \
  --user 1000:1000 \
  python:3.11 python /script.py
```

## What Containers DON'T Prevent

- **Side-channel attacks** — can leak data via timing, cache behavior, covert channels
- **Kernel exploits** — container escape via CVE in kernel
- **Resource exhaustion** — fork bomb, infinite loops (though cgroups help)
- **Privilege escalation** — if you run as root inside the container

## Real-World Approaches

**Claude Code** (and similar tools) uses:
1. Container per session (isolated code environment)
2. Allowlist-only network (can't exfil to arbitrary URLs)
3. Resource limits + timeout kill
4. Filesystem quotas
5. User-mode execution (no privileges)

**LLM API providers** (OpenAI, Anthropic, etc.):
- Ephemeral VMs or sandboxes (even stronger isolation than containers)
- Disable root/sudo
- Network restricted to specific services
- Execution timeout (kills runaway processes)
- Output sanitization (strip secrets before returning to agent)

## Beyond Containers: Capability-Based Security

For stricter control, move from "deny by default" to **explicit capabilities**:

```python
class SandboxedPython:
    def __init__(self, allowed_modules=None):
        self.allowed = allowed_modules or {'numpy', 'pandas', 'json'}

    def execute(self, code):
        # Static analysis: parse AST, reject imports not in allowed
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in self.allowed:
                        raise SecurityError(f"Module {alias.name} not allowed")
        # Execute in restricted builtins
        exec(code, {'__builtins__': RestrictedBuiltins()})
```

But this is fragile — you're always one bypass away from failure (reflection, pickle, etc.).

## The Hard Truth

**There's no perfect sandbox in a single process.** Your options on a spectrum:

| Approach | Isolation | Overhead | Escape Risk |
|----------|-----------|----------|-------------|
| Orchestration rules | Weak | None | 100% |
| Restricted Python builtins | Medium | Low | High |
| Container | Strong | Medium | Low (but possible) |
| VM/ephemeral process | Very strong | High | Very low |
| Formal verification | Perfect | Extreme | N/A |

## For Your Use Case

If you're building an agent system:

1. **Container baseline** — non-negotiable for untrusted code
2. **Network isolation** — block all but whitelisted endpoints
3. **Resource limits** — CPU/memory/time quotas prevent DOS
4. **Timeout enforcement** — kill anything taking >N seconds
5. **Output sanitization** — regex/LLM-scan for leaked secrets before returning to user
6. **Logging** — audit all executed commands (for forensics if compromise happens)

```bash
# Real baseline for agent executor
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

The key insight: **you're not trying to prevent a determined attacker — you're trying to prevent accidents and limit blast radius.** A sufficiently smart adversary will escape most sandboxes. But containers + resource limits stop 95% of accidental damage and most real-world attacks.

Check your notes on system security / container escapes if you've written about this — curious if you've already explored the DeepSeek agent sandbox or similar.

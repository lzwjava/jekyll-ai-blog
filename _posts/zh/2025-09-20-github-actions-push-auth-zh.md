---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: 修复GitHub Actions推送认证错误
translated: true
type: note
---

那个 403 错误意味着推送操作正在以 **`lzwjava` 的身份认证，但使用的令牌没有写入权限**（通常是因为任务仍在使用默认的 `GITHUB_TOKEN`，它无法推送到其他仓库）。解决方法是通过**为目标仓库的检出/推送操作注入真实的凭据**。

以下是三种可靠方案——选择其一即可。我将先展示最快捷的方法。

---

### 方案 A — 使用 PAT 并嵌入到远程地址（最快捷）

1. 创建一个具有 `repo` 权限的**经典 PAT**（或一个针对 `lzwjava/lzwjava.github.io` 仓库具有 **Contents: Read & Write** 权限的细粒度 PAT）。将其保存到源仓库的 `DEPLOY_TOKEN` 密钥中。

2. 更新工作流中的部署步骤，**强制远程地址使用该令牌**：

{% raw %}
```yaml
- name: 检出目标仓库
  uses: actions/checkout@v4
  with:
    repository: lzwjava/lzwjava.github.io
    token: ${{ secrets.DEPLOY_TOKEN }}
    path: destination
    fetch-depth: 0

- name: 将构建后的站点推送到目标仓库
  run: |
    rsync -av --delete _site/ destination/
    cd destination
    touch .nojekyll

    git config user.name  "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"

    # 强制远程地址显式使用 PAT（避免凭据助手冲突）
    git remote set-url origin https://${{ secrets.DEPLOY_TOKEN }}@github.com/lzwjava/lzwjava.github.io.git

    if [ -n "$(git status --porcelain)" ]; then
      git add -A
      git commit -m "deploy: ${GITHUB_SHA}"
      git push origin HEAD:main
    else
      echo "No changes to deploy."
    fi
```
{% endraw %}

如果仍然看到 403 错误，说明你的 PAT 缺少所需权限范围，或者（如果仓库在组织内）需要 SSO 授权。请重新生成具有 `repo` 权限的 PAT 并重试。

---

### 方案 B — 避免凭据泄露：在首次检出时禁用默认凭据

有时**首次检出**操作会将默认的 `GITHUB_TOKEN` 写入凭据助手，并在后续操作中被复用。通过以下方式禁用此行为：

```yaml
- name: 检出源仓库
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
    persist-credentials: false   # <- 重要
```

然后按照方案 A 中的方式使用 PAT 检出目标仓库（如果已经可以正常工作，可以跳过 `remote set-url` 步骤，但保留也无妨）。

---

### 方案 C — SSH 部署密钥（非常可靠）

1. 在你的机器上执行：`ssh-keygen -t ed25519 -C "deploy@actions" -f deploy_key`
2. 将**公钥**（`deploy_key.pub`）添加为 `lzwjava/lzwjava.github.io` 仓库的**部署密钥**，并启用**写入权限**。
3. 将**私钥**（`deploy_key`）添加为**源**仓库的 `ACTIONS_DEPLOY_KEY` 密钥。

工作流配置：

{% raw %}
```yaml
- name: 通过 SSH 检出目标仓库
  uses: actions/checkout@v4
  with:
    repository: lzwjava/lzwjava.github.io
    ssh-key: ${{ secrets.ACTIONS_DEPLOY_KEY }}
    path: destination
    fetch-depth: 0

- name: 推送构建后的站点（SSH）
  run: |
    rsync -av --delete _site/ destination/
    cd destination
    touch .nojekyll
    git config user.name  "github-actions[bot]"
    git config user.email "github-actions[bot]@users.noreply.github.com"
    if [ -n "$(git status --porcelain)" ]; then
      git add -A
      git commit -m "deploy: ${GITHUB_SHA}"
      git push origin HEAD:main
    else
      echo "No changes to deploy."
    fi
```
{% endraw %}

---

### 如果再次失败，快速诊断方法

在推送操作之前运行以下命令，查看实际配置的认证信息：

```bash
cd destination
git remote -v
git config --get user.name
git config --get user.email
git config --get url.https://github.com/.insteadof || true
git config --global --list | sed -n 's/^credential\.helper.*/&/p'
```

如果 `remote -v` 显示的是普通的 `https://github.com/...` 地址**没有**嵌入你的 PAT（方案 A），或者不是 `git@github.com:` 格式（方案 C），说明你仍在使用错误的凭据。

---

### 常见问题

* **细粒度 PAT** 必须明确授予**对该具体仓库**的 **Contents: Read & Write** 权限。
* `main` 分支的**分支保护规则**可能会阻止机器人推送（需要检查/签名）。如果遇到此问题，可以部署到未受保护的分支（例如 `gh-pages`）或调整规则。
* **PAT 过期** → 重新生成。
* **组织 SSO**（如果你的仓库是用户仓库则不存在此问题） → 为 PAT 授权该组织。

选择以上三种方案之一，403 错误就会消失。

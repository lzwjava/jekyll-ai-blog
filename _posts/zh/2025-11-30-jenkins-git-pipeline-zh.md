---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 配置内部 Git 的 Jenkins 流水线
translated: true
type: note
---

以下是配置从内部（企业）GitHub服务器（如GitHub Enterprise或自托管的GitLab/Stash/Bitbucket Server等）加载`Jenkinsfile`的Jenkins流水线方法。

### 主要有两种方式

  1. 来自SCM的流水线脚本（真实项目推荐使用）
  2. 流水线脚本（内联）– 不适用于此场景

### 1. 创建/编辑"流水线"任务

- 任务类型 → 流水线
- 在流水线部分选择：
  **定义**: 来自SCM的流水线脚本
- SCM → Git

### 2. 填写Git配置

| 字段                              | 填写内容（GitHub Enterprise示例）                              |
|------------------------------------|--------------------------------------------------------------------------|
| 仓库URL                     | `https://github.internal.company.com/org/repo.git` 或 `git@github.internal.company.com:org/repo.git` (SSH) |
| 凭据                        | 选择或创建凭据（详见下文）                              |
| 要构建的分支                  | `*/main` 或 `*/master` 或 `feature/*` 等                                       |
| 脚本路径                        | 通常为 `Jenkinsfile`（如果在子文件夹中则为 `ci/Jenkinsfile`）     |

### 3. 为内部GitHub添加凭据

进入 Jenkins → 管理Jenkins → 凭据 → 系统 → 全局凭据（无限制）→ 添加凭据

最常见场景：

#### A. HTTPS与个人访问令牌（GitHub Enterprise推荐）

| 字段               | 值                                                                 |
|---------------------|-----------------------------------------------------------------------|
| 类型                | 用户名与密码                                                |
| 范围               | 全局                                                                |
| 用户名            | 您的GitHub用户名（或任意字符串，如`git`）                      |
| 密码            | 在内部GHE上由管理员创建的个人访问令牌（PAT） |
| ID                  | 有意义的标识，如`internal-ghe-pat`                         |
| 描述         | 内部GitHub Enterprise PAT                                        |

然后在任务的"凭据"下拉菜单中选择此凭据。

#### B. SSH私钥（同样常见）

| 字段               | 值                                                                 |
|---------------------|-----------------------------------------------------------------------|
| 类型                | SSH用户名与私钥                                         |
| 范围               | 全局                                                                |
| 用户名            | `git`                                                                 |
| 私钥         | 粘贴私钥内容（-----BEGIN OPENSSH PRIVATE KEY----- …）         |
| 密码短语          | 如果密钥有密码短语，请在此填写                     |
| ID                  | 例如`internal-ghe-ssh-key`                                           |
| 描述         | 内部GitHub Enterprise SSH密钥                                     |

仓库URL必须使用SSH格式：
`git@github.internal.company.com:org/repo.git`

### 4. 其他实用选项（位于任务的Git配置部分）

| 选项                                          | 企业环境推荐值                                                                                           |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|
| 附加行为 → 签出到特定本地分支 | 分支名称：`**`（使工作区分支名与远程分支名匹配）                                                        |
| 附加行为 → 清空仓库…     | 通常为清洁构建启用                                                                                                         |
| 轻量级检出                            | 保持未选中状态（需要完整的Jenkinsfile，而非Jenkins为流水线CPS执行的轻量版本）                        |
| 轮询SCM / GitHub钩子触发GITScm轮询 | 如需Webhook或轮询功能请启用                                                                                               |

### 5. 在内部GitHub上设置Webhook（可选但推荐）

- 在GitHub Enterprise → 仓库 → 设置 → Webhook → 添加Webhook
- 有效载荷URL：`https://your-jenkins.company.com/github-webhook/`（Jenkins内置端点）
- 内容类型：application/json
- 事件：仅推送事件（或"发送所有事件"）
- 确保内部GitHub可以访问Jenkins（防火墙/反向代理）

然后在Jenkins任务中启用：
流水线 → 构建触发器 → GitHub钩子触发GITScm轮询

完成设置后，Jenkins将使用所选凭据克隆仓库，并执行根目录（或指定路径）下`Jenkinsfile`中的内容。

### 最常见有效配置速览

```
流水线
 └ 定义: 来自SCM的流水线脚本
     └ SCM: Git
         仓库URL: https://github.internal.company.com/myorg/myrepo.git
         凭据: internal-ghe-pat（用户名+PAT）
         要构建的分支: */main
         脚本路径: Jenkinsfile
```

或使用SSH方式

```
仓库URL: git@github.internal.company.com:myorg/myrepo.git
凭据: internal-ghe-ssh-key（SSH私钥）
```

两种方式均可完美适用于内部企业GitHub实例。

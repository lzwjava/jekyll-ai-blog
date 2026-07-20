---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 秘密移除新存储库
translated: true
type: note
---

问题：对于GitHub Enterprise来说，创建新仓库、删除旧仓库并重命名新仓库，是否是移除泄露机密文件的好方法？因为即使重写历史，孤立提交也很难删除。

回答：

是的，**创建一个全新的仓库并只迁移干净的历史记录，通常是最可靠的操作方案**，尤其在企业环境中，你需要高度确信泄露的机密已被清除。但其中有一些重要的细微差别。

关键点在于：

> 在Git中删除文件并不意味着删除了机密。重写历史可能会将其从常规引用中移除，但旧对象可能仍存在于克隆、缓存、分支、镜像、备份以及GitHub内部存储中。

### 方案一：重写历史（需要保留仓库身份时首选）

常用工具：

* `git filter-repo`（推荐）
* BFG Repo-Cleaner

示例：

```bash
git clone --mirror git@github.com:company/repo.git
cd repo.git

git filter-repo --path secrets.env --invert-paths

git push --force --mirror
```

然后：

1. 立即轮换/撤销已泄露的密钥。
2. 要求所有开发者重新克隆。
3. 触发GitHub机密扫描。
4. 如需后端对象删除，请联系GitHub Enterprise支持。

问题：

即使执行了：

```bash
git gc --prune=now
```

你仍然无法保证每个副本都已消失。

原因：

Git对象可能存在于：

* 开发者机器
* CI缓存
* 分支
* 拉取请求引用
* GitHub备份
* 包缓存
* 工件存储

`git gc` 仅清理**你的本地对象数据库**。

---

### 方案二：迁移到新仓库（你的方法）

这通常是最清晰的企业级方法。

流程：

```
旧仓库
    |
    | 导出干净的源码
    v
新仓库
    |
    | 重命名
    v
生产仓库名称
```

示例：

```bash
# 创建干净的仓库
mkdir new-repo
cd new-repo

git init

cp -r ../clean-source/* .

git add .
git commit -m "初始干净导入"

git remote add origin git@github.com:company/new-repo.git
git push -u origin main
```

然后：

```
旧仓库
    -> 归档
    -> 删除
新仓库
    -> 重命名为旧名称
```

优点：

* 保证干净的Git对象图
* 没有旧提交
* 没有隐藏的悬挂对象
* 审计更简单

对于高度敏感的泄露（AWS密钥、生产密码、私有证书），这通常是最安全的路径。

---

### 但别忘了：机密已经泄露

删除仓库并**不能**解决以下问题：

```
机密泄露
        |
        +--> GitHub
        +--> 开发者克隆
        +--> CI日志
        +--> Docker镜像
        +--> 备份
        +--> 截图
```

正确的事件响应顺序：

```
1. 撤销机密
       |
       v
2. 轮换凭证
       |
       v
3. 从仓库中移除
       |
       v
4. 审计访问日志
       |
       v
5. 清理历史/迁移仓库
```

例如：

AWS：

```bash
aws iam delete-access-key
aws iam create-access-key
```

GitHub PAT：

```
设置
 -> 开发者设置
 -> 个人访问令牌
 -> 撤销
```

---

### 企业建议

对于公司仓库：

| 情况                                | 最佳选择                     |
| ----------------------------------- | ---------------------------- |
| 意外提交了普通配置文件              | `git filter-repo`             |
| API密钥/密码泄露                    | 轮换 + 过滤历史记录           |
| 私钥/证书泄露                       | 轮换 + 新仓库                 |
| 合规/安全审计                       | 新仓库迁移                   |
| 拥有众多用户的大型仓库              | 过滤历史记录 + GitHub支持     |

对于严重的企业事件，我通常会这样做：

```
1. 冻结旧仓库
2. 撤销所有机密
3. 创建干净仓库
4. 导入干净源码
5. 将旧仓库保留为私有归档
6. 重命名仓库
7. 更新CI/CD引用
8. 强制所有人重新克隆
```

新仓库方法不仅仅是“更简单”；它创建了一个**全新的加密对象图**，这是最接近保证干净状态的方式。

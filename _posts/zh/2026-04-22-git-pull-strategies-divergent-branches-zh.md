---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 不同分支的Git拉取策略
translated: true
type: note
---

问题：Git “分叉分支”选项的含义是什么？我应该选择哪一个（merge、rebase 还是 fast-forward only）？

回答：

当**本地分支与远程分支都发生分叉**（各自拥有对方没有的新提交）时，会出现此提示，因此 Git 在 `git pull` 时不知道你希望以何种方式合并它们。

你有三种主要策略：

---

## 1. `merge`（团队协作的安全默认选项）

```bash
git config pull.rebase false
```

### 作用

* 创建一个**合并提交**
* 保留两个分支的*完整历史记录*

### 优点

* 非常安全
* 不会重写历史
* 适合协作场景

### 缺点

* 历史记录可能变得“混乱”（出现大量合并提交）

### 适用场景

* 团队协作
* 不希望重写历史记录
* 偏好显式的合并节点

---

## 2. `rebase`（保持线性历史——热门选择）

```bash
git config pull.rebase true
```

### 作用

* 将本地提交重新应用到更新后的远程分支顶端
* 生成**线性历史记录**

### 优点

* 清晰易读的历史记录
* 没有合并提交
* 现代工作流中普遍采用（GitHub、开源项目）

### 缺点

* 会在本地重写提交历史
* 若频繁出现冲突可能令人困惑
* 避免对共享/公共分支进行变基操作

### 适用场景

* 个人功能分支
* 希望保持历史记录整洁
* 熟悉冲突解决流程

---

## 3. `fast-forward only`（严格模式，生产流水线中最安全）

```bash
git config pull.ff only
```

### 作用

* 仅当不存在分叉时才允许拉取
* 若存在分叉 → Git 将拒绝拉取操作

### 优点

* 极其安全
* 防止意外合并/变基
* 保持严格线性历史

### 缺点

* 除非分支完全同步，否则常会失败
* 必须手动通过变基/合并解决

### 适用场景

* CI/CD 环境
* 严格的发布分支
* 强制要求保持历史整洁的团队

---

## 🔥 你应该如何选择？

基于典型的现代开发工作流：

### 👉 通用最佳建议：

```bash
git config --global pull.rebase true
```

原因：

* 保持历史记录整洁
* 适合个人开发及现代 GitHub 工作流
* 实践中灵活性最高

---

### 👉 若团队 Git 规范较宽松：

```bash
git config --global pull.rebase false
```

---

### 👉 若处于严格的生产/发布环境：

```bash
git config --global pull.ff only
```

---

## 💡 实用提示（重要）

无需全局固定设置——每次拉取时可单独指定：

```bash
git pull --rebase
git pull --no-rebase
git pull --ff-only
```

---

## 简易理解模型

* **merge** → “合并历史记录”
* **rebase** → “将我的工作重写至顶端”
* **ff-only** → “仅在无冲突时继续”

---

如果告知你的工作流类型（独立开发、团队协作、开源贡献等），我可以推荐更精确的配置方案和 Git 配置模板。
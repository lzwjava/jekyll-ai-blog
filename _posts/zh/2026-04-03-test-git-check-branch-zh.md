---
audio: false
generated: true
image: false
lang: en
layout: post
title: 同步分支
translated: false
type: note
---

**问题：**
如何在同步分支 A 的约 70 个 Angular 升级提交时，在多个分支 (B 和 C) 上协调一致的 `git cherry-pick` 策略，同时使用像 Copilot 这样的概率性 AI 助手并避免分歧？

**回答：**

你正在解决一个**带有 AI 在循环中的多分支回传问题**。核心问题不是 Git —— 而是**确定性**。
如果你在 B 和 C 上运行两次 AI，你会得到**不同的冲突解决**，这会导致**代码漂移**。

你需要**使过程确定性**，而不是基于提示的。

---

# 真正的问题

你当前：

* Cherry-pick A → B (AI resolves conflicts)
* Cherry-pick A → C (AI resolves conflicts again)
* Same prompt, but AI ≠ deterministic → results diverge

所以 B ≠ C 即使逻辑应该相同。

---

# 最佳解决方案（按排名）

## ✅ 最佳：创建中间“upgrade base”分支（确定性）

Instead of applying A→B and A→C separately:

```
          A (Angular 21)
         /
upgrade-base
       /   \
      B     C
```

### 步骤

### 1. 从共享祖先创建 base

```
git checkout common-ancestor
git checkout -b angular21-upgrade-base
```

### 2. 一次性 Cherry-pick 所有 70 个提交

```
git cherry-pick A~70..A
```

**一次**解决冲突（如果需要，使用 AI）

现在这个分支包含**规范性解决**

---

### 3. 将 base 合并到 B 和 C

```
git checkout B
git merge angular21-upgrade-base

git checkout C
git merge angular21-upgrade-base
```

现在：

* 相同的提交
* 相同的冲突解决
* 相同的文件结构
* 无分歧

这是**大公司进行大规模升级的方式**

---

## ✅ 第二最佳：使用 rerere（Git 记住冲突解决）

启用：

```
git config --global rerere.enabled true
```

然后：

1. Cherry-pick A → B
2. 手动/AI 解决冲突
3. Cherry-pick A → C

Git 自动应用**相同的冲突解决**

这非常强大。

Git 存储：

```
conflict input -> resolution output
```

所以第二个分支变得确定性。

---

## ✅ 第三：使用基于策略的 cherry-pick（自动化 yours/theirs）

你的规则：

```
tool/ -> theirs
business/logic -> ours
```

你可以自动化这个。

示例：

```
git cherry-pick -X theirs <commit>
```

或

```
git cherry-pick -X ours <commit>
```

但那是全局的 —— 你需要**基于路径的策略**

使用 `.gitattributes`

```
tool/** merge=theirs
business/** merge=ours
```

然后定义 merge drivers。

这完全消除了 AI 随机性。

---

## 你当前的方法（有什么问题）

你这样做：

```
git cherry-pick ca^..cb
AI fix
repeat
```

问题：

* AI 每次决策不同
* 批次大小改变上下文
* 冲突顺序改变
* 结果漂移

所以 B 和 C 分歧。

---

# 最健壮的工作流程（推荐）

### 步骤 1 —— 启用 rerere

```
git config --global rerere.enabled true
```

### 步骤 2 —— cherry-pick 到 B

```
git checkout B
git cherry-pick A~70..A
```

使用 AI 解决

---

### 步骤 3 —— cherry-pick 到 C

```
git checkout C
git cherry-pick A~70..A
```

Git 自动解决相同的冲突。

无分歧。

---

# 更好（企业方法）

使用**patch series 而非 cherry-pick**

```
git format-patch A~70..A
```

然后应用：

```
git am *.patch
```

应用到 B 和 C → 确定性。

---

# 超企业解决方案（适用于 1000+ 差异的最佳）

使用**stacked branches**

```
common-base
   ├── region-A-upgrade
   ├── region-B-upgrade
   └── region-C-upgrade
```

然后将每个分支 rebase 到相同的升级提交上。

这是这样做的：

* Chromium
* Android
* Linux kernel

处理大规模回传。

---

# 关键洞见

不要试图使**AI 确定性**
使**Git 确定性**，然后只使用一次 AI。

---

# 你的情况总结

你有：

* 2000 个共享提交
* 1000 个区域差异
* 70 个升级提交

最佳解决方案：

```
create angular21-base
apply once
merge into B and C
```

这保证：

* 相同的 Angular 升级
* 无漂移
* 相同行为
* 更少调试

---

# 额外提示（重要）

Cherry-pick **小批次**：

坏：

```
git cherry-pick 70 commits
```

好：

```
git cherry-pick 5 commits
```

冲突解决变得稳定。

---

# 最终推荐

使用这个组合：

1. 启用 rerere
2. cherry-pick 到 B
3. cherry-pick 到 C
4. 或创建 upgrade-base 分支

这完全消除了 AI 随机性。

---

References:

* [https://git-scm.com/docs/git-rerere](https://git-scm.com/docs/git-rerere)
* [https://git-scm.com/docs/git-cherry-pick](https://git-scm.com/docs/git-cherry-pick)
* [https://git-scm.com/docs/git-format-patch](https://git-scm.com/docs/git-format-patch)
* [https://git-scm.com/book/en/v2/Git-Tools-Rerere](https://git-scm.com/book/en/v2/Git-Tools-Rerere)

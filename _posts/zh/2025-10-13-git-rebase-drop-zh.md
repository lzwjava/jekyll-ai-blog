---
audio: false
generated: true
image: false
lang: zh
layout: post
model: openai/gpt-5
title: Git Rebase Drop 移除提交
translated: true
type: note
---

是的——完全正确。

当你在交互式 `git rebase -i` 中使用 **`drop`** 时，意味着 **“将该提交从历史记录中完全移除”**。

具体会发生以下情况：

* Git 在重放其他提交时会**跳过应用**该提交
* 最终分支看起来就像该提交**从未存在过**——其变更内容和提交信息都将消失
* 后续提交仍会被应用（只要它们不依赖于被移除的变更）

示例：

```bash
git rebase -i HEAD~4
```

你可能会看到类似内容：

```
pick a1b2c3d 修复拼写错误
pick b2c3d4e 添加README
pick c3d4e5f 实现登录功能
pick d4e5f6g 添加调试日志
```

若将最后一行改为：

```
drop d4e5f6g 添加调试日志
```

保存并关闭编辑器后，Git 将重新基于该分支并**排除该提交**。

因此没错——“drop”即表示**从分支历史记录中删除该提交**。

需要我说明这与 `revert`（会*撤销*提交但保留记录）的区别吗？

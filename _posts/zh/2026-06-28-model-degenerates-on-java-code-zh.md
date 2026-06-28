---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型在Java代码上的退化
translated: true
type: note
---

```java
import java.util.*;

public class 二叉搜索树 {
    private 节点 根节点;

    static class 节点 {
        int 键值;
        节点 左子节点, 右子节点;

        public 节点(int 项) {
            键值 = 项;
            左子节点 = 右子节点 = null;
        }
    }

    public 二叉搜索树() {
        根节点 = null;
    }

    void 插入(int 键值) {
        根节点 = 递归插入(根节点, 键值);
    }

    节点 递归插入(节点 根节点, int 键值) {
        if (根节点 == null) {
            根节点 = new 节点(键值);
            return 根节点;
        }
        if (键值 < 根节点.键值)
            根节点.左子节点 = 递归插入(根节点.左子节点, 键值);
        else if (键值 > 根节点.键值)
            根节点.右子节点 = 递归插入(根节点.右子节点, 键值);
        return 根节点;
    }

    void 中序遍历() {
        递归中序遍历(根节点);
    }

    void 递归中序遍历(节点 根节点) {
        if (根节点 != null) {
            递归中序遍历(根节点.左子节点);
            System.out.println(根节点.键值);
            递归中序遍历(根节点.右子节点);
        }
    }

    boolean 搜索(int 键值) {
```

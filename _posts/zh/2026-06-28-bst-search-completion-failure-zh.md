---
audio: false
generated: true
image: false
lang: zh
layout: post
title: BST搜索完成失败
translated: true
type: note
---

重要提示：在翻译Markdown内容时，请确保格式正确：

- 始终在标题（以#开头的行）和表格（以|开头的行）之间添加一个空行
- 保持正确的Markdown表格结构
- 保留所有原始格式和间距，除非格式规则要求更改
- 不要在翻译内容外围包裹Markdown代码块（```markdown或```）——内容将直接用于Kramdown的Jekyll中

翻译规则：

- 如果不确定，请勿翻译项目名称、公司名称或学校名称等特定项目
- 对于技术术语、新词和技术概念，保留英文不作翻译
- 中文翻译：专有名词和技术术语使用英文，而非中文音译
- 日文翻译：适当情况下技术术语使用英文，而非罗马字或片假名
- 所有语言：现代技术词汇、编程术语和品牌名称优先使用英文

以下是提示输入与模型输出的逐字对照：

=== 提示输入 (prompt_java.txt，第1-48行) ===

  import java.util.*;

  public class BinarySearchTree {
      private Node root;

      static class Node {
          int key;
          Node left, right;

          public Node(int item) {
              key = item;
              left = right = null;
          }
      }

      public BinarySearchTree() {
          root = null;
      }

      void insert(int key) {
          root = insertRec(root, key);
      }

      Node insertRec(Node root, int key) {
          if (root == null) {
              root = new Node(key);
              return root;
          }
          if (key < root.key)
              root.left = insertRec(root.left, key);
          else if (key > root.key)
              root.right = insertRec(root.right, key);
          return root;
      }

      void inorder() {
          inorderRec(root);
      }

      void inorderRec(Node root) {
          if (root != null) {
              inorderRec(root.left);
              System.out.println(root.key);
              inorderRec(root.right);
          }
      }

      boolean search(int key) {        <--- 提示在此结束

=== 模型续写 (300个新token，temp=0.8，top_k=200) ===

                   return;              <--- 垃圾内容立即开始
           }
       }
       public String get(String source)
           { return text;
        }
         }
                return true
 Property.TrveradataValue;
  }
    public Listi static
       {
            return new
}
 null;
           int()
(int) {
                 return new.Invalid(this.nameOf.Value);
        }
          this.value.n, this.v.S.S.S.S);
         }
             }
       return this.tree.GetAttribute(parent(this.name));

=== 结束 ===

提示（一个带有insert/inorder/search存根的完整BST）被原样重放。
随后在`boolean search(int key) {`之后，模型生成了：

- `return;` -- 语法正确但内容错误（search应当返回boolean）
- `public String get(String source)` -- 错误的方法，错误的类
- `Property.TrveradataValue` -- 非真实Java结构
- `this.v.S.S.S.S` -- 无意义的链式访问
- `this.tree.GetAttribute(parent(this.name))` -- 看起来像是某些DOM/JavaScript模式的泄露

模型显然从训练数据中记住了BST类，但无法连贯地完成search方法。

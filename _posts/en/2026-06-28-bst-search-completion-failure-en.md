---
audio: false
generated: true
image: false
lang: en
layout: post
title: BST Search Completion Failure
translated: false
type: note
---

Here's the exact prompt and response side by side:

=== PROMPT INPUT (prompt_java.txt, lines 1-48) ===

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

      boolean search(int key) {        <--- prompt ends here

=== MODEL CONTINUATION (300 new tokens, temp=0.8, top_k=200) ===

                   return;              <--- garbage start immediately
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

=== END ===

The prompt (a complete BST with insert/inorder/search stub) was replayed
verbatim. Then immediately after `boolean search(int key) {`, the model
produced:

  - `return;` -- valid Java syntax but wrong (search should return boolean)
  - `public String get(String source)` -- wrong method, wrong class
  - `Property.TrveradataValue` -- not a real Java construct
  - `this.v.S.S.S.S)` -- nonsensical chained access
  - `this.tree.GetAttribute(parent(this.name))` -- looks like some
    DOM/JavaScript pattern leaking in

The model clearly memorized the BST class from training data, but has
no ability to complete the search method coherently.

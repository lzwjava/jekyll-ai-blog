---
audio: false
generated: true
image: false
lang: en
layout: post
title: Model Degenerates on Java Code
translated: false
type: note
---

=== INPUT PROMPT (prompt_java.txt) ===

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

      boolean search(int key) {

=== MODEL OUTPUT (1000 new tokens, temp=0.8, top_k=200) ===

                   return;
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
                   }
                 if(i == this.name.First)(
                        return this.(this.left.Block.Type.RMap.S.x, type.M.Column.M.S., e, this.S.S.S.S
                             return;
                var = this..x.read.S.D.S.this.S.gl.S.S.S.S.;
                  }
                    ).
      public void()       {
               return;
             }
                }

                public var = false;
                 return newF.S.I.x.Gu2.S.S.S.S;
              }
             var.S.S.BufferType = array.S.S.S.S = null;
                     if (_cache.S.Py.S+1.S.S.0S.S, 0,
                                                     return instancethis.S.S.SType.Current;
             }
                   this.S.S.S.S.S.S{S.S.S.X.S.S];4, S.S.S.S.S.S.S.S.S.S;
                         }
                  ifS.S.S = !S.S.S.S.Sers.S.SRS.S.S.S.S, U.S.S.S.I) +S.S.S.S.S.S.S, 0,

=== END ===

Summary: prompt replay is clean (lines 1-48). Continuation immediately
falls apart — first ~20 tokens are garbled but Java-shaped, then it
enters the `S.S.S.S.S` degeneration loop and never recovers.

---
audio: false
generated: false
image: false
lang: zh
layout: post
title: Fletcher算法和Hamming 码问题
translated: true
type: post
---

这篇文章最初用中文写成并发布在CSDN上。

---

[问题链接](https://www.luogu.com.cn/problem/P1461)

问题要求找到字典序最小的 `n` 个数，使得任意两个数之间的汉明距离至少为 `d`。

汉明距离可以通过异或计算得到。`1^0=1`，`0^1=1`，`0^0=0`，`1^1=0`。因此，异或两个数会得到一个数，其中置位的比特位表示不同的位。然后可以计算异或结果中的置位数。

我曾经犯过一个错误，因为输出要求每行10个数，最后一行可能少于10个。我的初始输出在最后一行的最后一个数后面有一个尾随空格，后面跟一个换行符。

我认为这段代码是一种不错的函数式编程风格。优点是结构更清晰，使 `main` 看起来像 Lisp 或其他函数式语言中的顶级函数。

这样，我不需要创建一个新的 cpp 文件来测试不熟悉的函数或调试单个函数。我可以直接注释掉 `deal()` 并将 `main` 当作顶级的 REPL（读取-打印-求值-循环）。

Lisp 也教会我尽可能功能化地编程，FP！这样，每个函数都可以被提取和单独调试。语义也更清晰。例如：

`hamming(0, 7, 2)` 表示检查 0 和 7 的二进制表示是否至少有 2 个不同的位。7 是 `111`，所以它们有 3 个不同的位，函数返回 true。

所以，我可以注释掉 `deal()` 并添加 `hamming(0, 7, 2)` 来独立测试这个函数。

AC 代码：

```java
/*
{
ID: lzwjava1
PROG: hamming
LANG: C++
}
*/
#include<cstdio>
#include<cstring>
#include<math.h>
#include<stdlib.h>
#include<algorithm>
#include<ctime>
using namespace std;
const int maxn=1000;

bool hamming(int a,int b,int d)
{
 int c=a^b;
 int cnt=0;
 for(int i=0;i<=30;i++)
 {
  if((1<<i) & c)
  {
   cnt++;
   if(cnt>=d) return true;
  }
 }
 return false;
}

void printArr(int *A,int n)
{
 for(int i=0;i<n;i++)
 {
  printf("%d",A[i]);
  if((i+1)%10==0 || (i==n-1)) printf("\n");
  else printf(" ");
 }
}

bool atLesat(int *A,int cur,int i,int d)
{
 for(int j=0;j<cur;j++)
  if(!hamming(A[j],i,d))
   return false;
 return true;
}

void dfs(int *A,int cur,int n,int d)
{
 if(cur==n)
 {
  printArr(A,n);
  return;
 }
 int st=(cur==0? 0: A[cur-1]+1);
 for(int i=st;;i++)
 {
  if(atLesat(A,cur,i,d))
  {
   A[cur]=i;
   dfs(A,cur+1,n,d);
   return;
  }
 }
}

void deal()
{
 int n,b,d;
 scanf("%d%d%d",&n,&b,&d);
 int A[n];
 dfs(A,0,n,d);
}

int main()
{
  freopen("hamming.in","r",stdin);
  freopen("hamming.out","w",stdout);
 deal();
 //printf("%.2lf\n",(double)clock()/CLOCKS_PER_SEC);
  return 0;
}

/*
*/

```

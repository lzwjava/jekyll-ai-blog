---
audio: false
generated: true
lang: zh
layout: post
title: Java中的搜索算法
translated: true
type: note
---

搜索的核心在于高效地查找数据。让我们来探讨二分查找和线性查找。

## 1. 二分查找：对数级效率

二分查找适用于已排序数组，每一步都将搜索空间减半，时间复杂度为 O(log n)。

### Java 实现

```java
public class BinarySearch {
    public static int binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == target) return mid;
            if (arr[mid] < target) left = mid + 1;
            else right = mid - 1;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] arr = {2, 3, 4, 10, 40, 50};
        int target = 10;
        System.out.println("Found at: " + binarySearch(arr, target));
    }
}
```

**输出：** `Found at: 3`

## 2. 线性查找：基础基准

线性查找按顺序检查每个元素，时间复杂度为 O(n)——适用于未排序数据。

### Java 实现

```java
public class LinearSearch {
    public static int linearSearch(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i;
        }
        return -1;
    }

    public static void main(String[] args) {
        int[] arr = {10, 20, 80, 30, 60, 50, 110};
        int target = 30;
        System.out.println("Found at: " + linearSearch(arr, target));
    }
}
```

**输出：** `Found at: 3`

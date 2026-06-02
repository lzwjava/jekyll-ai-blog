---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Android活动启动生命周期序列
translated: true
type: note
---

正确答案是 **A. onCreate() → onStart() → onResume()**

### Android Activity 生命周期首次启动说明：

当 Activity 首次创建时（例如应用启动或用户跳转到新 Activity），系统会按以下固定顺序调用回调方法：

1. **onCreate()**
   - Activity 正在创建
   - 在此方法中设置布局（setContentView()）、初始化视图和准备核心组件
   - 此时 Activity 对用户不可见

2. **onStart()**
   - Activity 开始对用户可见
   - 此时界面已显示但尚未进入前台交互状态

3. **onResume()**
   - Activity 进入前台并完全进入交互状态
   - 此时 Activity 获得焦点并正常运行，用户可与其进行交互

因此正确顺序为：
**onCreate() → onStart() → onResume()**

其他选项错误原因：
- **B 和 C** 以 onStart() 或 onResume() 开头——这是不可能的，因为 onCreate() 必须首先执行
- **D** 将 onResume() 置于 onStart() 之前——顺序错误，onStart() 始终在 onResume() 之前执行

官方参考：[Android 开发者文档 - Activity 生命周期](https://developer.android.com/guide/components/activities/activity-lifecycle)

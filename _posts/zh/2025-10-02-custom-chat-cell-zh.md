---
audio: false
generated: true
image: false
lang: zh
layout: post
model: deepseek/deepseek-v3.2-exp
title: 自定义聊天会话表格单元格
translated: true
type: note
---

这是一个 Objective-C 实现的定制表格视图单元格，用于在聊天应用（如 iMessage 或 WhatsApp）中显示会话项。让我来解析关键组件：

## 概览
`LZConversationCell` 类创建的定制单元格可显示：
- 用户头像/图像
- 联系人姓名
- 最后消息预览
- 时间戳
- 未读消息徽章指示器

## 关键组件

### 1. 布局常量
```objc
static CGFloat kLZImageSize = 45;           // 头像尺寸
static CGFloat kLZVerticalSpacing = 8;      // 垂直内边距
static CGFloat kLZHorizontalSpacing = 10;   // 水平内边距
static CGFloat kLZTimestampeLabelWidth = 100; // 时间戳宽度
```

### 2. UI 元素
- **`avatarImageView`**: 用户头像（45x45 点）
- **`nameLabel`**: 联系人姓名显示
- **`messageTextLabel`**: 最后消息预览
- **`timestampLabel`**: 消息时间/日期
- **`litteBadgeView`**: 新消息小红点
- **`badgeView`**: 未读消息数字徽章

### 3. 单元格管理方法
- **`+dequeueOrCreateCellByTableView:`**: 标准表格视图单元格复用模式
- **`+registerCellToTableView:`**: 向表格视图注册单元格类
- **`+heightOfCell`**: 固定高度计算（61 点）

### 4. 布局设置
`setup` 方法：
- 根据比例计算标签高度
- 创建并定位所有子视图
- 使用基于帧的布局（非自动布局）

### 5. 帧计算
每个子视图相对于其他元素定位：
- 左侧头像固定间距
- 姓名和消息标签位于头像右侧
- 时间戳右对齐
- 徽章视图定位在头像上方

### 6. 内存管理
- **`prepareForReuse`**: 单元格回收时清除所有内容
- 所有子视图延迟初始化（仅在需要时创建）

## 使用模式
该单元格用于会话列表表格视图，可显示每个聊天会话的：
- 联系人信息
- 消息预览
- 已读/未读状态指示器
- 最后消息时间戳

该单元格遵循 iOS 设计模式，提供了消息应用中常见的视觉指示器。

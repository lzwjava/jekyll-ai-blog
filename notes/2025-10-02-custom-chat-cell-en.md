---
audio: false
generated: true
image: false
lang: en
layout: post
model: deepseek/deepseek-v3.2-exp
title: Custom Chat Conversation Table Cell
translated: false
type: note
---

This is an Objective-C implementation of a custom table view cell for displaying conversation items in a chat application (like iMessage or WhatsApp). Let me break down the key components:

## Overview

The `LZConversationCell` class creates a custom cell that displays:

- User avatar/image
- Contact name
- Last message preview
- Timestamp
- Badge indicators for unread messages

## Key Components

### 1. Layout Constants

```objc
static CGFloat kLZImageSize = 45;           // Avatar size
static CGFloat kLZVerticalSpacing = 8;      // Vertical padding
static CGFloat kLZHorizontalSpacing = 10;   // Horizontal padding
static CGFloat kLZTimestampeLabelWidth = 100; // Width for timestamp
```

### 2. UI Elements

- **`avatarImageView`**: User profile picture (45x45 points)
- **`nameLabel`**: Contact name display
- **`messageTextLabel`**: Last message preview
- **`timestampLabel`**: Message time/date
- **`litteBadgeView`**: Small red dot for new messages
- **`badgeView`**: Number badge for unread count

### 3. Cell Management Methods

- **`+dequeueOrCreateCellByTableView:`**: Standard table view cell reuse pattern
- **`+registerCellToTableView:`**: Registers cell class with table view
- **`+heightOfCell`**: Fixed height calculation (61 points)

### 4. Layout Setup

The `setup` method:

- Calculates label heights based on proportions
- Creates and positions all subviews
- Uses frame-based layout (no Auto Layout)

### 5. Frame Calculations

Each subview is positioned relative to others:

- Avatar on the left with fixed spacing
- Name and message labels to the right of avatar
- Timestamp aligned to the right edge
- Badge views positioned over the avatar

### 6. Memory Management

- **`prepareForReuse`**: Clears all content when cell is recycled
- Lazy initialization for all subviews (created only when needed)

## Usage Pattern

This cell would be used in a conversations list table view to display each chat conversation with:

- Contact info
- Message preview
- Read/unread status indicators
- Timestamp of last message

The cell follows iOS design patterns and provides visual indicators common in messaging apps.

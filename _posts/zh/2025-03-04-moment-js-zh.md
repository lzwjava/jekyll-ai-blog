---
audio: false
generated: true
lang: zh
layout: post
title: 在 JavaScript 中使用 Moment.js
translated: true
type: note
---

我将向你展示如何在 JavaScript 中使用 `moment` 和 `moment-timezone` 库。这些是处理日期和时间的常用库。

1. 首先，如果尚未安装，请先安装这些包：
```bash
npm install moment moment-timezone
```

2. 基础用法示例：

```javascript
// 导入库
const moment = require('moment');
const momentTimezone = require('moment-timezone');

// 基础 Moment.js 用法
// 当前日期和时间
const now = moment();
console.log(now.format('YYYY-MM-DD HH:mm:ss')); // 例如："2025-03-03 14:30:45"

// 解析特定日期
const date = moment('2025-12-25');
console.log(date.format('MMMM Do YYYY')); // "December 25th 2025"

// 操作日期
const tomorrow = moment().add(1, 'days');
console.log(tomorrow.format('ddd, MMM D')); // 例如："Tue, Mar 4"

// 使用 Moment-Timezone
// 获取特定时区的时间
const nyTime = momentTimezone.tz('America/New_York');
console.log(nyTime.format('YYYY-MM-DD HH:mm:ss z')); // 包含时区缩写

// 在时区之间转换时间
const localTime = moment();
const tokyoTime = localTime.clone().tz('Asia/Tokyo');
console.log(`本地时间: ${localTime.format('HH:mm')}`);
console.log(`东京时间: ${tokyoTime.format('HH:mm')}`);

// 列出所有可用时区
const timezones = momentTimezone.tz.names();
console.log(timezones); // 时区名称数组
```

常用格式化选项：
- `YYYY`：4位数年份（2025）
- `MM`：2位数月份（03）
- `DD`：2位数日期（03）
- `HH`：24小时制（14）
- `hh`：12小时制（02）
- `mm`：分钟（30）
- `ss`：秒（45）
- `z`：时区缩写

实用方法：
```javascript
// 日期操作
moment().add(7, 'days');     // 添加时间
moment().subtract(2, 'hours'); // 减去时间
moment().startOf('month');   // 周期开始
moment().endOf('month');     // 周期结束

// 日期比较
moment().isBefore(date);
moment().isAfter(date);
moment().isSame(date);

// 时区操作
momentTimezone.tz('2025-03-03', 'America/Los_Angeles');
momentTimezone.tz.guess(); // 猜测用户时区
```

注意事项：
1. 这些版本（^2.14.1 和 ^0.5.7）比较老旧（大约来自2016年）。除非有特定的兼容性要求，否则请考虑使用最新版本。
2. Moment.js 现在被视为处于维护模式的遗留项目。对于新项目，你可能需要考虑使用替代方案，如 `date-fns` 或 `luxon`。

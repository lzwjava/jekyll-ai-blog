---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 1582年十月消失的日子
translated: true
type: note
---

问题：为什么在1582年10月，iOS日历显示10月4日之后直接是10月15日，少了10天？

回答：

iOS日历（和许多其他数字日历）准确反映了一个真实的历史事件：1582年从 **Julian calendar** 到 **Gregorian calendar** 的过渡。

Julian calendar 由尤利乌斯·凯撒于公元前45年引入，它稍微高估了太阳年的长度（约11分钟）。几个世纪以来，这导致日历与季节脱节——最重要的是，春分（计算复活节的关键）比预期提前了。

到16世纪，这种偏差已经累积到大约 **10天**。为了纠正这一点，教皇格列高利十三世引入了 Gregorian calendar（我们今天仍在使用的日历）。改革内容：

- 跳过10天，使日历与太阳年重新对齐。
- 改变了闰年规则（只有能被400整除的世纪年才是闰年），以防止未来再次出现偏差。

这项改革于1582年开始在天主教国家实施：**1582年10月4日星期四** 之后立即是 **1582年10月15日星期五**。在这些地区，10月5日至14日这些日期在新系统中根本不存在。

选择10月作为跳过的月份是因为它主要宗教节日较少，从而将影响降到最低。

Apple的Calendar app精确地模拟了这一历史过渡，因此当你回溯到1582年10月时，它会从4日跳到15日——正如实际发生的那样。

参考资料:  

- [https://www.britannica.com/story/ten-days-that-vanished-the-switch-to-the-gregorian-calendar](https://www.britannica.com/story/ten-days-that-vanished-the-switch-to-the-gregorian-calendar)
- [https://en.wikipedia.org/wiki/Gregorian_calendar](https://en.wikipedia.org/wiki/Gregorian_calendar)
- [https://www.iflscience.com/why-october-is-missing-10-days-in-the-year-1582-on-your-phone-74872](https://www.iflscience.com/why-october-is-missing-10-days-in-the-year-1582-on-your-phone-74872)
- [https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/DatesAndTimes/Articles/dtHist.html](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/DatesAndTimes/Articles/dtHist.html) (Apple关于历史日历建模的文档)
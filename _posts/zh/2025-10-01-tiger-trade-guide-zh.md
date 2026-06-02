---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: 虎证交易App买卖指南
translated: true
type: note
---

### 如何在老虎证券全球版移动应用中显示买入/卖出功能

老虎证券应用（由老虎证券发布，在Google Play上又名Tiger Trade: Invest Globally或各地区应用商店的类似名称）支持交易美股、期权、ETF、期货等。截至2025年9月的最新版本为9.4.0.2，该版本增强了TigerAI分析功能及显示买卖趋势的股东功能[1]。

若要在应用中显示买入/卖出选项（假设您指的是股票或期权交易页面）：

1. **打开应用并定位股票**：
   - 在首页或市场页搜索股票（如AAPL）
   - 点击股票进入详情页，该页面包含图表、新闻和分析标签

2. **显示股票买卖按钮**：
   - 在股票页面滚动至底部或点击“交易”图标
   - 将出现买入和卖出按钮，可输入订单详情（如数量、市价单/限价单等订单类型）
   - 移动端应用图表上无持续显示的买卖悬浮按钮（与桌面端不同，桌面版可通过图表设置配置交易按钮[2]）

3. **显示期权买卖**：
   - 在股票页面点击“期权”标签查看期权链
   - 滚动选择到期日期，点击任一期权会显示隐含买卖操作的买/卖价（看涨/看跌期权的买入开仓，或持仓期权的卖出平仓[3][4]）
   - 若期权未显示买卖（如点击后列表空白），可能误选了“我的持仓”筛选器，需切换回期权链顶部的“全部期权”[4]

### 关于“每周投资”功能

应用中没有明确命名为“每周投资”或“AI每周投资”的功能，这可能指的是**自动投资**（亦称Tiger Invest）——针对美股和ETF的定期投资工具：

- 支持按固定周期（如每周）自动买入（非卖出），起始金额为2美元（或等值港币/其他货币），使用碎股交易[5]
- 访问路径：进入资产页 > 自动投资（或在应用菜单中搜索）
- 此功能不影响股票/页面的买卖显示，交易功能保持独立。若使用自动投资后买卖按钮消失，可重启应用或重新登录，可能是9.4.0.2版本的界面显示异常

若操作后按钮仍隐藏（如点击筛选器、图表切换或AI功能后），请检查：

- 确保账户资金充足且符合交易资格（老虎证券支持合格用户的碎股和期权交易[6]）
- 如TigerAI叠加层影响显示，可关闭该功能或切换图表时间周期
- 应用设置：点击个人资料 > 设置 > 检查显示选项（移动端无专门的买卖按钮开关）

如需进一步帮助，请访问老虎证券帮助中心或联系客服。若涉及桌面端Tiger Trade Windows/Mac版本，可通过选项 > 图表设置 > 交易启用图表交易按钮[2]。

引用来源：
[1] <https://apps.apple.com/nz/app/tiger-trade-buy-us-asx-shares/id1023600494>
[2] <https://support.tiger.com/english/windows/chart/chart-trading>
[3] <https://www.itiger.com/sg/help/detail/option-trading>
[4] <https://www.youtube.com/watch?v=5JKam5MP-nc>
[5] <https://www.itiger.com/nz/help/detail/15849694>
[6] <https://play.google.com/store/apps/details?id=com.tigerbrokers.stock&hl=en_US>

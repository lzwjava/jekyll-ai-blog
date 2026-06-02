---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 知识直播平台
translated: true
type: post
---

这是来自 GitHub 项目 [https://github.com/lzwjava/live-server](https://github.com/lzwjava/live-server) 的 README.md。

---

### Fun Live: 知识直播平台

* [live-server](https://github.com/lzwjava/live-server)
* [live-web](https://github.com/lzwjava/live-web)
* [live-mobile-web](https://github.com/lzwjava/live-mobile-web)

<div align="center">

<img src="./img/img1.jpg" width="300px" /><img/>

<img src="./img/img2.jpg" width="300px" /><img/>

</div>

![img3](./img/img3.jpg)

![img14](./img/img4.jpg)

Fun Live 是一个前沿的知识直播平台，旨在为用户提供各种学科的互动学习体验，包括编程和设计。通过 Fun Live，用户可以无缝参与直播讲座，通过费用或奖励贡献，并享受回放选项以增加便利。

#### 特性

* **直播讲座**: 实时访问涵盖广泛主题的知识讲座。
* **货币化选项**: 用户可以支付费用参加直播会议或奖励讲师的宝贵见解。
* **OBS 集成**: 讲师可以轻松使用 OBS 工具推送直播流，确保流畅的广播。
* **回放功能**: 享受实时参与讲座或稍后访问回放的灵活性。
* **无缝微信集成**: 无缝集成微信平台，包括通知功能以增强用户参与度。

#### 使用方法

1. 克隆仓库。
2. 在您喜欢的开发环境中打开项目。
3. 根据需要自定义和配置设置。
4. 将应用程序部署到您的服务器。
5. 开始直播有趣的知识讲座，让您的用户满意!

#### 统计

* **举办讲座**: 大约 80 场讲座举办。
* **用户基础**: 超过 30,000 名用户参与。
* **页面浏览量**: 产生数百万次页面浏览。

#### 文件结构

```
├── cache
│   └── index.html
├── config
│   ├── alipay.php
│   ├── autoload.php
│   ├── cacert.pem
│   ├── config.php
│   ├── constants.php
│   ├── database.php
│   ├── doctypes.php
│   ├── foreign_chars.php
│   ├── hooks.php
│   ├── index.html
│   ├── memcached.php
│   ├── migration.php
│   ├── mimes.php
│   ├── profiler.php
│   ├── rest.php
│   ├── routes.php
│   ├── smileys.php
│   └── user_agents.php
├── controllers
│   ├── Accounts.php
│   ├── Applications.php
│   ├── Attendances.php
│   ├── Charges.php
│   ├── Coupons.php
│   ├── Files.php
│   ├── Jobs.php
│   ├── LiveHooks.php
│   ├── LiveViews.php
│   ├── Lives.php
│   ├── Packets.php
│   ├── Qrcodes.php
│   ├── RecordedVideos.php
│   ├── Rest_server.php
│   ├── Rewards.php
│   ├── Shares.php
│   ├── Staffs.php
│   ├── Stats.php
│   ├── Subscribes.php
│   ├── Topics.php
│   ├── Users.php
│   ├── Videos.php
│   ├── Wechat.php
│   ├── WechatGroups.php
│   ├── Withdraws.php
│   └── index.html
├── core
│   ├── BaseController.php
│   └── index.html
├── data
│   ├── bjfudata.txt
│   └── iDev.json
├── helpers
│   ├── base_helper.php
│   └── index.html
├── hooks
│   └── index.html
├── id
├── index.html
├── language
│   ├── english
│   │   ├── index.html
│   │   └── rest_controller_lang.php
│   └── index.html
├── libraries
│   ├── Format.php
│   ├── JSSDK.php
│   ├── LeanCloud.php
│   ├── Pay.php
│   ├── QiniuLive.php
│   ├── REST_Controller.php
│   ├── Sms.php
│   ├── WeChatAppClient.php
│   ├── WeChatClient.php
│   ├── WeChatPlatform.php
│   ├── alipay
│   │   ├── Alipay.php
│   │   └── lib
│   │       ├── alipay_core.function.php
│   │       ├── alipay_notify.class.php
│   │       ├── alipay_rsa.function.php
│   ├── index.html
│   ├── wx
│   │   ├── WxPay.JsApiPay.php
│   │   ├── WxPay.php
│   │   ├── WxPayCallback.php
│   │   ├── cert
│   │   │   ├── ...
│   │   │   └── ...
│   │   └── lib
│   │       ├── WxPay.Api.php
│   │       ├── WxPay.Config.php
│   │       ├── WxPay.Data.php
│   │       ├── WxPay.Exception.php
│   │       └── WxPay.Notify.php
│   └── wxencrypt
│       ├── WxBizDataCrypt.php
│       ├── demo.php
│       ├── errorCode.php
│       └── pkcs7Encoder.php
├── logs
│   └── index.html
├── models
│   ├── AccountDao.php
│   ├── ApplicationDao.php
│   ├── AttendanceDao.php
│   ├── BaseDao.php
│   ├── ChargeDao.php
│   ├── CouponDao.php
│   ├── JobDao.php
│   ├── JobHelperDao.php
│   ├── LiveDao.php
│   ├── LiveViewDao.php
│   ├── PacketDao.php
│   ├── ParamDao.php
│   ├── PayNotifyDao.php
│   ├── QiniuDao.php
│   ├── RecordedVideoDao.php
│   ├── RewardDao.php
│   ├── ShareDao.php
│   ├── SnsUserDao.php
│   ├── StaffDao.php
│   ├── StatusDao.php
│   ├── SubscribeDao.php
│   ├── TopicDao.php
│   ├── TransactionDao.php
│   ├── UserDao.php
│   ├── UserPacketDao.php
│   ├── VideoDao.php
│   ├── WechatEventsDao.php
│   ├── WechatGroupDao.php
│   ├── WithdrawDao.php
│   ├── WxAppDao.php
│   ├── WxDao.php
│   ├── WxSessionDao.php
│   └── index.html
├── third_party
│   └── index.html
└── views
    ├── errors
    │   ├── cli
    │   │   ├── error_404.php
    │   │   ├── error_db.php
    │   │   ├── error_exception.php
    │   │   ├── error_general.php
    │   │   ├── error_php.php
    │   │   └── index.html
    │   ├── html
    │   │   ├── error_404.php
    │   │   ├── error_db.php
    │   │   ├── error_exception.php
    │   │   ├── error_general.php
    │   │   ├── error_php.php
    │   │   └── index.html
    │   └── index.html
    └── index.html
```

### 贡献者

| 提交 | 作者 |
| ------ | ---- |
|   555 | lzwjava|
|    28|  Liu-Sheng Xin|
|    24|  PegasusWang|
|    24 | wujunze|
|    18 | liushengxin|
|     5|  Anrika|
|     4  |Amast|

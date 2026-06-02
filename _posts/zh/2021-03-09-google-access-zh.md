---
audio: false
generated: false
image: true
lang: zh
layout: post
title: 如何访问谷歌
translated: true
type: post
---

这篇教程最初是用中文写的。

---

本节课内容涵盖：

1. 如何访问VPN服务的官方网站。
2. 如何在Windows上使用VPN。
3. Clash软件介绍。
3. 尝试打开Google、Twitter、YouTube和TikTok。

开始吧。以下是教小王访问Google的文字描述。

我们将使用一个名为“召唤师”的平台。网站地址是`https://zhshi.gitlab.io`。

<img src="/assets/images/google/zhs.png" alt="zhs" />

但是，它可能无法访问，因为它被防火墙屏蔽了。

![zhs_user](/assets/images/google/zhs_user.png)

这是登录后的样子。

实际上，绕过防火墙有两种方法。一种是购买我们自己的海外服务器。另一种是使用VPN平台，它提供许多海外服务器地址。

“绕过防火墙”意味着首先从国内访问海外服务器。然后，这个海外服务器可以访问被屏蔽的网站。

这样一个平台被称为“召唤师”。但是，如果官方网站无法访问，我们如何获得它提供的海外服务器地址呢？小王是第一次使用VPN，我远程教他。我该如何教他？

这时，我想到了让小王的Windows电脑绕过防火墙。我会给小王一个地址。然后小王就可以打开“召唤师”网站，注册账号，使用自己账号下的海外服务器地址。

![clash_win](/assets/images/google/clash_win.png)

![win_version](/assets/images/google/win_version.png)

接下来，检查你的电脑是64位还是32位。如果是64位，下载`Clash.for.Windows.Setup.0.14.8.exe`。如果是32位，下载`Clash.for.Windows.Setup.0.14.8.ia32.exe`。

小王的电脑是64位的。但是在他那边下载速度非常慢。所以我用我的电脑下载好，然后通过QQ邮箱发给他。

他从QQ邮箱下载，安装并打开。

![clash_win_exe](/assets/images/google/clash_win_exe.png)

我先给他我的Summoner配置地址。这个配置地址会下载一个包含许多VPN服务器地址的文件。在`Profiles`下粘贴地址并点击`Download`。

![zhs_url](/assets/images/google/zhs_url.png)

看，下载好了。注意上面的第二个配置。前面有一个绿色勾号，表示我们正在使用此配置。

![zhs_proxy](/assets/images/google/zhs_proxy.png)

接下来，打开`Proxies`选项卡。你会在这里看到一些东西。这些是`Clash`的一些配置。简单来说，就是国内网站不使用VPN，而国外网站使用。

注意`Proxy`的当前值为`DIRECT`，这意味着它是直接连接。我们将把它更改为一个节点。

![zhs_node](/assets/images/google/zhs_node.png)

我们选择了`US Rose`节点。

![clash_system](/assets/images/google/clash_system.png)

接下来，切换`System Proxy`设置以启用它。这意味着将`Clash`软件设置为系统的代理层。然后，系统的流量将首先到达`Clash`软件，然后访问外部网络。

<img src="/assets/images/google/google.png" alt="google" style="zoom:40%;" />

小王打开了Google。接下来，他尝试了TikTok、YouTube和Twitter。

好的，所以小王一直在使用我的Summoner账号。他如何注册呢？他需要打开Summoner官方网站。

<img src="/assets/images/google/zhs_register.png" alt="zhs_register" style="zoom:50%;" />

注册后，他发现充值购买服务需要一些步骤。这是我的账户截图。

![zeng](/assets/images/google/zeng.png)

它说需要绑定Telegram。

<img src="/assets/images/google/zhs_telegram.png" alt="zhs_telegram" style="zoom:50%;" />

小王去了Telegram网站并下载了Telegram Windows桌面版。

![telegram](/assets/images/google/telegram.png)

下载并安装后，注意上面的文字。

> 安装Telegram并注册后，点击与`小兔`或`城主`聊天，复制下面的二维码发送给他们，或者`点击此处自动复制代码并发送给Bot进行绑定`。

当你点击`小兔`时，它会自动跳转到`Telegram`软件并打开与`小兔`的聊天窗口。然后，把代码发送给他们。

![telegram_username](/assets/images/google/telegram_username.png)

但是，小王的`Telegram`账号是新注册的，没有`username`。这就像使用微信没有设置微信号一样。

找到Telegram菜单并设置它。然后，再次发送代码进行绑定。

<img src="/assets/images/google/zhs_set.png" alt="zhs_set" style="zoom:50%;" />

接下来，你可以捐赠以支持它。你可以先充值30元，使用两个月。

回到Summoner主页。在这里，找到“点击复制”按钮，获取地址，然后在`Clash`软件中下载配置。

然后小王就可以删除我给他的地址了。小王现在有了自己的Summoner账号。

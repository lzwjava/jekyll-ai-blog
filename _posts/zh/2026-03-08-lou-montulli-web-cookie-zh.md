---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 卢·蒙图利 网页Cookie先驱遗产
translated: true
type: note
---

问题：谁是 HTTP cookie 的发明者 Lou Montulli，他有哪些全面背景和遗产？

答案：

## Lou Montulli — Web Cookie 的发明者

---

### 早年生活和教育

Lou Montulli 于 1970 年出生于一个军人家庭，小时候在各个军队基地之间辗转，直至青少年时期在堪萨斯州定居。他出生在洛杉矶，其父在空军服役 23 年。他曾在美国各地生活——洛杉矶、阿尔伯克基、俄亥俄、纽约，最终他的家人搬到弗吉尼亚州的费尔法克斯，然后又迁至堪萨斯州的威奇托。他就读于 **University of Kansas**，最初学习电气和计算机工程，后来转到计算机科学专业。

---

### 早期职业生涯 — Lynx 浏览器

1991–1992 年，Montulli 在 University of Kansas 就读期间，与 Michael Grobe 和 Charles Rezac 共同编写了文本界面的网页浏览器 **Lynx**。这是最早的网页浏览器之一，如今仍处于积极维护和使用状态。

---

### 加入 Netscape

1994 年，Montulli 成为 **Netscape Communications** 的创始工程师（员工编号 9），并为 Netscape 网页浏览器的前几个版本编写了网络代码。除了 cookie 之外，他还发明了 **blink tag**、**server push**、**client pull**、**HTTP proxying**，以及浏览器中动画 GIF 的实现。

他是 **W3C HTML 工作组** 的创始成员，也是 **HTML 3.2 规范** 的贡献作者。他是 **World Wide Web Hall of Fame** 的成员。

---

### HTTP Cookie 的发明（1994 年）

#### 它解决的问题

Montulli 在 1994 年发明 cookie 时，他是 Netscape 的一名 23 岁工程师。当时早期网络面临一个紧迫问题：网站记忆力差。每次用户加载新页面时，网站都会将他们当作从未见过的陌生人对待，这使得无法构建购物车等功能来跟踪用户从一个页面到另一个页面。

#### 技术起源

“cookie”一词源自 **"magic cookie"**——程序接收并原样返回的数据包，这是 Unix 程序员使用的术语。Montulli 在 1994 年 6 月想到将其用于网络通信时，magic cookie 在计算领域已被使用。

正如 Montulli 本人所解释：“'cookies' 这个名字来自于几年前我读的一本旧操作系统手册中的软件技巧，这种技巧用于在用户和系统之间来回传递信息。不知为何，这种交换的小数据块被称为 'magic cookie'。”

#### 第一个 Cookie 代码

Montulli 在 1994 年秋天撰写的第一个历史性 cookie 代码片段如下：

`Set-Cookie: CUSTOMER=WILE_E_COYOTE; path=/; expires=Wednesday, 09-Nov-99 23:12:40 GMT`

这是他在 Netscape 作为首批员工之一撰写的一份简短标准文档的开篇语句。

#### MCI 购物车请求

Montulli 当时正在为 Netscape 客户 **MCI** 开发电子商务应用，MCI 实际上要求实现虚拟购物车——这是当时的新颖想法。他和他的团队设计了一种方法，让 Netscape 浏览器在网站访客的计算机上放置小文件来跟踪每个访客在该网站上的行为，从而让 MCI 无需在其自己的服务器上存储数据。

#### 以隐私为导向的设计

一个更简单的解决方案可能是为每个用户分配一个唯一的永久 ID 号，由他们的浏览器向访问的每个网站透露。但 Montulli 和 Netscape 团队 **拒绝了这个选项**，因为担心这会允许第三方跟踪人们的浏览活动。设计是故意的：cookie 只能被设置它的网站读取。

#### 专利

Montulli 在 1995 年申请了 cookie 技术的专利，美国专利 **5774670** 于 1998 年获得批准。Internet Explorer 在 1995 年 10 月发布的版本 2 中集成了对 cookie 的支持。

---

### 第三方 Cookie 问题和遗憾

两年内，广告商学会了本质上“破解”cookie 的方法，从而实现了 Montulli 试图避免的情况：跟踪人们在互联网上的活动。最终，他们创建了如今的 **基于 cookie 的广告定位** 系统。

1997 年，为了保护消费者隐私，一個工作组在最后努力试图阻止 cookie 用于广告跟踪，建议浏览器自动阻止第三方 cookie。但这一努力失败了，因为 Netscape 和微软的 Internet Explorer **接受了第三方 cookie**，尽管 Montulli 提出抗议。

Montulli 澄清道：“cookie 本身并不是坏东西——但 cookie 加上来自第三方的图像一起协作，允许广告跟踪器工作。”

如果今天 Montulli 要重新设计 cookie，他说：“基本设计会相同，但 **第三方 cookie 会被限定范围**，限定为第一方和第三方的组合，这样它们就不会像今天这样被滥用。”

---

### 监管影响

Montulli 在 1994 年撰写的那个小代码片段启发了多项国际监管法规，例如欧盟的 **2009 ePrivacy Directive**，该指令要求网络提供商在安装 cookie 前获得用户同意。

---

### 后期职业生涯

Netscape 之后，Montulli 创办并领导了多家公司：

- 他是 **Epinions.com** 的联合创始人，**Memory Matrix** 的 CEO（被 Shutterfly 收购），并担任 Shutterfly 的 **Vice President of Engineering**。
- 2008 年，他联合创办了云存储公司 **Zetta.net**。2015 年，他作为联合创始人和 CTO 加入 **JetInsight**。
- 2022 年，他因包括 HTTP cookie 和 Lynx 在内的重大技术贡献，被评为 **Hidden Heroes** 之一。

---

### Fishcam 彩蛋

在开发 Netscape 浏览器时，Montulli 构建了 **Fishcam**——最早的实时图像网站之一——它被著名地内置到 Netscape 浏览器的早期版本中作为彩蛋。Netscape 托管这个 fishcam 直到很久以后他们不再是 Netscape。

---

### 遗产

Lou Montulli 对 HTTP cookie 的发明重塑了整个网络体验——实现了登录持久性、购物车、个性化，最终催生了价值数十亿美元的在线广告行业。他的故事是一位注重隐私的工程师，其发明被远远超出原意的用途再利用，使他成为互联网历史上最具影响力和最具矛盾性的人物之一。

参考资料：

- [Lou Montulli and the invention of cookie | Hidden Heroes](https://hiddenheroes.netguru.com/lou-montulli)
- [Lou Montulli - Wikipedia](https://en.wikipedia.org/wiki/Lou_Montulli)
- [HTTP cookie - Wikipedia](https://en.wikipedia.org/wiki/HTTP_cookie)
- [The inventor of the digital cookie has some regrets - Quartz](https://qz.com/2000350/the-inventor-of-the-digital-cookie-has-some-regrets)
- [3 new insights from the inventor of website cookies - LiveIntent](https://www.liveintent.com/blog/3-new-insights-from-the-inventor-of-website-cookies-2/)
- [To understand where the cookie is headed, let's look at its history](https://digitalcontentnext.org/blog/2020/11/16/to-understand-where-the-cookie-is-headed-lets-look-at-its-history/)
- [An Interview With Lou Montulli | Internet History Podcast](https://www.internethistorypodcast.com/2014/03/chapter-1-supplemental-1-an-interview-with-lou-montulli/)
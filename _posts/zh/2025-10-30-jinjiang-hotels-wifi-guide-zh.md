---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 锦江酒店WiFi门户指南
translated: true
type: note
---

锦江酒店WiFi门户网站（https://portal.jinjianghotels.com.cn/）是专为现场接入设计的强制门户——在酒店网络外无法完全公开抓取，因此直接浏览常返回空白或错误页面。根据用户反馈和指南，以下是其典型的“路由”结构（即主要URL路径/端点）及接入方式。维也纳酒店（锦江旗下品牌）及国内类似连锁酒店均采用此模式。

### 主要路由与接入方式
- **主路由**：根路径 `/`（即 https://portal.jinjianghotels.com.cn/ 或 http://portal.jinjianghotels.com.cn/）
  - 当连接酒店WiFi后访问非HTTPS网站时，此着陆页面会自动加载
  - **接入步骤**：
    1. 将设备连接至酒店WiFi（如“ViennaHotel”“锦江之星Free”“Vienna_Free_WiFi”——初始无需密码）
    2. 打开浏览器访问任意HTTP网站（如 http://neverssl.com 或您首次查询中提到的本地网关IP http://172.16.16.1）
    3. 系统将重定向至门户根路径 `/` 页面。若未自动跳转，请手动输入 `http://172.16.16.1` 或门户URL（请使用HTTP协议，因强制门户常屏蔽HTTPS）
  - 页面为中文界面但操作简单：显示酒店品牌标识、使用条款和登录按钮，可使用浏览器翻译功能（如Chrome内置翻译）切换为英文

### 已知子路由/路径
该门户采用极简结构——主要为单页面应用，通过表单提交而非深层子路径。虽无公开文档列出所有端点，但根据用户视频和故障报告，常见路径包括：
- **短信登录路径**：通过根路径 `/` 上的表单处理（无独立 `/sms` 子路由，实际通过内部端点如 `/auth/sms` 发送POST请求）
  - **操作方式**：在主页面点击“短信验证”按钮，输入手机号（中国区为+86开头，国际号码需完整格式），接收短信验证码提交后即可认证，权限有效期为24小时
- **社交登录路径**：跳转至第三方端点的链接或内嵌框架，例如：
  - 微博/QQ登录：临时重定向至 `/oauth/weibo` 或 `/oauth/qq`（用于认证回调的子路由）
  - **操作方式**：在根页面点击对应社交按钮，将短暂跳转或弹出授权窗口
- **其他潜在子路由**（基于同类系统推断，未在锦江系统中确认）：
  - `/terms` 或 `/agreement`：查看完整条款（通常位于页面底部链接）
  - `/logout`：手动断开连接（较少使用）
  - 错误路径如 `/error` 或404页面（针对无效访问）

若需现场检查子路由（如用于开发工具），可在门户页面按F12打开浏览器开发者控制台——可能显示如短信提交接口 `/api/verify` 等AJAX调用

### 连接故障排除
- **无法重定向？** 清除浏览器缓存，忘记网络后重新连接，或短暂切换移动数据
- **国际手机号？** 多数号码支持但验证码可能延迟——可向前台索取公共验证码
- **安全提示**：所有流量均通过酒店网关（172.16.16.x 段）传输，建议登录后启用VPN

如需直观演示，可查看抖音短视频平台搜索“维也纳酒店 WiFi 登录”观看完整页面流程

参考资料：
[Reddit：中国酒店WiFi连接问题](https://www.reddit.com/r/travelchina/comments/1kjdngn/issues_with_wifi_connection/)
[抖音：维也纳酒店WiFi连接步骤](https://www.douyin.com/search/%E7%BB%B4%E4%B9%9F%E7%BA%B3%E9%85%92%E5%BA%97Wi-Fi%E8%BF%9E%E6%8E%A5%E6%AD%A5%E9%AA%A4)
[抖音：酒店无线网连接指南](https://www.douyin.com/search/%E9%85%92%E5%BA%97%E6%97%A0%E7%BA%BF%E7%BD%91%E6%80%8E%E4%B9%88%E8%BF%9E%E6%8E%A5)

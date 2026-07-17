---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信自动回复：仅支持订阅
translated: true
type: note
---

**问题：** 如何在微信公众号上设置（1）新关注感谢、（2）文章点赞/在看和（3）赞赏的自动回复？

**回答：**

只有第1项实际上可以通过官方API实现。第2项和第3项完全不向开发者开放——经查阅当前微信公众平台文档确认。

**1. 关注自动感谢——完全可以实现**

当有人关注时，微信会向配置的服务器URL推送一个`subscribe`事件。您可以在5秒内同步回复一个XML数据包（如果不想立即回复则返回空字符串）。

```python
from flask import Flask, request, Response
import time

app = Flask(__name__)

THANK_YOU_TEXT = "感谢关注！🙏"

@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        # 初始服务器配置时的签名验证
        return request.args.get("echostr", "")

    xml = request.data.decode("utf-8")
    from_user = extract(xml, "FromUserName")
    to_user = extract(xml, "ToUserName")
    event = extract(xml, "Event")

    if event == "subscribe":
        reply = f"""<xml>
<ToUserName><![CDATA[{from_user}]]></ToUserName>
<FromUserName><![CDATA[{to_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[{THANK_YOU_TEXT}]]></Content>
</xml>"""
        return Response(reply, mimetype="application/xml")

    return Response("success")  # 其他事件仅确认，不自动回复

def extract(xml, tag):
    import re
    m = re.search(f"<{tag}><!\\[CDATA\\[(.*?)\\]\\]></{tag}>", xml)
    return m.group(1) if m else ""
```

如果在公众平台后台开启了消息加密，则需要先对POST体进行AES解密——使用`wechatpy`（pip安装）可以干净地处理，无需手写XML解析：

```python
from wechatpy import parse_message, create_reply
from wechatpy.crypto import WeChatCrypto

crypto = WeChatCrypto(token, encoding_aes_key, app_id)
decrypted = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
msg = parse_message(decrypted)
if msg.type == "event" and msg.event == "subscribe":
    reply = create_reply(THANK_YOU_TEXT, msg)
    return Response(crypto.encrypt_message(reply.render(), nonce, timestamp))
```

**2. 文章点赞/在看——没有钩子**

推送规范中没有此类事件类型。微信服务器事件推送仅涵盖：`subscribe`/`unsubscribe`、`SCAN`、`LOCATION`、`CLICK`/`VIEW`（菜单）、模板消息状态等少数几种——文章上的点赞/在看完全是UI层面的遥测数据，腾讯根本不向公众号后端公开。也没有任何轮询端点。

**3. 赞赏——也没有钩子，而且根本不经过您的账户**

这是人们常常忽略的关键点：文章赞赏资金通过一个单独的“赞赏账户”小程序（T+7结算）直接结算到**作者的个人微信钱包**，而不是关联到公众号的商户账户。腾讯自己的文档对此描述为完全独立于开发者API的作者邀请流程——没有通知/回调，因为您的服务器从一开始就不在该支付路径中。

**如果您确实想要一个自己可控的赞赏流程，变通方法：** 不要使用原生文章赞赏。而是自行接入微信支付JSAPI/ Native下单（真实商户订单，而非文章赞赏组件）——这样您就能获得一个`notify_url`支付回调，然后可以通过`/cgi-bin/message/custom/send` API推送客服消息来感谢付款者。这是唯一接近“对赞赏自动回复”的途径。

参考资料：
- [消息与事件推送介绍 | 微信开放文档](https://developers.weixin.qq.com/doc/subscription/guide/dev/push/)
- [关注/取消关注事件 | 微信开放文档](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html)
- [公众号赞赏和喜欢作者功能介绍 | 微信开放社区](https://developers.weixin.qq.com/community/develop/article/doc/00004ed4f985800b65cdc33c85b413)
- [wechatpy docs](https://wechatpy.readthedocs.io/)
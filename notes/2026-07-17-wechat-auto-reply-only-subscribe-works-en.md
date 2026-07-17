---
audio: false
generated: true
image: false
lang: en
layout: post
title: "WeChat Auto-Reply: Only Subscribe Works"
translated: false
type: note
---

Question: How do I set up auto-reply for (1) new subscriber thanks, (2) article likes/"in-app reward" (点赞/在看), and (3) reward money (赞赏) on a WeChat Official Account (公众号)?

Answer:

Only #1 is actually possible through the official API. #2 and #3 are not exposed to developers at all — confirmed by checking the current WeChat MP docs.

**1. Subscribe (关注) auto-thanks — fully doable**

WeChat pushes a `subscribe` event to your configured server URL whenever someone follows. You reply synchronously within 5s with an XML payload (or empty string if you don't want to reply immediately).

```python
from flask import Flask, request, Response
import time

app = Flask(__name__)

THANK_YOU_TEXT = "Thanks for following! 🙏"

@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    if request.method == "GET":
        # signature verification for initial server config
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

    return Response("success")  # ack anything else, no auto-reply

def extract(xml, tag):
    import re
    m = re.search(f"<{tag}><!\\[CDATA\\[(.*?)\\]\\]></{tag}>", xml)
    return m.group(1) if m else ""
```

If message encryption is enabled in MP console, you'll also need to AES-decrypt the POST body first — `wechatpy` (pip) handles this cleanly instead of hand-rolling XML parsing:

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

**2. Article likes / "在看" — no hook exists**

There's no event type for this in the push spec. WeChat's server event pushes only cover: `subscribe`/`unsubscribe`, `SCAN`, `LOCATION`, `CLICK`/`VIEW` (menu), template-message status, and a few others — 点赞/在看 on articles is UI-only telemetry Tencent doesn't surface to the Official Account backend at all. There is no polling endpoint either.

**3. Reward money (赞赏) — also no hook, and it doesn't even go through your account**

This is the key thing people miss: article 赞赏 money settles directly to the **author's personal WeChat wallet** via a separate "赞赏账户" mini-program (T+7 settlement), not to your official-account-linked merchant account. Tencent's own docs on this describe it as an author-invitation flow entirely outside the developer API — there's no notify/callback because your server was never in that payment path to begin with.

**Workaround if you actually want a reward flow you control:** don't use native article 赞赏. Instead wire up your own WeChat Pay JSAPI/Native order (a real merchant order, not the article reward widget) — that *does* give you a `notify_url` payment callback, and from there you can push a customer-service message via the `/cgi-bin/message/custom/send` API to thank the payer. That's the only path to something resembling "auto-reply to reward."

References:

- [消息与事件推送介绍 | 微信开放文档](https://developers.weixin.qq.com/doc/subscription/guide/dev/push/)
- [关注/取消关注事件 | 微信开放文档](https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Receiving_event_pushes.html)
- [公众号赞赏和喜欢作者功能介绍 | 微信开放社区](https://developers.weixin.qq.com/community/develop/article/doc/00004ed4f985800b65cdc33c85b413)
- [wechatpy docs](https://wechatpy.readthedocs.io/)

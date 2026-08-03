---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Ultra Mobile：逗号被拒，@符号被接受
translated: true
type: note
---

问题：在 ultramobile.com 的密码字段中，`@` 可以作为特殊字符使用，但 `,`（逗号）不行吗？

答案：是的，这与他们的注册表单要求一致。Ultra Mobile 的密码策略（位于 `my.ultramobile.com/activation/enrollment`）为：至少 8 个字符，包含 1 个大写字母、1 个小写字母、1 个数字和 1 个特殊字符。

逗号不在大多数网站使用的标准“特殊字符”白名单中——它通常被限制，因为它是后端系统中常见的字段分隔符（CSV 导出、表单解析、SQL）。`@` 几乎总是能通过，因为它是一个“安全”的可打印符号，没有分隔符作用。因此，`,` 失败而 `@` 有效是预期行为，并非你的 bug。

如果你想确认他们接受哪些字符而不必逐个猜测：

```bash
# 在注册/重置页面的浏览器开发者工具控制台中快速暴力检查
for c in '!' '@' '#' '$' '%' '^' '&' '*' '(' ')' ',' '.' ';' ':' "'" '"'; do
  echo "try password: Abc12345${c}"
done
```

然后逐个提交并观察验证错误是否变为绿色——比盲目猜测更快。

关于“临时密码”问题：他们基于 SMS 的临时密码流程（`my.ultramobile.com/login/sms/temp`）是独立的——这是系统生成并通过短信发送的临时密码，让你登录，然后强制你设置符合上述规则的自己的密码。临时密码本身可能不遵循相同的特殊字符规则（它是系统生成的，不是用户输入的），因此在临时密码界面上测试特殊字符不会告诉你任何关于创建密码界面的规则——直接在“创建账户”/“设置新密码”表单上测试。

参考文献：
- [My Ultra Account – 注册页面](https://my.ultramobile.com/activation/enrollment)
- [通过短信发送密码](https://my.ultramobile.com/login/sms/temp)
---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Ultra Mobile: Comma Rejected, @ Accepted"
translated: false
type: note
---

Question: On ultramobile.com's password field, does `@` work as the special character but `,` (comma) doesn't?

Answer: Yes, that matches what their enrollment form requires. Ultra Mobile's password policy (at `my.ultramobile.com/activation/enrollment`) is: at least 8 characters, 1 uppercase, 1 lowercase, 1 number, and 1 special character.

Comma isn't in the standard "special character" whitelist most sites use — it's typically restricted because it's a common field-delimiter in backend systems (CSV exports, form parsing, SQL). `@` almost always passes because it's a "safe" printable symbol with no delimiter role. So `,` failing while `@` works is expected behavior, not a bug on your end.

If you want to confirm exactly which chars they accept without guessing one at a time:

```bash
# quick brute-check via browser devtools console on the signup/reset page
for c in '!' '@' '#' '$' '%' '^' '&' '*' '(' ')' ',' '.' ';' ':' "'" '"'; do
  echo "try password: Abc12345${c}"
done
```

Then submit each and watch for the validation error to flip green — faster than guessing blind.

On the "temp password" question: their SMS-based temp password flow (`my.ultramobile.com/login/sms/temp`) is separate — that's a system-generated temporary password sent via SMS to let you in, then you're forced to set your own password matching the rules above. The temp password itself may not follow the same special-char rules (it's system-generated, not user-typed), so testing special chars against the temp password screen won't tell you anything about the create-password screen's rules — test directly on the "Create Account" / "set new password" form instead.

References:
- [My Ultra Account – enrollment page](https://my.ultramobile.com/activation/enrollment)
- [Send Me a Password via SMS](https://my.ultramobile.com/login/sms/temp)

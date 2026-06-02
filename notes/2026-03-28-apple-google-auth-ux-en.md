---
audio: false
generated: true
image: false
lang: en
layout: post
title: Comparing Apple and Google Auth UX
translated: false
type: note
---

Question: Is Sign in with Apple better than Google Login on iOS due to not needing an extra browser? Does Android support Sign in with Apple? And regarding duplicate accounts when users mix up Apple and Google login — do we need to worry if both share the same email?

Answer:

## Sign in with Apple vs Google Login on iOS

You're right that **Sign in with Apple** on iOS feels more fluid. It uses native system APIs (Face ID / Touch ID) and does not need to open an external browser or Chrome Custom Tab. Google Sign-In on iOS, by contrast, redirects to a web-based flow, which introduces a brief context switch. So for iOS users, Apple Login does feel noticeably smoother.

---

## Does Android Support Sign in with Apple?

**Yes, but with caveats.**

You can use Sign in with Apple on participating apps and websites on other platforms like Android or Windows — it shows a secure, Apple-hosted webpage where you sign in to your Apple Account.

However, there's a key difference from iOS:

- On **iOS**, it uses native FaceID/TouchID with no browser pop-up.
- On **Android**, Apple Login works through a WebView dialog — similar to how Twitter and Facebook login work on Android. So it still requires a browser-like view, losing the "fluent, no extra browser" advantage that iOS users enjoy.

If you have to add Sign in with Apple to your iOS app, your users will need it on your Android app too — otherwise they won't be able to log in if they switch from iOS to Android. So if your app supports both platforms, you should implement it on Android as well, even though the experience is less seamless.

---

## The Duplicate Account Problem

This is a **real and well-known UX problem**. When Sign in with Apple is introduced into an existing application, many users who previously used other providers (like Google) may start using Apple Login instead — losing access to their original account's data. This scenario is known as user duplication.

Sometimes duplicated users can be detected if the accounts share a common attribute, such as a verified email address. However, Sign in with Apple gives users the option to hide their email address behind an alias unique to each app, so you cannot always rely on email matching.

This is the **critical catch** to your assumption:

### "If they share the same email, both methods can log in" — **NOT always true**

Apple has a **"Hide My Email"** feature. When a user chooses to hide their email, Apple generates a **random relay email** (like `abc123@privaterelay.appleid.com`) instead of sharing the real one. So:

| Scenario | Safe? |
|---|---|
| User uses Apple Login with real email shared | ✅ Same email → can be matched |
| User uses Apple Login with **Hide My Email** | ❌ Different email → creates duplicate account |
| User uses Google Login with their Gmail | ✅ Real email, matchable |

---

## Should You Worry? It Depends on the App

For **light-use, low-stakes apps** (e.g., a simple tool, a casual reader), having two separate accounts for the same user is generally harmless. The user can still use either account independently.

For **heavy-use apps with records** (e-commerce, order history, subscriptions, points, medical data), duplicate accounts are a serious issue — the user's history is split across two accounts and cannot easily be recovered.

### The recommended solution: **Account Linking**

Account linking allows users to link two accounts so they can use any of them to access the same user profile. This can prevent account duplication, reduce the risk of account lockout, and improve the login experience for multi-platform users.

The practical approach:

1. After login, check if the verified email already exists in your database.
2. If it does, prompt the user to **link** the new login method to the existing account.
3. If Apple's Hide My Email was used, you may need to ask the user to manually confirm their identity.

---

## Summary

| Topic | Key Point |
|---|---|
| Apple Login on iOS | Smooth, native, no browser |
| Apple Login on Android | Supported, but uses WebView (less smooth) |
| Duplicate account risk | Real risk, especially with "Hide My Email" |
| Same email = safe? | Only if the user shares their real email |
| Light-use apps | Tolerable even with two accounts |
| Heavy-use apps | Must implement account linking |

References:

- [Sign in with Apple - Apple Support](https://support.apple.com/en-us/102379)
- [Sign In with Apple on Android (Firebase)](https://firebase.google.com/docs/auth/android/apple)
- [Sign in with Apple Button for Android (GitHub)](https://github.com/willowtreeapps/sign-in-with-apple-button-android)
- [Account Linking to Improve Sign in with Apple Experience (Auth0)](https://auth0.com/blog/improving-the-sign-in-with-apple-experience-with-account-linking/)

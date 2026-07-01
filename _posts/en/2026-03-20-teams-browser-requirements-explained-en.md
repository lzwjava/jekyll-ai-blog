---
audio: false
generated: true
image: false
lang: en
layout: post
title: Microsoft Teams Approved Browser Requirements Explained
translated: false
type: note
---

**Question:** When your organization requires you to install an "approved browser" to view a Microsoft Teams link — common in large corporations — what does that mean, how do you fix it, what browsers are approved, and why does iOS Safari not work?

---

**Answer:**

## Why You're Seeing "Install an Approved Browser"

This message comes from **Microsoft Entra ID (Azure AD) Conditional Access policies** that large enterprises enforce. When your IT/security team configures a policy requiring an "approved client app" or "app protection policy," access to Microsoft 365 resources — including Teams — is blocked unless you are using a browser or app that Microsoft officially recognizes as compliant and manageable through Intune.

Safari is supported for device-based Conditional Access on a managed device, but it **cannot satisfy** the "Require approved client app" or "Require app protection policy" conditions. A managed browser like Microsoft Edge satisfies approved client app and app protection policy requirements. On iOS with non-Microsoft MDM solutions, only the Microsoft Edge browser supports device policy.

This is the core reason iOS Safari fails — it simply cannot pass these enterprise compliance checks, regardless of how up-to-date it is.

---

## What Are the "Approved" Browsers?

Teams on the web client is available on **Microsoft Edge**, **Chrome**, **Firefox**, and **Safari** browsers — but only when running on a **desktop computer**.

However, for corporate Conditional Access policies specifically, the hierarchy is:

| Browser | Desktop Support | iOS/Mobile | Passes "Approved App" Policy |
| --- | --- | --- | --- |
| **Microsoft Edge** | ✅ Full | ✅ (Intune-managed) | ✅ Yes |
| **Google Chrome** | ✅ Full | ❌ No web Teams | ⚠️ Partial |
| **Firefox** | ✅ Full | ❌ No | ⚠️ Partial |
| **Safari (macOS)** | ✅ With issues | ❌ Not supported | ❌ No |
| **iOS Safari** | N/A | ❌ Not supported | ❌ No |

Microsoft recommends using **Google Chrome** or **Microsoft Edge** to access Microsoft 365 online apps, including Teams. Known issues have been noted with Safari on Apple computers and Firefox on macOS/Windows.

---

## How to Fix It (By Scenario)

### ✅ Fix 1: On Desktop/Laptop — Use Microsoft Edge or Chrome

The simplest fix. Open the Teams link in the latest version of **Microsoft Edge** (preferred for corporate SSO) or **Google Chrome**. For cookies, you may also need to allow third-party cookies for Microsoft Teams URLs in your browser's Privacy and Security settings.

### ✅ Fix 2: On iOS — Install Microsoft Teams Mobile App

Teams for web is **not currently supported on mobile devices**. To use Teams on a mobile device, you must download the **Teams mobile app**. This is the official solution for iOS users.

### ✅ Fix 3: On iOS (Corporate-Managed) — Use Microsoft Edge for iOS

Microsoft Edge for iOS is recognized as a managed/approved browser, so it can satisfy conditional access grant controls. Other non-Microsoft apps are redirected to Edge to complete authentication. If your IT team has enrolled your iPhone in Intune (MDM), installing **Microsoft Edge for iOS** and signing in with your corporate account may allow access.

### ✅ Fix 4: Contact IT / Request an Exemption

In a corporate or academic setting, IT administrators might enforce specific sign-in methods or restrict external meeting links. If you suspect a policy is interfering, contact your IT department to confirm whether you have the necessary permissions to join external or public Teams meetings.

### ✅ Fix 5 (Admin): Review the Conditional Access Policy

Organizations must transition Conditional Access policies that use "Require approved client app" to also include "Require app protection policy" by **June 30, 2026**. Microsoft will stop enforcing the older "Require approved client app" grant control after that date. IT admins should review these policies and ensure they aren't inadvertently locking out valid users.

---

## Why iOS Safari Specifically Fails

iOS (and iPadOS) browsers are fundamentally limited:

1. All iOS browsers — Edge, Safari, Chrome, Firefox — present a page saying "Your browser version isn't supported. Quickest solution? Download the mobile app." This applies universally across iOS browsers for the web client.

2. As of mid-2025, Teams is no longer installable as a PWA via Safari. Official Microsoft documentation now only lists **Edge and Chrome** as supported browsers for installing Teams as a PWA.

3. On top of that, enterprise Conditional Access policies require the browser to pass Intune app protection checks — something only Edge for iOS can do on Apple mobile devices.

---

## Summary

The **correct approved browsers** for corporate Microsoft Teams access are:

- **Desktop**: Microsoft Edge (best for SSO), Google Chrome, Firefox
- **iOS/iPhone**: Microsoft Teams app (official), or Microsoft Edge for iOS (Intune-managed)
- **iOS Safari**: Not supported — use the Teams app instead

---

**References:**

- [Microsoft Learn: Teams for Web — Overview and Prerequisites](https://learn.microsoft.com/en-us/microsoftteams/teams-client-web)
- [Microsoft Learn: Conditional Access Conditions (Browser support)](https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-conditional-access-conditions)
- [Microsoft Learn: Migrate Approved Client App Policy](https://learn.microsoft.com/en-us/entra/identity/conditional-access/migrate-approved-client-app)
- [Microsoft Q&A: Teams is not supported on any iOS browser](https://learn.microsoft.com/en-us/answers/questions/4382369/teams-is-not-supported-on-any-ios-browser)
- [Microsoft Q&A: Did Microsoft remove Safari support for Teams PWA?](https://learn.microsoft.com/en-us/answers/questions/5518049/did-microsoft-remove-safari-support-for-teams-pwa)
- [Microsoft Learn: Troubleshooting Teams sign-in loops](https://learn.microsoft.com/en-us/troubleshoot/microsoftteams/teams-sign-in/sign-in-loop)

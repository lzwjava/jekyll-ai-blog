---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resolving SHL TalentCentral 500 Error
translated: false
type: note
---

Question: How can I fix the SHL TalentCentral 500 error during the `tcplus` auto-login integration?

Answer:

The detailed error message shows that the problem occurs in **SHL TalentCentral’s auto-login API**, specifically here:

```
POST /epl/api/v1/auth/auto-login
message: "Unable to apply response reuse for candidate on amcat"
status: 500
```

This means the **server failed to process your auto-login request** for your candidate account (possibly due to AMCAT integration or session handling). Since this is a **server-side issue**, there’s limited control from your end, but there are workarounds:

---

### 1. **Bypass Auto-Login**

* Instead of relying on auto-login, open the main TalentCentral login page:
  [https://talentcentral-experience.shlglobal.cn](https://talentcentral-experience.shlglobal.cn)
* Log in manually with the credentials or the email link you received.
* This avoids the `tcplus integration flow` which is failing.

---

### 2. **Browser Cleanup**

* **Clear cookies and cache** for the SHL domain.
* Try **incognito/private mode**.
* Disable extensions like ad blockers or script blockers.

---

### 3. **Network Considerations**

* Avoid corporate VPNs or proxies that might interfere with the API request.
* Use a stable home network.

---

### 4. **Wait and Retry**

* The 500 error might be a temporary server issue or deployment problem on SHL’s side.
* Waiting a few minutes or hours sometimes resolves it automatically.

---

### 5. **Contact SHL Support**

If manual login or retry fails:

* Email or call SHL support, providing:

  * Exact error message and timestamp
  * Your candidate ID (from the invitation email)
  * Screenshot of the console log
* Ask them to **reset your session** or generate a **new direct login link**.

---

### 6. **Technical Notes**

* `Unable to apply response reuse for candidate on amcat` suggests **session token reuse failed**. This is internal logic in SHL for candidates linked to AMCAT tests. Only SHL can fix it if the server keeps failing.

---

**Bottom line:** The fastest workaround is **manual login through the main portal** or asking HR to provide a **fresh login link**. If the issue persists across browsers and networks, it’s **100% a server-side fix** needed from SHL.

---

References:

* [SHL Support](https://www.shl.com/en/support/)
* [HTTP 500 Error Explanation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500)

---

If you want, I can give a **step-by-step procedure to safely bypass the auto-login API error and access the portal immediately**. Do you want me to do that?

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Ghostty Blocks gcloud OAuth Redirect
translated: false
type: note
---

**Question:** Why does `gcloud auth login` get stuck in Ghostty after clicking "Yes" on the Google portal (localhost:83xx redirect), while it works fine in iTerm on macOS?

**Answer:**

This is a known compatibility issue with some newer or less common terminal emulators (including Ghostty) on macOS when handling the OAuth loopback redirect for tools like `gcloud auth login`.

The Google Cloud SDK starts a tiny local web server on a random high port (often 8085, 8184, or in your case something in the 8300 range) to receive the authorization code from the browser redirect. After you approve in the Google consent screen, the browser redirects to `http://localhost:<port>/?code=...`, and the terminal's local server needs to receive that HTTP request to complete authentication.

In iTerm (and the default Terminal.app), this works reliably because they properly allow incoming loopback connections or don't interfere with the socket. In Ghostty, the redirect often fails to reach the local server — the terminal appears stuck (waiting forever), even though the browser may show a success page or error like "connection refused."

### Common causes and fixes

1. **Quickest workaround (recommended first)**
   Use the non-browser flow:

   ```
   gcloud auth login --no-launch-browser
   ```

   This prints a long URL. Copy-paste it into your browser, approve, then copy the final redirect URL (or the code if shown) back into the terminal prompt. This bypasses the local server entirely and works in any terminal.

2. **Alternative one-liner flow (if the above feels annoying)**

   ```
   gcloud auth application-default login --no-launch-browser
   ```

   (for ADC credentials — often what people actually need), or combine with scripting if you do this often.

3. **Other things to check / try**
   - Make sure no other process is using the specific port (rare, since it's random):

     ```
     lsof -i :83xx   # replace with your actual port if you see it
     ```

   - Try changing your default browser temporarily (some users report Safari vs Chrome differences, though usually not the root cause here).
   - Update Ghostty to the absolute latest version — newer builds sometimes fix quirks with loopback handling or child process I/O.
   - If you're comfortable, test with `--browser` flag explicitly (though unlikely to help):

     ```
     gcloud auth login --browser="/Applications/Safari.app"
     ```

4. **Long-term**
   This is likely a Ghostty-specific bug (or macOS socket/permissions interaction). You can search/report it on the Ghostty GitHub repo (mitchellh/ghostty) with details like your macOS version, Ghostty version, and exact behavior — similar localhost/socket issues have appeared in other tools (e.g. GitHub CLI, Gemini CLI).

Most users in this situation just use `--no-launch-browser` and it solves the problem immediately.

**References:**

- [https://stackoverflow.com/questions/71912626/gcloud-auth-login-localhost-redirect-failed](https://stackoverflow.com/questions/71912626/gcloud-auth-login-localhost-redirect-failed)
- [https://groups.google.com/g/google-cloud-sdk/c/-GLEhSaDHoM](https://groups.google.com/g/google-cloud-sdk/c/-GLEhSaDHoM)
- [https://github.com/google-gemini/gemini-cli/issues/2547](https://github.com/google-gemini/gemini-cli/issues/2547) (similar localhost OAuth stuck issue in another CLI on macOS)

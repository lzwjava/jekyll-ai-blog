---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Desktop Recording: Higher Information Leak Risk"
translated: false
type: note
---

Question: Is recording or shooting videos on a computer/laptop dangerous because it can easily leak information compared with a mobile phone home screen?

Answer:

Yes, that risk is real. In many situations, recording your computer screen is **more likely to expose sensitive information** than recording a mobile phone screen.

Common things that accidentally appear during a desktop recording include:

* Browser tabs revealing websites, work projects, or personal interests
* Bookmarks and browsing history
* Password managers and autofill suggestions
* Email notifications
* Chat applications such as Telegram, WeChat, Slack, Discord, etc.
* Source code repositories and company documents
* Cloud storage folders
* Meeting invitations and calendars
* API keys, tokens, SSH keys, and server addresses
* Personal files visible on the desktop
* Account names and email addresses

A few specific examples:

| Situation                                | Possible Leak                                     |
| ---------------------------------------- | ------------------------------------------------- |
| Sharing browser screen                   | Open tabs, bookmarks, logged-in accounts          |
| Recording software development work      | Internal code, company secrets, credentials       |
| Showing file explorer                    | Customer names, project names, confidential files |
| Receiving notifications during recording | Private messages, emails, OTP codes               |
| Telegram/WeChat open in background       | Private conversations, group memberships          |

Regarding Telegram groups, yes, if you are a member of groups discussing politics, activism, or criticism of governments, accidentally exposing those group names during a screen recording could reveal information about your interests or affiliations.

However, mobile phones are **not automatically safe** either. A phone recording can still expose:

* WeChat conversations
* Contacts
* Photos
* Notes
* Banking apps
* Password manager apps
* Location information
* Notification previews

The difference is that mobile operating systems typically show only one app at a time, while desktop operating systems often display many windows, tabs, notifications, and background applications simultaneously.

For professional screen recordings, people often:

1. Create a separate user account for recording.
2. Use a clean browser profile.
3. Disable notifications.
4. Close messaging apps.
5. Hide bookmarks and browser tabs.
6. Remove sensitive desktop files.
7. Record inside a virtual machine.
8. Review the video before publishing.

For software engineers, the biggest risks are usually:

* Browser tabs
* Terminal windows
* Git repository URLs
* API keys
* Chat applications
* Internal company documents

Many public data leaks have happened simply because someone shared a screenshot or screen recording without noticing sensitive information in the background. A few seconds of footage can reveal much more than people expect.

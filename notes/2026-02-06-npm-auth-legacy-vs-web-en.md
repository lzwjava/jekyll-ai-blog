---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: npm Authentication Legacy vs Web Flow
translated: false
type: note
---

npm has two authentication types that determine how you log in and manage credentials:

## `auth-type=legacy`

This is the traditional authentication method where npm stores your credentials locally in plaintext in your `.npmrc` file. When you run `npm login`, it prompts you for your username, password, and email, then stores an auth token directly in `.npmrc` like this:

```
//registry.npmjs.org/:_authToken=npm_xxxxxxxxxxxxx
```

The token is saved in your home directory's `.npmrc` file and used for all subsequent authenticated requests to the registry. This works well for automated systems and CI/CD pipelines where you need a simple token-based approach.

## `auth-type=web` (default since npm 9)

This is the modern browser-based authentication flow. When you run `npm login`, it:

1. Opens your default web browser
2. Takes you to npmjs.com's login page
3. You authenticate through the website (supporting 2FA, SSO, etc.)
4. The website sends the auth token back to your npm CLI
5. The token is stored in `.npmrc` just like with legacy auth

This method is more secure because your password never touches the command line, and it supports more sophisticated authentication methods like single sign-on and multi-factor authentication.

You can configure which method to use in your `.npmrc`:

```
auth-type=web    # or legacy
```

Most users should use `web` unless they're setting up automation where interactive browser login isn't possible.

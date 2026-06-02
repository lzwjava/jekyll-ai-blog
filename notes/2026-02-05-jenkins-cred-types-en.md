---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: Jenkins Credential Types Explained Simply
translated: false
type: note
---

Yes, that's correct! Jenkins credentials support multiple authentication types:

## Username and Password

- **Username with password** - Traditional credentials where you provide both a username and password
- Stored securely in Jenkins' credential store
- Common for basic authentication scenarios

## Token/Secret Text

- **Secret text** - For storing single secret values like API tokens, OAuth tokens, or access keys
- **Secret file** - For storing credential files like SSH keys or certificates

## Other Authentication Types

Jenkins also supports:

- **SSH Username with private key** - For SSH-based authentication
- **Certificate** - For certificate-based authentication
- **Username with password** (can also be used for username + personal access token in many cases)

## Using Tokens as Passwords

Many modern systems (like GitHub, GitLab, Bitbucket) now prefer personal access tokens over passwords. You can typically use these in two ways:

1. **Username with password credential** - Use your username and put the token in the password field
2. **Secret text credential** - Store just the token if the system only needs the token

For example, with GitHub:

- Username: your-github-username
- Password: ghp_yourPersonalAccessToken

The choice depends on what the system you're authenticating with requires. Would you like help setting up a specific type of credential in Jenkins?

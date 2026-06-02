---
audio: false
generated: true
image: false
lang: en
layout: post
title: Microsoft's Git Credential Manager Guide
translated: false
type: note
---

This is **Git Credential Manager (GCM)** — Microsoft's official secure Git credential helper, version 2.8.0.

What it is:

  A cross-platform (Windows/macOS/Linux) .NET application that handles Git authentication
  over HTTPS. When you `git push` or `git pull` and Git needs credentials, GCM intercepts
  that request and handles OAuth/device-code/browser-based auth flows for you.

Key facts:

  - Language:     C# (.NET 8, solution: Git-Credential-Manager.sln)
  - Repository:   github.com/git-credential-manager/git-credential-manager
  - Entry point:  src/shared/Git-Credential-Manager/Program.cs
  - UI framework: Avalonia (cross-platform GUI for auth prompts)

Architecture:

  Program.Main creates a CommandContext, registers 5 host providers (each with priority),
  then runs the app:

    Normal priority:
      - AzureReposHostProvider   (Azure DevOps)
      - BitbucketHostProvider    (Bitbucket)
      - GitHubHostProvider       (GitHub)
      - GitLabHostProvider       (GitLab)

    Low priority (fallback):
      - GenericHostProvider      (any HTTPS remote with username/password)

  The HostProviderRegistry selects the right provider by querying each in priority order
  against the Git credential input arguments (hostname, protocol, etc.).

Project structure:

  src/
    shared/                        Cross-platform core
      Core/                        Core abstractions (IHostProvider, HostProviderRegistry, etc.)
      Git-Credential-Manager/      Main entry point + app wiring
      GitHub/                      GitHub OAuth device-code flow
      GitLab/                      GitLab OAuth
      Atlassian.Bitbucket/         Bitbucket OAuth
      Microsoft.AzureRepos/        Azure DevOps auth
      GitHub.UI.Avalonia/          GitHub-specific Avalonia UI
      TestInfrastructure/          Shared test mocks
    windows/                       Windows installer (Inno Setup)
    linux/                         Linux packaging
    osx/                           macOS installer

It replaces the older Git Credential Manager for Windows (.NET Framework) and
Git Credential Manager for Mac and Linux (Java) with a single .NET codebase.

Relevant to you: you already use a Git credential manager — this is the upstream
source of that tool. If you ever need to debug auth issues with HTTPS remotes
(especially through your mihomo proxy), this is the code Git calls.

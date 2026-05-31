---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微软的 Git 凭据管理器指南
translated: true
type: note
---

这是 **Git Credential Manager (GCM)** — 微软官方安全 Git 凭据助手，版本 2.8.0。

功能概述：

  一款跨平台（Windows/macOS/Linux）的 .NET 应用程序，用于处理 Git 的 HTTPS 身份验证。  
  当你执行 `git push` 或 `git pull`，而 Git 需要凭据时，GCM 会拦截该请求，并为你处理基于 OAuth、设备码或浏览器的身份验证流程。

关键信息：

  - 语言：        C#（.NET 8，解决方案：Git-Credential-Manager.sln）
  - 仓库：        github.com/git-credential-manager/git-credential-manager
  - 入口点：      src/shared/Git-Credential-Manager/Program.cs
  - 界面框架：    Avalonia（跨平台 GUI，用于身份验证提示）

架构：

  Program.Main 创建 CommandContext，注册 5 个主机提供程序（各有优先级），然后运行应用：

    正常优先级：
      - AzureReposHostProvider   （Azure DevOps）
      - BitbucketHostProvider    （Bitbucket）
      - GitHubHostProvider       （GitHub）
      - GitLabHostProvider       （GitLab）

    低优先级（回退）：
      - GenericHostProvider      （任何需要用户名/密码的 HTTPS 远程仓库）

  HostProviderRegistry 根据 Git 凭据输入参数（主机名、协议等），按优先级顺序查询每个提供程序，并选择合适的提供程序。

项目结构：

  src/
    shared/                        跨平台核心
      Core/                        核心抽象（IHostProvider、HostProviderRegistry 等）
      Git-Credential-Manager/      主入口点 + 应用配置
      GitHub/                      GitHub OAuth 设备码流程
      GitLab/                      GitLab OAuth
      Atlassian.Bitbucket/         Bitbucket OAuth
      Microsoft.AzureRepos/        Azure DevOps 身份验证
      GitHub.UI.Avalonia/          专用于 GitHub 的 Avalonia UI
      TestInfrastructure/          共享测试模拟
    windows/                       Windows 安装程序（Inno Setup）
    linux/                         Linux 打包
    osx/                           macOS 安装程序

它用统一的 .NET 代码库替代了旧版的 Windows 版 Git Credential Manager（.NET Framework）以及 Mac 和 Linux 版 Git Credential Manager（Java）。

与你相关：你已经在使用 Git 凭据管理器——这正是该工具的上游源代码。如果你需要调试 HTTPS 远程仓库（尤其是通过你的 mihomo 代理）的身份验证问题，Git 调用的正是这段代码。
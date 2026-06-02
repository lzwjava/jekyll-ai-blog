---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在部署代码前进行备份
translated: true
type: note
---

问题：在将新代码或包部署到生产服务器时，在替换旧文件/包之前备份它们是一种好的做法吗？

答案：

是的，在部署期间保留旧版本几乎总是被认为是一种最佳实践，这样如果出现问题，您可以快速安全地回滚。

包含保留/备份旧版本的常见安全部署策略：

- **蓝绿部署（Blue-green deployments）** – 您保持旧（蓝色）环境完全不变，同时启动新（绿色）环境，然后切换流量。通过切换回来即可实现即时回滚。
- **带版本目录的滚动部署（Rolling deployments with versioned directories）** – 将新代码部署到 `/app/v2025.12.05-01`，更新软链接 `/app/current` → 新版本。旧目录保留在磁盘上，直到您在验证后手动删除它。
- **不可变工件 + 原子切换（Immutable artifacts + atomic switches）** – 构建新的容器镜像或包，与旧镜像或包并行部署，然后更新负载均衡器或服务管理器以指向新的。旧镜像/版本保持可用。
- **覆盖前的简单备份（Simple backup before overwrite）** – 即使在基本设置中（scp/ftp/rsync），首先将当前应用程序目录复制到 `.bak` 或带时间戳的文件夹：

  ```bash
  cp -r /var/www/myapp /var/www/myapp.bak.$(date +%Y%m%d-%H%M%S)
  ```

  或者

  ```bash
  tar czf /backups/myapp-$(date +%Y%m%d-%H%M%S).tgz /var/www/myapp
  ```

为什么您几乎不应该在没有回滚路径的情况下盲目覆盖部署：

- 单个语法错误或缺少依赖项可能会导致整个服务宕机。
- 配置错误或不兼容的数据库迁移很常见。
- 只有当旧代码仍然存在且可运行时，才能实现零停机回滚。
- 许多组织中的合规性/审计要求明确要求经过验证的回滚能力。

您可以跳过显式备份（但仍可回滚）的例外情况：

- 您正在使用 Kubernetes 并进行适当的 Deployment 回滚（`kubectl rollout undo`）。
- 您正在使用 Heroku、Vercel、Netlify 或 Cloud Run 等平台，它们会自动保留以前的版本。
- 基于 Git 的部署（例如，GitHub Actions 通过服务器上的 `git pull` 进行部署），您可以简单地 `git checkout` 之前的提交。

即使在这些情况下，大多数成熟的团队仍然会保留至少一些以前的工件/镜像几天。

底线：切勿在没有快速、经过测试的方法来恢复到正在运行的版本的情况下，通过永久删除或覆盖它来进行部署。保留备份或旧版本目录是一种廉价的保险。

参考资料：

- [The Twelve-Factor App – Deploy](https://12factor.net/)
- [Martin Fowler – BlueGreenDeployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Google SRE Book – Reliable Deployments (Chapter 27)](https://sre.google/sre-book/)

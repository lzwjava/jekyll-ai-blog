---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-code-fast-1
title: Clash代理继任者与Linux支持
translated: true
type: note
---

Clash是一款基于规则的代理工具，与Shadowsocks类似，其原始代码库于2023年因中国监管压力被作者删除。社区通过分支项目和继任者持续开发，其中Clash.Meta（现正式更名为Mihomo）被广泛认为是最可靠且积极维护的替代方案。它支持Linux二进制文件（包括Ubuntu），具备DNS over HTTPS（DoH）、隧道传输和基于规则的路由等功能。

针对Linux/Ubuntu用户，我推荐以下主延续项目。以下是基于社区采用度、更新频率和Linux支持度的顶级选项汇总：

### 推荐代码库

- **MetaCubeX/mihomo（Clash.Meta核心）**：作为Clash的主要继任者，在原项目删除后由社区分支维护。提供完整的代理功能、频繁更新以及适用于Linux（x86_64和arm64架构）的预编译二进制文件。其Ubuntu兼容性极佳，二进制文件已在18.04+版本通过测试。该项目开源、无广告，支持通过YAML配置文件高度定制。
  - GitHub：<https://github.com/MetaCubeX/mihomo>
  - 可靠性依据：超过1.4万星标，活跃社区，二进制文件包含用于路由的GeoIP数据库。发布页提供Linux CLI二进制文件直链。
  - Ubuntu安装指南：从发布页下载最新"mihomo-linux-amd64"二进制文件，添加执行权限（`chmod +x mihomo`）后运行。需配合包含代理规则的config.yaml配置文件。[1][2]
  - 备选方案：
    - **CarlDegio/verge**：基于Tauri开发的Clash.Meta图形界面封装，为Linux（含Ubuntu）提供直观控制面板。底层依赖Mihomo保障稳定性。
      - GitHub：<https://github.com/CarlDegio/verge>
      - 可靠性依据：支持桌面图形界面，超2000星标，便捷配置切换和系统托盘图标。Ubuntu用户可下载AppImage格式安装包。[3]
    - **chen08209/FlClash**：基于Clash.Meta的多平台客户端（含Linux二进制文件）。主打简洁设计与无广告体验，提供直观配置界面。
      - GitHub：<https://github.com/chen08209/FlClash>
      - 可靠性依据：轻量级应用，通过deb/AppImage格式支持Ubuntu，集成Mihomo内核。[4]
  - 历史版本备份：Kuingsmile/clash-core提供删除前核心的归档版本，内含Linux历史版本下载，适合需要未维护但具历史意义版本的用户。[5]

### 补充说明

- **安装提示**：确保系统具备libc（glibc 2.17+）环境。建议使用`systemd`或`screen`等工具实现后台服务运行。下载后请校验SHA256哈希值确保安全。
- **可靠性标准**：所列代码库均保持活跃贡献、拥有大量用户群体（高星标/分支数），规避了2023年后项目弃养风险。Clash.Premin（可能为Premium笔误）属付费分支但开源性较弱。
- **法律使用提醒**：Clash用于突破网络审查，在受限地区使用可能引起关注，请确保符合当地法律法规。
- 若需图形界面或特定功能（如多平台支持），verge或FlClash比核心Mihomo命令行版本更易用。详细信息请查阅各代码库的README文档。若遇问题，Mihomo代码库提供详尽说明文档。[6][7][1][8]

若以上方案均不适用或需要Ubuntu分步指南，请提供更多具体需求！

引用来源：
[1] <https://github.com/djoeni/Clash.Meta>
[2] <https://discussion.fedoraproject.org/t/rhbz-2305079-review-request-clash-meta-a-rule-based-network-proxy-tool-aka-mihomo/146312>
[3] <https://github.com/CarlDegio/verge>
[4] <https://github.com/chen08209/FlClash>
[5] <https://github.com/Kuingsmile/clash-core/releases>
[6] <https://github.com/fengwz17/Clash-For-Ubuntu>
[7] <https://news.ycombinator.com/item?id=38126160>
[8] <https://github.com/hiddify/Clash.Meta>

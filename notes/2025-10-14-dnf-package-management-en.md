---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: DNF Package Management in RHEL
translated: false
type: note
---

### Introduction to DNF in Red Hat Enterprise Linux

DNF (Dandified YUM) is the primary package management tool in Red Hat Enterprise Linux (RHEL), starting from RHEL 8 and continuing in RHEL 9. It serves as the successor to the older YUM (Yellowdog Updater, Modified) tool, offering improved performance, better dependency resolution, and support for modular content. In RHEL, DNF handles the installation, updating, and removal of software packages distributed via RPM (Red Hat Package Manager) repositories. It ensures access to essential content sets like BaseOS (for core OS functionality) and AppStream (for user-space applications, runtimes, and tools), all managed through your RHEL subscription.

DNF's purpose is to simplify software lifecycle management while maintaining system stability. It allows administrators and users to work with traditional RPM packages alongside modern modular formats, where components like languages or databases can have multiple parallel versions (called "streams") without disrupting the base OS.

#### Key Features

- **Modular Content Support**: Manages modules (groups of related RPMs), streams (version-specific repositories), and profiles (pre-configured package sets for specific use cases, e.g., web server or development environment).
- **Repository Handling**: Enables searching, enabling/disabling repos, and configuring sources like BaseOS, AppStream, and supplementary ones.
- **Installation and Updates**: Automatically resolves dependencies when installing packages, groups, or entire modules; supports checking for updates, upgrading specific packages, or the whole system.
- **Removal and Rollback**: Safely removes software and provides transaction history for undoing changes.
- **Customization and Automation**: Configurable via `/etc/dnf/dnf.conf` for exclusions, plugins, or caching; integrates with tools like DNF Automatic for scheduled updates.
- **Backward Compatibility**: The `yum` command is aliased to `dnf` in RHEL, easing the transition from older versions.

To get started, basic commands include `dnf install <package>` for installation, `dnf update` for upgrades, and `dnf search <term>` for finding software. For more advanced usage, refer to the official documentation.

[Red Hat Enterprise Linux 9: Managing Software with the DNF Tool](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html-single/managing_software_with_the_dnf_tool/index)

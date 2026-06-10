---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缩小ML包构建
translated: true
type: note
---

已完成！以下是操作详情：

发布版本：<https://github.com/lzwjava/ww/releases/tag/v0.1.0>

已完成的工作：

1. 从构建产物中排除 ww/ml/ 目录  
   - ww/ml/ 目录包含 133MB 的机器学习数据集/模型（.h5、.pkl.gz、.csv、.wav）  
   - 在 pyproject.toml 中添加了 hatch 构建配置以排除该目录  
   - Wheel 包大小：87MB → 713KB，源码包（sdist）大小：87MB → 687KB

2. 创建了 GitHub Actions 发布工作流  
   - 文件：.github/workflows/release.yml  
   - 触发条件：标签推送（v*）  
   - 使用 uv build 构建 Wheel 和源码包  
   - 创建 GitHub release，并自动生成发布说明  
   - 将 .whl 和 .tar.gz 文件作为可下载附件上传

3. 发布了 v0.1.0 版本  
   - 创建并推送了标签 v0.1.0  
   - 由 github-actions[bot] 创建了包含两个制品的 release

用户安装方式：

# 从 GitHub release 下载 .whl 文件安装

  pip install ww-0.1.0-py3-none-any.whl

# 或直接从仓库安装

  pip install git+<https://github.com/lzwjava/ww.git@v0.1.0>

未来发布 —— 只需更新 pyproject.toml 中的版本号并打标签：

# 将 pyproject.toml 中的版本号改为 0.2.0，然后提交，接着

  git tag v0.2.0
  git push origin main --tags

工作流会自动构建并发布 release。

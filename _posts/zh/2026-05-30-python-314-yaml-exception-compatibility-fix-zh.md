---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python 3.14 YAML 异常兼容性修复
translated: true
type: note
---

Test run complete. 以下是摘要：

```
Results: 339 passed, 1 failed (out of 340 tests)
Time:    4.25 seconds
```

单个失败：

```
FAILED tests/cloud/test_ec2.py::TestGetEc2Instances::test_unexpected_error
```

**根本原因：** 在 `ww/cloud/ec2.py:25` 中，`except yaml.YAMLError` 子句在 Python 3.14 上触发了 `TypeError`——在该版本中，`yaml.YAMLError` 不再继承自 `BaseException`。测试模拟了 `subprocess.run` 抛出 `RuntimeError("unexpected")`，该错误既未被现有的 `except subprocess.CalledProcessError` 捕获，也未被 `except yaml.YAMLError` 捕获，而后者本身还会引发异常。

这是 YAML 库异常层次结构在 Python 3.14 上的兼容性问题。快速修复方法如下：

1. 在现有异常捕获子句之后添加一个裸的 `except Exception` 子句，或者
2. 将 `pyyaml` 升级到兼容 3.14 的版本。

其余所有测试（339 个）均顺利通过。

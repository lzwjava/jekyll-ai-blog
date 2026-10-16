---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 近视逆转Flutter应用
translated: true
type: note
---

完成。我在 `/Users/lzwjava/projects/myopia-reversal` 构建了一个完整的 Flutter 应用（Android + iOS），并已提交到 git。

## 构建内容

「Myopia Reversal」——*在完全处方基础上低配 1.50D 舒适日常眼镜使用* 的配套应用：

### 📷 扫描验光单并记录（Premium）
- 相机界面拍摄验光单，或从相册导入
- Google ML Kit OCR（中文**和**拉丁文字），支持 EXIF 方向标准化以及旋转/重新扫描
- 启发式解析器检测 OD/右 和 OS/左 标记，并分离 球镜/柱镜/视力 值，同时处理小数（`-3.50`）和整数（`350`）格式——由单元测试覆盖
- 预览界面显示解析后的值以及原始 OCR 文本；用户在保存到历史记录前进行确认/更正

### 💳 应用内购买
- 通过 `in_app_purchase`（`com.lzwjava.myopia.premium`）一次性解锁 Premium，支持恢复购买 + 本地持久化
- 门控：OCR 扫描、进度图表、无限记录（免费版 = 10 条）、完整指南（免费版 = 1 篇文章）

### 其他功能
- **处方历史** — 添加/编辑/删除记录，可切换 `350°` 与 `-3.50` 显示
- **进度图表** — 每只眼睛的近视 + 散光（fl_chart），进度指导（约 0.25 D/季度）
- **低度矫正计算器** — 日常眼镜（−1.50 D）、驾驶眼镜（全矫），以及多焦点渐进设计（远用 −1.00 D / 近用 −1.75 D）
- **指南** — 8 篇文章总结方法、机制和作者 3 年的数据；可植入示例历程数据
- SQLite 存储，Material 3 浅色/深色主题，主页/历史/指南/设置标签页

## 验证
- `flutter analyze` 无警告，所有测试通过
- ✅ `flutter build apk --debug`（Android；为 JDK 21 将 AGP 升级到 8.2.1，添加了 desugaring 和 CAMERA 权限）
- ✅ `flutter build ios --no-codesign`（修复了损坏的 CocoaPods，将部署目标设为 15.5 以支持 ML Kit）

## 让 Unlock 按钮在真实商店中生效
在 App Store Connect 和 Google Play Console 中创建 id 为 `com.lzwjava.myopia.premium` 的非消耗型产品（可在 `lib/config.dart` 中更改）。详见 README。请注意，扫描仪 OCR 的准确性取决于验光单的质量——预览步骤可涵盖 OCR 错误。
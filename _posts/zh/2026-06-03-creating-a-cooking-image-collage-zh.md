---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 制作烹饪图片拼贴
translated: true
type: note
---

以下是我一步步完成的过程：

## 1. 素材发现

阅读 `original/2024-12-29-cooking-en.md` 后发现图片位于两个目录：

- `assets/images/cooking/` — 22 个文件（c1, c2, cooking1-11, porridge1-9）
- `assets/images/airfryer/` — 7 个文件（s1-s7）

## 2. 图片选择（9 张图片，3 个类别）

为体现多样性，挑选了 9 张图片：

- **炒菜/菜肴**：cooking1（牛肉小炒）、cooking2（红烧鱼）、cooking4（青椒炒锅）
- **粥品**：porridge1（肉丸粥）、porridge2（砂锅粥）、porridge3（电饭煲鱼片粥）
- **空气炸锅**：s1（薯条）、s3（鸡翅）、s5（烤鸡）

## 3. 图片合并 —— ImageMagick `montage`

核心工具是 ImageMagick 的 `montage` 命令，分两个阶段：

**阶段 A —— 将所有 9 张图统一调整为 400x400：**

```bash
for img in cooking1.jpg cooking2.jpg cooking4.jpg porridge1.jpg porridge2.jpg porridge3.jpg s1.jpg s3.jpg s5.jpg; do
  magick "$img" -resize 400x400^ -gravity center -extent 400x400 "/tmp/cooking_tiles/$name"
done
```

- `-resize 400x400^` —— 缩放使**较短边**达到 400 像素（`^` 表示“至少这么大”）
- `-gravity center -extent 400x400` —— 从中心裁剪至精确的 400x400

**阶段 B —— 合成 3x3 网格：**

```bash
magick montage \
  tile1.jpg tile2.jpg ... tile9.jpg \
  -tile 3x3 -geometry 400x400+4+4 -background white \
  cooking_collage.jpg
```

- `-tile 3x3` —— 3 列，3 行
- `-geometry 400x400+4+4` —— 每个单元格 400x400，图片之间留 4px 间距
- `-background white` —— 间距用白色填充

**为什么分两个阶段？** 在此 ImageMagick 构建版本（带有“Freetype delegate”警告）中，`montage` 的 geometry 参数无法可靠地缩放源图片。预先调整尺寸能保证统一的网格单元。

## 4. 压缩

原始拼贴图大小为 595KB，超过了预提交的 500KB 限制。通过以下命令解决：

```bash
magick cooking_collage.jpg -quality 80 cooking_collage.jpg
```

结果：359KB，通过检查。

## 5. 撰写章节

将内容添加到作品集“Passed Courses”和“What's Next”之间 —— 一个简洁的章节涵盖：

- 空气炸锅作为主要工具
- 粥品和炒菜技能
- 烹饪与编程的类比（相同工序适用于类似项目，操作顺序至关重要）
- 拼贴图及 Jekyll 兼容的居中/标题标记

## 使用的工具汇总

| 步骤 | 工具 | 命令 |
| ------ | ------ | --------- |
| 调整尺寸 | ImageMagick `magick` | `-resize 400x400^ -gravity center -extent 400x400` |
| 合成 | ImageMagick `montage` | `-tile 3x3 -geometry 400x400+4+4` |
| 压缩 | ImageMagick `magick` | `-quality 80` |
| 编辑 | `patch` 工具 | 在 .md 文件中查找替换 |
| Git | `gh` CLI | 提交、推送、`gh workflow run` |

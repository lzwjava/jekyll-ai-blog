---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 从Apple开发证书中提取团队ID
translated: true
type: note
---

以下是使用您信息编辑后的方法：

1. 查找您的签名身份：

   security find-identity -v -p codesigning

   输出：
   "Apple Development: <您的邮箱> (<身份哈希>)"

2. 从证书中提取 Team ID（OU 字段）：

   security find-certificate -c "Apple Development: <您的邮箱>" -p \
     | openssl x509 -noout -subject

   输出格式：
   subject= /UID=<UID>/CN=Apple Development: <邮箱> (<哈希>)/OU=<团队 ID>/O=<名称>/C=<国家>

   其中 OU= 的值就是您的 Team ID。

或者用单行命令直接提取 Team ID：

   security find-certificate -c "Apple Development" -p \
     | openssl x509 -noout -subject \
     | grep -o 'OU=[^/]*' | cut -d= -f2
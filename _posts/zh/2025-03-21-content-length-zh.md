---
audio: false
generated: true
lang: zh
layout: post
title: HTTP Content-Length 标头
translated: true
type: note
---

HTTP协议中**Content-Length**标头的单位是**字节**。

在HTTP协议中，**Content-Length**标头用于指示服务器向客户端发送的响应体大小。该大小以十进制数字表示消息体的字节数（或称八位组，1个八位组等于8位）。根据HTTP/1.1规范（RFC 7230第3.3.2节），**Content-Length**标头字段明确规定了消息体大小的八位组计量单位，这确认了其单位是字节。

例如，在标头显示`'content-length': '130700923'`的情况下，这表示响应体长度为**130,700,923字节**。为便于理解，这大约相当于**124.6兆字节(MB)**（因为1MB约等于1,048,576字节，即2^20字节）。对于HTTP响应中的大型文件或数据传输而言，这是一个合理的尺寸。

进一步说明：
- 该值为整数而非小数，排除了直接使用千字节或兆字节作为单位的可能性
- HTTP协议中消息体以字节序列形式传输，**Content-Length**对应客户端应接收的确切字节数
- 即使在HTTP/2等使用分帧传输替代单一**Content-Length**标头的版本中，有效载荷大小仍以字节计量

因此，HTTP协议中**Content-Length**的单位明确是**字节**。

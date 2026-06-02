---
audio: false
generated: true
lang: en
layout: post
title: HTTP Content-Length Header
translated: false
type: note
---

The unit of the **Content-Length** header in the HTTP protocol is **bytes**.

In HTTP, the **Content-Length** header is used to indicate the size of the response body that the server is sending to the client. This size is specified as a decimal number representing the number of bytes (or octets, where one octet equals 8 bits) in the message body. According to the HTTP/1.1 specification (RFC 7230, Section 3.3.2), the **Content-Length** header field explicitly states the size of the message body in octets, which confirms that the unit is bytes.

For example, in the provided case where the header is `'content-length': '130700923'`, this means the response body is **130,700,923 bytes** long. To give a sense of scale, this is approximately **124.6 megabytes (MB)**, since 1 MB is roughly 1,048,576 bytes (2^20 bytes). This is a plausible size for a large file or data transfer in an HTTP response.

To clarify further:
- The value is an integer, not a fractional number, ruling out units like kilobytes or megabytes directly.
- In HTTP, the body is transmitted as a sequence of bytes, and **Content-Length** corresponds to the exact number of bytes the client should expect.
- Even in other versions like HTTP/2, where framing is used instead of a single **Content-Length** header, the payload size is still measured in bytes.

Thus, the unit of **Content-Length** in the HTTP protocol is unequivocally **bytes**.

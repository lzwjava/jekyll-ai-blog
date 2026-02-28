---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP Reliability Flow and Connection Basics
translated: false
type: note
---

Question: Organize this transcript from the YouTube video, keeping the original text as much as possible while making it more coherent.

Answer: 

Here is an organized and cleaned-up version of the available transcript from the video "3.5-1 TCP Reliability, Flow Control, and Connection Management" (Part 1) by Jim Kurose. The original spoken text is preserved as closely as possible (including minor repetitions and natural speech patterns), but it has been formatted into coherent paragraphs, with removed excessive spacing/artifacts from the raw extraction, and minor punctuation added for readability. This covers the portion of the lecture captured in available sources (the video appears to be longer, but this is the extracted content).

**Introduction to TCP Reliable Data Transfer**

In this section we're going to take a look at how TCP provides reliable data transfer. We'll see that TCP uses all of the mechanisms that we studied earlier: checksums, acknowledgments, sequence numbers, timeout and retransmit, as well as pipelining. We'll also take a look at how TCP estimates the round-trip time between the sender and receiver and how it uses that to set the timeout interval. We'll also examine a number of TCP scenarios, looking at the TCP sender and receiver in action. So let's get started.

**TCP Overview and Semantics**

As we've seen, TCP operates in a point-to-point manner — that is, between one sender and one receiver. The semantics of its reliable data transfer is that of an in-order byte stream. We should contrast that with UDP, where UDP is message-oriented. What TCP implements is a reliable byte stream abstraction.

TCP is also full duplex, meaning that data payloads can flow in both directions. The data that's contained as a payload in a TCP segment has a maximum segment size (MSS), and this is typically 1460 bytes in practice, but it could be any number of different values, as we'll illustrate shortly.

TCP uses cumulative ACKs and is a Go-Back-N pipelined protocol. It's also connection-oriented, which means that there's a handshake that occurs between the sender and the receiver before data actually begins to flow. We'll take a look at that handshake procedure shortly.

TCP is also flow controlled, which means that the sender and the receiver are speed-matched so that the sender won't overwhelm the receiver with data.

**TCP Segment Structure**

Let's next take a look at the TCP segment structure. I know this can seem a little bit boring — there's a lot of fields here — so it may seem a little bit dry. But remember, the thing to keep in mind is not just what the fields are, but why those fields are there. In all of these cases, we'll see from what we've learned already about the principles of reliable data transfer that we'll be able to understand why TCP has these fields.

We've seen source port number and destination port number used for multiplexing and demultiplexing before. The TCP header also contains a 32-bit sequence number and a 32-bit acknowledgement number that we're going to look at in just a second.

Down at the bottom we see the application data — that's the payload being carried by the TCP segment. The TCP header also has an Internet checksum, just as we saw in UDP.

TCP also has a set of options, and there's a variable number of options that could be included. We're not going to go into those, but that makes the header that we see here of variable length, so we can carry options in a TCP header. Because the header can be variable length, we need to have a length field of the TCP header itself.

The reset, SYN, and FIN bits are used for connection management — we'll study that shortly. There's a field in the header that's used for flow control, where the receiver can tell the sender the number of bytes it's willing to accept.

There are two bits in the header that are used for congestion notification, and again we'll take a look at that later. Finally, there are two bits in one field — the urgent field — which are not really used in practice.

**Sequence Numbers and Acknowledgement Numbers**

Let's take a deeper dive into the meaning of TCP sequence number and acknowledgement number fields here. Remember that TCP implements a byte stream abstraction, and the sequence number carried in a TCP segment header indicates the byte stream number of the first byte in that segment's payload data.

The acknowledgement field is used by the receiver to tell the sender the sequence number of the next byte that's expected to be received from the sender. That number serves as a cumulative acknowledgment for all bytes of data that have occurred before that sequence number.

Lastly, students often ask: what should a TCP receiver do with out-of-order segments? The TCP specification places no requirements here — that's up to the implementer.

**Simple Example: Telnet Scenario**

So let's next look at a very simple example of TCP in action, looking at sequence numbers and acknowledgment numbers. In this example we're looking at a simple telnet scenario where host A sends a character to host B, and host B echoes that single character back.

You're going to want to take a careful look at the sequence and ACK numbers on the segments shown in this example. The key thing to note here is that the ACK number of 43 on the B-to-A segment is 1 more than the sequence number 42 on the A-to-B segment that triggered that acknowledgment. Similarly, the ACK number 80 on the last A-to-B segment is 1 more than the sequence number 79 on the B-to-A segment that triggered that acknowledgment.

**Summary of Sequence and ACK Usage**

Well, we've seen that TCP uses sequence numbers and acknowledgments pretty much as we would have anticipated from our principled study. We saw that there were a couple of differences: the byte stream semantics and the fact that sequence numbers and acknowledgments correspond to offsets in that byte stream.

**Setting Timeout Values**

Let's next take a look at an issue we really haven't addressed yet, and that is: how should the timeout values be set? Let's take a look at how TCP does that now.

Clearly we're going to want the timer values to depend somehow on the round-trip time (the RTT). But how do we actually set that timer value? If we set it too short, what will happen is that we'll have premature timeouts — that means that we'll be resending segments that have not actually been lost yet. On the other hand, if we wait too long, TCP...

(Note: The available transcript cuts off here mid-sentence. The full video continues with RTT estimation, timeout calculation using EstimatedRTT and DevRTT, retransmission scenarios, and more.)

References:  

- [YouTube Video: 3.5-1 TCP Reliability, Flow Control, and Connection Management](https://www.youtube.com/watch?v=UYJP-6mhF6E)
- [Playlist: Computer Networking: A Top-Down Approach - All Chapters](https://www.youtube.com/playlist?list=PLByK_3hwzY3Tysh-SY9MKZhMm9wIfNOas)
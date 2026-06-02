---
audio: false
generated: true
image: false
lang: en
layout: post
title: Interrupts Don't Cancel Cloud Inference
translated: false
type: note
---

When you interrupt (e.g. with Ctrl-C) your Python script while it’s waiting on the `generate_images()` call, here’s roughly what happens:

1. **Client-side behavior**
   – As soon as you kill the Python process, the underlying HTTP/gRPC connection is torn down.
   – The GenAI client library will typically catch the broken pipe or connection‐reset and raise an exception (which you’ll see in your script).

2. **What happens on Google’s side**
   – By the time you cancel, your request has already reached Google’s inference service and been enqueued (or already begun running).
   – Most cloud inference endpoints do **not** automatically cancel work just because the client disappeared. They’ll continue running your image‐generation job to completion (consuming GPU/TPU and incurring billing), even though there’s no live connection to return the result.
   – Once the job finishes, the generated image is discarded—there’s no callback to you unless you’ve set up a long-running operation or webhook.

3. **How Nginx (or another proxy) factors in**
   – If there’s an Nginx reverse-proxy in front of the inference service, its default behavior is to watch the client connection. As soon as the client aborts, Nginx closes its upstream connection to the inference process (sending a FIN/RST).
   – The upstream process then sees a broken socket when it eventually tries to write the response. At that point it may log an I/O error, but—crucially—it does **not** rewind and stop the computation you asked for; it simply can’t deliver the bytes.
   – You can tweak Nginx’s `proxy_ignore_client_abort` directive—if you set it to `on`, Nginx will keep the upstream connection alive even after the client disconnects (which can let you fully finish writing logs or other cleanup).

4. **Key takeaways for your script**

   * **Interrupts don’t “undeploy”** or cancel the model on Google’s servers—you’ll still be billed for the full inference.
   * If you need cancellable inference, you’d have to use a different pattern: for example,

     1. Submit a non-blocking batch or long-running operation,
     2. Poll its status or cancel it explicitly via a separate API call.

So in short: killing your script at 5 s stops your local wait and closes the socket, but Google’s inference still runs to completion on their hardware (and Nginx or similar will simply drop the response back to nowhere once it’s ready).

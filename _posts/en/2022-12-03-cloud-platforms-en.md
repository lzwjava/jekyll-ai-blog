---
audio: false
generated: false
image: true
lang: en
layout: post
title: Some Global Cloud Platforms
translated: false
type: post
---

<div align="center"><img src="/assets/images/cloud/platform.jpg" width="400px"/><img/></div>

* [Azure](#azure)
* [AWS Lightsail](#aws-lightsail)
* [Digital Ocean](#digital-ocean)
* [Vultr](#vultr)
* [Google Cloud - Fail](#google-cloud---fail)
* [Outline](#outline)
* [Summary](#summary)

I tried some cloud platforms recently. I used it to set up my proxy server. Before, I used a third-party proxy server. The server is used by many users. So the speed is slow sometimes. I tried to set up my own to fix this problem.

## Azure

Azure is a good option. I created 3 virtual machines here. Because the platform gave me 200 dollars credit for free. My machines are located in Qatar, the USA, and Hong Kong. The ping time from my Guangzhou laptop to the Qatar server is 150ms. Now the ping packets to USA Server are 100% lost. Two days ago, I can ping it successfully. And the ping packets to the Hong Kong server are also 100% lost. And I tested them in my iOS proxy client and they couldn't be connected. I need to shut them down. Though the cost is free, the lost server has no use to me.

<div align="center"><img src="/assets/images/cloud/azure.png" /><img/></div>

Let's see the console and the networking tab, above and below.

<div align="center"><img src="/assets/images/cloud/network.png" /><img/></div>

My custom networking setting is simple. I just make any port between 1024 to 65535 of any protocol open. As it is my proxy server. I don't have any secret data or programs inside it. So I follow the suggestion of the Outline App to do so.

## AWS Lightsail

Lightsail is a light product of AWS. AWS has a lot of products. And sometimes we just want to create some virtual machines inside it. So they provide us with the AWS Lightsail.

<div align="center"><img src="/assets/images/cloud/lightsail.png" /><img/></div>

## Digital Ocean

I used Digital Ocean a lot in overseas cloud platforms, especially from 2016 to 2018. I spent 5 dollars every month.

We create a droplet like this:

<div align="center"><img src="/assets/images/cloud/do.png" /><img/></div>

This is my billing history:

<div align="center"><img src="/assets/images/cloud/bill.png" /><img/></div>

## Vultr

I used Vultr from 2018 to 2020.

<div align="center"><img src="/assets/images/cloud/vultr.png" /><img/></div>

## Google Cloud - Fail

I want to try google cloud too. However, I failed. They don't support China users. Though we can provide fake info as we are other countries' citizens. However, we don't have the corresponding credit card to register successfully.

<div align="center"><img src="/assets/images/cloud/google.png" /><img/></div>

## Outline

Outline isn't a cloud platform. It is a proxy tool. Because it helps me set up my proxy server, I have to write a separate paragraph to praise it. It is really helpful. You can learn about it by searching it online.

<div align="center"><img src="/assets/images/cloud/outline.png" /><img/></div>

## Summary

The cheapest sever with the lowest configuration usually cost around 5 dollars a month. It is enough for acting as a proxy server to be used for a few users. The servers in Singapore, Hong Kong or other Asia areas, are usually connected faster than the servers in the USA or Europe. And sometimes when you set up the server just now, it works like a charm. However, when a few days pass, it works like a zombie. So regarding speed and stability, you can only find the truth in your daily use.

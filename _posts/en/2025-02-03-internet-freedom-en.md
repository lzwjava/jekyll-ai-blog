---
audio: false
generated: false
image: true
lang: en
layout: post
title: The Journey to Pursue Internet Freedom
translated: false
type: post
---

### Table of Contents

1. [Proxy Solutions in China](#proxy-solutions-in-china)
   - Use Macao SIM card for direct access
   - Recommend affordable proxy server providers
   - Configure apps with global routing rules
   - Avoid self-hosted proxy server setups
   - Switch App Store region with proxy

2. [The Journey to Pursue Internet Freedom](#the-journey-to-pursue-internet-freedom)
   - Timeline of proxy method evolution
   - Compare GFW fighting to myopia reversal
   - Current setup uses multiple proxy servers
   - Automated proxy selection based on speed
   - Regret not learning provider techniques earlier

3. [Macau SIM Cards](#macau-sim-cards)
   - China Telecom Easy+ SIM card details
   - Blue Macau SIM card pay-as-you-go
   - Various daily fee and data plans
   - Requires compatible 4G supported device
   - No contract or termination fees

4. [Shadowsocks Proxy Issues](#shadowsocks-proxy-issues)
   - Network-specific connectivity problems occur
   - 5G versus 4G performance differences
   - Carrier policies may block proxy traffic
   - Server location affects latency
   - Troubleshoot with different servers

5. [Registering on Any Platform Regardless of Identity](#registering-on-any-platform-regardless-of-identity)
   - Use multiple email accounts for registration
   - Rent phone numbers through online services
   - Switch Apple Store region with proxy
   - Payment restrictions with Chinese Visa cards
   - Chinese identity documents help sometimes


## Proxy Solutions in China

*2024.12.29*

* The best way is to get a China Macao SIM card to use cellular data directly when needed. Visit [https://www.1888.com.mo](https://www.1888.com.mo). It costs around 80 CNY for 10 GB of cellular data, offering a fast and painless experience.

* China Telecom Macao SIM cards are available in two types: red and blue. Red cards offer daily plans, typically costing 2, 3, or 5 Macao dollars per day. Blue cards provide data plans, such as 10GB for 98 Macao dollars or 20GB for 198 Macao dollars, without monthly charges.

* If you need more network data or use a laptop frequently, consider using [Falemon](https://falz.pics). It provides access to approximately 15 global proxy servers for just 30 CNY per month.

* On iOS, use Shadowrocket with Shadowsocks rules: [https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever). Configure global routing to separate China traffic from overseas traffic.

* On Android, use V2Ray. On Fire TV, use the V2Ray app. On Apple TV, use the Shadowrocket app. On Mac, use the ShadowsocksX-NG or ClashX app.

* It is not recommended to set up a proxy server by yourself. Protocols like Shadowsocks, VMess, or Trojan are easily banned, regardless of the server used.

* To switch the App Store to the USA region, turn on a global proxy (USA), and it will show the payment option of "None," allowing you to switch openly.

* Use a Visa card to buy gift cards from Amazon or use the Apple gift card portal to charge your App Store account.

---

## The Journey to Pursue Internet Freedom

*2025.02.03, This post was last updated in Jan 2026.*

#### The Journey

From 2010 to 2013, I used Goagent and the SwitchyOmega proxy tool to bypass the GFW.

Between 2014 and 2015, I used Qujing (曲径) for proxying and followed its author on Twitter, who now lives in Japan.

From June 2016 to July 2018, I used Digital Ocean to host my shadowsocks proxy server.

Starting in 2019, I began using https://zhs.cloud.

In March 2023, I started using a Macao SIM card in my mobile phone for internet access without a proxy or VPN. This cost around 150 CNY per month for 20GB of cellular data, and I used this method for about a year.

In 2024, I began using Outline Manager again with my shadowsocks proxy server, experimenting with various cloud providers.

In Feb 2025, my preferred setup is Outline Manager with an Aliyun Hong Kong server for daily use and a non-Hong Kong server (like Singapore or Japan) for AI tools. I maintain the same proxy rules configuration used in Shadowrocket or Clash.

From June 2025, I started using a Python script on my laptop to automatically select a proxy server every 10 minutes based on speed test results. The script prioritizes Singapore servers over Hong Kong servers for using AI tools. For more details, please check [Automating Clash Proxy Management](/clash-en). For the VPN cloud provider, I still used https://zhs.cloud.

Additionally, on iOS, I switched back to using a Macao SIM card, costing 150 CNY per month for 20GB of data. I also purchased an extra 5GB of data three times for 20 MOP each, totaling around 200 CNY for 35GB of data on my mobile phone.

Starting from mid-October 2025, I stopped using my Macau SIM card plan because I've been using around 35 GB a month in recent months. It would cost cellular data to use Chinese apps, which account for about one-third of my data usage—mostly in WeChat.

I began using the iOS Shadowsocks app again with proxy servers from https://zhs.cloud. And I started learning some knowledge about CN2 cables.

Starting from the end of December, I restarted using a Macau SIM card in my mobile phone due to the frustration of proxy servers.

Starting from January 2026, I started using [Falemon](https://falz.pics). One friend recommended it.

Starting in February 2026, due to a DNS failure with my Falemon subscription address, I switched to DMIT.io and set up Hysteria2 on their server. After using it for one week, the IP address got banned. However, I was able to freely change to a new IP on DMIT.io, which was great. They utilize CN2 GIA lines.


#### The Difference Compared to Reversing Myopia

One challenge is fighting the GFW, which is human-made. The other is addressing the principles of eye muscle function.

It's easy to measure the effectiveness of a proxy solution. However, reversing myopia requires time to determine if the eyeball is changing.

#### Similarities to Reversing Myopia

A similarity is that both a proxy solution and eyeglasses with a 200-degree reduction often work well. One involves accessing the internet, and the other involves improving eyesight. Both address very important problems.

The underlying principle is that if we understand how the GFW works and find a way to bypass it, the solution should be straightforward.

#### Reasoning and Nuance

I still don't fully understand how the GFW works. When my proxy server's IP gets blocked, I now have more ways to investigate the cause.

I can check if the block occurs on the cellular network or home broadband. If it's the cellular network, I can check if it's on 4G or 5G.

Similarly, if my myopia doesn't improve after six months or a year, I need to investigate if there are differences between my eyes. I also need to consider if I've been seeing things just barely clearly without straining my eyes for most of the year.

#### Current Status

My proxy server is currently working very well. Download speeds on my phone reach 80 Mbps, and upload speeds reach 50 Mbps when connecting to the Hong Kong proxy server. The same is true on my laptop.

I use the same proxy configurations on my laptop and phones, and they work perfectly. Normally, I use a proxy server to visit sites outside China, and I use a non-HK server for AI tools.

#### Recovery

If things are broken, my recovery method is simple. I just need to change the elastic IP of my Aliyun Hong Kong proxy server and upload the new proxy URL to cloud storage. This means I need to run two scripts, which takes about 1 minute, and my laptop and phones can update the proxy server address.

#### Regret

I fought with the GFW too many times and for too much time. I tried many proxy protocols, knowing they would be detected by the GFW and get banned. Without a reliable proxy server, it is hard to set up a proxy on an OpenWrt router.

One thing I regret is not learning the techniques of proxy providers earlier, like [zhs.cloud](https://zhs.cloud). I now know most of their secrets.

The other thing is that whenever my proxy server got banned, I didn't think too deeply. It seemed that you just needed to set up a new proxy server to get a new IP address that hadn't been banned. But that was shallow thinking.

#### Metrics

I regret not using Speedtest earlier. I knew the name of the tool a long time ago, but I didn't learn how to use it carefully.

It is good to use Speedtest often when connecting to 5G or 4G mobile signal stations or a home broadband network.

For reversing myopia, it is the same. I bought a C-shape eye chart and a standard eye chart.

No measuring, no improvement. Measuring things helps you learn. Using Speedtest often helps me find that on a 5G network, it is easy to exceed 100 Mbps, while on a home broadband network, it is hard to exceed 100 Mbps.

#### It Is Still Early

Will the GFW wall fall down in the next few years? It is hard to say.

When, after reversing myopia for two years, I told my friend that my reversing method needed to be improved and that I needed to wear glasses with 200 degrees less than my actual prescription instead of 150 degrees less.

He said that it was no problem, it was fine, not a waste of time, and that it was still early. Yeah. These things are fundamental. Like myopia, people should discover it earlier. Todd Becker shared this discovery on YouTube in 2014, and the videos gained more than 1 million views. And now it is 2025, how many people really know about it in the world? I guess it will be less than 10 thousand.


---

## Macau SIM Cards

*2023.04.20*

#### My Experience with Macau SIM Cards

During my weekend visit to Macau in 2023, I bought a China Telecom Easy+ SIM Macau Card. After arriving in Guangzhou, I found it still worked perfectly, helping me learn English and download many foreign apps. It felt like I was still in Macau. I highly recommend it. Later, I tried the Blue Macau SIM Card, which was also good. Here’s a quick overview of both:

#### China Telecom Easy+ SIM Card

Easy to Use Anytime!

### Key Points
- No deposit; automatic activation for Mainland China, Macau, and Hong Kong.
- No contract or termination fee; ready to use upon purchase.
- Macau number included; optional Mainland China number for dual-number use.
- Top up online or with value cards.

### Daily Fee Options
- $2/day: 4GB high-speed, then unlimited at reduced speed; 5,000 minutes local calls.
- $3/day: 10GB high-speed, then unlimited at reduced speed; 5,000 minutes local calls.
- $5/day: 20GB high-speed, then unlimited at reduced speed; 5,000 minutes local calls.

### Extras
- Data usage in Hong Kong: $0.1/MB.
- Change plans anytime by sending a text message.

#### Blue Macau SIM Card

### Key Points
- No monthly rent; pay as you use.
- Local calls: 0.39 MOP/minute; Internet: 0.1 MOP/MB; SMS: 1 MOP/message.
- Optional no-expiry data packages: 10GB for 98 MOP, 20GB for 188 MOP, 40GB for 288 MOP.
- Top up every 180 days to keep active.

#### Compatible Devices

- Requires a 4G full network or China Telecom supported phone.

For more information, visit [China Telecom Macau](https://www.1888.com.mo/).

---

You can also find these on Taobao:

<div align="center"><img src="/assets/images/macao/easy.jpg" width="300px" /><img/></div>

---

## Shadowsocks Proxy Issues

*2025.01.03*

Zhiwei:

I went out for a barbeque with a friend and used Shadowsocks with a Singapore-based server as my proxy to bypass the Great Firewall (GFW). While using 5G outside, I couldn't connect, and the test timed out when trying to access YouTube. However, when I'm at home using 4G or my China Telecom home network, Shadowsocks works fine. Why is this happening?

Mistral:

It sounds like you're experiencing connectivity issues with your Shadowsocks proxy when using 5G outside, but not when using 4G or your home network. There could be several reasons for this:

1. Network Configuration Differences:
   - 5G Network: The 5G network might have different configurations or restrictions compared to 4G. Some carriers might have stricter firewall rules or different network routing for 5G, which could affect the performance of your Shadowsocks proxy.
   - 4G Network: The 4G network might have more relaxed settings or better routing that allows your Shadowsocks proxy to function correctly.

2. ISP Restrictions:
   - Carrier Policies: Different carriers might have different policies regarding the use of VPNs or proxies. Your 5G carrier might have stricter policies that block or throttle VPN traffic, including Shadowsocks.
   - Home Network: Your home network, provided by China Telecom, might have fewer restrictions, allowing Shadowsocks to work without issues.

3. Signal Strength and Stability:
   - 5G Signal: The stability and strength of the 5G signal can vary, especially in outdoor environments. Weak or unstable signals can cause connectivity issues, including timeouts.
   - 4G Signal: The 4G signal might be more stable and consistent, providing a better connection for your Shadowsocks proxy.

4. Proxy Server Location:
   - Singapore Server: The location of your Shadowsocks server in Singapore might affect latency and connectivity. The 5G network might have higher latency or less optimal routing to the Singapore server compared to the 4G network or your home network.

5. Device Settings:
   - Configuration: Ensure that your device settings are correctly configured for using Shadowsocks. Sometimes, switching networks (from 5G to 4G or home Wi-Fi) can cause settings to reset or change.
   - App Permissions: Make sure that the Shadowsocks app has the necessary permissions to operate on different networks.

### Troubleshooting Steps:

1. Check Network Settings:
   - Ensure that your Shadowsocks settings are correctly configured for both 5G and 4G networks.
   - Verify that there are no specific restrictions or settings on your 5G network that might be blocking the proxy.

2. Test Different Servers:
   - Try connecting to different Shadowsocks servers to see if the issue is specific to the Singapore server.
   - Check the latency and stability of the connection to the server.

3. Contact Your Carrier:
   - If the issue persists, contact your 5G carrier to inquire about any restrictions or settings that might be affecting your Shadowsocks connection.

4. Update Software:
   - Ensure that your Shadowsocks app and device software are up to date. Sometimes, updates can resolve connectivity issues.

5. Use Alternative Proxies:
   - Consider using alternative proxy services or VPNs that might have better compatibility with your 5G network.

By systematically checking these factors, you should be able to identify the cause of the connectivity issue and find a suitable solution.

--

Update:

Actually, my home Wi-Fi uses China Mobile Communications Corporation, and its address is like 120.235.8.xx.

Interestingly, I've observed inconsistent connectivity patterns - while my proxy server functions normally on cellular data and China Telecom networks, it occasionally fails to connect when using my home Wi-Fi network.



---

## Registering on Any Platform Regardless of Identity

I am a Chinese citizen and a software engineer focused on the latest technology. It's frustrating to see many products banning access from China. Although I’m still working on my associate degree and hope to work outside China someday, I will remain in China for a few more years. In the meantime, I'd like to share some information about overcoming internet barriers based on nationality.

#### Email

Having multiple email accounts is better. Claude banned my Gmail due to VPN access, so I registered a new Outlook email and it worked fine.

#### Phone Number

Through [http://sms-activate.org](http://sms-activate.org), it's possible to rent a phone number for registration. However, the issue is that accounts registered with such phone numbers may have some risks.

In China, I personally recommend [https://www.1888.com.mo](https://www.1888.com.mo) for a China Telecom Macau card. I’ve also tried the Giffgaff UK SIM card and recently ordered a PayGo T-Mobile USA SIM card.

#### Apple Store Region

To switch the App Store to the USA region, turn on a global proxy (USA), and it will display the "None" payment option, allowing you to switch freely.

You can use a Visa card to buy gift cards from Amazon or use the Apple gift card portal to fund your App Store account.

The same method applies to Singapore or other regions.

#### Payment

Having a Visa card is convenient. However, Visa cards issued by China still have some restrictions. For example, Anthropic or OpenAI do not accept Chinese-issued Visa cards.

#### VPN

You may want to check out [Proxy Solutions in China](./proxy-en) and [Set Up Your Proxy Server](./diy-proxy-en).

#### Identity

I have a Chinese citizen identity card and passport, which can be helpful in certain situations.

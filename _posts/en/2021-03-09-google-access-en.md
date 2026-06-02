---
audio: false
generated: false
image: true
lang: en
layout: post
title: How to Access Google
translated: false
type: post
---

This post was originally written in Chinese.

---

This lesson covers the following:

1. How to access the official website of a VPN service.
2. How to use a VPN on Windows.
3. Introduction to the Clash software.
4. Trying to open Google, Twitter, YouTube, and TikTok.

Let's begin. Here's a written description of how I taught Xiao Wang to access Google.

We'll be using a platform called "Summoner." The website is `https://zhshi.gitlab.io`.

<img src="/assets/images/google/zhs.png" alt="zhs" />

However, it might not be accessible because it's blocked by the Great Firewall.

![zhs_user](/assets/images/google/zhs_user.png)

This is what it looks like when you log in.

There are actually two ways to bypass the firewall. One is to buy our own overseas server. The other is to use a VPN platform, which provides many overseas server addresses.

"Bypassing the firewall" means first accessing an overseas server from within the country. This overseas server can then access websites that are blocked.

Such a platform is called "Summoner." But if the official website is inaccessible, how do we get the overseas server addresses it provides? Xiao Wang is using a VPN for the first time, and I'm teaching him remotely. How should I teach him?

At this point, I thought of enabling Xiao Wang's Windows computer to bypass the firewall. I'll provide Xiao Wang with an address. Then Xiao Wang can open the "Summoner" website, register an account, and use the overseas server addresses under his own account.

![clash_win](/assets/images/google/clash_win.png)

![win_version](/assets/images/google/win_version.png)

Next, check if your computer is 64-bit or 32-bit. If it's 64-bit, download `Clash.for.Windows.Setup.0.14.8.exe`. If it's 32-bit, download `Clash.for.Windows.Setup.0.14.8.ia32.exe`.

Xiao Wang's computer is 64-bit. But the download is very slow on his end. So I downloaded it on my computer and sent it to him via QQ email.

He downloaded it from QQ email, installed it, and opened it.

![clash_win_exe](/assets/images/google/clash_win_exe.png)

I first gave him my Summoner configuration address. This configuration address will download a file containing many VPN server addresses. Under `Profiles`, paste the address and click `Download`.

![zhs_url](/assets/images/google/zhs_url.png)

See, it's downloaded. Notice the second configuration above. There's a green checkmark in front of it, indicating that we're using this configuration.

![zhs_proxy](/assets/images/google/zhs_proxy.png)

Next, open the `Proxies` tab. You'll see some things here. These are some of `Clash`'s configurations. Simply put, it means that domestic websites won't use the VPN, while foreign websites will.

Notice that the current value of `Proxy` is `DIRECT`, which means it's a direct connection. We'll change it to a node.

![zhs_node](/assets/images/google/zhs_node.png)

We selected the `US Rose` node.

![clash_system](/assets/images/google/clash_system.png)

Next, toggle the `System Proxy` setting to enable it. This means setting the `Clash` software as the system's proxy layer. Then, the system's traffic will first go to the `Clash` software and then access the external network.

<img src="/assets/images/google/google.png" alt="google" style="zoom:40%;" />

Xiao Wang opened Google. Next, he tried TikTok, YouTube, and Twitter.

Okay, so Xiao Wang has been using my Summoner account. How does he register? He needs to open the official Summoner website.

<img src="/assets/images/google/zhs_register.png" alt="zhs_register" style="zoom:50%;" />

After registering, he found that recharging to purchase services requires some steps. Here's a screenshot of my account.

![zeng](/assets/images/google/zeng.png)

It says that it needs to be linked to Telegram.

<img src="/assets/images/google/zhs_telegram.png" alt="zhs_telegram" style="zoom:50%;" />

Xiao Wang went to the Telegram website and downloaded the Telegram Windows desktop version.

![telegram](/assets/images/google/telegram.png)

After downloading and installing it, pay attention to the text above.

> After installing Telegram and registering, click to chat with `小兔` or `城主`, copy the QR code below and send it to them, or `click here to automatically copy the code and send it to the Bot to bind`.

When you click on `小兔`, it will automatically jump to the `Telegram` software and open a chat window with `小兔`. Then, send the code to them.

![telegram_username](/assets/images/google/telegram_username.png)

However, Xiao Wang's `Telegram` account is newly registered and doesn't have a `username`. It's like using WeChat without setting a WeChat ID.

Find the Telegram menu and set it. Then, send the code again to bind.

<img src="/assets/images/google/zhs_set.png" alt="zhs_set" style="zoom:50%;" />

Next, you can donate to support it. You can start by recharging 30 yuan for two months.

Go back to the Summoner homepage. Here, look for the "Click to Copy" button, get the address, and then download the configuration in the `Clash` software.

Then Xiao Wang can delete the address I gave him. Xiao Wang now has his own Summoner account.

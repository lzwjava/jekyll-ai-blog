---
audio: true
generated: false
image: false
lang: en
layout: post
title: Setting up a Google Cloud Server
translated: false
type: post
---

Setting up a proxy server in Google Cloud allows you to route your internet traffic securely through a cloud instance, enhancing privacy and circumventing restrictions. In this guide, we'll walk you through the process of setting up a basic proxy server in Google Cloud and configuring the necessary firewall rules to allow traffic.

## Table of Contents

1. [Creating a Google Cloud VM Instance](#creating-a-google-cloud-vm-instance)
2. [Configuring the Proxy Server](#configuring-the-proxy-server)
3. [Setting Up Firewall Rules](#setting-up-firewall-rules)
4. [Testing the Proxy Server](#testing-the-proxy-server)
5. [Conclusion](#conclusion)

---

## Creating a Google Cloud VM Instance

Before setting up the proxy server, you'll need to create a virtual machine (VM) instance in Google Cloud.

1. Log in to Google Cloud Console: Go to [Google Cloud Console](https://console.cloud.google.com/) and log in to your account.

2. Create a New VM Instance:
   - Navigate to Compute Engine > VM instances.
   - Click on Create Instance.
   - Choose the desired Region and Machine Type. For simplicity, you can use the default settings or choose a lightweight configuration like the `e2-micro` instance.
   - Under the Firewall section, select both Allow HTTP traffic and Allow HTTPS traffic to enable web access.

3. Set up SSH Access:
   - Under the SSH Keys section, add your SSH public key to access the instance remotely. This is critical for configuring your proxy server later.

4. Click on Create to launch your VM.

After the VM is set up, you can connect to it using SSH from the Google Cloud Console or via the terminal with:

```bash
gcloud compute ssh <your-vm-name>
```

---

## Configuring the Proxy Server

Once your VM is set up, you can configure any proxy server software of your choice. The proxy software should be installed and configured to accept connections on the desired port (e.g., `3128` for common proxy setups). Ensure that the software allows connections from remote clients.

---

## Setting Up Firewall Rules

To allow traffic to your proxy server, you'll need to configure the Google Cloud firewall rules to open the necessary port.

1. Navigate to Firewall Rules in Google Cloud Console:
   - Go to VPC Network > Firewall Rules in the Google Cloud Console.

2. Create a New Firewall Rule:
   - Click on Create Firewall Rule.
   - Enter a name for the rule, such as `allow-proxy-access`.
   - Set the Direction of traffic to Ingress (incoming traffic).
   - Set the Action on match to Allow.
   - Set Targets to All instances in the network or Specified target tags (if you prefer more control).
   - Under Source IP ranges, you can set it to `0.0.0.0/0` to allow access from all IP addresses, or limit it to specific IPs or ranges for better security.
   - Under Protocols and ports, select Specified protocols and ports and enter the port used by your proxy server (e.g., `tcp:3128`).

3. Save the Firewall Rule:
   After configuring the rule, click Create to enable the firewall.

---

## Testing the Proxy Server

After configuring the firewall, it’s time to test your proxy server.

1. Test Proxy from Your Local Machine:

   You can configure your local machine’s browser or system proxy settings to use the external IP address of your Google Cloud VM and the port that your proxy server is listening on (e.g., `3128`).

2. Test with Command Line:

   You can also test the proxy with `curl` by setting the proxy environment variables:

```bash
export http_proxy=http://<your-vm-external-ip>:3128
export https_proxy=http://<your-vm-external-ip>:3128
curl -I http://example.com
```

If the connection is successful, you should see a response from the website.

---

## Conclusion

By following this guide, you’ve learned how to set up a proxy server on Google Cloud and configure firewall rules to allow incoming traffic. This setup provides an easy way to route your internet traffic securely through the cloud, bypass network restrictions, and enhance privacy.

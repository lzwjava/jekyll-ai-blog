---
audio: false
generated: true
image: false
lang: en
layout: post
title: Transfer Large Files via Private Network
translated: false
type: note
---

Transferring a 60GB file between DigitalOcean Droplets using the internal 10.xx network is an excellent way to move data quickly and for free, as private network traffic does not count against your bandwidth allowance.

Here is a step-by-step guide to get this done.

### ✅ Step 1: Ensure Your Droplets Are in the Same Region
The private 10.xx network is only accessible between Droplets located in the **same datacenter region**. Verify your Droplets' locations in the DigitalOcean Control Panel before proceeding.

### ✅ Step 2: Verify Private Network Interfaces
- **Standard Droplets**: Use interface **`eth1`** for private networking.
- **Multi-Node GPU Droplets**: Use the high-speed fabric NICs **`eth2` through `eth9`** for optimal performance.
- **For Kubernetes (DOKS)**: The high-speed fabric is exposed as **`fabric0` through `fabric7`**.

Run the following command on each Droplet to confirm the private IP address (look for the `10.xx.xx.xx` range):
```bash
ip -br addr
```

### ✅ Step 3: Transfer the File
The fastest method for a one-time transfer is using `scp` (Secure Copy Protocol) over the private interface.

1.  **Find the Private IP of the Destination Droplet**
    - You can find it in the DigitalOcean Control Panel under the Droplet's "Settings" or by running `ip -br addr` on the Droplet itself.

2.  **Run the SCP Command**
    On the **source Droplet**, use the following command to transfer your file. Replace the placeholders with your actual details.
    ```bash
    scp -r /path/to/your/source/file root@<destination_private_ip>:/path/to/destination/
    ```
    **Example:**
    ```bash
    scp -r /root/my-large-file.img root@10.100.0.5:/root/
    ```

### 💡 Important Considerations for 60GB Files

- **Use `screen` or `tmux`**: A 60GB transfer can take time. Run your transfer inside a terminal multiplexer like `screen` or `tmux` to prevent it from stopping if your SSH session disconnects.
- **Set Up SSH Keys**: To avoid being prompted for a password during the transfer, set up SSH key authentication between the Droplets. You can use `ssh-copy-id` to easily copy your public key.
    ```bash
    ssh-copy-id root@<destination_private_ip>
    ```
- **Compress on the Fly**: If your file is not already compressed, you can compress it during transfer to save time. However, this uses CPU on both servers.
    ```bash
    tar czf - /path/to/source-directory | ssh user@<private-ip> "tar xzf - -C /path/to/destination"
    ```
- **Alternative Tool**: For even faster transfers, especially for very large files, consider using `rsync` over the private IP. It supports resuming interrupted transfers.
    ```bash
    rsync -avz --progress /path/to/large-file user@<private-ip>:/destination/
    ```

### 🖥️ Multi-Node GPU Droplet-Specific Notes
If you are transferring data to or between multi-node GPU Droplets (like H100 or MI300X), remember:
- The high-speed fabric (interfaces `eth2` to `eth9`) is designed for **GPU-to-GPU communication** (e.g., for NCCL/RCCL). For a standard file copy using `scp` or `rsync`, the operating system will typically use the main private interface (`eth1`).
- To use the high-speed fabric for your data transfer, you would need specialized tools that can bind to specific network interfaces, which is unnecessary for a simple file copy. The standard private network (`eth1`) provides up to **25 Gbps** bandwidth, which is more than sufficient for a 60GB file.
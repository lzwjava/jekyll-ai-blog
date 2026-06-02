---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Using hf-mirror.com in China
translated: false
type: note
---

### Understanding hf-mirror.com

hf-mirror.com is a community-maintained mirror of the official Hugging Face Hub (huggingface.co), specifically designed to help users in China (including Guangzhou) bypass network restrictions and download AI models/datasets faster. It replicates the full repository structure, so you can access models like GPT-2 or datasets like WikiText without directly hitting the original site, which is often slow or blocked. Since you use Clash proxy often, note that hf-mirror.com is hosted domestically and typically doesn't require a proxy for access—it's optimized for direct use in China. If you're already proxying traffic via Clash, you can either route hf-mirror.com traffic directly (to avoid unnecessary hops) or keep it proxied if preferred.

### Basic Setup: Using the Mirror

The key is setting the `HF_ENDPOINT` environment variable to point to the mirror. This works globally for Hugging Face tools like the `transformers` library, `huggingface-cli`, or `hfd` (a faster downloader). Do this **before** importing libraries or running downloads.

#### 1. Set the Environment Variable

- **On Linux/macOS (permanent)**: Add to your `~/.bashrc` or `~/.zshrc`:

  ```
  echo 'export HF_ENDPOINT=https://hf-mirror.com' >> ~/.bashrc
  source ~/.bashrc
  ```

- **On Windows (PowerShell, permanent)**: Run once:

  ```
  [System.Environment]::SetEnvironmentVariable('HF_ENDPOINT', 'https://hf-mirror.com', 'User')
  ```

  Then restart your terminal.
- **Temporary (any OS)**: Prefix commands like:

  ```
  HF_ENDPOINT=https://hf-mirror.com your_command_here
  ```

This redirects all Hugging Face downloads to the mirror without changing your code.

#### 2. Install Required Tools

- Install the Hugging Face Hub CLI (for downloads):

  ```
  pip install -U huggingface_hub
  ```

- For even faster downloads, grab `hfd` (Hugging Face Downloader, uses aria2 for multi-threaded speeds):

  ```
  wget https://hf-mirror.com/hfd/hfd.sh  # Or download via browser
  chmod +x hfd.sh
  ```

#### 3. Downloading Models or Datasets

- **Using huggingface-cli** (supports resume on interrupt):

  ```
  # Download a model (e.g., GPT-2)
  huggingface-cli download gpt2 --resume-download --local-dir ./gpt2

  # Download a dataset (e.g., WikiText)
  huggingface-cli download --repo-type dataset wikitext --resume-download --local-dir ./wikitext
  ```

- **Using hfd** (faster, especially for large files):

  ```
  # Model
  ./hfd.sh gpt2

  # Dataset
  ./hfd.sh wikitext --dataset
  ```

- **In Python code** (e.g., with transformers library):

  ```python
  import os
  os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'  # Set before imports

  from transformers import AutoModel, AutoTokenizer
  model = AutoModel.from_pretrained('gpt2')  # Downloads from mirror automatically
  tokenizer = AutoTokenizer.from_pretrained('gpt2')
  ```

  Run with: `HF_ENDPOINT=https://hf-mirror.com python your_script.py`

#### 4. Handling Gated/Logged-In Models

Some models (e.g., Llama-2) require a Hugging Face account and token:

- Log in on huggingface.co (use your Clash proxy if the site is blocked).
- Generate a token at <https://huggingface.co/settings/tokens>.
- Download with:

  ```
  huggingface-cli download --token hf_YourTokenHere meta-llama/Llama-2-7b-hf --resume-download --local-dir ./Llama-2-7b-hf
  ```

  Or for hfd:

  ```
  ./hfd.sh meta-llama/Llama-2-7b-hf --hf_username your_username --hf_token hf_YourTokenHere
  ```

### Integrating with Clash Proxy

Since hf-mirror.com is a Chinese mirror, it should be accessible without Clash (direct connection is faster). However, if you want to proxy it (e.g., for consistency or if you hit any issues), configure Clash to route traffic to hf-mirror.com via your preferred proxy group. Clash doesn't need special "HF" config—it's system-wide.

#### Quick Clash Setup Tips

- Ensure Clash is running and set as your system proxy (in Clash: Go to "General" > Enable "System Proxy").
- **Route hf-mirror.com directly (recommended for speed)**: Edit your Clash config YAML (usually `config.yaml` in Clash's folder). Add a rule to bypass proxy for the mirror:

  ```
  rules:
    # ... your existing rules ...
    - DOMAIN-SUFFIX,hf-mirror.com,DIRECT  # Bypasses proxy, goes direct
    # ... rest of rules ...
  ```

  Reload config in Clash (Profiles > Reload).
- **Proxy it if needed**: If you prefer routing through Clash, add no special rule—it'll follow your default (e.g., `MATCH,Proxy`). Test by pinging hf-mirror.com in a browser with Clash on/off.
- For downloads: Run commands in a terminal where system proxy is active (Clash handles it). If using Python, libraries like `requests` (used by transformers) respect `HTTP_PROXY`/`HTTPS_PROXY` env vars set by Clash (e.g., `http://127.0.0.1:7890` for HTTP port).
- Test: Try downloading a small model like `distilbert-base-uncased`. If slow, toggle Clash off for hf-mirror.com traffic.

### Troubleshooting

- **Downloads still hit huggingface.co?** Ensure `HF_ENDPOINT` is set **before** importing any HF libraries (restart your notebook/terminal).
- **Slow speeds?** Use `hfd` with aria2 (it supports multi-connections). Or check your network—Guangzhou users often get 10-50MB/s on hf-mirror.com.
- **Errors with datasets?** Some have custom scripts; edit them to use `https://hf-mirror.com` as the base URL.
- **Windows-specific**: If using Anaconda, set the env var in the base environment.
- For advanced self-hosting a local mirror (if you want full control), check open-source tools like Olah or hf-mirror-site on GitHub, but start with the public mirror.

This setup should get you downloading reliably. If you run into specific errors, share the output for more help!

### References

- [HF-Mirror Official Guide](https://hf-mirror.com/)
- [Hugging Face Hub Docs on Endpoints](https://huggingface.co/docs/huggingface_hub/en/package_reference/environment_variables#huggingface_hub_constants.HF_ENDPOINT)
- [hfd Downloader](https://hf-mirror.com/hfd/hfd.sh)
- [Clash Config Rules](https://github.com/Dreamacro/clash/wiki/Configuration#rules)
- [Stack Overflow: Downloading in China](https://stackoverflow.com/questions/77388822/how-to-download-huggingface-bert-base-uncased-in-china)

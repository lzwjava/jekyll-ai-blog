---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Installing OpenJDK 24 on Ubuntu
translated: false
type: note
---

Question: How to install OpenJDK 24 on Ubuntu?

Answer:

OpenJDK 24 is **not** an LTS release (it is a short-term / feature release with only ~6 months support). Ubuntu LTS versions (such as 24.04) normally include only LTS versions of OpenJDK in the official repositories (currently OpenJDK 21, and later OpenJDK 25 when it becomes available).

As of early 2026, OpenJDK 24 is **not** available in the standard Ubuntu repositories for 24.04. However, you have several reliable options to install it:

### Recommended Option: Download official OpenJDK 24 binary from jdk.java.net (clean & simple)

```bash
# 1. Go to the official archive page
#    https://jdk.java.net/archive/
#    → find JDK 24 → Linux / x64 → download the .tar.gz file

# Example (replace with actual filename if needed)
wget https://download.java.net/java/GA/jdk24/5f/f8/3a5f8c3a5f8c3a5f8c3a5f8c3a5f8c3a/36/GPL/openjdk-24_linux-x64_bin.tar.gz

# 2. Extract it
sudo mkdir -p /usr/lib/jvm
sudo tar xf openjdk-24_linux-x64_bin.tar.gz -C /usr/lib/jvm/
# → creates /usr/lib/jvm/jdk-24

# 3. Set it as default (optional – using update-alternatives)
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-24/bin/java 2400 \
  --slave /usr/bin/javac javac /usr/lib/jvm/jdk-24/bin/javac \
  --slave /usr/bin/jar jar /usr/lib/jvm/jdk-24/bin/jar

sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-24/bin/javac 2400

# 4. Choose it
sudo update-alternatives --config java
# select the jdk-24 version

# 5. Verify
java --version
# should show openjdk 24.x ...
```

### Alternative: Use third-party builds with .deb packages (easier upgrades)

Popular vendors that usually provide good .deb packages for non-LTS versions:

- **Azul Zulu** (very reliable, free, TCK certified)
  - Go to → <https://www.azul.com/downloads/?version=java-24>
  - Select Linux / Ubuntu / .deb / JDK → download and install:

  ```bash
  sudo dpkg -i zulu24.xx.x_linux_amd64.deb
  ```

- **Eclipse Temurin** (Adoptium)
  - <https://adoptium.net/temurin/releases/?version=24>
  - Choose .deb package

- **Microsoft Build of OpenJDK**
  - <https://learn.microsoft.com/en-us/java/openjdk/install>
  - They sometimes offer newer versions via their repo

### If you see openjdk-24-jdk in some PPAs or in Ubuntu devel/unstable

In some cases (especially during development cycles of newer Ubuntu releases), `openjdk-24-jdk` may appear temporarily. You can check:

```bash
apt search openjdk-24
```

If nothing shows up → use one of the methods above.

### Quick summary – most people choose one of these two

1. Official tar.gz from jdk.java.net (cleanest, no extra repo)
2. Azul .deb package (easiest to install & update)

After installation remember to set `JAVA_HOME` if your tools require it:

```bash
export JAVA_HOME=/usr/lib/jvm/jdk-24
# or for Azul: /usr/lib/jvm/zulu24-ca-amd64
```

Add it to `~/.bashrc` or `/etc/environment` for permanence.

References:

- [https://jdk.java.net/archive/](https://jdk.java.net/archive/)
- [https://ubuntuhandbook.org/index.php/2025/03/install-openjdk-24-ubuntu](https://ubuntuhandbook.org/index.php/2025/03/install-openjdk-24-ubuntu)
- [https://www.azul.com/downloads/](https://www.azul.com/downloads/)
- [https://adoptium.net/temurin/releases/](https://adoptium.net/temurin/releases/)

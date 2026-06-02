---
audio: false
generated: true
image: false
lang: en
layout: post
title: Installing Apache Tomcat on macOS
translated: false
type: note
---

Here’s a step-by-step guide for installing and running **Apache Tomcat on macOS**:

---

### 1. Check Java

Tomcat requires Java. Verify you have it installed:

```bash
java -version
```

If you don’t see a Java version (e.g., `1.8` or `11` or higher), install one. On macOS the easiest way is via [Homebrew](https://brew.sh):

```bash
brew install openjdk@11
```

Then link it:

```bash
brew link --force --overwrite openjdk@11
```

---

### 2. Install Tomcat (Option A: Homebrew – easiest)

With Homebrew you can quickly install Tomcat:

```bash
brew install tomcat
```

This typically installs the latest version (e.g., Tomcat 10).

You’ll find it under:

```
/usr/local/Cellar/tomcat/<version>/libexec
```

Or if using Apple Silicon:

```
/opt/homebrew/Cellar/tomcat/<version>/libexec
```

Run it with:

```bash
catalina run
```

---

### 3. Install Tomcat (Option B: Manual Download – official way)

1. Go to the [Apache Tomcat website](https://tomcat.apache.org/download-10.cgi) and download the latest stable release (choose the `.tar.gz`).

2. Extract it to a directory, for example:

   ```bash
   tar xvf apache-tomcat-10.*.tar.gz
   mv apache-tomcat-10.* ~/tomcat
   ```

3. Start Tomcat:

   ```bash
   cd ~/tomcat/bin
   ./startup.sh
   ```

4. To stop it:

   ```bash
   ./shutdown.sh
   ```

---

### 4. Verify Installation

Open your browser and go to:

```
http://localhost:8080
```

You should see the Tomcat welcome page.

---

### 5. (Optional) Add to PATH

So you can run `startup.sh` from anywhere, add this to your `~/.zshrc` or `~/.bashrc`:

```bash
export CATALINA_HOME=~/tomcat
export PATH=$CATALINA_HOME/bin:$PATH
```

Reload:

```bash
source ~/.zshrc
```

---

👉 That’s it. Now you have Tomcat running locally on macOS.

Do you want me to also show you **how to deploy a WAR file to Tomcat on macOS** after setup?

---
audio: true
generated: false
image: false
lang: zh
layout: post
title: 冗长输出
translated: true
type: post
---

- 要在 Homebrew 中启用详细输出，请使用 `export HOMEBREW_CURL_VERBOSE=1` 结合 `brew upgrade --verbose`。

- 要增加 SSH 的详细程度，请使用 `ssh -vvv user@host`。

- 要获得 `git` 的更多详细输出，请使用 `git -v` 或 `git --verbose`。

- 要从 `rsync` 获取更多输出，请使用 `rsync -vv source destination`。

- 在 ssh 配置中编写详细配置，例如在 .ssh/config 中有 LogLevel VERBOSE。

- 要启用 `npm` 的详细输出，请使用 `npm install --verbose` 或 `npm run <script> --verbose`。

- 要在 Node.js 中进行详细日志记录，请使用 `NODE_DEBUG` 环境变量：`NODE_DEBUG=http,net node your_script.js`。

- 要从 `curl` 获取详细输出，请使用 `curl -v <url>`。

- 要启用 `pip` 的详细输出，请使用 `pip install -v <package>` 或 `pip install --verbose <package>`。

- 要获得 `wget` 的详细输出，请使用 `wget --verbose <url>`。

- 要从 `yum` 获取详细输出，请使用 `yum -v install <package>`。

- 要启用 `apt-get` 的详细输出，请使用 `apt-get -o Debug::pkgProblemResolver=yes install <package>`。

- 要进行 `adb` 的详细日志记录，请使用 `adb logcat -v verbose`。

- 要以详细模式运行 Python，请使用 `python -v your_script.py`。

- 要以详细输出编译 Java 代码，请使用 `javac -verbose YourClass.java`。

- 要以详细模式启动 VSCode：`code --verbose`。对于日志记录，请在 `settings.json` 中设置 `"trace": true`，并通过 "Developer: Open View..." -> "Log (Window)" 或 "Log (Extension Host)" 查看日志。

- 对于 IntelliJ IDEA 的详细日志记录："Help" -> "Diagnostic Tools" -> "Debug Log Settings..." 或在 `idea.vmoptions` 中添加 `-Didea.logging.level=DEBUG`。日志位于 IntelliJ IDEA 配置目录下的 "log" 目录中。

- 要在 Eclipse 中启用详细输出，请修改 `eclipse.ini` 以包含 `-debug` 或 `-consoleLog`。对于详细日志记录，请配置 Log4j 或 java.util.logging。日志位置取决于日志配置。

- 要从 Maven 获取详细输出，请使用 `mvn -X <command>`。例如，`mvn -X clean install`。

- 要在 WebSphere Liberty Server 中启用详细日志记录，请配置 `server.xml` 文件以包含 `<logging traceSpecification="*=info:com.ibm.ws.*=all:"/>`。您还可以使用 `console.log` 和 `messages.log` 文件获取详细日志。

- 对于 AWS CLI 的详细输出，请使用 `--debug` 标志：`aws <command> --debug`。

- 要从 `gcloud` 获取详细输出，请使用 `--verbosity` 标志：`gcloud <command> --verbosity=debug`。

- 要在 Gradle 中启用详细输出，请使用 `-v` 或 `--verbose` 标志：`gradle <task> -v`。对于更详细的日志记录，请使用 `--debug`：`gradle <task> --debug`。

- 对于 Docker 的详细输出，请使用 `--verbose` 标志（如果特定命令可用）或检查 Docker 守护程序日志。您可以在 `daemon.json` 文件中配置 Docker 守护程序日志记录级别。

- 要从 Terraform 获取详细输出，请将 `TF_LOG` 环境变量设置为 `DEBUG` 或 `TRACE`：`export TF_LOG=DEBUG` 或 `export TF_LOG=TRACE`。

- 要启用 Ansible 的详细输出，请使用 `-v`、`-vv`、`-vvv` 或 `-vvvv` 标志以增加详细程度：`ansible-playbook playbook.yml -vvv`。

- 对于 Kubernetes `kubectl` 的详细输出，请使用 `--v` 标志后跟一个表示详细程度的数字（例如，`--v=6` 或 `--v=9`）：`kubectl get pods --v=6`。

- 要从 systemd 获取详细输出，请使用 `journalctl -b -x` 查看带有解释的日志或 `systemctl --full --all status <service>`。

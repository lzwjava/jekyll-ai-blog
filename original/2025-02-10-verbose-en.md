---
audio: false
generated: false
image: false
lang: en
layout: post
title: Verbose Output
translated: false
type: post
---

- To enable verbose output in Homebrew, use `export HOMEBREW_CURL_VERBOSE=1` in conjunction with `brew upgrade --verbose`.

- To increase verbosity in SSH, use `ssh -vvv user@host`.

- For more verbose output with `git`, use `git -v` or `git --verbose`.

- To get more output from `rsync`, use `rsync -vv source destination`.

- write verbose config in ssh config, like have LogLevel VERBOSE in .ssh/config.

- To enable verbose output with `npm`, use `npm install --verbose` or `npm run <script> --verbose`.

- For verbose logging in Node.js, use the `NODE_DEBUG` environment variable: `NODE_DEBUG=http,net node your_script.js`.

- To get verbose output from `curl`, use `curl -v <url>`.

- To enable verbose output with `pip`, use `pip install -v <package>` or `pip install --verbose <package>`.

- For verbose output with `wget`, use `wget --verbose <url>`.

- To get verbose output from `yum`, use `yum -v install <package>`.

- To enable verbose output with `apt-get`, use `apt-get -o Debug::pkgProblemResolver=yes install <package>`.

- For verbose logging with `adb`, use `adb logcat -v verbose`.

- To run Python in verbose mode, use `python -v your_script.py`.

- To compile Java code with verbose output, use `javac -verbose YourClass.java`.

- To start VSCode in verbose mode: `code --verbose`. For logging, set `"trace": true` in `settings.json` and view logs via "Developer: Open View..." -> "Log (Window)" or "Log (Extension Host)".

- For IntelliJ IDEA verbose logging: "Help" -> "Diagnostic Tools" -> "Debug Log Settings..." or add `-Didea.logging.level=DEBUG` to `idea.vmoptions`. Logs are in the "log" directory under the IntelliJ IDEA configuration directory.

- To enable verbose output in Eclipse, modify `eclipse.ini` with `-debug` or `-consoleLog`. For detailed logging, configure Log4j or java.util.logging. Log location depends on the logging configuration.

- To get verbose output from Maven, use `mvn -X <command>`. For example, `mvn -X clean install`.

- To enable verbose logging in WebSphere Liberty Server, configure the `server.xml` file to include `<logging traceSpecification="*=info:com.ibm.ws.*=all:"/>`. You can also use the `console.log` and `messages.log` files for detailed logs.

- For verbose output with the AWS CLI, use the `--debug` flag: `aws <command> --debug`.

- To get verbose output from `gcloud`, use the `--verbosity` flag: `gcloud <command> --verbosity=debug`.

- To enable verbose output in Gradle, use the `-v` or `--verbose` flag: `gradle <task> -v`. For more detailed logging, use `--debug`: `gradle <task> --debug`.

- For verbose output with Docker, use the `--verbose` flag (if available for the specific command) or check the Docker daemon logs. You can configure the Docker daemon logging level in the `daemon.json` file.

- To get verbose output from Terraform, set the `TF_LOG` environment variable to `DEBUG` or `TRACE`: `export TF_LOG=DEBUG` or `export TF_LOG=TRACE`.

- To enable verbose output with Ansible, use the `-v`, `-vv`, `-vvv`, or `-vvvv` flags for increasing verbosity: `ansible-playbook playbook.yml -vvv`.

- For verbose output with Kubernetes `kubectl`, use the `--v` flag followed by a number indicating the verbosity level (e.g., `--v=6` or `--v=9`): `kubectl get pods --v=6`.

- To get verbose output from systemd, use `journalctl -b -x` to view logs with explanations or `systemctl --full --all status <service>`.

- To enable verbose output with `bundle install`, use `bundle install --verbose`.

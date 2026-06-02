---
audio: false
date: 2025-09-11
generated: true
image: false
lang: en
layout: post
model: mistralai/mistral-medium-3.1
title: LLM Limits in Complex Workflows
translated: false
type: note
---

You're absolutely right! LLMs (including me) excel at **small, focused tasks**—like explaining a single concept, generating a short code snippet, or debugging a specific error—but struggle with **complex, multi-step workflows** that involve:

1. **Multiple interconnected configurations** (e.g., Maven `pom.xml` files, Jacoco agent args, Python test integration).
2. **Stateful dependencies** (e.g., "First update `module-A/pom.xml`, then run `mvn test` with these flags, then merge reports").
3. **Cross-system interactions** (e.g., Java + Python + CI tools like Jenkins/GitHub Actions).
4. **Context switching** (e.g., "Now forget the Java part—how do we parse the Jacoco XML in Python?").

---

### **Why LLMs Fail at Complex Workflows**
1. **No Persistent Memory**: We don’t "remember" past steps unless you explicitly remind us (and even then, context windows are limited).
2. **Linear Thinking**: We generate responses step-by-step but can’t dynamically track dependencies (e.g., "Did you run `mvn clean` before the agent?).
3. **Over-Optimization for Single Answers**: We’re trained to give *one* complete answer, not iterative guidance.
4. **No Execution Environment**: We can’t run commands to verify if `jacoco:prepare-agent` actually worked in your setup.

---

### **Better Approach: "Divide and Verify"**
For problems like **Jacoco + multi-module Maven + Python tests**, break it into **atomic steps** and verify each one. Example:

#### **Step 1: Verify Jacoco Agent Setup (Java Side)**
```bash
# In ONE module (e.g., module-A):
mvn clean test -Pcoverage
```
- **Check**: Does `target/site/jacoco/index.html` exist?
- **Debug**: If not, share the `pom.xml` snippet for Jacoco and the error log.

#### **Step 2: Generate Combined Report (Multi-Module)**
```bash
mvn jacoco:report-aggregate
```
- **Check**: Is `target/site/jacoco-aggregate/index.html` created?
- **Debug**: If missing, verify `<module>` paths in the parent `pom.xml`.

#### **Step 3: Export for Python (XML/CSV)**
```bash
# Convert Jacoco binary to XML
java -jar jacoco-cli.jar report jacoco.exec --xml output.xml
```
- **Check**: Does `output.xml` contain `<package>` tags?
- **Debug**: If empty, ensure tests ran with the agent (`-javaagent:jacocoagent.jar`).

#### **Step 4: Python Integration**
```python
import xml.etree.ElementTree as ET
tree = ET.parse("output.xml")
coverage = tree.find(".//counter[@type='LINE'][@covered]")
print(f"Covered lines: {coverage.get('covered')}/{coverage.get('missed')}")
```
- **Check**: Does the script output expected numbers?
- **Debug**: If not, share the XML structure and Python error.

---

### **How to Work with LLMs Effectively**
1. **Isolate the Problem**:
   - *"Here’s my `pom.xml` for module-A. Why doesn’t `jacoco:prepare-agent` add the VM arg?"*
   - *(Better than: "Help me set up Jacoco for 5 modules + Python.")*

2. **Share Minimal Reproducible Context**:
   - Error logs, config snippets (not entire files), and **what you’ve tried**.

3. **Iterative Debugging**:
   - **You**: "Step 1 failed with `No tests run`. Here’s the log."
   - **LLM**: "Add `<test>` goals to your `maven-surefire-plugin`."
   - **You**: "Now Step 2 works, but the report is empty..."

4. **Use Us for "Micro-Tasks"**:
   - *"Write a Python script to parse Jacoco XML and fail if coverage < 80%."*
   - *"Explain the `<execution>` tag in Maven for Jacoco."*

---

### **Tools to Automate Complex Workflows**
Since LLMs can’t manage state, use:
- **Shell scripts** (e.g., `setup_coverage.sh` to chain Maven/Python commands).
- **Makefiles** (define `make test-coverage` to run all steps).
- **CI templates** (GitHub Actions/Jenkins pipelines with explicit steps).
- **Docker** (containerize the environment to avoid "works on my machine" issues).

---
### **Key Takeaway**
**LLMs are like a super-powered `man` page or Stack Overflow on steroids**—great for **individual pieces**, but not for orchestrating entire systems. For complex tasks:
1. **Break it down**.
2. **Verify each step**.
3. **Ask targeted questions**.

Would you like me to dive deeper into any of the steps above (e.g., Jacoco XML parsing in Python or multi-module Maven setups)?

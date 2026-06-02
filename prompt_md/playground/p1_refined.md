What I want to do is use Python’s `unittest` to test API endpoints, and then generate a coverage report for a Java Spring project.

What’s special here is that the Python test cases live outside the Java project. That means I need the Maven Exec Plugin to run them.

I also need to start Jetty and keep it running. This is a multi-module project.

At first, I tried using JaCoCo’s aggregate goal.

One issue was that I added the plugins in `PlaygroundLib`, but `PlaygroundLib` has no code or tests. Running the JaCoCo plugin there misses the class file structure.

JaCoCo aggregate doesn’t work well in this setup because the coverage is not from unit tests; it’s from external Python integration tests.

So I fell back to generating per-module JaCoCo reports.

I’ve successfully done this for one module before. The flow is fine: run `jacoco:prepare-agent`, attach the Java agent to the JVM that runs Jetty or WebSphere Liberty, run the Python integration tests, and then generate the coverage report. That part works.

However, there’s a problem with one module. For `PlaygroundUtils`, there’s no controller, so there’s no integration test when building that module. But its classes do appear in the JaCoCo `.exec` file. Because of that, I need to run `PlaygroundWeb` twice—once with the JaCoCo agent for that module’s exec, and once with the agent for `PlaygroundUtils`.

What do you think overall? What’s a good strategy here? Suppose I have a larger project with ten modules—how should I approach it? If handling all ten at once is too complex, we could start with one or two modules.

Also, JaCoCo is more complicated than tools like Checkstyle or Spotless because it isn’t self-contained: it depends on external Python integration tests, and it requires JaCoCo exec files and JVM agent attachment. That makes things more complex.

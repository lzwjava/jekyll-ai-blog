
What I want to do is that use python unittest to test API endpoints, and then get coverage report from Java Spring project.

What this is special is that the python unittest cases is in outside Java project. Which means it need maven exec plugin to execute.

And it need jetty start and run.  Also this is multiple modules project.

At first, I use jacoco agggreage to do things.

One is that I use these plugin in PlaygroundLib  , however , Plaground Lib doesn't have the code or test, so jacoco plugin run there will missing class file sturute.

Jacoco aggregate can't do things like normal because it is not unit test coverage, it is outside python integration test coverage.

So I fallback to the method that we use per module jacoco report.

I have succesfully run for one module before. It is ok to combine, jacoco prepare agent, attach that java agent to jvm that jetty or Webphser Liberty Profile etc, and then run python integration test, and then get coverage report , we don't have problem with that.

But one module here, we have problem .For PlaygroundUtils, it doesn't have controller, so it doesn't have integration test when build these module. But they have class information in jacoco exe file here. So I need to run two times in PlaygroundWeb, one attach the jacoco agent exec of this module, one attach the jacoco agent exec of PlaygroundUtils.

How do you think overall? what's good strtegty to do that? Suppose I have another big project with 10 modules, how can I do? If we can't do for 10 modules, we can do for one or two modules first.

And this jacoco complicated with checkstyle or spotless is that it isn't self-contained like them, it depends outside Python integration unit test cases. Also it is that it have jacoco exec , jvm attach steps. This make things complicated.

---
audio: false
generated: true
image: false
lang: en
layout: post
title: Spring Servlet Context Initialization Failure
translated: false
type: note
---

[WARNING] org.aspectj.runtime.reflect.StringMaker scanned from multiple locations: jar:file:///Users/lzwjava/.m2/repository/org/aspectj/aspectjrt/1.9.24/aspectjrt-1.9.24.jar!/org/aspectj/runtime/reflect/StringMaker.class, jar:file:///Users/lzwjava/.m2/repository/org/aspectj/aspectjweaver/1.9.24/aspectjweaver-1.9.24.jar!/org/aspectj/runtime/reflect/StringMaker.class
[WARNING] org.aspectj.runtime.reflect.UnlockSignatureImpl scanned from multiple locations: jar:file:///Users/lzwjava/.m2/repository/org/aspectj/aspectjrt/1.9.24/aspectjrt-1.9.24.jar!/org/aspectj/runtime/reflect/UnlockSignatureImpl.class, jar:file:///Users/lzwjava/.m2/repository/org/aspectj/aspectjweaver/1.9.24/aspectjweaver-1.9.24.jar!/org/aspectj/runtime/reflect/UnlockSignatureImpl.class
[INFO] Scanning elapsed time=100ms
[INFO] No Spring WebApplicationInitializer types detected on classpath
[INFO] DefaultSessionIdManager workerName=node0
[INFO] No SessionScavenger set, using defaults
[INFO] node0 Scavenging every 600000ms
[INFO] Initializing Spring DispatcherServlet 'dispatcher'
2025-09-05T06:47:58.656+08:00 INFO  main trace- o.s.web.servlet.DispatcherServlet        :
                Initializing Servlet 'dispatcher'
2025-09-05T06:47:58.705+08:00 WARN  main trace- .s.AnnotationConfigWebApplicationContext :
                Exception encountered during context initialization - cancelling refresh attempt: org.springframework.beans.factory.BeanDefinitionStoreException: Failed to parse configuration class [org.lzw.AppConfig]; nested exception is java.io.FileNotFoundException: class path resource [jakarta/servlet/Filter.class] cannot be opened because it does not exist
2025-09-05T06:47:58.706+08:00 ERROR main trace- o.s.web.servlet.DispatcherServlet        :
                Context initialization failed
org.springframework.beans.factory.BeanDefinitionStoreException: Failed to parse configuration class [org.lzw.AppConfig]; nested exception is java.io.FileNotFoundException: class path resource [jakarta/servlet/Filter.class] cannot be opened because it does not exist
	at org.springframework.context.annotation.ConfigurationClassParser.parse(ConfigurationClassParser.java:184)
	at org.springframework.context.annotation.ConfigurationClassPostProcessor.processConfigBeanDefinitions(ConfigurationClassPostProcessor.java:325)
	at org.springframework.context.annotation.ConfigurationClassPostProcessor.postProcessBeanDefinitionRegistry(ConfigurationClassPostProcessor.java:242)
	at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanDefinitionRegistryPostProcessors(PostProcessorRegistrationDelegate.java:275)
	at org.springframework.context.support.PostProcessorRegistrationDelegate.invokeBeanFactoryPostProcessors(PostProcessorRegistrationDelegate.java:95)
	at org.springframework.context.support.AbstractApplicationContext.invokeBeanFactoryPostProcessors(AbstractApplicationContext.java:706)
	at org.springframework.context.support.AbstractApplicationContext.refresh(AbstractApplicationContext.java:532)
	at org.springframework.web.servlet.FrameworkServlet.configureAndRefreshWebApplicationContext(FrameworkServlet.java:702)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:668)
	at org.springframework.web.servlet.FrameworkServlet.createWebApplicationContext(FrameworkServlet.java:716)
	at org.springframework.web.servlet.FrameworkServlet.initWebApplicationContext(FrameworkServlet.java:591)
	at org.springframework.web.servlet.FrameworkServlet.initServletBean(FrameworkServlet.java:530)
	at org.springframework.web.servlet.HttpServletBean.init(HttpServletBean.java:170)
	at javax.servlet.GenericServlet.init(GenericServlet.java:244)
	at org.eclipse.jetty.servlet.ServletHolder$Wrapper.init(ServletHolder.java:1345)
	at org.eclipse.jetty.servlet.ServletHolder.initServlet(ServletHolder.java:632)
	at org.eclipse.jetty.servlet.ServletHolder.initialize(ServletHolder.java:415)
	at org.eclipse.jetty.servlet.ServletHandler.lambda$initialize$0(ServletHandler.java:750)
	at java.base/java.util.stream.SortedOps$SizedRefSortingSink.end(SortedOps.java:357)
	at java.base/java.util.stream.AbstractPipeline.copyInto(AbstractPipeline.java:571)
	at java.base/java.util.stream.AbstractPipeline.wrapAndCopyInto(AbstractPipeline.java:560)
	at java.base/java.util.stream.StreamSpliterators$WrappingSpliterator.forEachRemaining(StreamSpliterators.java:315)
	at java.base/java.util.stream.Streams$ConcatSpliterator.forEachRemaining(Streams.java:735)
	at java.base/java.util.stream.ReferencePipeline$Head.forEach(ReferencePipeline.java:807)
	at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:774)
	at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:379)
	at org.eclipse.jetty.webapp.WebAppContext.startWebapp(WebAppContext.java:1449)
	at org.eclipse.jetty.maven.plugin.JettyWebAppContext.startWebapp(JettyWebAppContext.java:328)
	at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1414)
	at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:916)
	at org.eclipse.jetty.servlet.ServletContextHandler.doStart(ServletContextHandler.java:288)
	at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:524)
	at org.eclipse.jetty.maven.plugin.JettyWebAppContext.doStart(JettyWebAppContext.java:397)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:73)
	at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:169)
	at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:117)
	at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:97)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:73)
	at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:169)
	at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:117)
	at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:97)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:73)
	at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:169)
	at org.eclipse.jetty.server.Server.start(Server.java:423)
	at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:110)
	at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:97)
	at org.eclipse.jetty.server.Server.doStart(Server.java:387)
	at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:73)
	at org.eclipse.jetty.maven.plugin.AbstractJettyMojo.startJetty(AbstractJettyMojo.java:449)
	at org.eclipse.jetty.maven.plugin.AbstractJettyMojo.execute(AbstractJettyMojo.java:310)
	at org.eclipse.jetty.maven.plugin.JettyRunMojo.execute(JettyRunMojo.java:150)
	at org.apache.maven.plugin.DefaultBuildPluginManager.executeMojo(DefaultBuildPluginManager.java:126)
	at org.apache.maven.lifecycle.internal.MojoExecutor.doExecute2(MojoExecutor.java:328)
	at org.apache.maven.lifecycle.internal.MojoExecutor.doExecute(MojoExecutor.java:316)
	at org.apache.maven.lifecycle.internal.MojoExecutor.execute(MojoExecutor.java:212)
	at org.apache.maven.lifecycle.internal.MojoExecutor.execute(MojoExecutor.java:174)
	at org.apache.maven.lifecycle.internal.MojoExecutor.access$000(MojoExecutor.java:75)
	at org.apache.maven.lifecycle.internal.MojoExecutor$1.run(MojoExecutor.java:162)
	at org.apache.maven.plugin.DefaultMojosExecutionStrategy.execute(DefaultMojosExecutionStrategy.java:39)
	at org.apache.maven.lifecycle.internal.MojoExecutor.execute(MojoExecutor.java:159)
	at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject(LifecycleModuleBuilder.java:105)
	at org.apache.maven.lifecycle.internal.LifecycleModuleBuilder.buildProject(LifecycleModuleBuilder.java:73)
	at org.apache.maven.lifecycle.internal.builder.singlethreaded.SingleThreadedBuilder.build(SingleThreadedBuilder.java:53)
	at org.apache.maven.lifecycle.internal.LifecycleStarter.execute(LifecycleStarter.java:118)
	at org.apache.maven.DefaultMaven.doExecute(DefaultMaven.java:261)
	at org.apache.maven.DefaultMaven.doExecute(DefaultMaven.java:173)
	at org.apache.maven.DefaultMaven.execute(DefaultMaven.java:101)
	at org.apache.maven.cli.MavenCli.execute(MavenCli.java:906)
	at org.apache.maven.cli.MavenCli.doMain(MavenCli.java:283)
	at org.apache.maven.cli.MavenCli.main(MavenCli.java:206)
	at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104)
	at java.base/java.lang.reflect.Method.invoke(Method.java:565)
	at org.codehaus.plexus.classworlds.launcher.Launcher.launchEnhanced(Launcher.java:255)
	at org.codehaus.plexus.classworlds.launcher.Launcher.launch(Launcher.java:201)
	at org.codehaus.plexus.classworlds.launcher.Launcher.mainWithExitCode(Launcher.java:361)
	at org.codehaus.plexus.classworlds.launcher.Launcher.main(Launcher.java:314)

---
audio: false
generated: true
lang: en
layout: post
title: Project Files in VSCode
translated: false
type: note
---

This issue with the `filterResources` tag being repeatedly added to your `.project` file in Maven Spring Boot projects is typically caused by the Eclipse/M2Eclipse integration that's happening in the background.

When you're working with a Maven project in an IDE (even VSCode), the Maven plugins can automatically generate or modify Eclipse project files (like `.project`). The `filterResources` tag specifically is added when Maven resource filtering is configured in your project.

Here are a few approaches to prevent this automatic generation:

1. **Configure your m2e plugin settings**:
   You can add configuration to your pom.xml that tells the m2e plugin how to handle resource filtering without modifying the .project file:

   ```xml
   <build>
     <pluginManagement>
       <plugins>
         <plugin>
           <groupId>org.eclipse.m2e</groupId>
           <artifactId>lifecycle-mapping</artifactId>
           <version>1.0.0</version>
           <configuration>
             <lifecycleMappingMetadata>
               <pluginExecutions>
                 <pluginExecution>
                   <pluginExecutionFilter>
                     <groupId>org.apache.maven.plugins</groupId>
                     <artifactId>maven-resources-plugin</artifactId>
                     <versionRange>[2.0,)</versionRange>
                     <goals>
                       <goal>resources</goal>
                       <goal>testResources</goal>
                     </goals>
                   </pluginExecutionFilter>
                   <action>
                     <ignore />
                   </action>
                 </pluginExecution>
               </pluginExecutions>
             </lifecycleMappingMetadata>
           </configuration>
         </plugin>
       </plugins>
     </pluginManagement>
   </build>
   ```

2. **VSCode specific settings**:
   In VSCode, you might be using the Java or Maven extensions. You can check their settings to see if you can disable the automatic Eclipse project file generation or modification:

   - Open settings (Ctrl+,)
   - Search for "maven" or "java" settings related to project generation
   - Look for options like "Update Configuration" or "Project Generation"

3. **Use .gitattributes instead of .gitignore**:
   If you want to keep the file, but prevent Git from seeing changes to it:

   ```
   moduleA/.project merge=ours
   ```

   This tells Git to always keep your version during merges.

4. **Examine your workspace settings**:
   Check if any VSCode extensions are automatically running Maven commands that might trigger this behavior.

The exact solution might depend on which Maven/Java extensions you're using in VSCode. If you share which specific extensions you're using for Maven/Java development, I could provide more targeted advice.

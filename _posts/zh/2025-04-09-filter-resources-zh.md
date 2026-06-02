---
audio: false
generated: true
lang: zh
layout: post
title: VSCode中的项目文件
translated: true
type: note
---

Maven Spring Boot 项目中 `.project` 文件反复被添加 `filterResources` 标签的问题，通常是由 Eclipse/M2Eclipse 集成在后台运行导致的。

当您在 IDE（即使是 VSCode）中处理 Maven 项目时，Maven 插件会自动生成或修改 Eclipse 项目文件（如 `.project`）。`filterResources` 标签特别会在项目配置了 Maven 资源过滤时被添加。

以下是几种防止自动生成的解决方案：

1. **配置 m2e 插件设置**：
   您可以在 pom.xml 中添加配置，指示 m2e 插件如何处理资源过滤而不修改 .project 文件：

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

2. **VSCode 特定设置**：
   在 VSCode 中，您可能正在使用 Java 或 Maven 扩展。可以检查相关设置以禁用自动生成或修改 Eclipse 项目文件的功能：

   - 打开设置（Ctrl+,）
   - 搜索与项目生成相关的 "maven" 或 "java" 设置
   - 查找如“更新配置”或“项目生成”等选项

3. **使用 .gitattributes 替代 .gitignore**：
   若希望保留文件但避免 Git 检测其变更：

   ```
   moduleA/.project merge=ours
   ```

   这会在合并时始终保留您的版本。

4. **检查工作区设置**：
   确认是否有 VSCode 扩展自动运行了可能触发此行为的 Maven 命令。

具体解决方案可能取决于您在 VSCode 中使用的 Maven/Java 扩展。如果您能说明正在使用哪些具体的 Maven/Java 开发扩展，我可以提供更具针对性的建议。

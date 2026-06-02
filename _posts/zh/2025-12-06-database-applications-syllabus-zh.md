---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 数据库及其应用教学大纲
translated: true
type: note
---

# 广东省高等教育自学考试
**课程：数据库及其应用（实践）**
**课程代码：13171**

## 一、考核目标
本课程旨在使学生掌握数据库系统的基本概念、理论和操作技术，为将来从事数据库管理系统及数据库应用系统的开发工作，打下坚实的理论基础和实践技能。

要求学生：
- 熟练掌握SQL结构化查询语言的基本语法
- 了解并会实现存储过程、存储函数、触发器、事务、数据库备份与恢复、权限管理
- 能够读懂、书写和调试代码
- 熟练使用MySQL创建、管理和维护数据库
- 在MySQL中实现存储过程、函数、触发器、事务、备份/恢复、权限管理
- 培养独立分析问题和解决问题的能力

## 二、参考教材
张英新主编，《数据库及其应用》，机械工业出版社，2023年版。

## 三、考核内容

### 1. SQL结构化查询语言
（1）MySQL准备：启动/停止MySQL服务，连接/断开服务器
（2）数据库创建：CREATE DATABASE、USE、SHOW DATABASES、DROP DATABASE等
（3）数据表创建：CREATE TABLE、PRIMARY KEY、FOREIGN KEY、ALTER TABLE、DROP TABLE等
（4）数据操纵：INSERT INTO、UPDATE、DELETE等
（5）查询语句：SELECT、FROM、WHERE、ORDER BY、GROUP BY、HAVING；统计函数；字符串操作算符、IS NULL/IS NOT NULL、BETWEEN AND、IN/NOT IN、UNION；编写SQL实现实际查询
（6）连接查询：自然连接、左/右外连接、自身连接；编写多表查询
（7）嵌套查询：子查询；编写简单嵌套查询

### 2. 数据库程序设计
（1）存储过程：CREATE PROCEDURE、调用过程、实现业务逻辑
（2）SQL程序设计基础：BEGIN…END、注释、变量（声明、赋值）、控制流语句
（3）存储函数：CREATE FUNCTION、RETURN、调用函数、实现业务逻辑
（4）触发器：概念、特点、优点；CREATE TRIGGER；NEW和OLD的用法；实现触发器

### 3. 事务与事务处理
（1）事务、ACID特性：START TRANSACTION、COMMIT、ROLLBACK
（2）并发性问题：脏读、不可重复读、幻读
（3）隔离级别：MySQL的四种隔离级别
（4）封锁协议：封锁粒度、共享锁（S）和排它锁（X）
（5）MySQL的锁：隐式加锁/显式加锁、行级锁和表级锁语句

### 4. 备份与恢复
（1）数据备份：完全备份与增量备份；mysqldump命令
（2）事务日志：概念、恢复原理；MySQL的7种日志文件及其作用；二进制日志操作
（3）利用二进制日志实现增量备份：开启/关闭binlog、进行增量备份
（4）恢复：简单恢复模式与完全恢复模式；利用mysqldump备份和二进制日志进行恢复

### 5. 安全管理
（1）MySQL权限体系：权限级别；DBA、数据库资源使用者、普通用户
（2）权限表：user、db、tables_priv等
（3）账户管理：CREATE USER、DROP USER；查看用户、修改密码
（4）授予/收回权限：GRANT、REVOKE
（5）角色：CREATE ROLE、将角色授予用户、撤销角色
（6）视图：CREATE VIEW、ALTER VIEW、DROP VIEW；可更新视图

## 四、考试形式（总分：100分）
1. 单选题：10题 × 1分 = 10分
2. 多选题：5题 × 2分 = 10分
3. 代码填空题：10空 × 2分 = 20分
4. 程序分析题：2题 × 10分 = 20分
5. 编程题：8题 × 5分（居多） = 40分

## 五、考试要求
- 仅笔试
- 时间：120分钟
- 覆盖率：覆盖所有章节
- 难度分配：容易题20%、中等偏易35%、中等偏难35%、难题10%

## 六、网络环境
无

## 七、考生须知
- 必须使用黑色/蓝色水笔作答（不可使用铅笔）
- 填空题、分析题、编程题所有代码均须使用MySQL兼容的SQL

## 八、题型示例

### 1. 单项选择题（10题，10分）
1. (   ) 是长期存储在计算机内、有组织、可共享、减少冗余度、数据独立性高的数据集合。
A．数据模型 B．数据 C．DBMS D．数据库
**答案：D**

### 2. 多项选择题（5题，10分）
1. MySQL有7种日志文件，以下属于MySQL日志文件的有（ ）
A．Redo log B．Undo log C．Binary log D．Slow query log
**答案：ABCD**

### 3. 代码填空题（10空，20分）
1. 查詢学生表，并对行记录加共享锁：
```sql
SELECT * FROM student
WHERE sno = 's001' LOCK IN ________;  -- 空1
```
**答案：SHARE MODE**

### 4. 程序分析题（2题，20分）
基于经典的“学生-课程”数据库模式。
示例分析CREATE TABLE语句，包含约束和触发器。

### 5. 编程题（8题，40分）
例：
已知：Course(Cno, Cname, Credit, Intro)，SC(Sno, Cno, Grade)，Student(Sno, Sname, Age, Dept)
（1）创建课程表Course，包含合适的字段类型和主键（5分）
（2）查询平均成绩大于等于60分的课程号和平均成绩（5分）
（3）查询选修“操作系统”课程的学生姓名和成绩，并按成绩降序排序（5分）
（4）创建视图C1，包含课程名、学分和简介（5分）
（5）利用视图C1查询学分为3的课程（5分）
（6）将学号为“202411”的学生的年龄更新为20岁（5分）
（7）在课程名上创建索引“index_1”（3分）
（8）删除选课表SC以及所有数据（5分）

**答案示例：**
```sql
(1) CREATE TABLE Course (
    Cno CHAR(12),
    Cname VARCHAR(50),
    Credit INT,
    Intro TEXT,
    PRIMARY KEY (Cno)
);
(2) SELECT Cno, AVG(Grade) FROM SC GROUP BY Cno HAVING AVG(Grade) >= 60;
(3) SELECT Sname, Grade
    FROM Student S JOIN SC ON S.Sno = SC.Sno
    JOIN Course C ON SC.Cno = C.Cno
    WHERE Cname = '操作系统'
    ORDER BY Grade DESC;
(4) CREATE VIEW C1 AS SELECT Cname, Credit, Intro FROM Course;
(5) SELECT * FROM C1 WHERE Credit = 3;
(6) UPDATE Student SET Age = 20 WHERE Sno = '202411';
(7) CREATE INDEX index_1 ON Course(Cname);
(8) DROP TABLE SC;
```

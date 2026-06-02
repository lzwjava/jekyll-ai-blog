---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Database and Its Applications Syllabus Translation
translated: false
type: note
---

Question: Please translate the full Guangdong Higher Education Self-Examination syllabus for the course "Database and Its Applications (Practical)" (Course Code: 13171) into English and format it neatly using clean Markdown.

Answer:

# Guangdong Higher Education Self-Examination
**Course: Database and Its Applications (Practical)**
**Course Code: 13171**

## I. Assessment Objectives
This course aims to enable students to master the basic concepts, theories, and operational techniques of database systems, laying a solid theoretical foundation and practical skills for future work in developing database management systems and database application systems.

Students are required to:
- Proficiently master the basic syntax of Structured Query Language (SQL)
- Understand and implement stored procedures, stored functions, triggers, transactions, database backup and recovery, and privilege management
- Be able to read, write, and debug code
- Proficiently use MySQL to create, manage, and maintain databases
- Implement stored procedures, functions, triggers, transactions, backup/recovery, and privilege management in MySQL
- Develop independent problem-analysis and problem-solving abilities

## II. Reference Textbook
*Database and Its Applications*, edited by Zhang Yingxin, China Machine Press, 2023 edition.

## III. Assessment Content

### 1. Structured Query Language (SQL)
(1) MySQL preparation: starting/stopping MySQL server, connecting/disconnecting from server
(2) Database creation: CREATE DATABASE, USE, SHOW DATABASES, DROP DATABASE, etc.
(3) Table creation: CREATE TABLE, PRIMARY KEY, FOREIGN KEY, ALTER TABLE, DROP TABLE, etc.
(4) Data manipulation: INSERT INTO, UPDATE, DELETE, etc.
(5) Query statements: SELECT, FROM, WHERE, ORDER BY, GROUP BY, HAVING; aggregate functions; string operators, IS NULL/IS NOT NULL, BETWEEN AND, IN/NOT IN, UNION; writing SQL for real-world queries
(6) Join queries: natural join, left/right outer join, self-join; writing multi-table queries
(7) Nested queries: subqueries; writing simple nested queries

### 2. Database Programming
(1) Stored procedures: CREATE PROCEDURE, calling procedures, implementing business logic
(2) SQL programming basics: BEGIN…END, comments, variables (declaration, assignment), control flow statements
(3) Stored functions: CREATE FUNCTION, RETURN, calling functions, implementing business logic
(4) Triggers: concept, features, advantages; CREATE TRIGGER; usage of NEW and OLD; implementing triggers

### 3. Transactions and Transaction Processing
(1) Transactions, ACID properties: START TRANSACTION, COMMIT, ROLLBACK
(2) Concurrency issues: dirty read, non-repeatable read, phantom read
(3) Isolation levels: MySQL's four isolation levels
(4) Locking protocols: lock granularity, shared (S) and exclusive (X) locks
(5) MySQL locking: implicit/explicit locking, row-level and table-level locking statements

### 4. Backup and Recovery
(1) Data backup: full vs. incremental backup; mysqldump command
(2) Transaction logs: concept, recovery principles; MySQL's 7 types of log files and their roles; binary log operations
(3) Incremental backup using binary logs: enabling/disabling binlog, performing incremental backup
(4) Recovery: simple and full recovery models; restoring from mysqldump backups and binary logs

### 5. Security Management
(1) MySQL privilege system: privilege levels; DBA, database resource users, ordinary users
(2) Privilege tables: user, db, tables_priv, etc.
(3) Account management: CREATE USER, DROP USER; viewing users, changing passwords
(4) Granting/revoking privileges: GRANT, REVOKE
(5) Roles: CREATE ROLE, granting roles to users, revoking roles
(6) Views: CREATE VIEW, ALTER VIEW, DROP VIEW; updatable views

## IV. Exam Structure (Total: 100 points)
1. Single-choice questions: 10 questions × 1 point = 10 points
2. Multiple-choice questions: 5 questions × 2 points = 10 points
3. Code completion (fill-in-the-blank): 10 blanks × 2 points = 20 points
4. Program analysis questions: 2 questions × 10 points = 20 points
5. Programming questions: 8 questions × 5 points (most) = 40 points

## V. Exam Requirements
- Paper-based exam only
- Duration: 120 minutes
- Must cover all chapters
- Difficulty distribution: Easy 20%, Moderately easy 35%, Moderately difficult 35%, Difficult 10%

## VI. Network Environment
None required

## VII. Notes for Candidates
- Use black/blue pen only (no pencil)
- All code in fill-in, analysis, and programming questions must use MySQL-compatible SQL

## VIII. Sample Question Types (Translated)

### 1. Single-Choice Questions (10 questions, 10 points)
1. (   ) is a large, organized, shared collection of data stored long-term in a computer, with minimal redundancy and high data independence.
A. Data model B. Data C. DBMS D. Database
**Answer: D**

### 2. Multiple-Choice Questions (5 questions, 10 points)
1. MySQL has 7 types of log files. Which of the following are MySQL log files? ( )
A. Redo log B. Undo log C. Binary log D. Slow query log
**Answer: ABCD**

### 3. Code Completion (10 blanks, 20 points)
1. To query the student table with a row-level shared lock:
```sql
SELECT * FROM student
WHERE sno = 's001' LOCK IN ________;  -- Blank 1
```
**Answer: SHARE MODE**

### 4. Program Analysis Questions (2 questions, 20 points)
Based on the classic Student-Course database schema.
Example analysis of a CREATE TABLE statement with constraints and triggers.

### 5. Programming Questions (8 questions, 40 points)
Example (translated and corrected):
Given tables: Course(Cno, Cname, Credit, Intro), SC(Sno, Cno, Grade), Student(Sno, Sname, Age, Dept)

(1) Create the Course table with appropriate data types and primary key (5 pts)
(2) Find course numbers and average grades for courses with average ≥60 (5 pts)
(3) Find names and grades of students who took the "Operating System" course, sorted by grade descending (5 pts)
(4) Create view C1 showing course name, credit, and introduction (5 pts)
(5) Query courses with 3 credits using view C1 (5 pts)
(6) Update age to 20 for student ID "202411" (5 pts)
(7) Create index "index_1" on course name (3 pts)
(8) Drop the SC table and all its data (5 pts)

**Sample Answers (corrected English version):**
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
    WHERE Cname = 'Operating System'
    ORDER BY Grade DESC;
(4) CREATE VIEW C1 AS SELECT Cname, Credit, Intro FROM Course;
(5) SELECT * FROM C1 WHERE Credit = 3;
(6) UPDATE Student SET Age = 20 WHERE Sno = '202411';
(7) CREATE INDEX index_1 ON Course(Cname);
(8) DROP TABLE SC;
```

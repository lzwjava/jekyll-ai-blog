---
audio: false
generated: true
image: false
lang: en
layout: post
model: anthropic/claude-4.5-sonnet
title: SQL Codebase Mastery Prompts Guide
translated: false
type: note
---

Here are some effective prompts for working with large SQL codebases:

## Understanding & Documentation
- "Analyze this SQL code and create a high-level overview of what it does, including main data flows"
- "Document each section of this stored procedure with inline comments explaining the business logic"
- "Create a data lineage diagram showing how data flows through these procedures"
- "List all tables, views, and temporary tables used in this code with their purposes"

## Analysis & Optimization
- "Identify potential performance bottlenecks in this SQL code"
- "Find any redundant queries or logic that could be consolidated"
- "Review this for SQL injection vulnerabilities and suggest fixes"
- "Analyze the indexing strategy needed to optimize these queries"
- "Point out any deprecated DB2 syntax that should be updated"

## Migration & Conversion
- "Convert this DB2 stored procedure to PostgreSQL/MySQL/SQL Server syntax"
- "Identify DB2-specific features in this code that would need alternatives when migrating"
- "Break this monolithic procedure into smaller, modular components"

## Debugging & Maintenance
- "Find potential null handling issues in this code"
- "Identify where error handling should be added"
- "Locate any hardcoded values that should be parameterized"
- "Check for transaction management issues or missing commits/rollbacks"

## Specific Deep Dives
- "Explain the logic in lines 450-520 step by step"
- "What would happen if [specific condition] occurs in this procedure?"
- "Trace the execution path when parameter X has value Y"

**Pro tips**: Break very long SQL into logical sections, provide context about the business purpose, mention any specific concerns upfront, and ask follow-up questions to drill into specific areas.
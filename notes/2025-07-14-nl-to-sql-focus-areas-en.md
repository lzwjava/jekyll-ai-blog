---
audio: false
generated: true
lang: en
layout: post
title: Building Accurate and Secure NL-to-SQL Systems
translated: false
type: note
---

### Key Focus Areas When Building an NL-to-SQL System

Building a natural language to SQL (NL-to-SQL) system involves translating user queries in everyday language into executable SQL statements, often using AI models like LLMs (e.g., GPT variants or specialized models like those from Hugging Face). Based on your PostgreSQL schema and example query, here are the main areas to focus on:

#### 1. **Accuracy and Understanding of the Schema**

- **Schema Awareness**: Always provide the full database schema (tables, columns, data types, relationships) in the AI prompt. This helps the model generate correct SQL. In your case, emphasize columns like `first_name`, `created_at`, `date_of_birth`, and `last_login` to avoid hallucinations (e.g., inventing non-existent fields).
- **Handling Ambiguity**: Natural language is vague—e.g., "around the day last month" could mean ±1 day, but clarify via prompts to interpret fuzzy terms (e.g., "recent week" as 7 days). Use examples in prompts to guide interpretations.
- **Data Types and Functions**: Focus on PostgreSQL-specific syntax, like using `AGE()` for dates, `ILIKE` for case-insensitive strings, and proper casting (e.g., `CAST(created_at AS DATE)` in your example). Train or fine-tune the model on SQL dialect differences.
- **Edge Cases**: Handle complex queries like joins (if multiple tables), aggregations (e.g., COUNT, SUM), or subqueries. Test for queries involving sensitive fields like `password_hash` or `account_balance`.

#### 2. **Performance and Optimization**

- Generate efficient SQL: Encourage the model to use indexes (e.g., on `created_at` or `first_name`), limit results (add `LIMIT` by default), and avoid full-table scans.
- Scalability: For large datasets, integrate query optimization tools or validate generated SQL against an explain plan.

#### 3. **Error Handling and Validation**

- Parse and validate generated SQL before execution (e.g., using a SQL parser library like `sqlparse` in Python).
- Provide fallback responses: If the query is unclear, prompt the user for clarification instead of generating invalid SQL.

#### 4. **Security and Safety**

- **Preventing SQL Injection**: The risk comes from executing the generated SQL. Never concatenate user input directly into SQL strings. Instead:
  - Use **parameterized queries** or prepared statements when executing (e.g., in Python with `psycopg2`: `cursor.execute("SELECT * FROM users WHERE first_name = %s", (name,))`).
  - Instruct the AI to generate SQL with placeholders (e.g., `WHERE first_name ILIKE %s`) and bind values separately.
  - Sanitize NL inputs: Pre-process user queries to remove malicious patterns (e.g., using regex to detect SQL keywords like "DROP" or ";").
  - Limit to read-only: Restrict the AI to generating SELECT queries only—block DDL (e.g., CREATE/DROP) or DML (e.g., INSERT/UPDATE) via prompt instructions like "Only generate SELECT statements; do not modify data."
- **Controlling Data Access**:
  - **Row-Level Security (RLS)**: In PostgreSQL, enable RLS policies on tables (e.g., `ALTER TABLE users ENABLE ROW LEVEL SECURITY; CREATE POLICY user_policy ON users USING (role = current_user);`). This ensures queries only return rows the user has access to.
  - **Views and Roles**: Create restricted views (e.g., `CREATE VIEW safe_users AS SELECT id, username, first_name FROM users;`) and grant access via database roles. The AI should query views instead of base tables.
  - **API Layer**: Wrap the system in an API (e.g., using FastAPI) that authenticates users and applies access controls (e.g., JWT tokens to determine user roles).
  - **Sandbox Execution**: Run queries in a read-only replica database or a containerized environment (e.g., Docker) to isolate from production data.
  - **Audit Logging**: Log all generated SQL and executions for monitoring.
- **Data Privacy**: Avoid exposing sensitive columns (e.g., `password_hash`, `email`) by blacklisting them in prompts: "Do not select sensitive fields like password_hash, email unless explicitly needed and authorized."
- **Rate Limiting and Quotas**: Prevent abuse by limiting queries per user/session.

#### 5. **Prompt Engineering for Controlled Conversion**

- The quality of NL-to-SQL depends heavily on how you instruct the AI. Use structured prompts with these elements:
  - **System Prompt Template**:

       ```
       You are an expert SQL generator for PostgreSQL. Given the schema below and a natural language query, generate a safe, accurate SELECT query.

       Schema:
       [Insert full schema here, e.g., CREATE TABLE users (...)]

       Rules:
       - Only generate SELECT statements. No INSERT, UPDATE, DELETE, or DDL.
       - Use parameterized placeholders (e.g., %s) for user-provided values to prevent injection.
       - Handle dates with PostgreSQL functions like AGE(), CURRENT_DATE, INTERVAL.
       - For ambiguous terms (e.g., "around last month"), interpret as [specific rule, e.g., ±1 day from the same day last month].
       - Limit results to 100 rows unless specified.
       - If the query involves age, calculate as of the current year or specified year (e.g., EXTRACT(YEAR FROM AGE(CURRENT_DATE, date_of_birth)) = 20).
       - Do not select sensitive columns like password_hash, email.
       - If unclear, respond with "Clarify: [question]".

       User Query: [NL query]
       ```

  - **Examples in Prompts**: Include 2-3 shot examples, like your provided query and generated SQL, to guide the model.
  - **Chain of Thought**: Instruct the model to reason step-by-step: "First, identify key filters. Second, map to columns. Third, build WHERE clause."
  - **Fine-Tuning**: If using a custom model, fine-tune on datasets like Spider or WikiSQL, augmented with your schema-specific examples.
  - **Testing**: Evaluate with metrics like execution accuracy (does it run without errors?) and semantic match (does it return expected results?).

#### Potential Improvements to Your Example Query

While not the main question, your generated SQL has some good elements but could be safer/more precise:

- Use parameters: Change to `WHERE first_name ILIKE %s` and bind 'andy'.
- Age "as of 2025": Use `EXTRACT(YEAR FROM AGE('2025-12-31'::date, date_of_birth)) = 20` to fix to a specific year-end.
- Add `ORDER BY last_login DESC LIMIT 10;` for safety.

Implementing this safely requires a backend layer (e.g., not executing SQL directly from the AI output). Start small with a script using an LLM library (e.g., LangChain for NL-to-SQL chains).

If you need code examples or help with specific parts (e.g., a Python implementation), provide more details!

**References**
[PostgreSQL Documentation: Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
[LangChain NL-to-SQL Tutorial](https://python.langchain.com/docs/tutorials/sql_qa/)
[Preventing SQL Injection in Python](https://realpython.com/prevent-python-sql-injection/)

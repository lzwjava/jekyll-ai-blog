---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-code-fast-1
title: Calling DB2 Stored Procedures with Parameters
translated: false
type: note
---

### Assumptions and Context

Your query appears to refer to calling a *stored procedure* (likely a typo for "store procedure") in an IBM database system, such as IBM DB2 (on Linux/Unix/Windows, z/OS, or iSeries). Stored procedures are executable scripts stored in the database that can accept input parameters, perform operations, and return output or results. The exact syntax depends on the programming language and IBM environment (e.g., SQL, COBOL, RPG, or Java via JDBC). I'll focus on the most common case: SQL-based CALL statements in DB2, as this is standard for relational databases.

If you're using a different IBM platform (e.g., IBM i CL commands, MQ, or Watson Query), provide more details for tailored advice.

### How to Pass Parameters in a DB2 Stored Procedure Call

Stored procedures in DB2 are called using the `CALL` statement in SQL. Parameters are passed in a comma-separated list within parentheses, matching the procedure's definition (e.g., IN for input, OUT for output, INOUT for both).

#### Step-by-Step Guide

1. **Define or Know the Procedure Signature**: Ensure you know the procedure's name and parameters. For example, a procedure might be defined as:

   ```sql
   CREATE PROCEDURE update_employee (IN emp_id INT, IN new_salary DECIMAL(10,2), OUT status_msg VARCHAR(100))
   ```

   - Here, `emp_id` is input (IN), `new_salary` is input, and `status_msg` is output (OUT).

2. **Use the CALL Statement**: In a SQL environment (e.g., DB2 Command Line Processor, or embedded in programs like Java), call the procedure like this:

   ```sql
   CALL update_employee(12345, 75000.00, ?);
   ```

   - The `?` is a placeholder for OUT parameters. In programmatic calls, handle outputs with result sets or host variables.
   - Inputs are passed as literals or variables; outputs are captured via placeholders or bound variables.

3. **Handling Parameter Types**:
   - **IN parameters**: Pass values directly (e.g., numbers, strings in quotes).
   - **OUT/INOUT parameters**: Use `?` in the CALL, then bind them in your code to retrieve values after execution.
   - Match the order and types exactly; mismatches cause errors (e.g., SQLCODE -440 for invalid parameters).

4. **In Code Examples**:
   - **Via DB2 CLP (Command Line)**: Direct SQL execution.

     ```sql
     CALL my_proc('input_value', ?);
     ```

     Retrieve OUT params with `FETCH FIRST FROM` or in scripts.
   - **Via JDBC (Java)**:

     ```java
     CallableStatement stmt = conn.prepareCall("{CALL update_employee(?, ?, ?)}");
     stmt.setInt(1, 12345);          // IN param
     stmt.setBigDecimal(2, new java.math.BigDecimal("75000.00")); // IN param
     stmt.registerOutParameter(3, Types.VARCHAR); // OUT param
     stmt.execute();
     String status = stmt.getString(3); // Retrieve OUT
     ```

   - **Via RPG on IBM i**: Use `CALLP` with variable declarations matching parameter types.

     ```rpg
     D PROC_PARAM    S                   LIKE(PARAM_TYPE)
     PROC_PARAM = 'value';
     CALLP MY_PROC(PROC_PARAM);
     ```

   - **Error Handling**: Check SQLSTATE or SQLCODE post-call; e.g., '00000' means success.

#### Key Tips and Evidence

- **Evidence from DB2 Documentation**: Per IBM's official DB2 SQL Reference (e.g., for LUW v11.5 or z/OS), the `CALL` statement is defined with optional parameter lists. For instance, the syntax is: `CALL procedure-name [(parameter [, parameter] ...)]`. This matches industry standards for relational databases and is supported across DB2 variants for consistency (see IBM Knowledge Center).
- **Variations**: In IBM i (AS400), procedures might use CL (Command Language) calls like `CALL PGM(MYPROC) PARM('value')` for RPG programs. For mainframe COBOL, embed `EXEC SQL CALL...` with host variables.
- **Testing**: Use `db2 describe routine procedure_name` to inspect parameters before calling.
- **Limitations**: Large parameter sets may need arrays or result sets; complex types require specific handling.

If this doesn't match your setup (e.g., if it's IBM Watson or another tool), share more context like the platform or language for precise instructions.

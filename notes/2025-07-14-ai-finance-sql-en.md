---
audio: false
generated: true
lang: en
layout: post
title: Using AI to Improve Products in Financial Projects
translated: false
type: note
---

Based on your experience working on the Finance Transformation Platform, where you're handling backend systems for financial data processing, workflows, and integrations with tools like Java, Spring Boot, and Db2, AI can indeed play a transformative role. Your idea of using AI to "search financial headers" aligns well with natural language processing (NLP) applications, like converting user queries into SQL for efficient data retrieval. This can democratize access to complex financial datasets, allowing non-technical stakeholders (e.g., finance teams) to query things like ledger entries, transaction headers, or approval statuses without writing code. Your example of generating SQL from natural language is a perfect starting point—let's break it down and expand on broader applications.

#### Analyzing Your SQL Generation Example
Your natural language query ("get some users whose firstname is andy, created_at around the day last month, who are 20 years old as of 2025, and whose last_login like recent week") is a solid demonstration of how AI can bridge everyday language to database operations. The generated SQL query you provided is mostly effective and leverages PostgreSQL features well:

```sql
SELECT *
FROM users
WHERE first_name ILIKE 'andy'
  AND CAST(created_at AS DATE) BETWEEN
      (CURRENT_DATE - INTERVAL '1 MONTH' - INTERVAL '1 DAY')
      AND
      (CURRENT_DATE - INTERVAL '1 MONTH' + INTERVAL '1 DAY')
  AND EXTRACT(YEAR FROM AGE(date_of_birth)) = 20
  AND last_login >= CURRENT_TIMESTAMP - INTERVAL '7 DAYS';
```

- **Strengths**:
  - `ILIKE 'andy'` handles case-insensitivity, which is user-friendly.
  - The `created_at` clause interprets "around the day last month" as a ±1 day window around the equivalent date last month (e.g., if today is July 14, 2025, it queries June 13–15). This is a reasonable approximation for "around," though the phrase is somewhat ambiguous—AI tools often need clear prompts to avoid misinterpretation.
  - `last_login >= CURRENT_TIMESTAMP - INTERVAL '7 DAYS'` accurately captures "recent week."

- **Potential Improvements**:
  - The age condition (`EXTRACT(YEAR FROM AGE(date_of_birth)) = 20`) calculates the current age as of July 14, 2025, which would select users who are exactly 20 years old today (accounting for whether their birthday has passed). However, "20 years old as of 2025" might better mean users who turn 20 during the year 2025 (i.e., born in 2005). A simpler, more precise alternative could be:
    ```sql
    AND date_of_birth BETWEEN '2005-01-01' AND '2005-12-31'
    ```
    Or equivalently:
    ```sql
    AND EXTRACT(YEAR FROM date_of_birth) = 2005
    ```
    This avoids runtime age calculations and focuses on the birth year, which is often more stable for "as of [year]" queries in financial or compliance contexts (e.g., age-based eligibility for accounts).
  - To make it more robust, add limits (e.g., `LIMIT 10`) if you want "some users," and consider time zones for timestamps if the system is global.
  - In a financial project, adapt this to your Db2 database—PostgreSQL syntax like `AGE()` and `ILIKE` might need tweaks (e.g., use `CURRENT DATE - date_of_birth` for age and `LOWER(first_name) LIKE 'andy'`).

AI tools like Copilot (which you mentioned using heavily) or advanced models (e.g., via APIs from OpenAI or Google Cloud) excel at this NL-to-SQL translation. In your setup, integrate it into workflows by building a chatbot interface that parses queries about financial headers (e.g., "Show unapproved headers from last quarter with balances over $10K") and generates/executes SQL safely, with guardrails for security.

#### Broader Ways to Use AI in Financial Backend Systems
In projects like yours—focusing on data import/validation/export, workflows, and banking systems—AI can boost efficiency, reduce errors, and enable innovation. Drawing from industry trends, here are practical applications tailored to backend engineering:

- **Automating Data Processing and Validation**:
  - Use machine learning (ML) models to detect anomalies in financial data imports (e.g., unusual ledger entries or mismatches in headers). For instance, train models on historical data to flag fraud or errors during validation, potentially reducing manual reviews by 30–50%. Tools like Python's scikit-learn or TensorFlow (available in your environment) can prototype this.
  - AI-driven OCR and NLP for document processing: Extract data from PDFs or scanned financial statements automatically, classifying headers and integrating with Db2.

- **Optimizing Workflows and Approvals**:
  - Implement predictive AI to forecast workflow bottlenecks (e.g., approval delays for new headers) based on historical patterns. This could use time-series analysis to prioritize tasks in Control-M schedules.
  - Generative AI for dynamic routing: In submission/approval flows, AI can suggest next steps or auto-approve low-risk items, speeding up releases from UAT to production.

- **Enhancing Code Development and Maintenance**:
  - As you've done with Copilot for root-cause analysis, Python scripts, and documentation, expand to AI-assisted code reviews or bug fixing. For multithreading issues in Java/Spring Boot, AI can generate optimized code snippets or profile performance (complementing YourKit).
  - Your AspectJ-based AI agent idea is innovative—collecting logs and converting debug states to text for AI analysis. This could evolve into a "banking-specific IDE" like Cursor, where AI queries logs in natural language (e.g., "Why did this transaction fail?") and suggests fixes. To implement: Use AspectJ for instrumentation, pipe logs to an LLM (via xAI API or similar), and build a feedback loop for continuous improvement.

- **Advanced Analytics and Insights**:
  - NL-to-SQL extensions: Beyond queries, use AI for generating reports on financial trends (e.g., "Summarize header submissions by department last month").
  - Risk and Compliance: AI models for real-time credit risk assessment or regulatory checks, analyzing ledger data to predict issues before export.

- **Scalability and Integration**:
  - Leverage AI for system optimization, like auto-scaling resources in WebSphere based on load predictions.
  - In outsourced setups, AI can standardize documentation (you mentioned 50 guides), making them searchable via semantic search.

These approaches can lead to cost savings (e.g., 20–30% productivity gains in software engineering) and better products, but start small: Pilot NL-to-SQL in a sandbox, ensure data privacy (critical in banking), and measure ROI through metrics like reduced deployment time.

If you're building that AI agent, consider open-source frameworks like LangChain for chaining log analysis with SQL generation. For pricing on APIs or subscriptions, check official sites as details vary.

**References**
- [AI and bank software development | Deloitte Insights](https://www.deloitte.com/us/en/insights/industry/financial-services/financial-services-industry-predictions/2025/ai-and-bank-software-development.html)
- [AI in Banking: Applications, Benefits and Examples | Google Cloud](https://cloud.google.com/discover/ai-in-banking)
- [Extracting value from AI in banking: Rewiring the enterprise | McKinsey](https://www.mckinsey.com/industries/financial-services/our-insights/extracting-value-from-ai-in-banking-rewiring-the-enterprise)
- [AI in Finance: Applications, Examples & Benefits | Google Cloud](https://cloud.google.com/discover/finance-ai)
- [Top AI Applications in Finance for 2025: [Benefits & Success Stories] | Acropolium](https://acropolium.com/blog/artificial-intelligence-applications-in-finance-real-world-success-cases/)
- [QueryGPT - Natural Language to SQL using Generative AI | Uber Blog](https://www.uber.com/blog/query-gpt/)
- [NL2SQL with BigQuery and Gemini | Google Cloud Blog](https://cloud.google.com/blog/products/data-analytics/nl2sql-with-bigquery-and-gemini)

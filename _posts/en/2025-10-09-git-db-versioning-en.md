---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Git-Friendly Database Version Control
translated: false
type: note
---

### Choosing Between JSON (or CSV) and SQLite for Git-Friendly Version Control

For a small database with 1-2 tables and 10k-100k records, both JSON and SQLite are viable options since the total file size should stay manageable (likely under 10-50 MB even for denser data). The key challenge you're facing—git diffs treating the entire file as a binary blob on every update—is common with databases. Git excels at text-based diffs, so formats like JSON shine there, while SQLite (a single binary file) requires workarounds for readable changes.

I'll break it down by pros/cons, then recommend based on your priorities.

#### Quick Comparison

| Aspect              | JSON (or CSV)                                                                 | SQLite                                                                 |
|---------------------|-------------------------------------------------------------------------------|------------------------------------------------------------------------|
| **File Format**    | Text-based (human-readable). Easy line-by-line diffs in git.                  | Binary file. Git shows full-file changes; diffs are unreadable by default. |
| **Size for 10k-100k Records** | Small if records are simple (e.g., 1-5 KB per record → 10-500 MB total). Compresses well in git. | Similar size, but no compression gains from text diffs.                |
| **Git Experience** | Excellent: See exact added/edited lines. Use tools like `git diff --word-diff` for structured changes. Sort data consistently for clean diffs. | Poor out-of-box. Fix with custom git config (e.g., dump to SQL on diff). Or use extensions like Dolt for git-like database versioning. |
| **Updates**        | Full rewrite on save, but diffs highlight changes if you load/edit/save selectively (e.g., via scripts). | Atomic transactions, but every commit looks like a full replace in git. |
| **Querying/Features** | Basic (filter with code like jq/Python). No indexing/transactions. Good for flat data. | Full SQL: Queries, joins (for 2 tables), indexes, constraints. Better for any "database" feel. |
| **Use Case Fit**   | Ideal if your app/script handles CRUD in memory and you prioritize collab/diffs. | Better if you need real DB ops; diffs are secondary.                   |
| **Tools Needed**   | Native git + jq (for JSON) or csvkit (for CSV).                               | sqlite3 CLI + git attributes for custom diffs.                         |

#### Recommendations
- **Go with JSON (or CSV) if easy diffs are your top priority**: This keeps everything text-based and git-native. For 1-2 tables:
  - Use **one JSON file** as an array of objects (e.g., `[{"id":1, "name":"foo", ...}, ...]`). It's flexible for simple relations (embed one table in the other).
  - Or **CSV files** (one per table) for stricter tabular data—super lightweight and diff-friendly. Tools like Pandas can load/edit/export them.
  - **Workflow tip**: Always sort records by ID/key before saving (e.g., in Python: `df.sort_values('id').to_csv(...)`). This makes diffs show only real changes, not reorder noise. For updates, read → modify specific rows → sort → write. File size stays small, and git history is clean.
  - Drawback: For 100k records, loading the whole file into memory each time might be slow without optimization (e.g., use streaming libs like ijson).

- **Use SQLite if you need database functionality**: It's more robust for queries/joins, and the single-file setup is simple for git commits. To fix the diff issue:
  - Add a `.gitattributes` file: `*.db diff=sqlite` and a `.gitconfig` snippet to dump the DB to SQL on diff (e.g., via `sqlite3 db dump.sql`). This converts binary changes to readable SQL inserts/updates.
  - Example setup script (in bash/Python): On commit, export schema/data as SQL files for review.
  - For advanced needs, consider Dolt—it's like "git for databases" with branchable tables and proper diffs, but it's heavier for tiny setups.

Start with JSON/CSV for simplicity—it's "good enough" for small-scale and aligns with your git concern. If you outgrow it (e.g., need complex queries), migrate to SQLite later. Prototype both: Dump sample data to files and test a few git commits.

If your records have a specific structure, share more details for tailored code snippets.

[Versioning SQLite in Git](https://dunkels.com/adam/git-diff-sqlite3/)
[JSON vs DB for Small Data](https://www.reddit.com/r/flask/comments/lvccgo/using_a_database_such_as_sqlite3_versus_json_to/)
[Data Version Control Options](https://dolthub.com/blog/2022-04-27-data-version-control/)

import psycopg2

# Connect to your postgres database
conn = psycopg2.connect(
    dbname="mydatabase",
    user="lzw",
    password="lzwpassword",  # Replace with your actual password
    host="localhost",
)

cur = conn.cursor()

# Example: Create a simple table named 'example_table'
cur.execute("""
    CREATE TABLE IF NOT EXISTS example_table (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

conn.commit()
cur.close()

print("Table created successfully.")

# Insert some rows into 'example_table' using the same connection
cur = conn.cursor()
cur.execute(
    "INSERT INTO example_table (name) VALUES (%s), (%s), (%s);",
    ("Alice", "Bob", "Charlie"),
)
conn.commit()
cur.close()

print("Rows inserted successfully.")
# Query some rows from 'example_table' using the same connection
cur = conn.cursor()
cur.execute("SELECT id, name, created_at FROM example_table;")
rows = cur.fetchall()
for row in rows:
    print(row)
cur.close()
conn.close()

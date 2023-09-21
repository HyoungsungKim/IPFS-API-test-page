import sqlite3

conn = sqlite3.connect("../db/asset-metadata.db")

cur = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS asset_metadata (
    api_key TEXT,
    content_id TEXT,
    name TEXT,
    category TEXT,
    sub_category TEXT,
    attributes TEXT
)
"""

# Create table
cur.execute(create_table_query)

# Create separate tables for main, sub, and subsub
cur.execute("""
CREATE TABLE IF NOT EXISTS category (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_value TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sub_category (
    sub_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sub_category_value TEXT UNIQUE
)
""")



cur.execute("""
CREATE TABLE IF NOT EXISTS attributes (
    attributes_id INTEGER PRIMARY KEY AUTOINCREMENT,
    attributes_value TEXT UNIQUE
)
""")



# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
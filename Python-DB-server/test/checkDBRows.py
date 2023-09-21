import sqlite3

def view_table_data(table_name):
    # Connect to the database
    conn = sqlite3.connect("../db/asset-metadata.db")
    cur = conn.cursor()

    # Execute a query to fetch all rows from the table
    cur.execute(f"SELECT * FROM {table_name}")

    # Fetch all the rows and print the data
    rows = cur.fetchall()
    for row in rows:
        print(row)

    # Close the connection
    conn.close()

# Replace 'your_table_name' with the name of the table you want to view
view_table_data('asset_metadata')

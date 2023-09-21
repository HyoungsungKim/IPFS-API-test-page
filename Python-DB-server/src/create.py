import sqlite3
import json

from fastapi import FastAPI

from utils import Item

app = FastAPI()


def check_and_add_category(conn, cur, category_value, category_table):
    """

    """    
    # Check if the category exists in the category_table
    cur.execute(f"SELECT {category_table}_id FROM {category_table} WHERE {category_table}_value=?", (category_value,))
    category_id = cur.fetchone()

    if not category_id:
        # If the category does not exist, insert it into the category_table
        cur.execute(f"INSERT INTO {category_table} ({category_table}_value) VALUES (?)", (category_value,))
        conn.commit()
        category_id = cur.lastrowid
        added_new_category = True
    else:
        category_id = category_id[0]
        added_new_category = False

    return category_id, added_new_category


@app.post("/upload_data")
def upload_data(item: Item):
    # Access the data using the item parameter
    api_key = item.api_key
    content_id = item.content_id
    name = item.name
    category = item.category
    sub_category = item.sub_category
    attributes = json.dumps(item.attributes)

    # Insert the data into the SQLite database
    conn = sqlite3.connect("../db/asset-metadata.db")
    cur = conn.cursor()
    
    # Check and add category, sub_category, and attributes
    category_id, category_added = check_and_add_category(conn, cur, category, "category")
    sub_category_id, sub_category_added = check_and_add_category(conn, cur, sub_category, "sub_category")
    attributes_id, attributes_added = check_and_add_category(conn, cur, attributes, "attributes")

    # Print notice for duplicate categories
    if not category_added:
        print(f"Warning: Duplicate main category '{category}' encountered at id '{category_id}'.")
    if not sub_category_added:
        print(f"Warning: Duplicate sub category '{sub_category}' encountered at id '{sub_category_id}'.")
    if not attributes_added:
        print(f"Warning: Duplicate attributes '{attributes}' at id '{attributes_id}'.")
    
    cur.execute("INSERT INTO asset_metadata (api_key, content_id, name, category, sub_category, attributes) VALUES (?, ?, ?, ?, ?, ?)",
                (api_key, content_id, name, category, sub_category, attributes))
    conn.commit()
    conn.close()

    return {"message": "Data uploaded successfully"}

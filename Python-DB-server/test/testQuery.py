import requests
import sqlite3

# Database connection
conn = sqlite3.connect("../db/asset-metadata.db")
cur = conn.cursor()

# Test data
test_data = [
    ('test123', 'QmULnvqn2Pknc8iUifYRkZQN5AZsDB9fPtGHiagvxERLe4', 'test_chair', 'Animals', 'Mammals', '["Dog, white"]'),
    ('test123', 'QmULnvqn2Pknc8iUifYRkZQN5AZsDB9fPtGHiagvxERLe4', 'test_chair', 'Animals', 'Birds', '["Swallow, white"]')
]

# Insert test data
for data in test_data:
    cur.execute(
        "INSERT INTO asset_metadata (api_key, content_id, name, category, sub_category, attributes) VALUES (?, ?, ?, ?, ?, ?)",
        data
    )
conn.commit()

# API server address
api_server_address = "http://127.0.0.1:8000"
response0 = requests.get(f"{api_server_address}/query")

# Test the API endpoint with category only and category with sub-category
response1 = requests.get(f"{api_server_address}/query/categories?category=Animals")
response2 = requests.get(f"{api_server_address}/query/categories?category=Animals&sub_category=Birds")

# Print the responses
print("Response for ping:")
print(response0.json())

print("Response for category 'Animals':")
print(response1.json())

print("Response for category 'Animals' and sub-category 'Birds':")
print(response2.json())

# Remove test data
'''
for data in test_data:
    cur.execute(
        "DELETE FROM asset_metadata WHERE api_key = ? AND content_id = ? AND name = ? AND category = ? AND sub_category = ? AND attributes = ?",
        data
    )
conn.commit()
'''
# Close the database connection
conn.close()

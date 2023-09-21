from fastapi import FastAPI

from create import app as create_app  # Assuming this contains routes for creating entries
from query import app as query_app    # Assuming this contains routes for querying entries

app = FastAPI()
app.mount("/create", create_app)
app.mount("/query", query_app)

@app.get("/")
def read_status():
    return {"status": "Online"}

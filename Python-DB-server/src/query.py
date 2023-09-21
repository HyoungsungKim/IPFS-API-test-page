from typing import Union, List
import json

import sqlite3

from fastapi import FastAPI, HTTPException

from utils import AssetMetadataResponse

app = FastAPI()
@app.get("/")
def read_status():
    return {"status": "Online"}

@app.get("/categories", response_model=List[AssetMetadataResponse])
def query_to_ipfs(category: str, sub_category: Union[str, None] = None):
    """
        This endpoint queries the SQLite database to retrieve asset metadata based on the specified category and optionally, the sub-category.

        Args:
        category (str): The category to filter the assets. This parameter is required.
        sub_category (str, optional): The sub-category to filter the assets within the specified category. This parameter is optional.

        Returns:
        List[AssetMetadataResponse]: A list of asset metadata matching the specified category and sub-category filters. Each item in the list is a dictionary containing the following keys:
            - content_id (str): The ID of the content.
            - name (str): The name of the content.
            - category (str): The category of the content.
            - sub_category (str): The sub-category of the content.
            - attributes (str): The attributes of the content.

        Raises:
        HTTPException: If there is a database error or an unexpected error occurs during the query process.
    """
    try:
        with sqlite3.connect("../db/asset-metadata.db") as conn:
            cur = conn.cursor()

            if sub_category:
                cur.execute(
                    "SELECT content_id, name, category, sub_category, attributes FROM asset_metadata WHERE category=? AND sub_category=?",
                    (category, sub_category)
                )
            else:
                cur.execute(
                    "SELECT content_id, name, category, sub_category, attributes FROM asset_metadata WHERE category=?",
                    (category,)
                )
            
            results = cur.fetchall()
            return [AssetMetadataResponse(
                content_id=row[0],
                name=row[1],
                category=row[2],
                sub_category=row[3],
                attributes=[item.strip() for item in json.loads(row[4])[0].split(',')]
            ) for row in results]
    except sqlite3.DatabaseError as err:
        raise HTTPException(status_code=500, detail="Database error") from err
    except Exception as err:
        raise HTTPException(status_code=500, detail="Unexpected error") from err

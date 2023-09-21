from pydantic import BaseModel

# Define a Pydantic model to represent the data in the request body
class Item(BaseModel):
    """
        Class defining database table. This table represents metadata of asset.
    """
    api_key: str
    content_id: str
    name: str
    category: str
    sub_category: str
    attributes: list

class AssetMetadataResponse(BaseModel):
    '''
        This metadata does not include api_key for a security/privacy issue
    '''
    content_id: str
    name: str
    category: str
    sub_category: str
    attributes: list
from pydantic import BaseModel

class ApiKeyInfo(BaseModel):
    key_id: str
    creation_time: str


class ApiKey(BaseModel):
    api_key: str
    key_id: str

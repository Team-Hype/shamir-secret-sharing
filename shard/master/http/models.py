from pydantic import BaseModel

class KeyValueSecret(BaseModel):
    key: str
    value: str

class KeySecret(BaseModel):
    key: str

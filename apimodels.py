from pydantic import BaseModel

class UserObject(BaseModel):
    id: str
    name: str
    email:str


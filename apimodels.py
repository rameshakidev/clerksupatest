from pydantic import BaseModel

class UserObject(BaseModel):
    user_id: str
    name: str
    email:str


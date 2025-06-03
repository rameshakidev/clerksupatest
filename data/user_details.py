from apimodels import UserObject

class UserDetails:
    userId:str
    name:str
    email:str

    def __init__(self, userId:str, name:str, email:str)->None:
        self.userId = userId
        self.name = name
        self.email = email

    def getReponseUser(self)->UserObject:
        return UserObject(user_id=self.userId, name=self.name, email=self.email)
    
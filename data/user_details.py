from apimodels import UserObject

class UserDetails:
    userId:str
    name:str
    address:str

    def __init__(self, userId:str, name:str, address:str)->None:
        self.userId = userId
        self.name = name
        self.address = address

    def getReponseUser(self)->UserObject:
        return UserObject(user_id=self.userId, name=self.name, address=self.address)
    
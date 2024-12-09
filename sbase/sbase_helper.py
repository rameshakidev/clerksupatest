import os
from supabase import create_client, Client
from data.user_details import UserDetails

class SupabaseHelper:
    supabaseURL:str = 'https://ehgvhvtkautoneuqhpic.supabase.co'
    supabaseKey:str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVoZ3ZodnRrYXV0b25ldXFocGljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg5Mzc2MDcsImV4cCI6MjA0NDUxMzYwN30.L4igPTVpL5Pc2WchEFYyTiOHdvFRq25rPwkOFHafaBE'
    supabaseClient:Client

    def __init__(self)->None:
        #self.supabaseURL = os.environ.get("SUPABASE_URL")
        #self.supabaseKey = os.environ.get("SUPABASE_KEY")
        #print(f'URL is {self.supabaseURL} and Key is {self.supabaseKey}')
        self.supabaseClient = create_client(self.supabaseURL, self.supabaseKey)

    def create_user(self, jwtTemplate:str, name:str, address:str)->list[UserDetails]:
        self.supabaseClient.postgrest.auth(jwtTemplate)
        query_result = self.supabaseClient.table("TestTable_Ignore").insert({"name": name, "address":address}).execute()
        if (len(query_result.data) > 0):
            users = query_result.data[0]
            return users
        else:
            return None

    def get_user_details(self, jwtTemplate:str)->list[UserDetails]:
        self.supabaseClient.postgrest.auth(jwtTemplate)
        query_result = self.supabaseClient.table("TestTable_Ignore").select("*").execute()
        if (len(query_result.data) > 0):
            users = []
            for nextUser in query_result.data:
                usrInfo:UserDetails = UserDetails(
                    userId=nextUser["user_id"], 
                    name=nextUser["name"],
                    address=nextUser["address"],
                )
                users.append(usrInfo)
            return users
        else:
            return None

if (__name__ == "__main__"):
    supabaseHelper = SupabaseHelper()
    query_result = supabaseHelper.get_user_details(1)
    if (query_result):
        print(f'Found {len(query_result)} users in the system')
    else:
        print(f'Failed to retrieved any users in the system')
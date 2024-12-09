import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from starlette.middleware.sessions import SessionMiddleware
from apimodels import UserObject
from sbase.sbase_helper import SupabaseHelper
from clerk.clerk_helper import ClerkHelper
from config import SESSION_SECRET_KEY
from data.user_details import UserDetails

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY, max_age=None)
app.mount("/static", StaticFiles(directory="static",html = True), name="static")
    
# Get information about all users
@app.get("/users",
         tags=["Users"], 
         dependencies=[Depends(HTTPBearer())],
         summary="Get information about all users in the system", 
         response_model= list[UserObject])
async def get_users(request:Request, session_id:str):
    clerkHelper = ClerkHelper()
    signedIn = clerkHelper.is_signed_in(request, session_id)
    if (not signedIn):
        return {"message": f'Unauthorized: Failed to validate user.'}
    jwtTemplate = clerkHelper.getJWTTemplateToken(session_id)
    supabaseHelper = SupabaseHelper()
    #supabaseHelper.create_user(jwtTemplate.jwt, "Second User", "Second Address")
    user_details:UserDetails = supabaseHelper.get_user_details(jwtTemplate.jwt)
    if (not user_details):
        return {"message": f'Failed to find any users in the system'}
    users = []
    for user in user_details: 
        respUser = user.getReponseUser()
        users.append(respUser)
    return users

if (__name__ == '__main__'):
     uvicorn.run(app, host="0.0.0.0", port=10000)

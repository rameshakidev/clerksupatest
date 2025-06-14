import uvicorn
import os
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBearer
from starlette.middleware.sessions import SessionMiddleware
from apimodels import UserObject
from sbase.sbase_helper import SupabaseHelper
from clerk.clerk_helper import ClerkHelper
from config import SESSION_SECRET_KEY
from data.user_details import UserDetails

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY, max_age=None)
templates = Jinja2Templates(directory="templates")

supabaseURL:str = os.environ.get('SUPABASE_URL')
supabaseKey:str = os.environ.get('SUPABASE_KEY')
clerk_dev_instance_url:str = os.environ.get('CLERK_DEV_INSTANCE_URL')
clerk_dev_publishable_key:str = os.environ.get('CLERK_DEV_PUBLISHABLE_KEY')
clerk_dev_secret_key:str = os.environ.get('CLERK_DEV_SECRET_KEY')
url_to_invoke:str = os.environ.get('URL_TO_INVOKE')
token_to_use:str = os.environ.get("TOKEN_TO_USE")

# Get index file
@app.get("/",
         tags=["/"], 
         summary="Get index file", 
         response_model= str)
async def get_index(request:Request):
    environment = 'development'
    clerk_instance_url = clerk_dev_instance_url
    clerk_publishable_key = clerk_dev_publishable_key
    url_to_invoke = f'get/users'
    return templates.TemplateResponse("index.html", 
                                      {"request": request, 
                                       "environment": environment,
                                       "clerk_instance_url": clerk_instance_url,
                                       "clerk_publishable_key": clerk_publishable_key, 
                                       "url_to_invoke":url_to_invoke})

# Get information about all users
@app.get("/get/users",
         tags=["Users"], 
         dependencies=[Depends(HTTPBearer())],
         summary="Get information about all users in the system", 
         response_model= list[UserObject])
async def get_users(request:Request, session_id:str):
    clerk_secret_key = clerk_dev_secret_key
    clerkHelper = ClerkHelper(clerk_secret_key)
    signedIn = clerkHelper.is_signed_in(request, session_id)
    if (not signedIn):
        return {"message": f'Unauthorized: Failed to validate user.'}
    jwtTemplate = clerkHelper.getJWTTemplateToken(session_id)
    supabaseHelper = SupabaseHelper(supabaseURL, supabaseKey)
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
     uvicorn.run(app, host="127.0.0.1", port=8000)

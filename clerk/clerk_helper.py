from clerk_backend_api import Clerk
from clerk_backend_api.models import VerifyClientRequestBody
import jwt
from  jwt.algorithms import RSAAlgorithm


class ClerkHelper:

    bearer_token:str
    template_id:str
    client:Clerk

    def __init__(self, clerk_secret_key:str, template_id:str=None):
        self.template_id = "supabase" if (template_id == None) else template_id
        self.client = Clerk(bearer_auth=clerk_secret_key)


    def getJWTTemplateToken(self, session_id:str, template_id=None):
        res = self.client.sessions.create_token_from_template(
            session_id=session_id, 
            template_name=self.template_id if (template_id == None) else template_id)
        return res
        
    def is_signed_in(self, request, sessionId):
        jwtToken = request.headers["authorization"].replace('Bearer', '').lstrip().rstrip()
        payload = None
        #print(f'Token in request is {jwtToken}')

        # Decode the token and check contents
        jwks_data = self.client.jwks.get()
        public_key = jwks_data.keys[0]
        #print(f'JSON: {public_key.model_dump_json()}')
        public_key = RSAAlgorithm.from_jwk(public_key.model_dump_json())
        try:
            payload = jwt.decode(
                jwtToken,
                public_key,
                algorithms=["RS256"],
                options={"verify_signature": True},
            )
        except jwt.ExpiredSignatureError:
            print(f"Token has expired.")
        except jwt.DecodeError as e:
            print(f"Token decode error.")
        except jwt.InvalidTokenError:
            print(f"Invalid token.")

        print(f'Payload is: {payload}')
        user_id = payload.get("sub")

        # Verify the request token
        try:
            resp = self.client.clients.verify(request={"token":jwtToken})
        except Exception as e:
            print(f'Failed to verify token, exception is: {e}')
            return True if (payload.get('sid') == sessionId) else False
        
        return resp

if (__name__ == "__main__"):
    ch = ClerkHelper("")
    tmpl = ch.getJWTTemplateToken('')
    print(f"The template is {tmpl}")
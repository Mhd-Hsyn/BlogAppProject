from decouple import config
import jwt, datetime
from webApi.models import *

def UserGenerateToken(fetchuser):
    try:
        secret_key = config("user_jwt_token")
        total_days = 1
        token_payload = {
            "id": str(fetchuser.id),
            "email":fetchuser.email,
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=total_days),
        }
        detail_payload = {
            "id": str(fetchuser.id),
            "email":fetchuser.email,
            "first_name": fetchuser.fname,
            "last_name": fetchuser.lname,
            "profile": fetchuser.profile.url
        }
        token = jwt.encode(token_payload, key= secret_key, algorithm="HS256")
        UserJWTWhiteListToken.objects.create(user_id = fetchuser, token = token)
        return {"status": True, "token" : token, "payload": detail_payload}
    except Exception as e:
        return {"status": False, "message": f"Error during generationg token {str(e)}"}


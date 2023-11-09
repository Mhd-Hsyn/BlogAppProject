from decouple import config
import jwt, datetime
from webApi.models import *

def UserGenerateToken(fetchuser):
    """
    Generate JWT token for User
    and save the token in User-JWT-Whitelist table
    """
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


def UserDeleteToken(fetchuser, request):
    """
    Delete the Users authenticate token 
    as well as delete users all expiry tokens
    expiry token can get when we decode the token
    """
    try:
        token = request.META["HTTP_AUTHORIZATION"][7:]
        whitelist_token = UserJWTWhiteListToken.objects.filter(user_id = fetchuser, token = token).first()
        whitelist_token.delete()
        user_all_tokens = UserJWTWhiteListToken.objects.filter(user_id = fetchuser)
        for fetch_token in user_all_tokens:
            try:
                decode_token = jwt.decode(fetch_token.token, config('user_jwt_token'), "HS256")
            except:    
                fetch_token.delete()
        return True
    except Exception :
        return False


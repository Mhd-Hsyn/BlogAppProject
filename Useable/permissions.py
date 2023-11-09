import jwt 
from decouple import config
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from webApi.models import UserJWTWhiteListToken

class UserPermission(BasePermission):
    """
    Creating Custom Permission class for User
        - Get JWT token, then decode the token
        - if token decode successuflly then get the id from token
        - Then query to User-whitelist-Token Table if exists, then give the permission 
    """
    def has_permission(self, request, view):
        try:
            auth_token = request.META["HTTP_AUTHORIZATION"][7:]
            decode_token = jwt.decode(auth_token, config('user_jwt_token'), "HS256")
            whitelist = UserJWTWhiteListToken.objects.filter(user_id =  decode_token['id'], token = auth_token).exists()
            if not whitelist:
                raise AuthenticationFailed("You must need to Login first")
            request.auth = decode_token
            return True
        except AuthenticationFailed as af:
            raise af
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed({"status": False,"error":"Session Expired !!"})
        except jwt.DecodeError:
            raise AuthenticationFailed({"status": False,"error":"Invalid token"})
        except Exception as e:
            raise AuthenticationFailed({"status": False,"error":"Need Login"})
        

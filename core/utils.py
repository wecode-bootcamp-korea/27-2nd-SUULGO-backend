import jwt
import requests

from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models           import User
from suulgo.settings        import SECRET_KEY, ALGORITHM

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization')

            if not token:
                return JsonResponse({'message':'TOKEN_REQUIRED'}, status=401)

            payload      = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            request.user = User.objects.get(id = payload['id'])

            return func(self, request, *args, **kwargs)

        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)

    return wrapper

class KakaoAPI:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_user(self):
        self.url = 'https://kapi.kakao.com/v2/user/me'
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        result = requests.get(self.url, headers=self.headers).json()

        return result

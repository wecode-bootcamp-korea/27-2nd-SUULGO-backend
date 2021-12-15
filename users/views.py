import json

import requests
import jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models           import User, Survey
from suulgo.settings        import SECRET_KEY, ALGORITHM

class KakaoLoginView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization']
            url          = 'https://kapi.kakao.com/v2/user/me'
            headers      = {
                "Authorization": f"Bearer {access_token}",
            }
            result       = requests.get(url,headers=headers).json()

            kakao_id          = result["id"]
            name              = result["properties"]["nickname"]
            profile_image_url = result["kakao_account"]["profile"]["profile_image_url"]
            email             = result["kakao_account"]["email"]

            User.objects.filter(kakao_id=kakao_id).update(
                profile_image_url = profile_image_url
            )

            user, created = User.objects.get_or_create(
                kakao_id          = kakao_id,
                name              = name,
                email             = email,
                profile_image_url = profile_image_url
            )

            payload = {'id' : user.id}

            token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)

            if Survey.objects.filter(id=user.id).exists():
                return JsonResponse({"MESSAGE": "SUCCESS", "TOKEN": token, "RESULT": result, "SURVEY": True}, status=200)
            else:
                return JsonResponse({"MESSAGE": "SUCCESS", "TOKEN": token, "RESULT": result, "SURVEY": False}, status=200)

        except ValidationError:
            return JsonResponse({"MESSAGE": "VALIDATION_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

import requests
import jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError

from users.models           import User, Survey
from suulgo.settings        import SECRET_KEY, ALGORITHM
from core.utils             import authorization

class ProfileView(View):
    @authorization
    def get(self, request):

        user    = request.user

        results = {
                'name'             : user.name,
                'profile_image_url': user.profile_image_url,
                'email'            : user.email,
                'survey_info'      : [
                    {
                        'class_number'     : survey.class_number,
                        'stack'            : survey.stack,
                        'alcohol_limit'    : survey.alcohol_limit,
                        'alcohol_level'    : survey.alcohol_level,
                        'comment'          : survey.comment,
                        'favorite_place'   : survey.favorite_place,
                        'favorite_food'    : survey.favorite_food,
                        'hobby'            : survey.hobby,
                        'gender'           : survey.gender.name,
                        'mbti_name'        : survey.mbti.name,
                        'mbti_information' : survey.mbti.information
                    }
                    for survey in user.survey_set.all()
                ]
        }


        return JsonResponse({"RESULT": results, "MESSAGE": "SUCCESS"}, status=200)

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
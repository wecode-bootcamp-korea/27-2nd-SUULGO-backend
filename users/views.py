import requests
import jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from enum                   import Enum

from users.models           import *
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

class Stack(Enum):
    FRONT = 1
    BACK  = 2

class AlcoholLimit(Enum):
    ZERO  = 1
    HALF  = 2
    ONE   = 3
    N     = 4

class ProductView(View):
    @authorization
    def get(self, request, product_id):
        try:
            product                 = Survey.objects.get(user=product_id)
            user_survey             = Survey.objects.get(user=request.user)
            user_drinking_methods   = DrinkingMethod.objects.filter(surveys__id = user_survey.id)
            user_alcohol_categories = AlcoholCategory.objects.filter(surveys__id = user_survey.id)
            user_flavor             = Flavor.objects.filter(surveys__id = user_survey.id)

            stack_dict = {1:"프론트", 2:"백"}
            alcohol_limit_dict = {1:"알쓰", 2:"반병", 3:"한병", 4:"N병"}

            result = {
                "id"                       : product.user.id,
                "profile_image_url"        : product.user.profile_image_url,
                "text_name"                : product.user.name,
                "text_email"               : product.user.email,
                "text_gender"              : product.gender.name,
                "text_mbti_title"          : product.mbti.name,
                "text_mbti_description"    : product.mbti.information,
                "text_class_number"        : product.class_number,
                "text_comment"             : product.comment,
                "text_favorite_place"      : product.favorite_place, 
                "text_favorite_food"       : product.favorite_food, 
                "text_favorite_hobby"      : product.hobby,
                "text_stack"               : stack_dict.get(product.stack),
                "alcohol_limit"            : {
                    "name" : alcohol_limit_dict.get(product.alcohol_limit),
                    "is_matching" : product.alcohol_limit == user_survey.alcohol_limit 
                    },
                "alcohol_level"            : { 
                    "name" : product.alcohol_level, 
                    "is_matching" : product.alcohol_level == user_survey.alcohol_level 
                    },
                "alcohol_drinking_methods" : [{
                    "name" : product_drinking.drinking_method.name, 
                    "is_matching" : product_drinking.drinking_method in user_drinking_methods
                    } for product_drinking in product.surveydrinkingmethod_set.prefetch_related("drinking_method")],
                "alcohol_categories"       : [{
                    "name" : product_alcohol_category.alcohol_category.name, 
                    "is_matching" : product_alcohol_category.alcohol_category in user_alcohol_categories
                    } for product_alcohol_category in product.surveyalcoholcategory_set.prefetch_related("alcohol_category")],
                "alcohol_flavors"          : [{
                    "name" : product_flavor.flavor.name, 
                    "is_matching" : product_flavor.flavor in user_flavor
                    } for product_flavor in product.surveyflavor_set.prefetch_related("flavor")]
            }

            return JsonResponse({ "result" : result }, status=200)

        except Survey.DoesNotExist:
            return JsonResponse({ "message" : "DoesNotExist" }, status=400)


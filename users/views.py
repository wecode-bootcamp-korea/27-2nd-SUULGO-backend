import json, requests, jwt

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from enum                   import Enum

from users.models           import *
from datetime               import datetime
from core.utils             import KakaoAPI, authorization
from suulgo.settings        import SECRET_KEY, ALGORITHM

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

        return JsonResponse({"result": results, "message": "SUCCESS"}, status=200)

class KakaoLoginView(View):
    def get(self, request):
        try:
            access_token = request.headers['Authorization']

            kakao_client = KakaoAPI(access_token)
            user_info = kakao_client.get_user()

            kakao_id          = user_info["id"]
            name              = user_info["properties"]["nickname"]
            profile_image_url = user_info["kakao_account"]["profile"]["profile_image_url"]
            email             = user_info["kakao_account"]["email"]

            user, created = User.objects.get_or_create(
                kakao_id          = kakao_id,
                name              = name,
                email             = email,
                defaults          = {"profile_image_url" : profile_image_url}
            )

            User.objects.filter(kakao_id=kakao_id).update(
                profile_image_url = profile_image_url
            )

            payload = {'id' : user.id}

            token   = jwt.encode(payload, SECRET_KEY, ALGORITHM)

            return JsonResponse({"message": "SUCCESS", "token": token, "result": user_info, "survey": Survey.objects.filter(id=user.id).exists()}, status=200)

        except ValidationError:
            return JsonResponse({"message": "VALIDATION_ERROR"}, status=400)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)

class Stack(Enum):
    FRONT = 1
    BACK  = 2

class AlcoholLimit(Enum):
    ZERO  = 1
    HALF  = 2
    ONE   = 3
    N     = 4

class UserView(View):
    @authorization
    def get(self, request, user_id):
        try:
            opponent                = Survey.objects.get(user=user_id)
            user_survey             = Survey.objects.get(user=request.user)
            user_drinking_methods   = user_survey.drinking_methods.all()
            user_alcohol_categories = user_survey.alcohol_categories.all()
            user_flavors            = user_survey.flavors.all()

            result = {
                "id"                       : opponent.user.id,
                "profile_image_url"        : opponent.user.profile_image_url,
                "text_name"                : opponent.user.name,
                "text_email"               : opponent.user.email,
                "text_gender"              : opponent.gender.name,
                "text_mbti_title"          : opponent.mbti.name,
                "text_mbti_description"    : opponent.mbti.information,
                "text_class_number"        : opponent.class_number,
                "text_comment"             : opponent.comment,
                "text_favorite_place"      : opponent.favorite_place,
                "text_favorite_food"       : opponent.favorite_food,
                "text_favorite_hobby"      : opponent.hobby,
                "text_stack"               : opponent.stack.name,
                "alcohol_limit"            : {
                    "name"                 : opponent.alcohol_limit.name,
                    "is_matching"          : opponent.alcohol_limit.name == user_survey.alcohol_limit.name
                    },
                "alcohol_level"            : {
                    "name"                 : opponent.alcohol_level,
                    "is_matching"          : opponent.alcohol_level == user_survey.alcohol_level
                    },
                "alcohol_drinking_methods" : [{
                    "name"                 : opponent_drinking.name,
                    "is_matching"          : opponent_drinking in user_drinking_methods
                    } for opponent_drinking in opponent.drinking_methods.all()],
                "alcohol_categories"       : [{
                    "name"                 : opponent_alcohol_category.name,
                    "is_matching"          : opponent_alcohol_category in user_alcohol_categories
                    } for opponent_alcohol_category in opponent.alcohol_categories.all()],
                "alcohol_flavors"          : [{
                    "name"                 : opponent_flavor.name,
                    "is_matching"          : opponent_flavor in user_flavors
                    } for opponent_flavor in opponent.flavors.all()]
            }

            return JsonResponse({ "result" : result }, status=200)

        except Survey.DoesNotExist:
            return JsonResponse({ "message" : "DoesNotExist" }, status=400)

class UserListView(View):
    def get(self, request):

        offset              = int(request.GET.get("offset", 0))
        limit               = int(request.GET.get("limit", 100))
        alcohol_category_id = int(request.GET.get("alcohol_category_id", 0))

        users = User.objects.filter(survey__surveyalcoholcategory__alcohol_category_id=alcohol_category_id).prefetch_related('survey_set')[offset:offset+limit]

        result_list = [{
            "id"                : user.id,
            "name"              : user.name,
            "class_number"      : Survey.objects.get(user=user).class_number,
            "profile_image_url" : user.profile_image_url,
        } for user in users ]

        return JsonResponse({'result':result_list}, status=200)

class AppointmentView(View):
    @authorization
    def post(self, request):
        try:
            data         = json.loads(request.body)
            requester    = request.user
            respondent   = User.objects.get(id=data['respondent_id'])
            string_date  = data['time']

            date_format  = '%Y-%m-%d'
            promise_date = datetime.strptime(string_date,date_format).date()

            if datetime.now().date() >= promise_date:
                return JsonResponse({'message':'DATE_ERROR'}, status=400)

            if Meeting.objects.filter(requester=requester, time=promise_date).exists():
                return JsonResponse({'message':'ALREADY_EXISTS'}, status=400)

            Meeting.objects.create(requester=requester, respondent=respondent, time=promise_date)
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message':'DoesNotExist'}, status=400)

class AppointmentAlarmView(View):
    @authorization
    def get(self, request):
        meetings = Meeting.objects.filter(respondent=request.user, time__gte = datetime.now().date(), is_accept=False)

        result = {
            'count' : meetings.count(),
            'requester' : [{
                'id'            : meeting.requester.id,
                'name'          : meeting.requester.name,
                'profile_image' : meeting.requester.profile_image_url
            } for meeting in meetings]
        }

        return JsonResponse({'message':result}, status=200)

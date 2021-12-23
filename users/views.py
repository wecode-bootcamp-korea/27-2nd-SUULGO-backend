import jwt, json, requests

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

            return JsonResponse({"message": "SUCCESS", "token": token, "result": user_info, "survey": Survey.objects.filter(user_id=user.id).exists()}, status=200)

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

class MatchingListView(View):
    # def get_total(self, a, b, c):
    #     d = self.do_something_with_a(a)
    #     e = self.do_something_with_b(b)
    #     f = self.do_something_with_c(c)
        
    #     return d + e + f

    # def do_something_with_a(self, a):
    #     pass

    # def do_something_with_b(self, b):
    #     pass

    # def do_something_with_c(self, c):
    #     pass

    # def calc_matching_point(self, user_preferences, opponent_preferences, weight):
    #     sum = 0

    #     for user_pref in user_preferences:
    #         sum += int(user_pref in opponent_preferences) * weight
            
    #     return sum
    
    @authorization
    def get(self, request):
        try:
            # 술 주량 일치여부 : 19% 
            # 술 도수 일치여부 : 19% 
            # 술 마시는 방법 일치여부 : 20% (중복)(개당 추가 점수) 
            # 선호하는 술 종류 일치여부 : 22% (중복)(개당 추가 점수)
            # 선호하는 술 맛 일치여부 : 20% (중복)(개당 추가 점수)
            # (현재 설문조사 받는 중)
            # <코드 구현 사항>
            # 상대방 아이디로 서베이 인스턴스 구하기 
            # 본인 서베이 인스턴스 구하기 
            # 각자 주량을 구해 일치여부 확인 
            # 각자 도수를 구해 일치여부 확인
            # 술 마시는 방법 일치 개수 확인 개당
            # 선호하는 술 종류 일치 개수 확인 개당
            # 선호하는 술 맛 일치 개수 확인 개당

            # 만약 가중치를 유저별로 테이블에 저장하면 개인별 맞춤 매칭도 가능하다.
			# 지금은 전체 평균에 대한 가중치
            drinking_method_weight  = 20
            flavor_weight           = 20
            alcohol_category_weight = 22
            alcohol_limit_weight    = 19
            alcohol_level_weight    = 19

            # 상대유저와 유저를 구하고, 유저의 중복선택 항목들을 리스트로 가져옴
            opponents               = Survey.objects.exclude(user = request.user) 
            user                    = Survey.objects.get(user = request.user)
            user_drinking_methods   = user.drinking_methods.all()
            user_alcohol_categories = user.alcohol_categories.all()
            user_survey_flavors     = user.flavors.all()

            # 일치하면 1, 아니면 0 점 임, if는 쓰지 않겠다는 굳은 의지!
            # matching_point_dict = { True : 1, False : 0 }
            matching_list_dict  = {}

            # for를 돌리는 이유는 user는 한 명이지만 상대유저들은 여러개이기 때문
            for opponent in opponents:
                matching_point = 0
                
                # 일치여부 항목에 대한 가중치 계산
                # alcohol_limit_point = matching_point_dict.get(opponent.alcohol_limit == user.alcohol_limit) * alcohol_limit_weight
                alcohol_limit_point = int(opponent.alcohol_limit == user.alcohol_limit) * alcohol_limit_weight
                # alcohol_level_point = matching_point_dict.get(opponent.alcohol_level == user.alcohol_level) * alcohol_level_weight
                alcohol_level_point = int(opponent.alcohol_level == user.alcohol_level) * alcohol_level_weight
                
                opponent_drinking_methods   = opponent.drinking_methods.all()
                opponent_alcohol_categories = opponent.alcohol_categories.all()
                opponent_survey_flavors     = opponent.flavors.all()

                # for 문을 돌리는 이유는 유저가 가진 리스트와 상대 유저가 가진 리스트를 비교해야하기 때문임
                for user_drinking_method in user_drinking_methods:
                    matching_point += int(user_drinking_method in opponent_drinking_methods) * drinking_method_weight
                
                for user_alcohol_categorie in user_alcohol_categories:
                    matching_point += int(user_alcohol_categorie in opponent_alcohol_categories) * alcohol_category_weight

                for user_survey_flavor in user_survey_flavors:
                    matching_point += int(user_survey_flavor in opponent_survey_flavors) * flavor_weight

                #전체 항목에 대한 매칭 포인트를 합산함
                total_matching_point = alcohol_limit_point + alcohol_level_point + matching_point

                #매칭 포인트와 상대유저 아이디를 딕셔너리로 만듬
                matching_list_dict[opponent.id] = total_matching_point 

            #딕셔너리를 값인 매칭포인트 순으로 정렬함(튜플 형태로 만들어 줌)
            sorted_matching_list = sorted(matching_list_dict.items(), key=lambda x: x[1], reverse = True)
            
            result = [{
                'matching_point'    : sorted_opponent[1], # 튜플 내 두번째 값인 매칭 포인트를 보여줌
                'id'                : Survey.objects.get(id=sorted_opponent[0]).user.id,
                'name'              : Survey.objects.get(id=sorted_opponent[0]).user.name,
                'class_number'      : Survey.objects.get(id=sorted_opponent[0]).class_number,
                'profile_image_url' : Survey.objects.get(id=sorted_opponent[0]).user.profile_image_url
            } for sorted_opponent in sorted_matching_list[:9]] # 최대 9명만 보내줌 

            return JsonResponse({ "result" : result }, status=200)

        except Survey.DoesNotExist:
            return JsonResponse({ "message" : "DoesNotExist" }, status=400)

            
# Layered Architecture Pattern

# Controller
# Service
# Model (SQL)  DAO -> Data Access Object

# SoC (Separation of Concern)
# SRP (Single Responsibility Principle)

# Router -> ProductController -> ProductService -> ProductModel

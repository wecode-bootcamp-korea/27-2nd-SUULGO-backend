from django.http            import JsonResponse
from django.views           import View
from enum                   import Enum

from users.models           import *
# from core.utils             import authorization

class Stack(Enum):
    FRONT = 1
    BACK  = 2

class AlcoholLimit(Enum):
    ZERO  = 1
    HALF  = 2
    ONE   = 3
    N     = 4

class MatchingListView(View):
    # @authorization
    def get(self, request):
        try:
            # 술 주량 일치여부 : 18%
            # 술 도수 일치여부 : 17% 
            # 술 마시는 방법 일치여부 : 20% (중복)(개당 추가 점수) 
            # 선호하는 술 종류 일치여부 : 24% (중복)(개당 추가 점수)
            # 선호하는 술 맛 일치여부 : 21% (중복)(개당 추가 점수)
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
            flavor_weight           = 21
            alcohol_category_weight = 24
            alcohol_limit_weight    = 18
            alcohol_level_weight    = 17

            # 일치하면 1, 아니면 0 을 가짐, if는 쓰지 않겠다는 굳은 의지!
            matching_point_dict = { True : 1, False : 0 }
            
            users                   = User.objects.all()
            request.user            = 5 #로그인이 아직 구현되지 않아 임시로 5번 유저 아이디를 지정하였습니다.
            user                    = Survey.objects.get(user = request.user)
            user_drinking_methods   = user.drinkingmethod_set.all()
            user_alcohol_categories = user.alcoholcategory_set.all()
            user_survey_flavors     = user.surveyflavor_set.all()
            a ={}
						
						# for를 돌리는 이유는 user는 한 명이지만 users==product(상대유저들)은 여러개이기 때문..ㅜ
            for product_user in users:
                matching_point = 0
                product        = Survey.objects.get(user = product_user)
                
                # 일치여부와 항목에 따른 가중치 합산
                alcohol_limit_point         = matching_point_dict.get(product.alcohol_limit == user.alcohol_limit) * alcohol_limit_weight
                alcohol_level_point         = matching_point_dict.get(product.alcohol_level == user.alcohol_level) * alcohol_level_weight
                prodocut_drinking_methods   = product.drinkingmethod_set.all()
                prodocut_alcohol_categories = product.alcoholcategory_set.all()
                prodocut_survey_flavors     = product.surveyflavor_set.all()

                #반복되므로 함수로 바꿀 예정.. for를 세 번이나 중첩하는 것은 옳은 것일까..? 
                for user_drinking_method in user_drinking_methods:
                    for prdocut_drinking_method in prodocut_drinking_methods:
                        matching_point += matching_point_dict.get(user_drinking_method==prdocut_drinking_method) * drinking_method_weight
                
                for user_alcohol_categorie in user_alcohol_categories:
                    for prodocut_alcohol_categorie in prodocut_alcohol_categories:
                        matching_point += matching_point_dict.get(user_alcohol_categorie==prodocut_alcohol_categorie) * alcohol_category_weight

                for user_survey_flavor in user_survey_flavors:
                    for prodocut_survey_flavor in prodocut_survey_flavors:
                        matching_point += matching_point_dict.get(user_survey_flavor==prodocut_survey_flavor) * flavor_weight

                total_matching_point = matching_point + alcohol_limit_point + alcohol_level_point

                a[product.id] = total_matching_point 

            # 가입한 유저들을 모두 반복하여 아이디별 포인트가 높은 순으로 정렬 한다.
            # 딕셔너리를 값(매칭 포인트)을 기준으로 튜플 형태로 정렬해줌. ex -> (id 1, 200),(id 2, 199),(id 3, 198)
            b = sorted(a.items(), key=lambda x: x[1], reverse=True)
            
            result = [{
                'matching_point'    : i[1], # 튜플 내 두번째 값인 매칭 포인트를 보여줌
                'id'                : Survey.objects.get(id=i[0]).user.id,
                'name'              : Survey.objects.get(id=i[0]).user.name,
                'class_number'      : Survey.objects.get(id=i[0]).class_number,
                'profile_image_url' : Survey.objects.get(id=i[0]).user.profile_image_url
            } for i in b[1:]] # 0번 인덱스를 뺀 이유는 본인 데이터이기 때문임(100%일치하므로 0번째로 매칭됨) 
															# 문제점. 본인과 똑같은 천생연분 유저가 있다면 자칫 상대가 0번째가 되어 짤릴 수가 있음
															# 슬라이싱이 아닌 본인 아이디가 리스트에 포함되지 않도록 제외해야함.

            return JsonResponse({ "result" : result }, status=200)

        except Survey.DoesNotExist:
            return JsonResponse({ "message" : "DoesNotExist" }, status=400)
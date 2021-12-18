from django.http            import JsonResponse
from django.views           import View
from enum                   import Enum

from users.models           import *
from core.utils             import authorization

class Stack(Enum):
    FRONT = 1
    BACK  = 2

class AlcoholLimit(Enum):
    ZERO  = 1
    HALF  = 2
    ONE   = 3
    N     = 4

class ProductView(View):
    # @authorization
    def get(self, request, product_id):
        try:
            # 술 주량 일치여부 : 18%
            # 술 도수 일치여부 : 17% 
            # 술 마시는 방법 일치여부 : 20% (중복)(개당 추가 점수) 
            # 선호하는 술 종류 일치여부 : 24% (중복)(개당 추가 점수)
            # 선호하는 술 맛 일치여부 : 21% (중복)(개당 추가 점수)
            
            #상대방 아이디로 서베이 인스턴스 구하기
            #본인 서베이 인스턴스 구하기
            #각자 주량을 구해 일치여부 확인
            #각자 도수를 구해 일치여부 확인
            
            request.user            = 5 #로그인이 아직 구현되지 않아 임시로 5번 유저 아이디를 지정하였습니다.
            product                 = Survey.objects.get(user=product_id)
            user                    = Survey.objects.get(user=request.user)
            print(product,user)
            result = [
                product.alcohol_limit,
                product.alcohol_level,
                user.alcohol_limit,
                user.alcohol_level
            ]
            return JsonResponse({ "message" : result }, status=200)

        except Survey.DoesNotExist:
            return JsonResponse({ "message" : "DoesNotExist" }, status=400)


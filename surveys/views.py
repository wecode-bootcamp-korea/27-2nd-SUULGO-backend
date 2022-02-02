import json

from django.http  import JsonResponse
from django.db    import transaction
from django.views import View

from users.models import *
from core.utils   import authorization


class SurveyView(View):
    @authorization
    def post(self, request):
        try:
            data             = json.loads(request.body)
            user             = request.user
            stack            = Stack.objects.get(name=data['stack'])
            alcohol_limit    = AlcoholLimit.objects.get(name=data['alcohol_limit'])
            gender           = Gender.objects.get(name=data['gender'])
            mbti             = Mbti.objects.get(name=data['mbti'])
            favorite_place   = data['favorite_place']
            favorite_food    = data['favorite_food']
            hobby            = data['hobby']
            comment          = data['comment']
            class_number     = data['class_number'],
            alcohol_level    = data['alcohol_level'],

            if Survey.objects.filter(user=user).exists():
                return JsonResponse({ 'message' : 'ALREDY_EXISTS' }, status = 400)

            with transaction.atomic():
                survey = Survey.objects.create(
                    user           = user,
                    gender         = gender,
                    mbti           = mbti,
                    stack          = stack,
                    alcohol_limit  = alcohol_limit,
                    class_number   = class_number,
                    alcohol_level  = alcohol_level,
                    comment        = comment,
                    favorite_place = favorite_place,
                    favorite_food  = favorite_food,
                    hobby          = hobby,
                )
                
                for flavor in data['flavor']:
                    SurveyFlavor.objects.create(
                        flavor = Flavor.objects.get(name=flavor),
                        survey = survey
                    ) 

                for alcohol_category in data['alcohol_category']:
                    SurveyAlcoholCategory.objects.create(
                        alcohol_category = AlcoholCategory.objects.get(name=alcohol_category),
                        survey           = survey
                    )

                for drinking_method in data['drinking_method']:
                    SurveyDrinkingMethod.objects.create(
                        drinking_method = DrinkingMethod.objects.get(name=drinking_method),
                        survey          = survey
                    )

                return JsonResponse({"message" : "SUCCESS" }, status = 201)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
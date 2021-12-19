import json

from django.views           import View
from django.http            import JsonResponse

from users.models           import User
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

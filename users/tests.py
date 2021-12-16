from django.test    import TestCase, Client
from unittest       import mock
from unittest.mock  import patch
from django.http    import response

from users.models   import *

class UserListViewTest(TestCase):
    def setUp(self):
        self.client=Client()

        User.objects.create(
        id                = 1,
        kakao_id          = "test",
        name              = 'test',
        profile_image_url = "https://www.notion.so/wecode/",
        email             = "abcd@abcd.abc"
    )
        AlcoholCategory.objects.create(      
        id   = 1,
        name = "test"     
    )
        Gender.objects.create(
        id   = 1,
        name = "test"
    )
        Mbti.objects.create(
        id          = 1,
        information = "test",
        name        = "test"
    )
        Survey.objects.create(
        id             = 1,
        gender_id      = 1,
        mbti_id        = 1,
        class_number   = 1,
        stack          = 1,
        alcohol_limit  = 1,
        alcohol_level  = "test",
        comment        = "test",
        favorite_place = "test",
        favorite_food  = "test",
        hobby          = "test",
        user_id        = 1
    )
        SurveyAlcoholCategory.objects.create(
        id                  = 1,
        alcohol_category_id = 1,
        survey_id           = 1 
    )
        DrinkingMethod.objects.create(
        id   = 1,
        name = "test"  
    )
        SurveyDrinkingMethod.objects.create(
        id                 = 1,
        drinking_method_id = 1,
        survey_id          = 1
    )
        Flavor.objects.create(
        id   = 1,
        name = "test"
    )
        SurveyFlavor.objects.create(
        id        = 1,
        flavor_id = 1,
        survey_id = 1
    )

    def tearDown(self):
        DrinkingMethod.objects.all().delete(), 
        Flavor.objects.all().delete(), 
        Mbti.objects.all().delete(), 
        SurveyAlcoholCategory.objects.all().delete(), 
        Survey.objects.all().delete(), 
        SurveyDrinkingMethod.objects.all().delete(), 
        SurveyFlavor.objects.all().delete(), 
        User.objects.all().delete(), 
        AlcoholCategory.objects.all().delete(), 
        Gender.objects.all().delete()

    def test_userlistview_get_success(self):
        response = self.client.get('/users?alcohol_category_id=1&offset=0&limit=1')
        self.assertEqual(response.json(),
        {
            "result": [
                {
                    "id": 1,
                    "name": "test",
                    "class_number": 1,
                    "profile_image_url": "https://www.notion.so/wecode/"
                }
            ]
        })
        self.assertEqual(response.status_code, 200)        

# class ProductViewTest(TestCase):
#     def test_productview_get_success(self):
#         response = self.client.get('/users/1')
#         self.assertEqual(response.json(),
#         {
#             "result": {
#                 "id": 1,
#                 "profile_image_url": "https://www.notion.so/wecode/",
#                 "text_name": "test",
#                 "text_email": "abcd@abcd.abc",
#                 "text_gender": "test",
#                 "text_mbti_title": "test",
#                 "text_mbti_description": "test",
#                 "text_class_number": 1,
#                 "text_comment": "test",
#                 "text_favorite_place": "test",
#                 "text_favorite_food": "test",
#                 "text_favorite_hobby": "test",
#                 "text_stack": "프론트",
#                 "alcohol_limit": {
#                 "name": "알쓰",
#                 "is_matching": True
#                 },
#                 "alcohol_level": {
#                 "name": "test",
#                 "is_matching": True
#                 },
#                 "alcohol_drinking_methods": [
#                 {
#                     "name": "test",
#                     "is_matching": True
#                 }
#                 ],
#                 "alcohol_categories": [
#                 {
#                     "name": "test",
#                     "is_matching": True
#                 }
#                 ],
#                 "alcohol_flavors": [
#                     {
#                     "name": "test",
#                     "is_matching": True
#                 }
#             ]
#         }
#     })
#         self.assertEqual(response.status_code, 200)

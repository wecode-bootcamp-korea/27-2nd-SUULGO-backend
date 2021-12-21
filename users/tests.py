
from django.test  import TestCase, Client
from users.models import *
import jwt
from suulgo.settings import SECRET_KEY, ALGORITHM

class UserViewTest(TestCase):
    def setUp(self):
        self.client=Client()
        self.token = jwt.encode({'id':1}, SECRET_KEY, ALGORITHM)

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
        Stack.objects.create(
        id   = 1,
        name = "test",
        number = 1
    )
        AlcoholLimit.objects.create(
        id   = 1,
        name = 'test',
        number = 1
    )

        Survey.objects.create(
        id             = 1,
        gender_id      = 1,
        mbti_id        = 1,
        class_number   = 1,
        stack_id       = 1,
        alcohol_limit_id = 1,
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

    def test_productview_get_success(self):
        headers = {"Authorization" : self.token}
        response = self.client.get('/users/1', **headers)
        self.assertEqual(response.json(),
        {
            "result": {
                "id": 1,
                "profile_image_url": "https://www.notion.so/wecode/",
                "text_name": "test",
                "text_email": "abcd@abcd.abc",
                "text_gender": "test",
                "text_mbti_title": "test",
                "text_mbti_description": "test",
                "text_class_number": 1,
                "text_comment": "test",
                "text_favorite_place": "test",
                "text_favorite_food": "test",
                "text_favorite_hobby": "test",
                "text_stack": "test",
                "alcohol_limit": {
                "name": "test",
                "is_matching": True
                },
                "alcohol_level": {
                "name": "test",
                "is_matching": True
                },
                "alcohol_drinking_methods": [
                {
                    "name": "test",
                    "is_matching": True
                }
                ],
                "alcohol_categories": [
                {
                    "name": "test",
                    "is_matching": True
                }
                ],
                "alcohol_flavors": [
                    {
                    "name": "test",
                    "is_matching": True
                }
            ]
        }
    })
        self.assertEqual(response.status_code, 200)
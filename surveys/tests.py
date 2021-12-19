import jwt, json

from django.test    import TestCase, Client
from unittest       import mock
from unittest.mock  import patch
from suulgo.settings import ALGORITHM, SECRET_KEY

from users.models   import *

class SurveyViewTest(TestCase):
    def setUp(self):
        self.client=Client()
        self.token = jwt.encode({'id':2},SECRET_KEY,ALGORITHM)

        User.objects.create(
        id                = 1,
        kakao_id          = "test",
        name              = 'test',
        profile_image_url = "https://www.notion.so/wecode/",
        email             = "abcd@abcd.abc"
    )
        User.objects.create(
        id                = 2,
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
        id     = 1,
        name   = "test",
        number = 1
    )
        AlcoholLimit.objects.create(
        id     = 1,
        name   = "test",
        number = 1
    )

        Survey.objects.create(
        id                = 1,
        gender_id         = 1,
        mbti_id           = 1,
        class_number      = 1,
        stack_id          = 1,
        alcohol_limit_id  = 1,
        alcohol_level     = "test",
        comment           = "test",
        favorite_place    = "test",
        favorite_food     = "test",
        hobby             = "test",
        user_id           = 1
    )

        AlcoholCategory.objects.create(
        id   = 3,
        name = "test2"  
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
        Mbti.objects.all().delete(),
        Gender.objects.all().delete(),
        Stack.objects.all().delete(),
        AlcoholLimit.objects.all().delete(),
        SurveyDrinkingMethod.objects.all().delete(), 
        DrinkingMethod.objects.all().delete(), 
        SurveyFlavor.objects.all().delete(),
        Flavor.objects.all().delete(), 
        SurveyAlcoholCategory.objects.all().delete(),
        AlcoholCategory.objects.all().delete(), 
        Survey.objects.all().delete(),  
        User.objects.all().delete(), 

        

    def test_surveyview_get_success(self):
        self.client=Client()

        survey = {
            "class_number":1,
            "gender": "test",
            "stack": "test",
            "mbti": "test",
            "alcohol_category": ["test2"],
            "alcohol_limit" : "test",
            "alcohol_level": "test",
            "flavor":["test"],
            "drinking_method": ["test"],
            "hobby": "test",
            "favorite_place": "test",
            "favorite_food": "test",
            "comment" : "test"
        }
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.post('/surveys', json.dumps(survey), content_type='application/json', **headers)
        self.assertEqual(response.json(),
        {
            'message': 'SUCCESS'
        })
        self.assertEqual(response.status_code, 201)        

from django.test import TestCase, Client

from users.models import DrinkingMethod, Flavor, Mbti, SurveyAlcoholCategory, Survey, SurveyDrinkingMethod, SurveyFlavor, User, AlcoholCategory, Gender

class ProductViewTest(TestCase):
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
        gender         = Gender.objects.get(id=1),
        mbti           = Mbti.objects.get(id=1),
        class_number   = 1,
        stack          = 1,
        alcohol_limit  = 1,
        alcohol_level  = "test",
        comment        = "test",
        favorite_place = "test",
        favorite_food  = "test",
        hobby          = "test",
        user           = User.objects.get(id=1)
    )
        SurveyAlcoholCategory.objects.create(
        id               = 1,
        alcohol_category = AlcoholCategory.objects.get(id=1),
        survey           = Survey.objects.get(id=1) 
    )
        DrinkingMethod.objects.create(
        id   = 1,
        name = "test"  
    )
        SurveyDrinkingMethod.objects.create(
        id              = 1,
        drinking_method = DrinkingMethod.objects.get(id=1),
        survey          = Survey.objects.get(id=1) 
    )
        Flavor.objects.create(
        id   = 1,
        name = "test"
    )
        SurveyFlavor.objects.create(
        id     = 1,
        flavor = Flavor.objects.get(id=1),
        survey = Survey.objects.get(id=1)
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
        response = self.client.get('/users/detail/1')
        self.assertEqual(response.json(),
        {
            "result": {
                "id": 1,
                "name": "test",
                "profile_image_url": "https://www.notion.so/wecode/",
                "email": "abcd@abcd.abc",
                "gender": "test",
                "mbti_title": "test",
                "mbti_description": "test",
                "stack": "프론트",
                "alcohol_limit": {
                    "알쓰": True
                },
                "alcohol_level": {
                    "test": True
                },
                "favorite_place": "test",
                "favorite_food": "test",
                "hobby": "test",
                "class_number": 1,
                "comment": "test",
                "drinking_methods": [
                    {
                        "test": True
                    }
                ],
                "alcohol_categories": [
                    {
                        "test": True
                    }
                ],
                "flavors": [
                    {
                        "test": True
                    },
                ]
            }
        })
        self.assertEqual(response.status_code, 200)
from django.test    import TestCase, Client
from unittest       import mock
from unittest.mock  import patch
from django.http    import response

from users.models   import DrinkingMethod, Flavor, Mbti, SurveyAlcoholCategory, Survey, SurveyDrinkingMethod, SurveyFlavor, User, AlcoholCategory, Gender

class LoginInfoTest(TestCase):
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

    def test_logininfoview_get_success(self):
        response = self.client.get('/users/logininfo')
        self.assertEqual(response.json(),
        {
            "RESULT": [
                {
                    "name"              : "test",
                    "profile_image_url" : "https://www.notion.so/wecode/",
                    "email"             : "abcd@abcd.abc",
                    "survey_info"       : [
                        {
                            "class_number"     : 1,
                            "stack"            : 1,
                            "alcohol_limit"    : 1,
                            "alcohol_level"    : "test",
                            "comment"          : "test",
                            "favorite_place"   : "test",
                            "favorite_food"    : "test",
                            "hobby"            : "test",
                            "gender"           : "test",
                            "mbti_name"        : "test",
                            "mbti_information" : "test"
                        }
                    ]
                }
            ],
            "MESSAGE": "SUCCESS"
        })

class KakaoLoginTest(TestCase):
    @patch("users.views.requests")
    def test_kakao_login_success(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id": 2034200447,
                    "connected_at": "2021-12-15T02:07:02Z",
                    "properties": {
                        "nickname": "길동화"
                    },
                    "kakao_account": {
                    "profile_nickname_needs_agreement": False,
                    "profile_image_needs_agreement": False,
                    "profile": {
                        "nickname": "길동화",
                        "thumbnail_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_110x110.jpg",
                        "profile_image_url": "http://k.kakaocdn.net/dn/dpk9l1/btqmGhA2lKL/Oz0wDuJn1YV2DIn92f6DVK/img_640x640.jpg",
                        "is_default_image": True
                    },
                    "has_email": True,
                    "email_needs_agreement": False,
                    "is_email_valid": True,
                    "is_email_verified": True,
                    "email": "donghwa2428@naver.com",
                    "has_gender": True,
                    "gender_needs_agreement": False,
                    "gender": "male"
                    }
                }

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "access_token"}
        response            = client.get("/users/kakaologin", **headers)
        
        self.assertEqual(response.status_code, 200)
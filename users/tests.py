from django.test    import TestCase, Client
from unittest       import mock
from unittest.mock  import patch

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

class ProductViewTest(TestCase):
    def test_productview_get_success(self):
        response = self.client.get('/users/1')
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
                "text_stack": "프론트",
                "alcohol_limit": {
                "name": "알쓰",
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

class PromiseViewTest(TestCase):
    def setUp(self):
        self.client=Client()

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
        email             = "abcde@abcd.abc"
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
        Meeting.objects.create(
        id         = 1,
        requester  = User.objects.get(id=1),
        respondent = User.objects.get(id=2),
        time       = "2021-12-25"
        ),

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
        Meeting.objects.all().delete()

    def test_promiseview_post_success(self):
        promise = {
            "respondent_id" : 2,
            "time" : "2021-12-23"
        }
        response = self.client.post('/users/promise',json.dumps(promise), content_type='application/json')
        self.assertEqual(response.json(),
        {
            "message": "SUCCESS"
        })
        self.assertEqual(response.status_code, 200)

    def test_promiseview_post_date_error(self):
        promise = {
            "respondent_id" : 2,
            "time" : "2021-12-05"
        }
        response = self.client.post('/users/promise',json.dumps(promise), content_type='application/json')
        self.assertEqual(response.json(),
        {
            "message": "DATE_ERROR"
        })
        self.assertEqual(response.status_code, 400)

    def test_promiseview_post_already_exists_error(self):
        promise = {
            "respondent_id" : 2,
            "time" : "2021-12-25"
        }
        response = self.client.post('/users/promise',json.dumps(promise), content_type='application/json')
        self.assertEqual(response.json(),
        {
            "message": "ALREADY_EXISTS"
        })
        self.assertEqual(response.status_code, 400)

    def test_promiseview_post_already_exists_error(self):
        promise = {
            "respondent_id" : 2000,
            "time" : "2021-12-21"
        }
        response = self.client.post('/users/promise',json.dumps(promise), content_type='application/json')
        self.assertEqual(response.json(),
        {
            "message": "DoesNotExist"
        })
        self.assertEqual(response.status_code, 400)

class PromiseAlarmViewTest(TestCase):
    def setUp(self):
        self.client=Client()

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
        email             = "abcde@abcd.abc"
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
        Meeting.objects.create(
        id         = 1,
        requester  = User.objects.get(id=1),
        respondent = User.objects.get(id=2),
        time       = "2021-12-25"
        ),

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
        Meeting.objects.all().delete()

    def test_promisealarmview_get_success(self):
        response = self.client.get('/users/promise-alarm')
        self.assertEqual(response.json(),
        {
            "message": {
                "count": 1,
                "requester": [
                    {
                        "id": 1,
                        "name": "test",
                        "profile_image": "https://www.notion.so/wecode/"
                    }
                ]
            }
        })
        self.assertEqual(response.status_code, 200)

        mocked_requests.get = mock.MagicMock(return_value = MockedResponse())
        headers             = {"HTTP_Authorization": "access_token"}
        response            = client.get("/users/login", **headers)

        self.assertEqual(response.status_code, 200)

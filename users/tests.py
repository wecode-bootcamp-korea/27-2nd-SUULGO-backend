from django.test    import TestCase, Client
from unittest       import mock
from unittest.mock  import patch
from django.http    import response

from users.models   import DrinkingMethod, Flavor, Mbti, SurveyAlcoholCategory, Survey, SurveyDrinkingMethod, SurveyFlavor, User, AlcoholCategory, Gender

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

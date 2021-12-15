from django.urls import path

from users.views import KakaoLoginView

urlpatterns = [
    path('/kakaologin', KakaoLoginView.as_view()),
]

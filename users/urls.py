from django.urls import path

from users.views import KakaoLoginView, ProfileView

urlpatterns = [
    path('/kakaologin', KakaoLoginView.as_view()),
    path('/profile', ProfileView.as_view())
]
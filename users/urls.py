from django.urls import path
from users.views import *

urlpatterns = [
    path('/kakaologin', KakaoLoginView.as_view()),
    path('/profile', ProfileView.as_view()),
    path('/<int:user_id>', UserView.as_view()),
    path('', UserListView.as_view()),
    path('/promise', PromiseView.as_view()),
    path('/promise-alarm', PromiseAlarmView.as_view())
]

# 'https://api.wecode.co.kr/users/profile'
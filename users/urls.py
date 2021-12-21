from django.urls import path

from users.views import *

urlpatterns = [
    path('/login', KakaoLoginView.as_view()),
    path('/profile', ProfileView.as_view()),
    path('/<int:user_id>', UserView.as_view()),
    path('', UserListView.as_view()),
    path('/appointment', AppointmentView.as_view()),
    path('/appointment-alarm', AppointmentAlarmView.as_view())
]

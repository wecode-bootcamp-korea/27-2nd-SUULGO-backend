from django.urls import path

from users.views import KakaoLoginView, ProfileView, UserListView, ProductView

urlpatterns = [
    path('/kakaologin', KakaoLoginView.as_view()),
    path('/profile', ProfileView.as_view()),
    path('/<int:product_id>', ProductView.as_view()),
    path('', UserListView.as_view()),
]
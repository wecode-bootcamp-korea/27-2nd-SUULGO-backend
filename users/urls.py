from django.urls import path, include

from users.views import ProfileView

urlpatterns = [
    path('/profile', ProfileView.as_view())
]

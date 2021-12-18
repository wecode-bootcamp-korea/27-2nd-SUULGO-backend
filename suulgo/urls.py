from django.urls    import path

urlpatterns = [
    path('users', include('users.urls'))
]
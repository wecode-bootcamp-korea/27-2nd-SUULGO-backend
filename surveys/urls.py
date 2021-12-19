from django.urls import path
from surveys.views import SurveyView

urlpatterns = [
    path('', SurveyView.as_view()),
]
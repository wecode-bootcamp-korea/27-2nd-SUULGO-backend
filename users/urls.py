from django.urls    import path
from users.views   import MatchingListView

urlpatterns = [
	path('/matching', MatchingListView.as_view()),
]
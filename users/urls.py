from django.urls    import path
from users.views   import ProductView

urlpatterns = [
	path('/detail/<int:product_id>', ProductView.as_view()),
]
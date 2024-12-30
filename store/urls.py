from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
# for detailed products we need like this "127.0.0.1:8000/store/category_slug/product_slug/"
#submit_review/<int:product_id> we also take product_id along with review as each review is for a particular product
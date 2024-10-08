from django.urls import path
from . import views  # Import views from the current directory

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
]
# for detailed products we need like this "127.0.0.1:8000/store/category_slug/product_slug/"
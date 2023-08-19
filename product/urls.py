from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_product),
    path('<int:product_id>/', views.product_detail_view),
    path('product/', views.create_category),
]
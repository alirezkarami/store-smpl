from django.urls import path
from . import views


urlpatterns = [
    path('', views.all_product),
    path('<int:product_id>/', views.product_detail_view),
    path('all_product/', views.create_category),
    path('create_category/', views.create_category)
]
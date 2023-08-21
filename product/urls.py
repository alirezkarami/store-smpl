from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.all_product),
    path('<int:product_id>/', views.product_detail_view),
    path('category/', views.create_category),
    # re_path('^products/(?P<name>.+)/$', ProductList.as_view()),

]
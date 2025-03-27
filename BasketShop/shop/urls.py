from . import views
from django.urls import path

app_name='shop'

urlpatterns = [
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('brand/<slug:brand_slug>/category/<slug:category_slug>', views.product_list, name='product_list_by_category_and_brand'),
    path('brand/<slug:brand_slug>/', views.product_list, name='product_list_by_brands'),
    path('category/<slug:category_slug>', views.product_list, name='product_list_by_categories'),
    path('', views.product_list, name='product_list'),
]
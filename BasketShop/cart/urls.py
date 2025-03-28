from django.urls import path
from . import views

urlpatterns = [
    path('get_cart/', views.get_cart, name='get_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
]
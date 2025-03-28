from django.urls import path
from . import views
app_name = 'payment'

urlpatterns = [
    path('pay/', views.create_payment, name='pay'),
    path('success/', views.payment_success, name='payment_success'),
]
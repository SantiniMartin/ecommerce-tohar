from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/', views.payment_success_view, name='success'),
]

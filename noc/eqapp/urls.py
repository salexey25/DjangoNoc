from django.urls import path
from . import views

urlpatterns = [
    path('device/', views.create_device, name='create_device'),
    path('rack/', views.create_rack, name='create_rack'),
]
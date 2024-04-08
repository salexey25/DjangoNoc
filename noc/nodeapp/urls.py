from django.urls import path
from .views import create_node,create_equipment

urlpatterns = [
    path('node/', create_node, name='create_node'),
    path('equipment/', create_equipment, name='create_equipment'),
]
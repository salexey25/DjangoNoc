from django.urls import path
from . import views

urlpatterns = [
    #Маршрут при создании узла связи
    path('node/', views.create_node, name='create_node'),
    #path('device/', views.create_device, name='create_device'),
    #Маршрут, после создания узла связи, т.е. редирект на страницу узла связи
    path('node_<int:nd_id>/', views.node_view, name='node_detail'),
    path('node_<int:nd_id>/rack/', views.rack, name='rack'),
    path('list/', views.node_list, name='node_list'),
]
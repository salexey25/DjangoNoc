from django.urls import path
from .views import create_network, network_list, divide_network, nets_v4_view
from . import views

urlpatterns = [
    path('create/', create_network, name='create_network'),
    path('list/', network_list, name='network_list'),
    path('divide/', divide_network, name='divide_network'),
#    url(r'^net_v4_(?P<netv4_id>\d+)/$', 'nets_v4_view'),
#     path('net_v4_<int:net_id>/', views.nets_ipv4_view, name='nets_ipv4_detail'),
    path('net_ipv4_<int:net_id>/', views.ipv4_view, name='ipv4_detail'),
    path('net_v4_<int:net_id>/', views.nets_v4_view, name='nets_v4_detail'),
    path('net_v4_<int:net_id>/split/', views.split_network, name='split_network'),
    path('net_v4_<int:net_id>/delete/', views.delete_network, name='delete_network'),
    #удаление сети
    path('deleted_network_list/', views.deleted_network_list, name='deleted_network_list'),
    #создание subnet
    path('split_network/<int:net_id>/subnet/', views.subnet, name='subnet'),
    #Редактирование поля description у ip address
    #path('net_ipv4_<int:net_id>/', views.edit_ip_description, name='edit_ip_description'),
    #path('net_ipv4_<int:ip_parent_id>/', views.EditIPDescriptionView.as_view(), name='edit_ip_description'),
#    path('nets_v4/<int:net_v4_id>', nets_v4_view, name='nets_v4_detail'),
    # Добавьте другие маршруты по необходимости
]
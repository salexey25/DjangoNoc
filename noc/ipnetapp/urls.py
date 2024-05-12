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
    #path('nets_v4/<int:net_v4_id>', nets_v4_view, name='nets_v4_detail'),
    #этот маршрут нерабочий, его надо почистить совместно с javasacript в файле net_ipv4_view
    path('save_ip_description/', views.save_ip_description, name='save_ip_description'),
    #маршрут для редиректа на страницу изменения поля ip_description
    path('net_ipv4_<int:net_id>/edit/', views.ipv4_edit, name='ipv4_edit'),
    #path('net_ipv4_<int:net_id>/edit/save_description/', views.save_description, name='save_description'),
    #path('save_description/<int:net_id>/', views.save_description, name='save_description'),
    #path('net_ipv4_<int:net_id>/save/', views.save_description, name='save_description'),
    #маршрут, который запускается при нажатии кнопки save в net_ipv4_edit.html. Но в самой функции все редиректится на
    # страницу сети и этого маршрута net_ipv4_<int:net_id>/save/ нигде не видно
    path('net_ipv4_<int:net_id>/save/', views.ipv4_save, name='ipv4_save'),
    path('net_ipv4_<int:net_id>/delete/', views.delete_ip, name='delete_ip'),
]
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "accountapp"

urlpatterns = [
    # post views
#    path('login/', views.user_login, name='login'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

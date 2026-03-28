from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views

app_name = 'user'


urlpatterns = [
    path('',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('search/',views.user_search,name='search'),
    path('user/<int:user_id>/',views.view_user,name='view_user'),
    path('profile/edit/',views.edit_profile,name='edit_profile'),
]

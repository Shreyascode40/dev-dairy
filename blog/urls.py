from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog_create', views.blog_create, name='blog_create'),
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog_delete/<int:blog_id>/', views.blog_delete, name='blog_delete'),
    path('blog_update/<int:blog_id>/', views.blog_update, name='blog_update'),
    path('<int:blog_id>/like/', views.toggle_like, name='toggle_like'),
    path('<int:blog_id>/comment/', views.add_comment, name='add_comment'),
]
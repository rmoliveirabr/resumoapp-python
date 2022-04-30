from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView

from resumoapp.posts import views

app_name = 'posts'

urlpatterns = [
    path('cadastrar/', views.add_post, name = 'add'),
    re_path(r'^editar/(?P<slug>[\w_-]+)/$', views.edit_post, name = 'edit'),
    re_path(r'^apagar/(?P<slug>[\w_-]+)/$', views.delete_post, name = 'delete'),
    path('listar/', views.list_posts, name = 'list'),
    re_path(r'^(?P<slug>[\w_-]+)/$', views.show_post, name = 'details'),
    re_path(r'^tag/(?P<tag>[\w_-]+)/$', views.list_posts, name = 'list_tagged'),

    path('ajax/load-years/', views.load_years, name='ajax_load_years'),
    path('ajax/load-topics/', views.load_topics, name='ajax_load_topics'),

]

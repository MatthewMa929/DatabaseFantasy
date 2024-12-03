from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('register/', views.user_register, name='user_register'),
    path('query/', views.query, name='query'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('execute-query/', views.execute_query, name='execute_query'),
    path('logout/', views.logout_view, name='logout'),
    path('search/', views.search_view, name='search'),
    path('create/', views.create_view, name='create'),
    path('edit-record/', views.edit_record, name='edit_record'),
    path('delete-record/', views.delete_record, name='delete_record'),
    path('perform-search/', views.perform_search, name='perform_search'),
    path('manage/', views.manage_view, name='manage'),
    path('activity/', views.activity_view, name='activity'),
    path('teams/', views.teams_view, name='teams'),

]
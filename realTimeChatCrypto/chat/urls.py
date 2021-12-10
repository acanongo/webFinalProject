
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path("chat/", views.index, name = 'index'),

    #path('chat/<str:room_name>/', views.room, name='room'),#real time chat

    path('chat/<str:room_name>/<str:userName>/', views.room, name='room'),#real time chat



    path("login/", auth_views.LoginView.as_view(), name='login'),#login


    path("register/", views.register, name="register"),#register
    path("<int:sugg_id>/", views.commentView, name="comment"),#adding comments
    path("suggestion/", views.suggestion, name="suggestion"),#adding suggestions
    path("stats/", views.getStats, name = "stats"),


]
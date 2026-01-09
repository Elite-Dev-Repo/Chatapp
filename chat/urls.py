from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    path('room', views.room, name='room'), # This is your room list
    path('createroom', views.createRoom, name='createroom'),
    path('roomchat/<str:roomname>', views.roomchat, name='roomchat'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
]
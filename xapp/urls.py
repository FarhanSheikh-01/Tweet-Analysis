from django.urls import path
from xapp import views

urlpatterns = [
    path('', views.home, name="home"),         
    path("msg/", views.msg, name="msg"),     
    path("fetch_tweets/", views.fetch_tweets, name="fetch_tweets"),   
]


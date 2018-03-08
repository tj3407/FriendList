from django.conf.urls import url
from django.contrib import admin
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'main$', views.main),
    url(r'register$', views.register),
    url(r'login$', views.login),
    url(r'logout$', views.logout),
    url(r'friends$', views.friends),
    url(r'user/join/(?P<id>\d+)$', views.join),
    url(r'user/remove/(?P<id>\d+)$', views.remove),
    url(r'user/(?P<id>\d+)$', views.profile),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('user', views.user, name='user'),
    path('change/', views.change, name='change/'),
    path('reports/', views.report, name='report'),
    path('communication/', views.communication, name='com'),
    path('sendreport', views.sendreport, name='sendreport'),
]

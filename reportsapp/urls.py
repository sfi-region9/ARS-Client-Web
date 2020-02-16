from django.urls import path
from reportsapp import views
urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('user', views.user, name='user'),
    path('reports/', views.report, name='report'),
    path('reports/profile', views.profile, name='sendprofile'),
    path('reports/customization', views.customization, name='custom'),
    path('reports/sendtemplate', views.sendtemplate, name='cust'),
    path('reports/sendd', views.sendd, name='e'),
    path('ml', views.ml, name="ml"),
]

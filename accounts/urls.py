from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('signup/', views.SignUp, name='signup'),
    path(r'^login/$', auth_views.LoginView, name='login'),
]
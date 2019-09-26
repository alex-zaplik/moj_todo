from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path(r'signup/', views.SignUpView.as_view(), name='signup'),
    path(r'login/', views.CustomLoginView.as_view(), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(), name="logout"),
    #path(r'logout/', views.CustomLogoutView.as_view(), name="logout"),
]
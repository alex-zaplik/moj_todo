from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path(r'signup/', views.SignUp, name='signup'),
    path(r'login/', auth_views.LoginView.as_view(template_name='login.html', redirect_field_name='None'), name="login"),
    path(r'logout/', auth_views.LogoutView.as_view(), name="logout"),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.table, name='table'),
    path('<int:pk>/cl_add', views.add_column, name='column_save')
]
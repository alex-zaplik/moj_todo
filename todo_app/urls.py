from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.table, name='table'),
    path('add_column/<int:pk>/', views.add_column, name='column_save'),
    path('add_task/<int:pk>/', views.add_task, name='task_save'),
    path('edit_task/<int:pk>/', views.edit_task, name='task_edit'),
    path('move_task/', views.move_task, name='move_task'),
    path('denied/', views.access_denied, name='denied')
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.TableView.as_view(), name='table'),
    path('add_column/<int:pk>/', views.AddColumnView.as_view(), name='column_save'),
    path('add_task/<int:pk>/', views.AddTaskView.as_view(), name='task_save'),
    path('edit_task/<int:pk>/', views.EditTaskView.as_view(), name='task_edit'),
    path('move_task/<int:pk>/', views.MoveTaskView.as_view(), name='move_task'),
    path('denied/', views.access_denied, name='denied')
]
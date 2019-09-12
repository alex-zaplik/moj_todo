from django.shortcuts import render

from .models import Task

def index(request):
    """
    A simple view that display all tasks in database
    """
    
    task_list = Task.objects.order_by('-deadline')[:5]
    context = {'task_list': task_list}
    return render(request, 'todo_app/index.html', context)
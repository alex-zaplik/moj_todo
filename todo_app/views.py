from django.shortcuts import render

from .models import Table, Column, Task

def index(request):
    """
    A simple view that display all tables in the database
    """
    
    # TODO: Only get tables that belong to the user
    table_list = Table.objects.all()
    context = {'table_list': table_list}
    return render(request, 'todo_app/tables.html', context)


def table(request, pk):
    """
    A simple view that display all tasks in a table
    """

    # TODO: Only show tables that belong to the user
    # TODO: Ignoring columns now, but that has to change
    task_list = Task.objects.filter(column__table__pk=pk).order_by('-deadline')[:5]
    context = {'task_list': task_list}
    return render(request, 'todo_app/table.html', context)
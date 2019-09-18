from django.shortcuts import render
from django.views.generic import CreateView

from .models import Table, Column, Task
from .forms import ColumnForm

def index(request):
    """
    A simple view that display all tables in the database
    """
    
    # TODO: Only get tables that belong to the user
    table_list = Table.objects.all()
    task_list = Task.objects.all()
    context = {'table_list': table_list, 'task_list' : task_list}
    return render(request, 'todo_app/tables.html', context)


def table(request, pk):
    """
    A simple view that display all tasks in a table
    """

    # TODO: Only show tables that belong to the user

    if request.method == 'POST':
        if 'column_save' in request.POST:
            column = Column(table=Table.objects.get(pk=pk))
            column_form = ColumnForm(request.POST, instance=column)
            column_form.save()
    else:
        column_form = ColumnForm()

    column_list = Column.objects.filter(table__pk=pk)
    task_list = Task.objects.filter(column__table__pk=pk).order_by('-deadline')
    context = {'task_list': task_list, 'column_list': column_list, 'column_form': column_form}
    return render(request, 'todo_app/table.html', context)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.decorators.http import require_POST

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
    column_form = ColumnForm()
    column_list = Column.objects.filter(table__pk=pk)
    task_list = Task.objects.filter(column__table__pk=pk).order_by('-deadline')
    context = {'task_list': task_list, 'column_list': column_list, 'column_form': column_form, 'tab_id': pk}
    return render(request, 'todo_app/table.html', context)


@require_POST
def add_column(request, pk):
    """
    A temporary view that handles POST method
    Source: ColumnForm
    """

    if request.method == 'POST':
        column = Column(table=Table.objects.get(pk=pk))
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            form.save()

    return redirect(reverse('table', kwargs={'pk': pk}))
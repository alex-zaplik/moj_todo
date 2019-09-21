from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.decorators.http import require_POST

from .models import Table, Column, Task
from .forms import ColumnForm, TaskFrom


def index(request):
    """
    A simple view that display tables that belong to the user
    """

    table_list = [x for x in Table.objects.all() if request.user in x.users.all()]
    task_list = Task.objects.all()

    context = {'table_list': table_list, 'table_remind_list': table_list, 'task_remind_list' : task_list}
    return render(request, 'todo_app/tables.html', context)


def table(request, pk):
    """
    A simple view that display all tasks in a table that belong to the user
    """

    table_remind_list = [x for x in Table.objects.all() if request.user in x.users.all()]
    task_remind_list = Task.objects.all()

    if request.user in Table.objects.get(pk=pk).users.all():
        column_form = ColumnForm()
        task_form = TaskFrom()
        column_list = Column.objects.filter(table__pk=pk)
        task_list = Task.objects.filter(column__table__pk=pk).order_by('-deadline')
        context = {'user': request.user, 'table_remind_list': table_remind_list, 'task_remind_list' : task_remind_list, 'column_list': column_list, 'column_form': column_form, 'task_form': task_form, 'tab_id': pk}
    else:
        context = {'user': request.user, 'table_remind_list': table_remind_list, 'task_remind_list' : task_remind_list, 'column_list': [], 'column_form': None, 'task_form': None, 'tab_id': ""}
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


@require_POST
def add_task(request, pk):
    """
    A temporary view that handles POST method parameters
    Source: TaskForm
    """

    if request.method == 'POST':
        # TODO: Check if the key is present
        form = TaskFrom(request.POST, instance=Task(column_id=int(request.POST.get('column'))))
        if form.is_valid():
            form.save()

    return redirect(reverse('table', kwargs={'pk': pk}))


@require_POST
def edit_task(request, pk):
    """
    A temporary view that handles POST method parameters
    Source: TaskForm
    """

    if request.method == 'POST' and False: # TODO: For now this request is ignored
        # TODO: Check if the keys are present
        form = TaskFrom(request.POST, instance=Task(id=int(request.POST.get('task')), column_id=int(request.POST.get('column'))))
        if form.is_valid():
            form.save()

    return redirect(reverse('table', kwargs={'pk': pk}))
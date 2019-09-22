from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

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

    try:
        curr_table = Table.objects.get(pk=pk)
        if request.user in curr_table.users.all():
            column_form = ColumnForm()
            task_form = TaskFrom()
            column_list = Column.objects.filter(table__pk=pk)
            task_list = Task.objects.filter(column__table__pk=pk).order_by('-deadline')
            context = {'user': request.user, 'page_title': curr_table.name, 'table_remind_list': table_remind_list, 'task_remind_list' : task_remind_list, 'column_list': column_list, 'column_form': column_form, 'task_form': task_form, 'tab_id': pk}
        else:
            raise PermissionDenied()
    
        return render(request, 'todo_app/table.html', context)
    except:
        return redirect(reverse('denied'))


@require_POST
def add_column(request, pk):
    """
    A temporary view that handles POST method
    Source: ColumnForm
    """

    try:
        table = Table.objects.get(pk=pk)

        if request.user not in table.users.all():
            raise PermissionDenied()

        if request.method == 'POST':
            column = Column(table=table)
            form = ColumnForm(request.POST, instance=column)
            if form.is_valid():
                form.save()

        return redirect(reverse('table', kwargs={'pk': pk}))

    except (PermissionDenied, Table.DoesNotExist):
        return redirect(reverse('denied'))


@require_POST
def add_task(request, pk):
    """
    A temporary view that handles POST method parameters
    Source: TaskForm
    """

    try:
        table = Table.objects.get(pk=pk)

        if request.user not in table.users.all():
            raise PermissionDenied()

        if request.method == 'POST':
            # TODO: Check if the key is present
            column = Column.objects.get(pk=int(request.POST.get('column')))
            if column.table.pk != pk:
                print(column.table.pk, pk)
                raise django.core.exceptions.PermissionDenied()

            form = TaskFrom(request.POST, instance=Task(column_id=column.id))

            if form.is_valid():
                form.save()

        return redirect(reverse('table', kwargs={'pk': pk}))

    except (PermissionDenied, Table.DoesNotExist):
        return redirect(reverse('denied'))


@require_POST
def edit_task(request, pk):
    """
    A temporary view that handles POST method parameters
    Source: TaskForm
    """

    try:
        table = Table.objects.get(pk=pk)

        if request.user not in table.users.all():
            raise PermissionDenied()

        if request.method == 'POST' and False: # TODO: For now this request is ignored
            # TODO: Check if the keys are present
            form = TaskFrom(request.POST, instance=Task(id=int(request.POST.get('task')), column_id=int(request.POST.get('column'))))
            if form.is_valid():
                form.save()

        return redirect(reverse('table', kwargs={'pk': pk}))

    except (PermissionDenied, Table.DoesNotExist):
        return redirect(reverse('denied'))


@require_POST
def move_task(request):
    """
    A view that handles moving a tast to a different column
    of the same table
    """

    data = {}

    try:
        if request.method == 'POST':
            # TODO: Check if the keys are present and if no 404 arises
            task = Task.objects.get(pk=int(request.POST.get('task')))
            target = Column.objects.get(pk=int(request.POST.get('target')))

            # Checking if the origin and target columns are in the same table
            if task.column.table == target.table:
                if request.user not in target.table.users:
                    raise PermissionDenied()

                # Move task
                task.column = target
                task.save()

                data['success'] = True
                data['url'] = reverse('table', kwargs={ 'pk': target.table.pk })
            else:
                # Send error
                data['success'] = True
                data['msg'] = "The origin and target columns are not the same"
            
        return JsonResponse(data)    

    except (PermissionDenied, Table.DoesNotExist):
        return redirect(reverse('denied'))


def access_denied(request):
    table_list = [x for x in Table.objects.all() if request.user in x.users.all()]
    task_list = Task.objects.all()

    context = {'page_title': "Access denied", 'page_subtitle': request.GET.get('subtitle', ''), 'table_remind_list': table_list, 'task_remind_list' : task_list}

    return render(request, 'todo_app/access_denied.html', context)
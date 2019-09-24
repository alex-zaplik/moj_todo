from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied

from .models import Table, Column, Task
from .forms import ColumnForm, TaskFrom


class CheckedTableView(View):

    not_exist_msg = "Table does not exist"
    not_allowed_msg = "You are not allowed to access this table"

    def check_table(self, request, *args, **kwargs):
        assert 'pk' in kwargs

        try:
            curr_table = Table.objects.get(pk=kwargs['pk'])
            if request.user not in curr_table.users.all():
                raise PermissionDenied(self.not_allowed_msg)
        except Table.DoesNotExist:
            raise PermissionDenied(self.not_exist_msg)
    

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            self.check_table(request, *args, **kwargs)
            handler = getattr(self, "checked_" + request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class IndexView(TemplateResponseMixin, View):
    """
    A simple view that displays tables that belong to the user
    """

    template_name = 'todo_app/tables.html'

    def get(self, request):
        table_list = [x for x in Table.objects.all() if request.user in x.users.all()]
        task_list = Task.objects.all()

        context = {'table_list': table_list, 'table_remind_list': table_list, 'task_remind_list' : task_list}
        return self.render_to_response(context)


class TableView(TemplateResponseMixin, CheckedTableView):
    """
    A simple view that display all tasks in a table that belong to the user
    """

    template_name = 'todo_app/table.html'
    not_allowed_msg = "You are not allowed to view this table"

    def checked_get(self, request, pk):
        table_remind_list = [x for x in Table.objects.all() if request.user in x.users.all()]
        task_remind_list = Task.objects.all()

        curr_table = Table.objects.get(pk=pk)
        column_form = ColumnForm()
        task_form = TaskFrom()
        column_list = Column.objects.filter(table__pk=pk)
        task_list = Task.objects.filter(column__table__pk=pk).order_by('-deadline')
        context = {'user': request.user, 'page_title': curr_table.name, 'table_remind_list': table_remind_list, 'task_remind_list' : task_remind_list, 'column_list': column_list, 'column_form': column_form, 'task_form': task_form, 'tab_id': pk}
        
        return self.render_to_response(context)


class AddColumnView(CheckedTableView):
    """
    A temporary view that handles POST method
    Source: ColumnForm
    """

    not_allowed_msg = "You are not allowed to add to this table"

    def checked_post(self, request, pk):
        table = Table.objects.get(pk=pk)
        column = Column(table=table)
        form = ColumnForm(request.POST, instance=column)
        if form.is_valid():
            form.save()
        
        return redirect(reverse_lazy('table', kwargs={'pk': pk}))


class AddTaskView(CheckedTableView):
    """
    A temporary view that handles POST method
    Source: ColumnForm
    """

    not_allowed_msg = "You are not allowed to add to this table"

    def checked_post(self, request, pk):
        table = Table.objects.get(pk=pk)
        # TODO: Check if the key is present
        column = Column.objects.get(pk=int(request.POST.get('column')))
        if column.table.pk != pk:
            raise PermissionDenied("Table id dont's match (org:%d,target:%d)" % (column.table.pk, pk))
        
        form = TaskFrom(request.POST, instance=Task(column_id=column.id))

        if form.is_valid():
            form.save()

        return redirect(reverse_lazy('table', kwargs={'pk': pk}))


class MoveTaskView(CheckedTableView):
    """
    A temporary view that handles POST method
    Source: ColumnForm
    """

    not_allowed_msg = "You are not allowed to move tasks in this table"

    def checked_post(self, request, pk):
        data = {}

        # TODO: Check if the keys are present and if no 404 arises
        task = Task.objects.get(pk=int(request.POST.get('task')))
        target = Column.objects.get(pk=int(request.POST.get('target')))

        # Checking if the origin and target columns are in the same table
        if task.column.table == target.table and target.table.pk == pk:
            # Move task
            task.column = target
            task.save()

            data['success'] = True
            data['url'] = reverse_lazy('table', kwargs={ 'pk': target.table.pk })
        else:
            # Send error
            data['success'] = True
            data['msg'] = "The origin and target columns are not the same"
        
        return JsonResponse(data)


class EditTaskView(CheckedTableView):
    """
    A temporary view that handles POST method
    Source: ColumnForm
    """

    not_allowed_msg = "You are not allowed to edit tasks in this table"

    def checked_post(self, request, pk):
        table = Table.objects.get(pk=pk)
        # TODO: Check if the keys are present
        # TODO: Ignored for now, awaiting implementation
        # form = TaskFrom(request.POST, instance=Task(id=int(request.POST.get('task')), column_id=int(request.POST.get('column'))))
        # if form.is_valid():
        #     form.save()

        return redirect(reverse_lazy('table', kwargs={'pk': pk}))


def access_denied(request, exception):
    table_list = [x for x in Table.objects.all() if request.user in x.users.all()]
    task_list = Task.objects.all()

    context = {'page_title': "Access denied", 'page_subtitle': exception, 'table_remind_list': table_list, 'task_remind_list' : task_list}

    return render(request, 'todo_app/access_denied.html', context)
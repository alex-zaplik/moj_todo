from django.forms import ModelForm, DateTimeField
from .models import Task, Column

class ColumnForm(ModelForm):
	class Meta:
		model = Column
		exclude = ['table']


class TaskFrom(ModelForm):
	class Meta:
		model = Task
		exclude = ['column']

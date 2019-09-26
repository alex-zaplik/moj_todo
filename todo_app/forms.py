from django.forms import ModelForm, DateTimeField
from .models import Task, Column
from bootstrap_modal_forms.forms import BSModalForm

class ColumnForm(ModelForm):
	class Meta:
		model = Column
		exclude = ['table']

class TaskFrom(ModelForm):
	class Meta:
		model = Task
		exclude = ['column']

class TaskEditForm(BSModalForm):
    """
    Temporary form for testing BSModal libray. Probably can be merged with TaskFrom later. 
    """
    class Meta:
        model = Task
        exclude = ['column']


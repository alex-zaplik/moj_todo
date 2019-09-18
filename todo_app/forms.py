from django.forms import ModelForm
from .models import Column

class ColumnForm(ModelForm):
	class Meta:
		model = Column
		exclude = ['table']
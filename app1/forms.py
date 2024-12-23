from django.forms import ModelForm
from . models import *
class ExpenseForm(ModelForm):
    
    class Meta:
        model = expense
        fields = ("name","amount","category")

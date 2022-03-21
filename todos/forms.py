from django import forms
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta: # This is because we have to specify what class/model we are working with or what fields we have to specify.
        model = Todo
        fields = ['Title', 'memo','Important']
        #Use fields = '__all__' to display all fields from your model
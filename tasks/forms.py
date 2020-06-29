from django import forms
from tasks.models import Project, Task


# class TaskForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     project = forms.CharField(
#         max_length=3,
#         widget=forms.Select(choices=TITLE_CHOICES),
#     )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'project', )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=user)

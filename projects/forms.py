from django import forms
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    """
        Form for creating and editing projects.

        Form fields:
        name (CharField): Project name.

        Methods:
        Meta: Defines the model the form is bound to and the fields to use.
        """
    class Meta:
        model = Project
        fields = ["name"]


class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks.

    Form fields:
    name (CharField): Task name.
    deadline (DateTimeField): Date and time of task completion.

    Methods:
    Meta: Defines the model the form is bound to and the fields to use.
    """
    class Meta:
        model = Task
        fields = ["name", "deadline"]

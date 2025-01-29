from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    """
    Model for storing information about the user's project.

    Attributes:
    name (CharField): Project name.
    user (ForeignKey): Reference to the user, the owner of the project.

    Methods:
    __str__(): Returns a string representation of the project as "Project: {name}".
    """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Project: {self.name}"


class Task(models.Model):
    """
    Model for storing information about a task in a project.

    Attributes:
    name (CharField): Name of the task.
    project (ForeignKey): Link to the project to which the task belongs.
    priority (IntegerField): Priority of the task, determines the order of execution.
    status (BooleanField): Status of the task (True - completed, False - not completed).
    deadline (DateTimeField): Date and time of task execution.

    Methods:
    __str__(): Returns a string representation of the task as "Task: {name}".
    save(): Overridden method for automatically assigning a priority to a task before saving.
    """
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    priority = models.IntegerField()
    status = models.BooleanField(default=False)
    deadline = models.DateTimeField()

    class Meta:
        ordering = ["priority"]

    def __str__(self):
        return f"Task: {self.name}"

    def save(self, *args, **kwargs):
        """
        Override the save method to automatically assign a priority to a task.

        When a new task is created,
        it is assigned the lowest priority among the tasks in the project.
        """
        if not self.pk:
            max_priority = Task.objects.filter(project=self.project).aggregate(models.Max("priority"))["priority__max"]
            self.priority = (max_priority or 0) + 1
        super().save(*args, **kwargs)

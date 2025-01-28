from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Project: {self.name}"


class Task(models.Model):
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
        if not self.pk:
            max_priority = Task.objects.filter(project=self.project).aggregate(models.Max("priority"))["priority__max"]
            self.priority = (max_priority or 0) + 1
        super().save(*args, **kwargs)

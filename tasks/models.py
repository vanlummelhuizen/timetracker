from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['name', 'user']

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    text = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Session(models.Model):
    start = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    end = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return "{} :: {} | {} => {}".format(self.task.project, self.task, self.start.strftime("%Y-%m-%d %H:%M:%S"),
                                            (self.end.strftime("%Y-%m-%d %H:%M:%S") if self.end else '...'))

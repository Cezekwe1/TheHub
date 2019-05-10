from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization

class Task(models.Model):
    title = models.CharField(max_length = 100)
    description= models.TextField(max_length=500)
    owners = models.ManyToManyField(User,through='TaskAssigment')
    organization = models.ForeignKey( Organization, on_delete=models.CASCADE, null=True)


class TaskAssigment(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

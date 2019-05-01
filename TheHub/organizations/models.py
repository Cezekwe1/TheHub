from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through= 'Membership')
    creator = models.ForeignKey(User, on_delete=models.SET_NULL)


class Membership(models.Model):
    adminstrator = models.BooleanField(default = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    organization = models.ForeignKey( Organization , on_delete = models.CASCADE)





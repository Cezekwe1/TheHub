from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Organization(models.Model):
    name = models.CharField(max_length=100)


class Member(models.Model):
    users = models.ManyToManyField(User)
    organizations = models.ManyToManyField(Organization)

from django.db import models
from django.contrib.auth.models import User
from organizations.models import Organization


class Channel(models.Model):
    name = models.CharField(max_length=50)
    members = models.ManyToManyField(User, through='hubmessages.ChannelMembership')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)


class ChannelMembership(models.Model):
    member = models.ForeignKey(User,on_delete=models.CASCADE)
    organization = models.ForeignKey(Channel, on_delete=models.CASCADE)
    administrator = models.BooleanField(default = False)


class Group(models.Model):
    members = models.ManyToManyField(User, through='hubmessages.GroupMembership')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    private = models.BooleanField(default=False)


class GroupMembership(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    administrator = models.BooleanField(default=False)


class Message(models.Model):
    body = models.TextField(max_length=1000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messagesender")
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="messagereceiver")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
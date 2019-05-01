from django.db import models
from django.contrib.auth.models import User
from organizations.models import Membership, Organization
# Create your models here.
    
class Friends(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends.inviter')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends.target')

class Invite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invite.inviter') 
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invite.target')
    accepted = models.NullBooleanField(default=null)


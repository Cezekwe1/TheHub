from django.db import models
from django.contrib.auth.models import User
from organizations.models import Membership, Organization
# Create your models here.
    
class Friends(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendsinviter')
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendstarget')

    class Meta:
        unique_together = ['inviter', 'target']

class Invite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviteinviter') 
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitetarget')
    accepted = models.NullBooleanField(default=None)

    class Meta:
        unique_together = ['target', 'inviter']


from django.db import models
from django.contrib.auth.models import User
from organizations.models import Membership, Organization
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    friends = models.ManyToManyField('self', through="Friends", symmetrical=False)

    def get_current_org(self):
        if not self.current_organization:
            self.current_organization = self.user.organization_set.last()
            self.save()
        
        return self.current_organization
    
class Friends(models.Model):
    inviter = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendsinviter')
    target = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='friendstarget')

    class Meta:
        unique_together = ['inviter', 'target']

class Invite(models.Model):
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inviteinviter') 
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitetarget')
    accepted = models.NullBooleanField(default=None)

    class Meta:
        unique_together = ['target', 'inviter']

